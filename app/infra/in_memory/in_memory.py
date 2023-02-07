from collections import defaultdict
from typing import DefaultDict, Optional, List

from app.core.transactions.interactor import Transaction
from app.core.users.interactor import User
from app.core.wallets.interactor import Wallet


class InMemoryRepository:
    _users: DefaultDict[int, User]
    _wallets: DefaultDict[str, Wallet]
    _transactions: DefaultDict[int, Transaction]

    def __init__(self) -> None:
        self._users = defaultdict()
        self._wallets = defaultdict()
        self._transactions = defaultdict()

    # USER
    def add_user(self, new_user: User) -> bool:  # api_key is always unique
        if new_user in list(self._users.values()):
            return False
        else:
            self._users[new_user.get_user_id()] = new_user
            return True

    def get_user_by_username(self, username: str) -> Optional[User]:
        for _, current_user in self._users.items():
            if current_user.get_username() == username:
                return current_user

        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id, None)

    def get_all_users(self) -> List[User]:
        return list(self._users.values())

    def get_max_user_id(self) -> int:
        return len(self._users)


