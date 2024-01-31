from dataclasses import dataclass
from typing import Annotated, Any

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.errors import (
    InvalidAddressError,
    InvalidBalanceError,
    InvalidTransactionError,
)
from bitcoin_wallet.app.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
)

transaction_api = APIRouter(tags=["Transactions"])


@dataclass
class TransactionItem:
    from_wallet_address: str
    to_wallet_address: str
    amount: int


class TransactionItemEnvelope(BaseModel):
    transaction: TransactionItem


class CreateTransactionRequest(BaseModel):
    from_wallet_address: str
    to_wallet_address: str
    amount: int


@transaction_api.post(
    "/transactions",
    status_code=200,
    response_model=TransactionItemEnvelope,
)
def create_transaction(
    request: CreateTransactionRequest,
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
    x_api_key: Annotated[str | None, Header()] = None,
) -> dict[str, Any] | JSONResponse:
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
        _transaction = TransactionItem(**request.model_dump())
        transaction_service.create_transaction(
            _transaction.from_wallet_address,
            _transaction.to_wallet_address,
            _transaction.amount,
            user,
        )

        return {"transaction": _transaction}
    except InvalidAddressError:
        return JSONResponse(
            status_code=400,
            content={"message": "invalid wallet address"},
        )
    except InvalidTransactionError:
        return JSONResponse(
            status_code=400,
            content={"message": "invalid/alogical transaction."},
        )
    except InvalidBalanceError:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Insufficient funds in the source wallet or invalid amount."
            },
        )
