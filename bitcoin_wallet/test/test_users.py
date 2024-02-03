from unittest.mock import ANY

import pytest
from faker import Faker
from starlette.testclient import TestClient

from bitcoin_wallet.app.runner.setup import init_app

faker: Faker = Faker()


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def test_should_create_user(client: TestClient) -> None:
    username = faker.name()
    response = client.post("/users", json={"username": username})
    assert response.status_code == 201
    assert response.json() == {
        "user": {"api_key": ANY, "username": username, "wallet_count": 0}
    }


def test_should_not_create_user_with_same_username(client: TestClient) -> None:
    username = faker.name()
    client.post("/users", json={"username": username})
    response = client.post("/users", json={"username": username})
    assert response.status_code == 409
    assert response.json() == {
        "message": f"User with username<{username}> already exist."
    }
