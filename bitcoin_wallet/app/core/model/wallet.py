from dataclasses import dataclass
from typing import Optional


@dataclass
class Wallet:
    user_id: int
    address: str
    satoshi: int
    id: Optional[int] = None

    def get_user_id(self) -> int:
        return self.user_id

    def get_address(self) -> str:
        return self.address

    def get_satoshi(self) -> int:
        return self.satoshi

    def get_id(self) -> int | None:
        return self.id


@dataclass
class WalletItem:
    address: str
    balance: dict[str, float]
