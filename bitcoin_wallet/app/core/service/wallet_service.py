from bitcoin_wallet.app.core.repository.wallet_repository import IWalletRepository


class WalletService:
    def __init__(self, wallet_repository: IWalletRepository):
        self._wallet_repository = wallet_repository

    def create_wallet(self, user_id: int) -> str:
        return self._wallet_repository.create_wallet(user_id)
