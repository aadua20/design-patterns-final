from dotenv import load_dotenv
from fastapi import FastAPI

from bitcoin_wallet.app.core.repository.user_repository import UserRepository
from bitcoin_wallet.app.infra.fastapi.users import user_api
from bitcoin_wallet.app.infra.sqlite.database import Database, DatabaseInitializer


def init_app() -> FastAPI:
    load_dotenv()
    app = FastAPI()
    db = Database()
    DatabaseInitializer.init_tables(db)

    app.include_router(user_api)

    app.state.users = UserRepository(db)

    return app
