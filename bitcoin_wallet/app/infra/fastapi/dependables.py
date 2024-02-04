from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from bitcoin_wallet.app.core.service.transaction_service import TransactionService
from bitcoin_wallet.app.core.service.user_service import UserService
from bitcoin_wallet.app.core.service.wallet_service import WalletService


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service  # type: ignore


def get_wallet_service(request: Request) -> WalletService:
    return request.app.state.wallet_service  # type: ignore


def get_transaction_service(request: Request) -> TransactionService:
    return request.app.state.transaction_service  # type: ignore


UserServiceDependable = Annotated[UserService, Depends(get_user_service)]
WalletServiceDependable = Annotated[WalletService, Depends(get_wallet_service)]
TransactionServiceDependable = Annotated[
    TransactionService, Depends(get_transaction_service)
]
