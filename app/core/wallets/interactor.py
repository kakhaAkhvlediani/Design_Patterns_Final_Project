from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol


@dataclass
class Wallet:
    _user_id: int
    _address: str
    _balance_btc: float

    def deposit(self, amount: float) -> None:
        self._balance_btc += amount

    def withdraw(self, amount: float) -> None:
        self._balance_btc -= amount

    def get_address(self) -> str:
        return self._address

    def get_balance_in_btc(self) -> float:
        return self._balance_btc

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Wallet):
            return NotImplemented
        return (
            self.get_owner_id() == other.get_owner_id()
            and self.get_address() == other.get_address()
            and self.get_balance_in_btc() == other.get_balance_in_btc()
        )

    def to_dict(self) -> Dict[str, str | float]:
        return {"address": self._address, "balance_in_btc": self._balance_btc}

    def get_owner_id(self) -> int:
        return self._user_id


class IWalletRepository(Protocol):
    def add_wallet(self, wallet: Wallet) -> None:
        pass

    def get_wallet(self, address: str) -> Optional[Wallet]:
        pass

    def deposit(self, address: str, amount: float) -> bool:
        pass

    def withdraw(self, address: str, amount: float) -> bool:
        pass

    def get_all_wallets_of_user(self, user_id: int) -> List[Wallet]:
        pass

    def get_number_of_wallets_of_user(self, user_id: int) -> int:
        pass


@dataclass
class WalletsInteractor:
    _wallets_repository: IWalletRepository

    def create_wallet(
        self, user_id: int, address: str, balance_in_btc: float
    ) -> Wallet:
        wallet: Wallet = Wallet(
            _user_id=user_id, _address=address, _balance_btc=balance_in_btc
        )
        self._wallets_repository.add_wallet(wallet=wallet)
        return wallet

    def deposit(self, address: str, amount: float) -> None:
        self._wallets_repository.deposit(address=address, amount=amount)

    def withdraw(self, address: str, amount: float) -> None:
        self._wallets_repository.withdraw(address=address, amount=amount)

    def get_wallet(self, address: str) -> Optional[Wallet]:
        return self._wallets_repository.get_wallet(address=address)

    def get_all_wallets_of_user(self, user_id: int) -> List[Wallet]:
        return self._wallets_repository.get_all_wallets_of_user(user_id)

    def get_number_of_wallets_of_user(self, user_id: int) -> int:
        return self._wallets_repository.get_number_of_wallets_of_user(user_id)