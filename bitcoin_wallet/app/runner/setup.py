from fastapi import FastAPI

from bitcoin_wallet.app.infra.sqlite.database import Database, DatabaseInitializer


def init_app() -> FastAPI:
    app = FastAPI()
    db = Database()
    DatabaseInitializer.init_tables(db)
    return app
