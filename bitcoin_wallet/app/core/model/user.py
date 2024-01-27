from dataclasses import dataclass, field
from uuid import UUID, uuid4

from pydantic import BaseModel


@dataclass
class User:
    user_id: int
    username: str
    wallet_count: int
    api_key: UUID = field(default_factory=uuid4)

    def __init__(self, username: str):
        self.username = username
        self.api_key = uuid4()

    def get_id(self) -> int:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def get_wallet_count(self) -> int:
        return self.wallet_count

    def get_api_key(self) -> str:
        return str(self.api_key)


class IUser(BaseModel):
    def get_id(self) -> int:
        pass

    def get_username(self) -> str:
        pass

    def get_wallet_count(self) -> int:
        pass

    def get_api_key(self) -> str:
        pass
