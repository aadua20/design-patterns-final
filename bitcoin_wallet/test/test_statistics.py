import os
from unittest.mock import ANY

import pytest
from faker import Faker
from starlette.testclient import TestClient

from bitcoin_wallet.app.runner.setup import init_app

faker: Faker = Faker()


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def test_get_statistics_with_missing_api_key(client: TestClient) -> None:
    response = client.get("/statistics")
    assert response.status_code == 401
    assert response.json() == {"message": "API key is missing"}


def test_get_statistics_with_valid_api_key_and_existing_user(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]

    response = client.get("/statistics", headers={"X-API-KEY": api_key})
    assert response.status_code == 401
    assert response.json() == {"message": "Invalid API key"}


def test_get_statistics_with_valid_admin_user(client: TestClient) -> None:
    response = client.get(
        "/statistics", headers={"X-API-KEY": str(os.getenv("ADMIN_API_KEY"))}
    )
    assert response.status_code == 200
    assert response.json() == {"statistics": {"num_transactions": ANY, "profit": ANY}}
