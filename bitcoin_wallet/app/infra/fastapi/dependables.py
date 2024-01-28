from typing import Annotated

from fastapi import Depends
from fastapi.requests import Request

from bitcoin_wallet.app.core.repository.user_repository import UserRepository
from bitcoin_wallet.app.core.service.wallet_service import WalletService


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.users  # type: ignore


def get_wallet_service(request: Request) -> WalletService:
    return request.app.state.wallet_service  # type: ignore


UserRepositoryDependable = Annotated[UserRepository, Depends(get_user_repository)]
WalletServiceDependable = Annotated[WalletService, Depends(get_wallet_service)]
