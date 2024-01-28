from fastapi import APIRouter
from pydantic import BaseModel

from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.infra.fastapi.dependables import WalletServiceDependable

wallet_api = APIRouter(tags=["Wallets"])


class WalletItemEnvelope(BaseModel):
    wallet: WalletItem


@wallet_api.post(
    "/wallets",
    status_code=201,
    response_model=WalletItemEnvelope,
)
def create_user(wallet_service: WalletServiceDependable) -> WalletItemEnvelope:
    wallet_item: WalletItem = wallet_service.create_wallet(1)
    return WalletItemEnvelope(wallet=wallet_item)
