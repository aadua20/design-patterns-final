from fastapi import APIRouter
from pydantic import BaseModel

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
def create_user() -> WalletItemEnvelope:
    return WalletItemEnvelope(wallet=WalletItem(address="1", balance=2))
