from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.core.repository.user_repository import IUserRepository


class UserService:
    _user_repository: IUserRepository

    def __init__(
        self,
        user_repository: IUserRepository,
    ):
        self._user_repository = user_repository

    def add_user(self, user: User) -> None:
        self._user_repository.add_user(user)

    def get_user(self, user_id: int) -> User | None:
        return self._user_repository.get_user(user_id)

    def user_exists(self, username: str) -> bool:
        return self._user_repository.user_exists(username)

    def get_user_by_api_key(self, api_key: str) -> User | None:
        return self._user_repository.get_user_by_api_key(api_key)
