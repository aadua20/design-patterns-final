from dataclasses import dataclass
from typing import Optional


@dataclass
class Wallet:
    user_id: int
    address: str
    satoshi: int
    id: Optional[int] = None


@dataclass
class WalletItem:
    address: str
    balance: dict[str, float]
