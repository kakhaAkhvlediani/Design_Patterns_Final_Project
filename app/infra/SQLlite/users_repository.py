import sqlite3 as database
from typing import List, Optional

from app.core.users.interactor import User


class SQLUsersRepository:
    def __init__(self) -> None:
        self._database_name = "bitcoin.db"
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                );
                """
            )

    def add_user(self, new_user: User) -> bool:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            try:
                c.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (new_user.get_username(), new_user.get_password()),
                )
                return True
            except database.IntegrityError:
                return False

    def get_user_by_username(self, username: str) -> Optional[User]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            result = c.fetchone()
            if result is not None:
                return User(
                    _user_id=result[0], _username=result[1], _password=result[2]
                )
            else:
                return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?", (user_id,))
            result = c.fetchone()
            if result is not None:
                return User(
                    _user_id=result[0], _username=result[1], _password=result[2]
                )
            else:
                return None

    def get_all_users(self) -> List[User]:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            result = c.fetchall()
            return [
                User(_user_id=row[0], _username=row[1], _password=row[2])
                for row in result
            ]

    def get_max_user_id(self) -> int:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT max(id) FROM users")
            result = c.fetchone()
            return 1 if result is None or result[0] is None else int(result[0]) + 1