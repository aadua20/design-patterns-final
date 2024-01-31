from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.errors import MaximumNumberOfWalletsError
from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.infra.fastapi.dependables import (
    UserServiceDependable,
    WalletServiceDependable,
)

wallet_api = APIRouter(tags=["Wallets"])


class WalletItemEnvelope(BaseModel):
    wallet: WalletItem


@wallet_api.post(
    "/wallets",
    status_code=201,
    response_model=WalletItemEnvelope,
)
def create_wallet(
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    x_api_key: Annotated[str | None, Header()] = None,
) -> WalletItemEnvelope | JSONResponse:
    if x_api_key is None:
        return JSONResponse(
            status_code=401,
            content={"message": "API key is missing"},
        )
    user = user_service.get_user_by_api_key(x_api_key)
    if user is None:
        return JSONResponse(
            status_code=401,
            content={"message": "given API key doesn't belong to any user"},
        )
    try:
        wallet_item: WalletItem = wallet_service.create_wallet(int(user.get_id()))
    except MaximumNumberOfWalletsError:
        return JSONResponse(
            status_code=400,
            content={"message": "Cannot create more than 3 wallets!"},
        )
    return WalletItemEnvelope(wallet=wallet_item)
