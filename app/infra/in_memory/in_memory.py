from collections import defaultdict
from typing import DefaultDict

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
