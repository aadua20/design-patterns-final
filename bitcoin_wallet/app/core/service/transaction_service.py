from typing import List

from bitcoin_wallet.app.core.errors import (
    InvalidAddressError,
    InvalidBalanceError,
    InvalidTransactionError,
    InvalidWalletError,
)
from bitcoin_wallet.app.core.model.transaction import Statistics, Transaction
from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.core.repository.transaction_repository import (
    ITransactionRepository,
)
from bitcoin_wallet.app.core.service.wallet_service import WalletService


class TransactionService:
    def __init__(
        self,
        transaction_repository: ITransactionRepository,
        wallet_service: WalletService,
    ):
        self._transaction_repository = transaction_repository
        self._wallet_service = wallet_service

    def create_transaction(
        self,
        from_wallet_address: str,
        to_wallet_address: str,
        amount: int,
        caller: User,
    ) -> None:
        from_wallet = self._wallet_service.get_wallet_by_address(from_wallet_address)
        to_wallet = self._wallet_service.get_wallet_by_address(to_wallet_address)

        if from_wallet is None or to_wallet is None:
            raise InvalidAddressError

        if (
            caller.get_id() != str(from_wallet.user_id)
            or from_wallet_address == to_wallet_address
        ):
            raise InvalidTransactionError

        from_balance = from_wallet.satoshi
        to_balance = to_wallet.satoshi

        if from_balance < amount or amount <= 0:
            raise InvalidBalanceError

        same_user = from_wallet.user_id == to_wallet.user_id
        profit = 0 if same_user else amount * 0.015
        self._transaction_repository.create_transaction(
            from_wallet.id, to_wallet.id, amount, profit
        )

        self._wallet_service.update_wallet_balance(
            from_wallet.id, from_balance - amount
        )
        self._wallet_service.update_wallet_balance(to_wallet.id, to_balance + amount)

    def get_transactions(self) -> List[Transaction]:
        return self._transaction_repository.get_transactions()

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return self._transaction_repository.get_user_transactions(user_id)

    def get_wallet_transactions(self, address: str) -> List[Transaction]:
        wallet = self._wallet_service.get_wallet_by_address(address)
        if wallet is None:
            raise InvalidWalletError
        return self._transaction_repository.get_wallet_transactions(wallet.get_id())

    def get_statistics(self) -> Statistics:
        return self._transaction_repository.get_statistics()
