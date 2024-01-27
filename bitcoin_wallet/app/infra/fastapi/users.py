from fastapi import APIRouter
from pydantic import BaseModel

from bitcoin_wallet.app.core.model.user import User
from bitcoin_wallet.app.infra.fastapi.dependables import UserRepositoryDependable

user_api = APIRouter(tags=["Users"])


class CreateUserRequest(BaseModel):
    username: str


class UserItem(BaseModel):
    user_id: int
    username: str
    wallet_count: int
    api_key: str


class UserItemEnvelope(BaseModel):
    user: UserItem


class UserListEnvelope(BaseModel):
    users: list[UserItem]


@user_api.post(
    "/users",
    status_code=201,
    response_model=UserItemEnvelope,
)
def create_user(request: CreateUserRequest, users: UserRepositoryDependable):
    print("ANAA")
    user = User(**request.model_dump())
    users.create(user)

    return {"user": user}
