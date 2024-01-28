from fastapi import APIRouter
from pydantic import BaseModel

from bitcoin_wallet.app.infra.fastapi.dependables import WalletServiceDependable

wallet_api = APIRouter(tags=["Wallets"])


class WalletItem(BaseModel):
    address: str
    balance: int


class WalletItemEnvelope(BaseModel):
    wallet: WalletItem


@wallet_api.post(
    "/wallets",
    status_code=201,
    response_model=WalletItemEnvelope,
)
def create_user(wallet_service: WalletServiceDependable) -> WalletItemEnvelope:
    address = wallet_service.create_wallet(1)
    return WalletItemEnvelope(wallet=WalletItem(address=address, balance=2))
