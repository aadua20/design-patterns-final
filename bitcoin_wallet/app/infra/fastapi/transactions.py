from typing import Annotated, Any

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.errors import (
    InvalidAddressError,
    InvalidBalanceError,
    InvalidTransactionError,
)
from bitcoin_wallet.app.core.model.transaction import TransactionItem
from bitcoin_wallet.app.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
    WalletServiceDependable,
)

transaction_api = APIRouter(tags=["Transactions"])


class TransactionItemEnvelope(BaseModel):
    transaction: TransactionItem


class TransactionListEnvelope(BaseModel):
    transactions: list[TransactionItem]


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


@transaction_api.get(
    "/transactions",
    status_code=200,
    response_model=TransactionListEnvelope,
)
def get_transactions(
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
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
    transactions = transaction_service.get_user_transactions(int(user.get_id()))
    if not transactions:
        return JSONResponse(
            status_code=200,
            content={"message": f"No transactions found for {user.get_username()}."},
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
