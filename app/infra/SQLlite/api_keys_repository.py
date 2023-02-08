import sqlite3 as database


class SQLAPIKeysRepository:
    def __init__(self) -> None:
        self._database_name = "bitcoin.db"
        with database.connect(self._database_name) as conn:
            c = conn.cursor()

            c.execute(
                """
            CREATE TABLE IF NOT EXISTS api_keys (
                user_id INTEGER,
                api_key TEXT UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            )

    def add_api_key_id_pair(self, api_key: str, user_id: int) -> None:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO api_keys (user_id, api_key) VALUES (?, ?)",
                (user_id, api_key),
            )

    def get_user_id_by_api_key(self, api_key: str) -> int:
        with database.connect(self._database_name) as conn:
            c = conn.cursor()
            c.execute("SELECT user_id FROM api_keys WHERE api_key=?", (api_key,))
            result = c.fetchone()
            if result is not None:
                return int(result[0])
            else:
                return -1
