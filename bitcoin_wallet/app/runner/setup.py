from fastapi import FastAPI

from bitcoin_wallet.app.infra.fastapi.users import user_api
from bitcoin_wallet.app.infra.sqlite.database import Database, DatabaseInitializer


def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(user_api)
    db = Database()
    DatabaseInitializer.init_tables(db)

    return app
