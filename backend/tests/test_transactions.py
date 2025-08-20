import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, Transaction, ChildProfile
from datetime import datetime, timedelta, timezone

@pytest.mark.asyncio
async def test_get_user_transactions_success(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    txn = Transaction(user_id=child_id, type="earn", amount=20, description="Allowance", category="bonus", created_at=datetime.now(timezone.utc))
    session.add(txn)
    await session.commit()
    response = await client.get(f"/api/users/{child_id}/transactions")
    assert response.status_code == 200
    data = response.json()
    assert any(t["description"] == "Allowance" for t in data["transactions"])

@pytest.mark.asyncio
async def test_get_user_transactions_filter_type(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    txn = Transaction(user_id=child_id, type="spend", amount=10, description="Candy", category="food", created_at=datetime.now(timezone.utc))
    session.add(txn)
    await session.commit()
    response = await client.get(f"/api/users/{child_id}/transactions?type=spend")
    assert response.status_code == 200
    data = response.json()
    assert all(t["type"] == "spend" for t in data["transactions"])

@pytest.mark.asyncio
async def test_create_transaction_success(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    profile = profile.scalar_one()
    profile.coins = 100
    session.add(profile)
    await session.commit()
    txn_data = {"type": "spend", "amount": 30, "description": "Buy Book", "category": "education"}
    response = await client.post(f"/api/users/{child_id}/transactions", json=txn_data)
    assert response.status_code == 200
    data = response.json()
    assert data["new_coin_balance"] == 70

@pytest.mark.asyncio
async def test_create_transaction_insufficient_coins(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    profile = profile.scalar_one()
    profile.coins = 10
    session.add(profile)
    await session.commit()
    txn_data = {"type": "spend", "amount": 50, "description": "Expensive Item", "category": "toys"}
    response = await client.post(f"/api/users/{child_id}/transactions", json=txn_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient coins for spending"

@pytest.mark.asyncio
async def test_get_user_transactions_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get("/api/users/otheruser/transactions")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_transaction_forbidden(auth_client: dict):
    client = auth_client["client"]
    txn_data = {"type": "earn", "amount": 10, "description": "Not allowed", "category": "bonus"}
    response = await client.post("/api/users/otheruser/transactions", json=txn_data)
    assert response.status_code == 403
