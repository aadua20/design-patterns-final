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
