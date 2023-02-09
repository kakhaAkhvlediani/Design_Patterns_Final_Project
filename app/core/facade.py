from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from app.core.api_key.interactor import APIKeyInteractor, IAPIKeysRepository
from app.core.transactions.interactor import (
    ITransactionsRepository,
    Transaction,
    TransactionsInteractor,
)
from app.core.users.interactor import IUsersRepository, User, UsersInteractor
from app.core.wallets.interactor import IWalletsRepository, Wallet, WalletsInteractor

MAX_NUM_OF_WALLET: int = 3
ADMIN_API_KEY: str = "admin_api_key"
WALLET_STARTING_BALANCE: float = 1
EXTERNAL_TRANSACTION_ID: int = -10


class IHasher(Protocol):
    def use_my_hash(self, *args: object) -> str:
        pass

    def __call__(self, *args: object) -> str:
        return self.use_my_hash(args)


class ICurrencyConverter(Protocol):
    def convert_to_usd(self, amount_in_btc: float) -> float:
        pass

    def convert_to_btc(self, amount_in_usd: float) -> float:
        pass


@dataclass
class UserResponse:
    status: int
    api_key: str = ""


@dataclass
class WalletResponse:
    status: int
    wallet_info: Dict[str, Any] = field(default_factory=lambda: {})
    transactions: List[Dict[str, Any]] = field(default_factory=lambda: [])


@dataclass
class TransactionResponse:
    status: int


@dataclass
class StatisticsResponse:
    status: int
    platform_profit_in_btc: float = 0
    platform_profit_in_usd: float = 0
    total_number_of_transactions: int = 0


class IFeeRateStrategy(Protocol):
    def get_fee_rate_for_different_owners(self) -> float:
        pass

    def get_fee_rate_for_same_owner(self) -> float:
        pass

    def get_fee_rate_for_deposit(self) -> float:
        pass

    def get_fee_rate_for_withdraw(self) -> float:
        pass


class IUniqueValueGenerators(Protocol):
    def generate_wallet_address(self) -> str:
        pass

    def generate_api_key(self) -> str:
        pass


