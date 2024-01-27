from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    username: str
    wallet_count: int = 0
    user_id: UUID = field(default_factory=uuid4)
    api_key: UUID = field(default_factory=uuid4)

    def get_id(self) -> str:
        return str(self.user_id)

    def get_username(self) -> str:
        return self.username

    def get_wallet_count(self) -> int | None:
        return self.wallet_count

    def get_api_key(self) -> str:
        return str(self.api_key)
