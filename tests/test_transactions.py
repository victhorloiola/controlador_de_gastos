import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def create_category(client: TestClient, name: str, transaction_type: str):
    response = client.post(
        "/categories",
        json={"name": name, "type": transaction_type},
    )

    assert response.status_code == 201

    return response.json()


def create_transaction(
    client: TestClient,
    category_id: int,
    description: str = "Market",
    amount: str = "120.50",
    transaction_date: str = "2026-07-10",
    transaction_type: str = "expense",
):
    response = client.post(
        "/transactions",
        json={
            "description": description,
            "amount": amount,
            "date": transaction_date,
            "type": transaction_type,
            "category_id": category_id,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_transaction(client: TestClient):
    category = create_category(client, name="Food", transaction_type="expense")

    transaction = create_transaction(
        client,
        category_id=category["id"],
        description="Groceries",
        amount="89.90",
    )

    assert transaction["description"] == "Groceries"
    assert transaction["amount"] == "89.90"
    assert transaction["type"] == "expense"
    assert transaction["category_id"] == category["id"]
    assert "id" in transaction


def test_create_transaction_requires_existing_category(client: TestClient):
    response = client.post(
        "/transactions",
        json={
            "description": "Invalid transaction",
            "amount": "50.00",
            "date": "2026-07-10",
            "type": "expense",
            "category_id": 999,
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_transaction_crud_flow(client: TestClient):
    category = create_category(client, name="Salary", transaction_type="income")
    transaction = create_transaction(
        client,
        category_id=category["id"],
        description="July salary",
        amount="3000.00",
        transaction_type="income",
    )

    get_response = client.get(f"/transactions/{transaction['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["description"] == "July salary"

    update_response = client.put(
        f"/transactions/{transaction['id']}",
        json={"description": "Updated July salary"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated July salary"

    delete_response = client.delete(f"/transactions/{transaction['id']}")
    assert delete_response.status_code == 204

    not_found_response = client.get(f"/transactions/{transaction['id']}")
    assert not_found_response.status_code == 404
    assert not_found_response.json() == {"detail": "Transaction not found"}


def test_list_transactions_with_filters(client: TestClient):
    food_category = create_category(client, name="Food", transaction_type="expense")
    salary_category = create_category(client, name="Salary", transaction_type="income")

    create_transaction(
        client,
        category_id=food_category["id"],
        description="Groceries",
        amount="100.00",
        transaction_date="2026-07-01",
    )
    create_transaction(
        client,
        category_id=food_category["id"],
        description="Restaurant",
        amount="80.00",
        transaction_date="2026-07-15",
    )
    create_transaction(
        client,
        category_id=salary_category["id"],
        description="Salary",
        amount="3000.00",
        transaction_date="2026-07-05",
        transaction_type="income",
    )

    category_response = client.get(
        f"/transactions?category_id={food_category['id']}"
    )
    assert category_response.status_code == 200
    assert len(category_response.json()) == 2

    type_response = client.get("/transactions?type=income")
    assert type_response.status_code == 200
    assert len(type_response.json()) == 1
    assert type_response.json()[0]["description"] == "Salary"

    date_response = client.get(
        "/transactions?start_date=2026-07-10&end_date=2026-07-31"
    )
    assert date_response.status_code == 200
    assert len(date_response.json()) == 1
    assert date_response.json()[0]["description"] == "Restaurant"
