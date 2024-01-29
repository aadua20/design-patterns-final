from datetime import datetime
from typing import Protocol

from bitcoin_wallet.app.infra.sqlite.database import Database


class ITransactionRepository(Protocol):
    def create_transaction(
        self, from_wallet_id: int, to_wallet_id: int, amount: int, same_user: bool
    ) -> None:
        pass


class TransactionRepository(ITransactionRepository):
    _db: Database

    def __init__(self, db: Database):
        self._db = db

    def create_transaction(
        self, from_wallet_id: int, to_wallet_id: int, amount: int, same_user: bool
    ) -> None:
        profit = 0 if same_user else amount * 0.015
        current_timestamp = datetime.now()
        query = (
            "INSERT INTO transactions "
            "(from_wallet_id, to_wallet_id, amount, profit, date) "
            "VALUES(?, ?, ?, ?, ?)"
        )
        params = (from_wallet_id, to_wallet_id, amount, profit, str(current_timestamp))
        self._db.execute_query(query, params)
