import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile

@pytest.mark.asyncio
async def test_get_current_user_profile_success(auth_child_client: dict):
    client = auth_child_client["client"]
    response = await client.get("/api/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "role" in data

@pytest.mark.asyncio
async def test_get_user_profile_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = User(id="child1", email="child1@demo.com", name="Child One", role="younger_child")
    session.add(child)
    await session.commit()
    response = await client.get(f"/api/users/{child.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "child1"
    assert data["role"] == "younger_child"

@pytest.mark.asyncio
async def test_update_user_profile_success(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/api/users/{child_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_create_child_account_success(auth_parent_client: dict):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child_data = {"email": "newchild@demo.com", "password": "pass123", "name": "New Child", "age": 10}
    response = await client.post(f"/api/users/{parent_id}/children", json=child_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newchild@demo.com"
    assert data["role"] in ["younger_child", "older_child"]

@pytest.mark.asyncio
async def test_get_coins_success(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    profile = profile.scalar_one()
    profile.coins = 50
    session.add(profile)
    await session.commit()
    response = await client.get(f"/api/users/{child_id}/coins")
    assert response.status_code == 200
    assert response.json() == 50

@pytest.mark.asyncio
async def test_update_coins_success(auth_child_client: dict, session: AsyncSession):
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    profile = profile.scalar_one()
    profile.coins = 20
    session.add(profile)
    await session.commit()
    update_data = {"coins": 100}
    response = await client.post(f"/api/users/{child_id}/coins", json=update_data)
    assert response.status_code == 200
    assert response.json() == 100

@pytest.mark.asyncio
async def test_get_user_profile_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get(f"/api/users/otheruser")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_profile_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.put(f"/api/users/otheruser", json={"name": "Should Fail"})
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_child_account_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.post(f"/api/users/otherparent/children", json={"email": "fail@demo.com", "password": "fail", "name": "Fail", "age": 8})
    assert response.status_code == 403
