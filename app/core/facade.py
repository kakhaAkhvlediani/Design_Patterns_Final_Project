import uuid
from asyncio import Protocol
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from starlette import status

from app.core.api_key.interactor import APIKeyInteractor, IAPIKeyRepository
from app.core.transactions.interactor import Transaction
from app.core.users.interactor import UsersInteractor, IUserRepository, User
from app.core.wallets.interactor import IWalletRepository, WalletsInteractor, Wallet
from app.infra.utils.hasher import DefaultHashFunction
from app.infra.utils.rate_provider import DefaultRateProvider

MAX_NUM_OF_WALLET = 3  # todo add constants class


@dataclass
class UserResponse:
    status: int
    msg: str = ""
    api_key: str = ""

@dataclass
class WalletResponse:
    status: int
    msg: str = ""
    wallet_info: Dict[str, Any] = field(default_factory=lambda: {})
    transactions: List[Dict[str, Any]] = field(default_factory=lambda: [])


class IHasher(Protocol):
    def use_my_hash(self, *args: object) -> str:
        pass

    def __call__(self, *args: object) -> str:
        return self.use_my_hash(args)


class IRateProvider(Protocol):
    def get_exchange_rate(self) -> float:
        pass


@dataclass
class BitcoinWalletCore:
    _users_interactor: UsersInteractor
    _wallets_interactor: WalletsInteractor
    _api_key_interactor: APIKeyInteractor
    _hash: IHasher
    _rate_provider: IRateProvider

    @classmethod
    def create(
            cls,
            users_repository: IUserRepository,
            wallets_repository: IWalletRepository,
            api_key_repository: IAPIKeyRepository,
            hash_function: IHasher = DefaultHashFunction(),
            rate_provider: IRateProvider = DefaultRateProvider(),
    ) -> "BitcoinWalletCore":
        return cls(
            _users_interactor=UsersInteractor(_users_repository=users_repository),
            _wallets_interactor=WalletsInteractor(_wallets_repository=wallets_repository),
            _api_key_interactor=APIKeyInteractor(_api_key_repository=api_key_repository),
            _hash=hash_function,
            _rate_provider=rate_provider,
        )

    # USER RESPONSE
    def _generate_api_key(self, args: object) -> str:
        return "api_key_" + self._hash(args)

    def get_user_id_by_api_key(self, api_key: str) -> int:
        return self._api_key_interactor.get_user_id_by_api_key(api_key)

    def get_user(self, username: str) -> Optional[User]:
        return self._users_interactor.get_user(username)

    def is_correct_api_key(self, api_key: str) -> bool:
        return self.get_user_id_by_api_key(api_key=api_key) != -1

    def register_user(self, username: str, password: str) -> UserResponse:
        api_key: str = self._generate_api_key((username, password))
        user: Optional[User] = self._users_interactor.register_user(
            username=username, password=self._hash(password)
        )
        if user is None:
            return UserResponse(status=status.HTTP_400_BAD_REQUEST, msg="Is Registered")

        self._api_key_interactor.add_api_key_id_pair(
            api_key=api_key, user_id=user.get_user_id()
        )

        return UserResponse(
            status=status.HTTP_201_CREATED, msg="Registered", api_key=api_key
        )

    # Wallet RESPONSE
    def _generate_wallet_address(self) -> str:
        return "wallet_" + str(uuid.uuid4())[0:12]

    def _check_if_user_has_max_num_of_wallets(self, user_id: int) -> bool:
        return (
                self._wallets_interactor.get_number_of_wallets_of_user(user_id)
                == MAX_NUM_OF_WALLET
        )

    def _calculate_exchange_value_in_usd(self, amount_in_btc: float) -> float:
        return amount_in_btc * self._rate_provider.get_exchange_rate()

    def _calculate_exchange_value_in_btc(self, amount_in_usd: float) -> float:
        return amount_in_usd / self._rate_provider.get_exchange_rate()

    def create_wallet(self, api_key: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        address: str = self._generate_wallet_address()

        if user_id == -1:
            return WalletResponse(
                status=status.HTTP_403_FORBIDDEN, msg="Invalid api_key"
            )

        if self._check_if_user_has_max_num_of_wallets(user_id=user_id):
            return WalletResponse(
                status=status.HTTP_400_BAD_REQUEST,
                msg="User has reached the max number of wallets",
            )

        wallet: Wallet = self._wallets_interactor.create_wallet(
            user_id=user_id,
            address=address,
            balance_in_btc=self._wallet_starting_balance,
        )

        to_dict: Dict[str, Any] = wallet.to_dict()
        to_dict["balance_in_usd"] = self._calculate_exchange_value_in_usd(
            amount_in_btc=wallet.get_balance_in_btc()
        )

        return WalletResponse(
            status=status.HTTP_201_CREATED,
            msg="Wallet created",
            wallet_info=to_dict,
        )

    def get_wallet(self, api_key: str, address: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)

        if user_id == -1:
            return WalletResponse(
                status=status.HTTP_403_FORBIDDEN, msg="Invalid api_key"
            )

        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return WalletResponse(
                status=status.HTTP_404_NOT_FOUND, msg="No wallet with this address"
            )
        elif user_id != wallet.get_owner_id():
            return WalletResponse(
                status=status.HTTP_403_FORBIDDEN, msg="Wrong api_key for this wallet"
            )

        to_dict: Dict[str, Any] = wallet.to_dict()
        to_dict["balance_in_usd"] = self._calculate_exchange_value_in_usd(
            amount_in_btc=wallet.get_balance_in_btc()
        )

        return WalletResponse(
            status=status.HTTP_200_OK, msg="Returning Wallet", wallet_info=to_dict
        )

    def get_transactions_of_wallet(self, api_key: str, address: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        if user_id == -1:
            return WalletResponse(
                status=status.HTTP_403_FORBIDDEN, msg="Invalid api_key"
            )

        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return WalletResponse(
                status=status.HTTP_404_NOT_FOUND, msg="Wallet not found"
            )
        elif wallet.get_owner_id() != user_id:
            return WalletResponse(status=status.HTTP_403_FORBIDDEN, msg="Wrong api_key")

        transactions: List[
            Transaction
        ] = self._transactions_interactor.get_transactions_of_wallet(address)
        transactions_to_send_back: List[Dict[str, Any]] = [
            transaction.to_dict() for transaction in transactions
        ]

        return WalletResponse(
            status=status.HTTP_200_OK,
            msg="Transactions have been acquired",
            transactions=transactions_to_send_back,
        )
