from unittest.mock import ANY

import pytest
from faker import Faker
from starlette.testclient import TestClient

from bitcoin_wallet.app.runner.setup import init_app

faker: Faker = Faker()


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def test_should_not_create_wallet_with_empty_api_key(client: TestClient) -> None:
    response = client.post("/wallets", json={})
    assert response.status_code == 401
    assert response.json() == {"message": "API key is missing"}


def test_should_not_create_wallet_with_invalid_api_key(client: TestClient) -> None:
    response = client.post("/wallets", json={}, headers={"X-API-KEY": "key"})
    assert response.status_code == 401
    assert response.json() == {"message": "given API key doesn't belong to any user"}


def test_should_create_wallet(client: TestClient) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    assert response.status_code == 201
    assert response.json() == {
        "wallet": {"address": ANY, "balance": {"BTC": 1, "USD": ANY}}
    }
