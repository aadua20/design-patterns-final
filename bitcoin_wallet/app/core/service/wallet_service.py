from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.core.repository.wallet_repository import IWalletRepository
from bitcoin_wallet.app.core.service.convert_service import IConvertor


class WalletService:
    def __init__(self, wallet_repository: IWalletRepository, convertor: IConvertor):
        self._wallet_repository = wallet_repository
        self._convertor = convertor

    def create_wallet(self, user_id: int) -> WalletItem:
        wallet = self._wallet_repository.create_wallet(user_id)
        btc: float = wallet.satoshi / 100_000_000
        balance_dict = {"BTC": btc, "USD": self._convertor.btc_to_usd(btc)}
        return WalletItem(address=wallet.address, balance=balance_dict)

    def get_wallet_id_by_address(self, address: str) -> int | None:
        return self._wallet_repository.get_wallet_id_by_address(address)

    def get_wallet_user_id_by_address(self, address: str) -> int | None:
        return self._wallet_repository.get_wallet_user_id_by_address(address)

    def get_wallet_balance_by_address(self, address: str) -> int:
        return self._wallet_repository.get_wallet_balance_by_address(address)

    def update_wallet_balance(self, wallet_id: int, amount: int) -> None:
        return self._wallet_repository.update_wallet_balance(wallet_id, amount)
