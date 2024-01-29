import uuid
from typing import Protocol

from bitcoin_wallet.app.core.model.wallet import Wallet
from bitcoin_wallet.app.infra.sqlite.database import Database


class IWalletRepository(Protocol):
    def create_wallet(self, user_id: int) -> Wallet:
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
