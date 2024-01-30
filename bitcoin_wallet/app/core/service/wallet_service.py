from bitcoin_wallet.app.core.errors import MaximumNumberOfWalletsError
from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.core.repository.wallet_repository import IWalletRepository
from bitcoin_wallet.app.core.service.convert_service import IConvertor


class WalletService:
    MAX_WALLET_SUPPORT = 3

    def __init__(self, wallet_repository: IWalletRepository, convertor: IConvertor):
        self._wallet_repository = wallet_repository
        self._convertor = convertor

    def _check_user_has_available_wallet_slots(self, user_id: int) -> None:
        user_wallets = self._wallet_repository.get_user_wallets(user_id)
        if len(user_wallets) == WalletService.MAX_WALLET_SUPPORT:
            raise MaximumNumberOfWalletsError

    def create_wallet(self, user_id: int) -> WalletItem:
        self._check_user_has_available_wallet_slots(user_id)
        wallet = self._wallet_repository.create_wallet(user_id)
        btc: float = wallet.satoshi / 100_000_000
        balance_dict = {"BTC": btc, "USD": self._convertor.btc_to_usd(btc)}
        return WalletItem(address=wallet.address, balance=balance_dict)
