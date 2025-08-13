import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ParentProfile, ChildProfile, Goal, Transaction, UserModuleProgress
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_get_parent_dashboard_success(auth_parent_client: dict, session: AsyncSession):
    """
    Test successful retrieval of parent dashboard data.
    """
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]

    # Add a child profile
    child = ChildProfile(user_id="child1", age=10, coins=100, level=2, streak_days=5, parent_id=parent_id)
    session.add(child)
    await session.commit()

    response = await client.get("/api/parent/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "stats" in data
    assert "children" in data
    assert any(c["id"] == "child1" for c in data["children"])

@pytest.mark.asyncio
async def test_add_child_success(auth_parent_client: dict, session: AsyncSession):
    """
    Test successful creation of a child account by parent.
    """
    client = auth_parent_client["client"]
    child_data = {"name": "Test Child", "age": 9}
    response = await client.post("/api/parent/children", json=child_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "child" in data
    assert data["child"]["name"] == "Test Child"

@pytest.mark.asyncio
async def test_get_child_progress_success(auth_parent_client: dict, session: AsyncSession):
    """
    Test successful retrieval of child progress for parent.
    """
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child2", age=12, coins=80, level=3, streak_days=4, parent_id=parent_id)
    session.add(child)
    await session.commit()
    response = await client.get(f"/api/parent/children/{child.user_id}/progress")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_rewards" in data or "lessons_completed" in data

@pytest.mark.asyncio
async def test_get_parent_dashboard_forbidden(auth_client: dict):
    """
    Test that a non-parent user cannot access parent dashboard.
    """
    client = auth_client["client"]
    response = await client.get("/api/parent/dashboard")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_add_child_forbidden(auth_client: dict):
    """
    Test that a non-parent user cannot add a child.
    """
    client = auth_client["client"]
    child_data = {"name": "Forbidden Child", "age": 8}
    response = await client.post("/api/parent/children", json=child_data)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_child_progress_forbidden(auth_client: dict):
    """
    Test that a non-parent user cannot get child progress.
    """
    client = auth_client["client"]
    response = await client.get("/api/parent/children/child2/progress")
    assert response.status_code == 403
