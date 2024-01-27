from typing import Protocol

from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.infra.sqlite.database import Database


class UserRepository:
    _db: Database

    def __init__(self, db: Database):
        self._db = db

    def add_user(self, user: User) -> None:
        query = "INSERT INTO users (username, api_key, wallet_count) VALUES(?, ?, ?) "
        params = (user.get_username(), user.get_api_key(), 0)
        self._db.execute_query(query, params)


class IUserRepository(Protocol):
    def add_user(self, user: User) -> None:
        pass

    def get_user(self, user_id: int) -> User:
        pass

    def user_exists(self, username: str) -> bool:
        pass

    def is_registered(self, api_key: str) -> bool:
        pass
