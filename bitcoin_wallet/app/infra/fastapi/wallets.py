from typing import Annotated

from fastapi import APIRouter, Header, Path
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.errors import (
    InvalidWalletError,
    MaximumNumberOfWalletsError,
)
from bitcoin_wallet.app.core.model.transaction import TransactionItem
from bitcoin_wallet.app.core.model.wallet import WalletItem
from bitcoin_wallet.app.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
    WalletServiceDependable,
)
from bitcoin_wallet.app.infra.fastapi.transactions import TransactionListEnvelope

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


@wallet_api.get(
    "/wallets/{address}",
    response_model=WalletItemEnvelope,
)
def get_wallet_by_address(
    wallet_service: WalletServiceDependable,
    user_service: UserServiceDependable,
    address: str = Path(..., title="The address of the wallet"),
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
    wallet = wallet_service.get_wallet_by_address(address)
    if wallet is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Wallet not found for the given address"},
        )
    if not wallet_service.check_user_has_wallet(
        int(user.get_id()), wallet.get_address()
    ):
        return JSONResponse(
            status_code=403,
            content={"message": "You do not have permission to access this wallet"},
        )
    return WalletItemEnvelope(wallet=wallet_service.map_wallet_to_walletItem(wallet))


@wallet_api.get(
    "/wallets/{address}/transactions",
    response_model=TransactionListEnvelope,
)
def get_wallet_transactions(
    wallet_service: WalletServiceDependable,
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
    address: str = Path(..., title="The address of the wallet"),
    x_api_key: Annotated[str | None, Header()] = None,
) -> TransactionListEnvelope | JSONResponse:
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
        transactions = transaction_service.get_wallet_transactions(address)
    except InvalidWalletError:
        return JSONResponse(
            status_code=404,
            content={"message": "Wallet not found for the given address"},
        )
    wallet = wallet_service.get_wallet_by_address(address)
    if not wallet_service.check_user_has_wallet(
        int(user.get_id()), wallet.get_address()  # type: ignore
    ):
        return JSONResponse(
            status_code=403,
            content={"message": "You do not have permission to access this wallet"},
        )
    transaction_items = [
        TransactionItem(
            from_wallet_address=wallet_service.get_wallet_by_id(
                t.get_from_wallet_id()  # type: ignore
            ).get_address(),
            to_wallet_address=wallet_service.get_wallet_by_id(
                t.get_to_wallet_id()  # type: ignore
            ).get_address(),
            amount=t.get_amount(),
        )
        for t in transactions
    ]
    return TransactionListEnvelope(transactions=transaction_items)
