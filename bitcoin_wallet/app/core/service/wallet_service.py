from bitcoin_wallet.app.core.errors import MaximumNumberOfWalletsError
from bitcoin_wallet.app.core.model.wallet import Wallet, WalletItem
from bitcoin_wallet.app.core.repository.wallet_repository import IWalletRepository
from bitcoin_wallet.app.core.service.convert_service import IConvertor


class WalletService:
    MAX_WALLET_SUPPORT = 3

    def __init__(self, wallet_repository: IWalletRepository, convertor: IConvertor):
        self._wallet_repository = wallet_repository
        self._convertor = convertor

    def _check_user_has_available_wallet_slots(self, user_id: int) -> None:
        user_wallets = self._wallet_repository.get_user_wallets(user_id)
        if len(user_wallets) >= WalletService.MAX_WALLET_SUPPORT:
            raise MaximumNumberOfWalletsError

    def create_wallet(self, user_id: int) -> WalletItem:
        self._check_user_has_available_wallet_slots(user_id)
        wallet = self._wallet_repository.create_wallet(user_id)
        return self.map_wallet_to_walletItem(wallet=wallet)

    def map_wallet_to_walletItem(self, wallet: Wallet) -> WalletItem:
        btc: float = wallet.get_satoshi() / 100_000_000
        balance_dict = {"BTC": btc, "USD": self._convertor.btc_to_usd(btc)}
        return WalletItem(address=wallet.get_address(), balance=balance_dict)

    def get_wallet_by_address(self, address: str) -> Wallet | None:
        return self._wallet_repository.get_wallet_by_address(address)

    def update_wallet_balance(self, wallet_id: int | None, amount: int) -> None:
        return self._wallet_repository.update_wallet_balance(wallet_id, amount)
