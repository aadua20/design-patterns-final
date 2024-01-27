from typing import Any
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.errors import ExistsError
from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.infra.fastapi.dependables import UserRepositoryDependable

user_api = APIRouter(tags=["Users"])


class CreateUserRequest(BaseModel):
    username: str


class UserItem(BaseModel):
    api_key: UUID
    user_id: UUID
    username: str
    wallet_count: int


class UserItemEnvelope(BaseModel):
    user: UserItem


class UserListEnvelope(BaseModel):
    users: list[UserItem]


# TODO
# id - გვაქვს uuid - გვინდა იყოს auto increment რიცხვი
# wallet_count საერთოდ რომ არ გადავცეთ კარგი იქნებოდა
@user_api.post(
    "/users",
    status_code=201,
    response_model=UserItemEnvelope,
)
def create_user(
    request: CreateUserRequest, users: UserRepositoryDependable
) -> dict[str, Any] | JSONResponse:
    try:
        user = User(username=request.username, wallet_count=0)
        users.add_user(user)

        return {"user": user}
    except ExistsError:
        return JSONResponse(
            status_code=409,
            content={
                "message": f"User with username<{request.username}> already exist."
            },
        )
