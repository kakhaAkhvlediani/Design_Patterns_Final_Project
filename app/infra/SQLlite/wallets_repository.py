import sqlite3 as database
from typing import List, Optional

from app.core.wallets.interactor import Wallet


class SQLWalletsRepository:
    def __init__(self) -> None:
        self._database_name = "bitcoin.db"
        with database.connect(self._database_name) as conn:
            c = conn.cursor()

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS wallets (
                    user_id INTEGER,
                    address TEXT UNIQUE,
                    balance_in_btc REAL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
                """
            )

    # WALLETS

    def add_wallet(self, wallet: Wallet) -> None:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO wallets (user_id, address, balance_in_btc) "
                "VALUES (?, ?, ?)",
                (
                    wallet.get_owner_id(),
                    wallet.get_address(),
                    wallet.get_balance_in_btc(),
                ),
            )
            conn.commit()

    def get_wallet(self, address: str) -> Optional[Wallet]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT user_id, address, balance_in_btc "
                "FROM wallets WHERE address = ?",
                (address,),
            )
            result = c.fetchone()
            if result is not None:
                return Wallet(
                    _user_id=result[0], _address=result[1], _balance_btc=result[2]
                )
            else:
                return None

    def deposit(self, address: str, amount: float) -> bool:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT balance_in_btc FROM wallets WHERE address = ?", (address,)
            )
            result = c.fetchone()
            if result is not None:
                current_balance = result[0]
                c.execute(
                    "UPDATE wallets SET balance_in_btc = ? WHERE address = ?",
                    (current_balance + amount, address),
                )
                conn.commit()
                return True
            else:
                return False

    def withdraw(self, address: str, amount: float) -> bool:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT balance_in_btc FROM wallets WHERE address = ?", (address,)
            )
            result = c.fetchone()
            if result is not None:
                current_balance = result[0]
                if current_balance >= amount:
                    c.execute(
                        "UPDATE wallets SET balance_in_btc = ? WHERE address = ?",
                        (current_balance - amount, address),
                    )
                    conn.commit()
                    return True
                else:
                    return False
            else:
                return False

    def get_all_wallets_of_user(self, user_id: int) -> List[Wallet]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT address, balance_in_btc FROM wallets WHERE user_id = ?",
                (user_id,),
            )
            rows = c.fetchall()
            return [
                Wallet(_user_id=user_id, _address=row[0], _balance_btc=row[1])
                for row in rows
            ]

    def get_number_of_wallets_of_user(self, user_id: int) -> int:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM wallets WHERE user_id = ?", (user_id,))
            return int(c.fetchone()[0])