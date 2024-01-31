from datetime import datetime
from typing import Protocol

from bitcoin_wallet.app.infra.sqlite.database import Database


class ITransactionRepository(Protocol):
    def create_transaction(
        self,
        from_wallet_id: int | None,
        to_wallet_id: int | None,
        amount: int,
        profit: float,
    ) -> None:
        pass


class TransactionRepository(ITransactionRepository):
    _db: Database

    def __init__(self, db: Database):
        self._db = db

    def create_transaction(
        self,
        from_wallet_id: int | None,
        to_wallet_id: int | None,
        amount: int,
        profit: float,
    ) -> None:
        current_timestamp = datetime.now()
        query = (
            "INSERT INTO transactions "
            "(from_wallet_id, to_wallet_id, amount, profit, date) "
            "VALUES(?, ?, ?, ?, ?)"
        )
        params = (from_wallet_id, to_wallet_id, amount, profit, str(current_timestamp))
        self._db.execute_query(query, params)
