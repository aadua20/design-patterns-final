from typing import Annotated, Any

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.model.transaction import TransactionItem
from bitcoin_wallet.app.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
    WalletServiceDependable,
)

transaction_api = APIRouter(tags=["Transactions"])


class TransactionItemEnvelope(BaseModel):
    transaction: TransactionItem


class CreateTransactionRequest(BaseModel):
    from_wallet_address: str
    to_wallet_address: str
    amount: int


@transaction_api.post(
    "/transactions",
    status_code=201,
    response_model=TransactionItemEnvelope,
)
def create_transaction(
    request: CreateTransactionRequest,
    user_service: UserServiceDependable,
    wallet_service: WalletServiceDependable,
    transaction_service: TransactionServiceDependable,
    x_api_key: Annotated[str | None, Header()] = None,
) -> dict[str, Any] | JSONResponse:
    _transaction = TransactionItem(**request.model_dump())
    sender_id = wallet_service.get_wallet_user_id_by_address(
        _transaction.from_wallet_address
    )
    receiver_id = wallet_service.get_wallet_user_id_by_address(
        _transaction.to_wallet_address
    )
    from_wallet_id = wallet_service.get_wallet_id_by_address(
        _transaction.from_wallet_address
    )
    to_wallet_id = wallet_service.get_wallet_id_by_address(
        _transaction.to_wallet_address
    )

    if (
        sender_id is None
        or receiver_id is None
        or from_wallet_id is None
        or to_wallet_id is None
    ):
        return JSONResponse(
            status_code=401,
            content={"message": "invalid wallet address"},
        )

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

    if user.get_id() != str(sender_id):
        return JSONResponse(
            status_code=400,
            content={
                "message": "You must be the owner to make transaction from a wallet."
            },
        )

    if _transaction.from_wallet_address == _transaction.to_wallet_address:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Source and dest wallet addresses cannot be identical."
            },
        )

    from_balance = wallet_service.get_wallet_balance_by_address(
        _transaction.from_wallet_address
    )
    to_balance = wallet_service.get_wallet_balance_by_address(
        _transaction.to_wallet_address
    )

    if from_balance < _transaction.amount:
        return JSONResponse(
            status_code=400,
            content={"message": "Insufficient funds in the source wallet."},
        )

    same_user = sender_id == receiver_id
    transaction_service.create_transaction(
        from_wallet_id, to_wallet_id, _transaction.amount, same_user
    )

    wallet_service.update_wallet_balance(
        from_wallet_id, from_balance - _transaction.amount
    )
    wallet_service.update_wallet_balance(to_wallet_id, to_balance + _transaction.amount)

    return {"transaction": _transaction}
