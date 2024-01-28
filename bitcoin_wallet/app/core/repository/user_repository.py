import sqlite3
from typing import Protocol

from bitcoin_wallet.app.core.errors import ExistsError
from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.infra.sqlite.database import Database


class IUserRepository(Protocol):
    def add_user(self, user: User) -> None:
        pass

    def get_user(self, user_id: int) -> User | None:
        pass

    def user_exists(self, username: str) -> bool:
        pass

    def is_registered(self, api_key: str) -> bool:
        pass


class UserRepository(IUserRepository):
    _db: Database

    def __init__(self, db: Database):
        self._db = db

    def add_user(self, user: User) -> None:
        try:
            query = (
                "INSERT INTO users (username, api_key, wallet_count) " "VALUES(?, ?, ?)"
            )
            params = (
                user.get_username(),
                user.get_api_key(),
                user.get_wallet_count(),
            )
            self._db.execute_query(query, params)
        except sqlite3.IntegrityError:
            raise ExistsError(user)

    def get_user(self, user_id: int) -> User | None:
        query = "SELECT id, username, api_key, wallet_count FROM users WHERE id = ?"
        user = self._db.fetch_one(query, (user_id,))
        return (
            User(
                user_id=user[0], username=user[1], api_key=user[2], wallet_count=user[3]
            )
            if user
            else None
        )

    def user_exists(self, username: str) -> bool:
        query = "SELECT * FROM users WHERE username = ?"
        user = self._db.fetch_one(query, (username,))
        return user is not None

    def is_registered(self, api_key: str) -> bool:
        query = "SELECT * FROM users WHERE api_key = ?"
        user = self._db.fetch_one(query, (api_key,))
        return user is not None
