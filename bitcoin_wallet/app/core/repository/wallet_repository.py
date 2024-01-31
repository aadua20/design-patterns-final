import uuid
from typing import Protocol

from bitcoin_wallet.app.core.model.wallet import Wallet
from bitcoin_wallet.app.infra.sqlite.database import Database


class IWalletRepository(Protocol):
    def create_wallet(self, user_id: int) -> Wallet:
        pass

    def get_wallet_by_address(self, address: str) -> Wallet | None:
        pass

    def update_wallet_balance(self, wallet_id: int | None, amount: int) -> None:
        pass

    def get_user_wallets(self, user_id: int) -> list[Wallet]:
        pass

    def get_wallet_by_id(self, wallet_id) -> Wallet | None:
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
        return Wallet(address=address, satoshi=initial_satoshi, user_id=user_id)

    def get_wallet_by_address(self, address: str) -> Wallet | None:
        query = "SELECT id, user_id, address, satoshi FROM wallets WHERE address = ?"
        wallet = self._db.fetch_one(query, (address,))
        return (
            Wallet(
                id=wallet[0], user_id=wallet[1], address=wallet[2], satoshi=wallet[3]
            )
            if wallet
            else None
        )

    def update_wallet_balance(self, wallet_id: int | None, amount: int) -> None:
        query = """
                    UPDATE wallets
                    SET satoshi = ?
                    WHERE id = ?
                    """
        self._db.execute_query(query, (amount, wallet_id))

    def get_user_wallets(self, user_id: int) -> list[Wallet]:
        query = """
            SELECT id, user_id, address, satoshi
            FROM wallets
            WHERE user_id = ?
        """
        results = self._db.fetch_all(query, (user_id,))

        user_wallets = [
            Wallet(user_id=result[0], address=result[1], satoshi=result[2]) for result in results
        ]
        return user_wallets

    def get_wallet_by_id(self, wallet_id) -> Wallet | None:
        query = "SELECT * FROM wallets WHERE id = ?"
        wallet = self._db.fetch_one(query, (wallet_id,))
        return (
            Wallet(
                id=wallet[0], user_id=wallet[1], address=wallet[2], satoshi=wallet[3]
            )
            if wallet
            else None
        )
