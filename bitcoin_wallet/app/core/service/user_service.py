from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.core.repository.user_repository import UserRepository
from bitcoin_wallet.app.infra.sqlite.database import Database


class UserService:
    _user_repository: UserRepository

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self._user_repository = user_repository

    @classmethod
    def create(cls, db: Database) -> "UserService":
        return cls(user_repository=UserRepository(db))

    def add_user(self, user: User) -> None:
        self._user_repository.add_user(user)
