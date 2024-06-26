from datetime import datetime
from typing import Protocol

from bitcoin_wallet.app.core.model.transaction import Statistics, Transaction
from bitcoin_wallet.app.infra.sqlite.database import Database


class ITransactionRepository(Protocol):
    def create_transaction(
        self,
        from_wallet_id: int | None,
        to_wallet_id: int | None,
        amount: int,
        profit: int,
    ) -> None:
        pass

    def get_wallet_transactions(self, wallet_id: int | None) -> list[Transaction]:
        pass

    def get_statistics(self) -> Statistics:
        pass

    def get_user_transactions(self, user_id: int) -> list[Transaction]:
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
        profit: int,
    ) -> None:
        current_timestamp = datetime.now()
        query = (
            "INSERT INTO transactions "
            "(from_wallet_id, to_wallet_id, amount, profit, date) "
            "VALUES(?, ?, ?, ?, ?)"
        )
        params = (from_wallet_id, to_wallet_id, amount, profit, str(current_timestamp))
        self._db.execute_query(query, params)

    def get_user_transactions(self, user_id: int) -> list[Transaction]:
        wallets: list[int] = self._get_user_wallets(user_id)
        all_transactions: list[Transaction] = []

        for wallet_id in wallets:
            wallet_transactions = self.get_wallet_transactions(wallet_id)
            all_transactions.extend(wallet_transactions)

        return list(set(all_transactions))

    def get_wallet_transactions(self, wallet_id: int | None) -> list[Transaction]:
        query = """
            SELECT from_wallet_id, to_wallet_id, amount, profit, date
            FROM transactions
            WHERE from_wallet_id = ? OR to_wallet_id = ?
            ORDER BY date
        """
        results = self._db.fetch_all(
            query,
            (
                wallet_id,
                wallet_id,
            ),
        )

        transactions = [
            Transaction(
                from_wallet=result[0],
                to_wallet=result[1],
                amount=result[2],
                profit=result[3],
                date=result[4],
            )
            for result in results
        ]
        return transactions

    def get_statistics(self) -> Statistics:
        transactions = self._get_transactions()
        profit = sum(t.get_profit() for t in transactions)
        return Statistics(num_transactions=len(transactions), profit_in_satoshi=profit)

    def _get_transactions(self) -> list[Transaction]:
        query = """
            SELECT from_wallet_id, to_wallet_id, amount, profit, date
            FROM transactions
        """
        results = self._db.fetch_all(
            query,
        )

        transactions = [
            Transaction(
                from_wallet=result[0],
                to_wallet=result[1],
                amount=result[2],
                profit=result[3],
                date=result[4],
            )
            for result in results
        ]
        return transactions

    def _get_user_wallets(self, user_id: int) -> list[int]:
        query = """
                    SELECT id
                    FROM wallets
                    WHERE user_id = ?
                """
        wallets = self._db.fetch_all(query, (user_id,))
        wallet_ids = [wallet[0] for wallet in wallets]
        return wallet_ids
