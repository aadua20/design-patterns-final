from datetime import datetime
from typing import Protocol

from bitcoin_wallet.app.core.model.transaction import Transaction
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

    def get_transactions(self) -> list[Transaction]:
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

    def get_transactions(self) -> list[Transaction]:
        query = """
            SELECT from_wallet_id, to_wallet_id, amount, profit, date
            FROM transactions
        """
        results = self._db.fetch_all(query, )

        transactions = [
            Transaction(
                from_wallet=result[0],
                to_wallet=result[1],
                amount=result[2],
                profit=result[3],
                date=result[4]
            ) for result in results
        ]
        return transactions
