from collections import defaultdict
from typing import DefaultDict, List

from app.core.transactions.interactor import Transaction


class InMemoryAPIKeyRepository:
    _transactions: DefaultDict[int, Transaction]

    def __init__(self) -> None:
        self._api_keys_user_ids = defaultdict()

    # TRANSACTION
    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions[len(self._transactions)] = transaction

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        transactions: List[Transaction] = []
        for _, transaction in self._transactions.items():
            if (
                    transaction.get_from_address() == address
                    or transaction.get_to_address() == address
            ):
                transactions.append(transaction)

        return transactions

    def get_all_transactions(self) -> List[Transaction]:
        return list(self._transactions.values())
