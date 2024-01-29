import uuid
from typing import Protocol

from bitcoin_wallet.app.core.model.wallet import Wallet
from bitcoin_wallet.app.infra.sqlite.database import Database


class IWalletRepository(Protocol):
    def create_wallet(self, user_id: int) -> Wallet:
        pass

    def get_wallet_id_by_address(self, address: str) -> int | None:
        pass

    def get_wallet_user_id_by_address(self, address: str) -> int | None:
        pass

    def get_wallet_balance_by_address(self, address: str) -> int:
        pass

    def update_wallet_balance(self, wallet_id: int, amount: int) -> None:
        pass


def generate_unique_address() -> str:
    return str(uuid.uuid4())


class WalletRepository(IWalletRepository):
    _db: Database

    def __init__(self, db: Database):
        self._db = db

    def create_wallet(self, user_id: int) -> Wallet:
        address = generate_unique_address()
        initial_satoshi = 100_000_000
        query = """
            INSERT INTO wallets (user_id, address, satoshi)
            VALUES (?, ?, ?)
        """
        self._db.execute_query(query, (user_id, address, initial_satoshi))
        return Wallet(address=address, satoshi=initial_satoshi)

    def get_wallet_id_by_address(self, address: str) -> int | None:
        query = "SELECT id FROM wallets WHERE address = ?"
        wallet = self._db.fetch_one(query, (address,))
        return wallet[0] if wallet else None

    def get_wallet_user_id_by_address(self, address: str) -> int | None:
        query = "SELECT user_id FROM wallets WHERE address = ?"
        wallet = self._db.fetch_one(query, (address,))
        return wallet[0] if wallet else None

    def get_wallet_balance_by_address(self, address: str) -> int:
        query = "SELECT satoshi FROM wallets WHERE address = ?"
        wallet = self._db.fetch_one(query, (address,))
        return int(wallet[0])

    def update_wallet_balance(self, wallet_id: int, amount: int) -> None:
        query = """
                    UPDATE wallets
                    SET satoshi = ?
                    WHERE id = ?
                    """
        self._db.execute_query(query, (amount, wallet_id))
