import pytest
from faker import Faker
from starlette.testclient import TestClient

from bitcoin_wallet.app.runner.setup import init_app

faker: Faker = Faker()


@pytest.fixture
def client() -> TestClient:
    return TestClient(init_app())


def test_should_not_create_transaction_with_empty_api_key(client: TestClient) -> None:
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": "addr_from",
            "to_wallet_address": "addr_to",
            "amount": 0,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"message": "API key is missing"}


def test_should_not_create_transaction_with_invalid_api_key(client: TestClient) -> None:
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": "addr_from",
            "to_wallet_address": "addr_to",
            "amount": 0,
        },
        headers={"X-API-KEY": "key"},
    )
    assert response.status_code == 401
    assert response.json() == {"message": "given API key doesn't belong to any user"}


def test_should_not_create_transaction_with_invalid_wallet_address(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": "addr_from",
            "to_wallet_address": "addr_to",
            "amount": 0,
        },
        headers={"X-API-KEY": api_key},
    )
    assert response.status_code == 400
    assert response.json() == {"message": "invalid wallet address"}


def test_should_not_create_transaction_to_the_same_wallet_address(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address = wallet_response.json()["wallet"]["address"]
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": wallet_address,
            "to_wallet_address": wallet_address,
            "amount": 0,
        },
        headers={"X-API-KEY": api_key},
    )
    assert response.status_code == 400
    assert response.json() == {"message": "invalid/alogical transaction."}


def test_should_not_create_transaction_without_your_wallet_address(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    response = client.post("/users", json={"username": faker.name()})
    api_key2 = response.json()["user"]["api_key"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_from = wallet_response.json()["wallet"]["address"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_to = wallet_response.json()["wallet"]["address"]
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": wallet_address_from,
            "to_wallet_address": wallet_address_to,
            "amount": 0,
        },
        headers={"X-API-KEY": api_key2},
    )
    assert response.status_code == 400
    assert response.json() == {"message": "invalid/alogical transaction."}


def test_should_not_create_transaction_with_insufficient_funds(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_from = wallet_response.json()["wallet"]["address"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_to = wallet_response.json()["wallet"]["address"]
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": wallet_address_from,
            "to_wallet_address": wallet_address_to,
            "amount": 1000000000000000000000,
        },
        headers={"X-API-KEY": api_key},
    )
    assert response.status_code == 400
    assert response.json() == {
        "message": "Insufficient funds in the source wallet or invalid amount."
    }


def test_should_create_transaction(
    client: TestClient,
) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_from = wallet_response.json()["wallet"]["address"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_to = wallet_response.json()["wallet"]["address"]
    response = client.post(
        "/transactions",
        json={
            "from_wallet_address": wallet_address_from,
            "to_wallet_address": wallet_address_to,
            "amount": 100,
        },
        headers={"X-API-KEY": api_key},
    )
    assert response.status_code == 200
    assert response.json() == {
        "transaction": {
            "from_wallet_address": wallet_address_from,
            "to_wallet_address": wallet_address_to,
            "amount": 100,
        }
    }


def test_get_wallet_without_api_key(client: TestClient) -> None:
    response = client.get("/transactions")
    assert response.status_code == 401
    assert response.json() == {"message": "API key is missing"}


def test_get_transactions_with_invalid_api_key(client: TestClient) -> None:
    response = client.get("/transactions", headers={"X-API-KEY": "api_key"})
    assert response.status_code == 401
    assert response.json() == {"message": "given API key doesn't belong to any user"}


def test_get_transactions_with_valid_api_key(client: TestClient) -> None:
    name = faker.name()
    response = client.post("/users", json={"username": name})
    api_key = response.json()["user"]["api_key"]
    client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    response = client.get("/transactions", headers={"X-API-KEY": api_key})
    assert response.status_code == 200
    assert response.json() == {"transactions": []}


def test_get_transactions_no_transactions_found(client: TestClient) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key = response.json()["user"]["api_key"]

    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_from = wallet_response.json()["wallet"]["address"]
    wallet_response = client.post("/wallets", json={}, headers={"X-API-KEY": api_key})
    wallet_address_to = wallet_response.json()["wallet"]["address"]
    client.post(
        "/transactions",
        json={
            "from_wallet_address": wallet_address_from,
            "to_wallet_address": wallet_address_to,
            "amount": 100,
        },
        headers={"X-API-KEY": api_key},
    )

    response = client.get("/transactions", headers={"X-API-KEY": api_key})
    assert response.status_code == 200
    assert len(response.json()["transactions"]) == 1


def test_should_not_get_others_wallets_transactions(client: TestClient) -> None:
    response = client.post("/users", json={"username": faker.name()})
    api_key_1 = response.json()["user"]["api_key"]

    response = client.post("/users", json={"username": faker.name()})
    api_key_2 = response.json()["user"]["api_key"]

    create_wallet_response = client.post(
        "/wallets", json={}, headers={"X-API-KEY": api_key_1}
    )
    wallet_address = create_wallet_response.json()["wallet"]["address"]
    response = client.get(
        f"/wallets/{wallet_address}/transactions", headers={"X-API-KEY": api_key_2}
    )
    assert response.status_code == 403
