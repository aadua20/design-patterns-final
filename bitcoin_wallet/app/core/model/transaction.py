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

    def __eq__(self, other):  # type: ignore
        if not isinstance(other, Transaction):
            return False
        return (
            self.from_wallet == other.from_wallet
            and self.to_wallet == other.to_wallet
            and self.amount == other.amount
            and self.profit == other.profit
            and self.date == other.date
        )

    def __hash__(self):  # type: ignore
        return hash(
            (self.from_wallet, self.to_wallet, self.amount, self.profit, self.date)
        )


@dataclass
class Statistics:
    num_transactions: int
    profit_in_satoshi: int


@dataclass
class TransactionItem:
    from_wallet_address: str
    to_wallet_address: str
    amount: int
