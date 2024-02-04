from dotenv import load_dotenv
from fastapi import FastAPI

from bitcoin_wallet.app.core.repository.transaction_repository import (
    TransactionRepository,
)
from bitcoin_wallet.app.core.repository.user_repository import UserRepository
from bitcoin_wallet.app.core.repository.wallet_repository import WalletRepository
from bitcoin_wallet.app.core.service.convert_service import ConvertService
from bitcoin_wallet.app.core.service.transaction_service import TransactionService
from bitcoin_wallet.app.core.service.user_service import UserService
from bitcoin_wallet.app.core.service.wallet_service import WalletService
from bitcoin_wallet.app.infra.fastapi import transaction_api, user_api, wallet_api
from bitcoin_wallet.app.infra.fastapi.statistics import statistics_api
from bitcoin_wallet.app.infra.sqlite.database import Database, DatabaseInitializer


def init_app() -> FastAPI:
    load_dotenv()
    app = FastAPI()
    db = Database()
    DatabaseInitializer.init_tables(db)

    app.include_router(user_api)
    app.include_router(wallet_api)
    app.include_router(transaction_api)
    app.include_router(statistics_api)

    wallet_repository = WalletRepository(db)
    user_repository = UserRepository(db)
    transaction_repository = TransactionRepository(db)
    convertor = ConvertService()

    app.state.user_service = UserService(user_repository)
    app.state.wallet_service = WalletService(wallet_repository, convertor)
    app.state.transaction_service = TransactionService(
        transaction_repository, app.state.wallet_service
    )

    return app
