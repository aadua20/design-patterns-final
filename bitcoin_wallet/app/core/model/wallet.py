from dataclasses import dataclass


@dataclass
class Wallet:
    address: str
    satoshi: int


@dataclass
class WalletItem:
    address: str
    balance: dict[str, float]
