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
    username = faker.name()
    response = client.post("/users", json={"username": username})
    assert response.status_code == 201
    assert response.json() == {
        "user": {
            "api_key": ANY,
            "username": username,
            "wallet_count": 0
        }
    }

    response = client.post("/users", json={"username": username})
    assert response.status_code == 409
    assert response.json() == {"message": f"User with username<{username}> already exist."}
