import sqlite3
from typing import Any


class Database:
    def __init__(self, db_name: str = "btc.db"):
        self.db_name = db_name

    def execute_query(self, query: str, params: Any = None) -> None:
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            connection.commit()

    def fetch_all(self, query: str, params: Any = None) -> list[Any]:
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            return cursor.fetchall()


class DatabaseInitializer:
    @staticmethod
    def init_tables(db: Database) -> None:
        # Create users table
        db.execute_query(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username VARCHAR UNIQUE,
                    api_key VARCHAR UNIQUE,
                    wallet_count INTEGER
                )
            """
        )

        # Create wallets table
        db.execute_query(
            """
                CREATE TABLE IF NOT EXISTS wallets (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id),
                    address VARCHAR UNIQUE,
                    satoshi INTEGER
                )
            """
        )

        # Create transactions table
        db.execute_query(
            """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    from_wallet_id INTEGER REFERENCES wallets(id),
                    to_wallet_id INTEGER REFERENCES wallets(id),
                    amount INTEGER,
                    profit INTEGER,
                    date TIMESTAMP
                )
            """
        )
