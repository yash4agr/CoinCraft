import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile, Goal, Transaction

# Placeholder for teen endpoint tests. Add tests when context is available.

@pytest.mark.asyncio
async def test_get_teen_dashboard_success(auth_teen_client: dict, session: AsyncSession):
    client = auth_teen_client["client"]
    teen_id = auth_teen_client["user_id"]
    profile = ChildProfile(user_id=teen_id, coins=200, level=4, streak_days=10)
    session.add(profile)
    await session.commit()
    response = await client.get("/api/teen/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "teen" in data
    assert "budget_overview" in data
    assert "goals" in data
    assert "activities" in data
    assert "achievements" in data
    assert "stats" in data

@pytest.mark.asyncio
async def test_get_teen_dashboard_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get("/api/teen/dashboard")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_teen_goals_success(auth_teen_client: dict, session: AsyncSession):
    client = auth_teen_client["client"]
    teen_id = auth_teen_client["user_id"]
    goal = Goal(user_id=teen_id, title="Save for Laptop", target_amount=500, current_amount=100)
    session.add(goal)
    await session.commit()
    response = await client.get("/api/teen/goals")
    assert response.status_code == 200
    data = response.json()
    assert any(g["title"] == "Save for Laptop" for g in data)

@pytest.mark.asyncio
async def test_create_teen_goal_success(auth_teen_client: dict, session: AsyncSession):
    client = auth_teen_client["client"]
    teen_id = auth_teen_client["user_id"]
    goal_data = {"title": "New Phone", "target_amount": 800, "description": "Save for a phone"}
    response = await client.post("/api/teen/goals", json=goal_data)
    assert response.status_code == 200
    data = response.json()
    assert data["goal"]["title"] == "New Phone"
    assert data["goal"]["target_amount"] == 800

@pytest.mark.asyncio
async def test_get_teen_activities_success(auth_teen_client: dict):
    client = auth_teen_client["client"]
    response = await client.get("/api/teen/explore")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_conversion_request_success(auth_teen_client: dict, session: AsyncSession):
    client = auth_teen_client["client"]
    teen_id = auth_teen_client["user_id"]
    profile = ChildProfile(user_id=teen_id, coins=100)
    session.add(profile)
    await session.commit()
    request_data = {"coins_amount": 50, "description": "Convert coins"}
    response = await client.post("/api/teen/conversion-requests", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True or "remaining_coins" in data

@pytest.mark.asyncio
async def test_get_conversion_requests_success(auth_teen_client: dict):
    client = auth_teen_client["client"]
    response = await client.get("/api/teen/conversion-requests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_teen_analytics_success(auth_teen_client: dict):
    client = auth_teen_client["client"]
    response = await client.get("/api/teen/analytics")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