@dataclass
class BitcoinWalletCore:
    _users_interactor: UsersInteractor
    _wallets_interactor: WalletsInteractor
    _transactions_interactor: TransactionsInteractor
    _api_key_interactor: APIKeyInteractor

    _hash: IHasher
    _currency_converter: ICurrencyConverter
    _fee_strategy: IFeeRateStrategy
    _unique_value_generator: IUniqueValueGenerators

    @classmethod
    def create(
            cls,
            users_repository: IUsersRepository,
            wallets_repository: IWalletsRepository,
            transactions_repository: ITransactionsRepository,
            api_key_repository: IAPIKeysRepository,
            hash_function: IHasher,
            currency_converter: ICurrencyConverter,
            fee_strategy: IFeeRateStrategy,
            unique_value_generator: IUniqueValueGenerators,
    ) -> "BitcoinWalletCore":
        return cls(
            _users_interactor=UsersInteractor(_users_repository=users_repository),
            _wallets_interactor=WalletsInteractor(
                _wallets_repository=wallets_repository
            ),
            _transactions_interactor=TransactionsInteractor(
                _transactions_repository=transactions_repository
            ),
            _api_key_interactor=APIKeyInteractor(
                _api_key_repository=api_key_repository
            ),
            _hash=hash_function,
            _currency_converter=currency_converter,
            _fee_strategy=fee_strategy,
            _unique_value_generator=unique_value_generator,
        )

    # USER RESPONSE

    def get_user_id_by_api_key(self, api_key: str) -> int:
        return self._api_key_interactor.get_user_id_by_api_key(api_key)

    def get_user(self, username: str) -> Optional[User]:
        return self._users_interactor.get_user(username)

    def register_user(self, username: str, password: str) -> UserResponse:
        api_key: str = self._unique_value_generator.generate_api_key()
        user: Optional[User] = self._users_interactor.register_user(
            username=username, password=self._hash(password)
        )
        if user is None:
            return UserResponse(status=400)

        self._api_key_interactor.add_api_key_id_pair(
            api_key=api_key, user_id=user.get_user_id()
        )

        return UserResponse(
            status=201, api_key=api_key
        )

    # Wallet RESPONSE

    def _check_if_user_has_max_num_of_wallets(self, user_id: int) -> bool:
        return (
                self._wallets_interactor.get_number_of_wallets_of_user(user_id)
                == MAX_NUM_OF_WALLET
        )

    def create_wallet(self, api_key: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        address: str = self._unique_value_generator.generate_wallet_address()

        if user_id == -1:
            return WalletResponse(
                status=403
            )

        if self._check_if_user_has_max_num_of_wallets(user_id=user_id):
            return WalletResponse(
                status=400
            )

        wallet: Wallet = self._wallets_interactor.create_wallet(
            user_id=user_id,
            address=address,
            balance_in_btc=WALLET_STARTING_BALANCE,
        )

        to_dict: Dict[str, Any] = wallet.to_dict()
        to_dict["balance_in_usd"] = self._currency_converter.convert_to_usd(
            amount_in_btc=wallet.get_balance_in_btc()
        )

        return WalletResponse(
            status=201,
            wallet_info=to_dict,
        )

    def get_wallet(self, api_key: str, address: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)

        if user_id == -1:
            return WalletResponse(
                status=403
            )

        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return WalletResponse(
                status=404
            )
        elif user_id != wallet.get_owner_id():
            return WalletResponse(
                status=403
            )

        to_dict: Dict[str, Any] = wallet.to_dict()
        to_dict["balance_in_usd"] = self._currency_converter.convert_to_usd(
            amount_in_btc=wallet.get_balance_in_btc()
        )

        return WalletResponse(
            status=200, wallet_info=to_dict
        )

    def get_transactions_of_wallet(self, api_key: str, address: str) -> WalletResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        if user_id == -1:
            return WalletResponse(
                status=403
            )  # TODO non-existent api_Key

        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return WalletResponse(
                status=404
            )  # TODO RIGHT API KEY, WRONG ADDRESS
        elif wallet.get_owner_id() != user_id:  # TODO Existing api key, existing wallet but api key is of other user
            return WalletResponse(status=403)

        transactions: List[
            Transaction
        ] = self._transactions_interactor.get_transactions_of_wallet(address)
        transactions_to_send_back: List[Dict[str, Any]] = [
            transaction.to_dict() for transaction in transactions
        ]

        return WalletResponse(
            status=200,
            transactions=transactions_to_send_back,
        )

    # Transaction RESPONSE
    def _get_fee(self, sender_id: int, receiver_id: int, amount: float) -> float:
        if sender_id == receiver_id:
            return amount * self._fee_strategy.get_fee_rate_for_same_owner()
        elif sender_id == EXTERNAL_TRANSACTION_ID:
            return amount * self._fee_strategy.get_fee_rate_for_deposit()
        elif receiver_id == EXTERNAL_TRANSACTION_ID:
            return amount * self._fee_strategy.get_fee_rate_for_withdraw()
        return (
                amount * self._fee_strategy.get_fee_rate_for_different_owners()
        )

    def deposit(
            self, api_key: str, address: str, amount_in_usd: float
    ) -> TransactionResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        if user_id == -1:
            return TransactionResponse(
                status=403
            )

        amount_in_btc: float = self._currency_converter.convert_to_btc(
            amount_in_usd=amount_in_usd
        )

        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return TransactionResponse(
                status=404
            )
        elif wallet.get_owner_id() != user_id:
            return TransactionResponse(status=403)

        fee: float = self._get_fee(
            sender_id=EXTERNAL_TRANSACTION_ID,
            receiver_id=wallet.get_owner_id(),
            amount=amount_in_btc,
        )
        self._transactions_interactor.make_transaction(
            from_address="DEPOSIT", to_address=address, amount=amount_in_btc, fee=fee
        )

        self._wallets_interactor.deposit(address, amount_in_btc - fee)
        return TransactionResponse(
            status=201
        )

    def withdraw(
            self, api_key: str, address: str, amount_in_usd: float
    ) -> TransactionResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        if user_id == -1:
            return TransactionResponse(
                status=403
            )

        amount_in_btc: float = self._currency_converter.convert_to_btc(
            amount_in_usd=amount_in_usd
        )
        wallet: Optional[Wallet] = self._wallets_interactor.get_wallet(address=address)
        if wallet is None:
            return TransactionResponse(
                status=404
            )
        elif wallet.get_owner_id() != user_id:
            return TransactionResponse(status=403)
        elif wallet.get_balance_in_btc() < amount_in_btc:
            return TransactionResponse(
                status=400
            )

        fee: float = self._get_fee(
            sender_id=wallet.get_owner_id(),
            receiver_id=EXTERNAL_TRANSACTION_ID,
            amount=amount_in_btc,
        )
        self._transactions_interactor.make_transaction(
            from_address=address, to_address="WITHDRAW", amount=amount_in_btc, fee=fee
        )
        self._wallets_interactor.withdraw(address, amount_in_btc - fee)
        return TransactionResponse(
            status=201
        )

    def make_transaction(
            self, api_key: str, from_address: str, to_address: str, amount: float
    ) -> TransactionResponse:
        user_id: int = self.get_user_id_by_api_key(api_key)
        if user_id == -1:
            return TransactionResponse(  # TODO
                status=403
            )
        sender: Optional[Wallet] = self._wallets_interactor.get_wallet(
            address=from_address
        )
        receiver: Optional[Wallet] = self._wallets_interactor.get_wallet(
            address=to_address
        )
        if sender is None:
            return TransactionResponse(  # TODO
                status=404
            )
        elif sender.get_owner_id() != user_id:
            return TransactionResponse(
                status=403
            )
        elif sender.get_balance_in_btc() < amount:
            return TransactionResponse(
                status=400
            )
        elif receiver is None:
            return TransactionResponse(
                status=404
            )
        elif sender.get_address() == receiver.get_address():
            return TransactionResponse(
                status=403
            )

        fee: float = self._get_fee(
            sender_id=sender.get_owner_id(),
            receiver_id=receiver.get_owner_id(),
            amount=amount,
        )

        self._transactions_interactor.make_transaction(
            from_address, to_address, amount, fee
        )
        self._wallets_interactor.withdraw(address=sender.get_address(), amount=amount)
        self._wallets_interactor.deposit(
            address=receiver.get_address(), amount=amount - fee
        )

        return TransactionResponse(
            status=201
        )

    # STATISTICS RESPONSE
    def get_statistics(self, admin_api_key: str) -> StatisticsResponse:
        if admin_api_key != ADMIN_API_KEY:
            return StatisticsResponse(
                status=403
            )
        transactions: List[
            Transaction
        ] = self._transactions_interactor.get_all_transactions()

        platform_profit: float = 0
        total_number_of_transactions: int = 0
        for transaction in transactions:
            total_number_of_transactions += 1
            platform_profit += transaction.get_fee()

        return StatisticsResponse(
            status=200,
            platform_profit_in_btc=platform_profit,
            platform_profit_in_usd=self._currency_converter.convert_to_usd(
                amount_in_btc=platform_profit
            ),
            total_number_of_transactions=total_number_of_transactions,
        )
