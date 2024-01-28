from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.core.repository.wallet_repository import IWalletRepository


class WalletService:
    def __init__(self, wallet_repository: IWalletRepository):
        self._wallet_repository = wallet_repository

    def create_wallet(self, user_id: int) -> WalletItem:
        wallet = self._wallet_repository.create_wallet(user_id)
        balance_dict = {"BTC": wallet.satoshi / 100_000_000}
        return WalletItem(address=wallet.address, balance=balance_dict)
