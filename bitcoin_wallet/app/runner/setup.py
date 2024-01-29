from dotenv import load_dotenv
from fastapi import FastAPI

from bitcoin_wallet.app.core.repository.user_repository import UserRepository
from bitcoin_wallet.app.core.repository.wallet_repository import WalletRepository
from bitcoin_wallet.app.core.service.convert_service import CoingateConvertService
from bitcoin_wallet.app.core.service.user_service import UserService
from bitcoin_wallet.app.core.service.wallet_service import WalletService
from bitcoin_wallet.app.infra.fastapi import wallet_api
from bitcoin_wallet.app.infra.fastapi.users import user_api
from bitcoin_wallet.app.infra.sqlite.database import Database, DatabaseInitializer


def init_app() -> FastAPI:
    load_dotenv()
    app = FastAPI()
    db = Database()
    DatabaseInitializer.init_tables(db)

    app.include_router(user_api)
    app.include_router(wallet_api)

    wallet_repository = WalletRepository(db)
    convertor = CoingateConvertService()

    app.state.users = UserRepository(db)
    app.state.user_service = UserService(app.state.users)
    app.state.wallet_service = WalletService(wallet_repository, convertor)

    return app
