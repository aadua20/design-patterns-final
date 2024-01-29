from bitcoin_wallet.app.core.repository.transaction_repository import (
    ITransactionRepository,
)


class TransactionService:
    def __init__(self, transaction_repository: ITransactionRepository):
        self._transaction_repository = transaction_repository

    def create_transaction(
        self, from_wallet_id: int, to_wallet_id: int, amount: int, same_user: bool
    ) -> None:
        self._transaction_repository.create_transaction(
            from_wallet_id, to_wallet_id, amount, same_user
        )
