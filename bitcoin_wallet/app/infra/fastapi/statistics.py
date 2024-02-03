import os
from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.responses import JSONResponse

from bitcoin_wallet.app.core.model.transaction import Statistics
from bitcoin_wallet.app.infra.fastapi.dependables import (
    TransactionServiceDependable,
    UserServiceDependable,
)

statistics_api = APIRouter(tags=["Statistics"])


class StatisticsEnvelope(BaseModel):
    statistics: Statistics


@statistics_api.get(
    "/statistics",
    status_code=200,
    response_model=StatisticsEnvelope,
)
def get_statistics(
    user_service: UserServiceDependable,
    transaction_service: TransactionServiceDependable,
    x_api_key: Annotated[str | None, Header()] = None,
) -> StatisticsEnvelope | JSONResponse:
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
    if x_api_key != os.getenv("ADMIN_API_KEY"):
        return JSONResponse(
            status_code=401,
            content={"message": "Invalid API key"},
        )
    statistics: Statistics = transaction_service.get_statistics()

    return StatisticsEnvelope(statistics=statistics)
