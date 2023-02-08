from collections import defaultdict
from typing import DefaultDict

from app.core.transactions.interactor import Transaction


class InMemoryAPIKeyRepository:
    _transactions: DefaultDict[int, Transaction]

    def __init__(self) -> None:
        self._api_keys_user_ids = defaultdict()
