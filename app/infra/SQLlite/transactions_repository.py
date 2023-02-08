import sqlite3 as database
from typing import List

from app.core.transactions.interactor import Transaction


class SQLTransactionsRepository:
    def __init__(self) -> None:
        self._database_name = "bitcoin.db"
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    from_address TEXT,
                    to_address TEXT,
                    amount REAL,
                    fee REAL
                );
                """
            )

    def add_transaction(self, transaction: Transaction) -> None:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO transactions (from_address, to_address, amount, fee) "
                "VALUES (?,?,?,?)",
                (
                    transaction.from_address,
                    transaction.to_address,
                    transaction.amount,
                    transaction.fee,
                ),
            )

    def get_all_transactions(self) -> List[Transaction]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT from_address, to_address, amount, fee FROM transactions")
            rows = c.fetchall()
            return [
                Transaction(
                    from_address=row[0], to_address=row[1], amount=row[2], fee=row[3]
                )
                for row in rows
            ]

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT from_address, to_address, amount, fee "
                "FROM transactions "
                "WHERE from_address = ? OR to_address = ?",
                (address, address),
            )
            rows = c.fetchall()
            return [Transaction(*row) for row in rows]