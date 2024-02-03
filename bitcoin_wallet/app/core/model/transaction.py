from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    from_wallet: int
    to_wallet: int
    amount: int
    profit: int
    date: datetime

    def get_from_wallet_id(self) -> str:
        return str(self.from_wallet)

    def get_to_wallet_id(self) -> str:
        return str(self.to_wallet)

    def get_amount(self) -> int:
        return self.amount

    def get_profit(self) -> int:
        return self.profit

    def get_date(self) -> datetime:
        return self.date


@dataclass
class Statistics:
    num_transactions: int
    profit: float
