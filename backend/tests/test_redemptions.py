import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile, ParentProfile, RedemptionRequest
from datetime import datetime

@pytest.mark.asyncio
async def test_get_conversion_requests_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of conversion requests for a child.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    request = RedemptionRequest(user_id=child_id, coins_amount=50, cash_amount=5.0, description="Convert coins")
    session.add(request)
    await session.commit()
    response = await client.get(f"/api/redemptions/users/{child_id}/conversion-requests")
    assert response.status_code == 200
    data = response.json()
    assert any(r["coins_amount"] == 50 for r in data)

@pytest.mark.asyncio
async def test_create_conversion_request_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful creation of a conversion request.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    # Ensure child has coins and parent profile
    parent_profile = ParentProfile(user_id="parent1", exchange_rate=0.1)
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 100
    child_profile.parent_id = "parent1"
    session.add(parent_profile)
    session.add(child_profile)
    await session.commit()
    request_data = {"coins_amount": 50, "description": "Convert coins"}
    response = await client.post(f"/api/redemptions/users/{child_id}/conversion-requests", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert data["remaining_coins"] == 50

@pytest.mark.asyncio
async def test_create_conversion_request_insufficient_coins(auth_child_client: dict, session: AsyncSession):
    """
    Test creating a conversion request with insufficient coins.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 10
    session.add(child_profile)
    await session.commit()
    request_data = {"coins_amount": 50, "description": "Convert coins"}
    response = await client.post(f"/api/redemptions/users/{child_id}/conversion-requests", json=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient coins"

@pytest.mark.asyncio
async def test_approve_redemption_request_success(auth_parent_client: dict, session: AsyncSession):
    """
    Test successful approval of a redemption request by parent.
    """
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child3", coins=100, parent_id=parent_id)
    session.add(child)
    await session.commit()
    request = RedemptionRequest(user_id="child3", coins_amount=50, cash_amount=5.0, description="Convert coins")
    session.add(request)
    await session.commit()
    response = await client.put(f"/api/redemptions/redemption-requests/{request.id}/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"

@pytest.mark.asyncio
async def test_reject_redemption_request_success(auth_parent_client: dict, session: AsyncSession):
    """
    Test successful rejection of a redemption request by parent.
    """
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child4", coins=100, parent_id=parent_id)
    session.add(child)
    await session.commit()
    request = RedemptionRequest(user_id="child4", coins_amount=30, cash_amount=3.0, description="Convert coins")
    session.add(request)
    await session.commit()
    response = await client.put(f"/api/redemptions/redemption-requests/{request.id}/reject")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"

@pytest.mark.asyncio
async def test_approve_redemption_request_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-parent user cannot approve redemption requests.
    """
    client = auth_client["client"]
    request = RedemptionRequest(user_id="child5", coins_amount=20, cash_amount=2.0, description="Convert coins")
    session.add(request)
    await session.commit()
    response = await client.put(f"/api/redemptions/redemption-requests/{request.id}/approve")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_reject_redemption_request_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-parent user cannot reject redemption requests.
    """
    client = auth_client["client"]
    request = RedemptionRequest(user_id="child6", coins_amount=20, cash_amount=2.0, description="Convert coins")
    session.add(request)
    await session.commit()
    response = await client.put(f"/api/redemptions/redemption-requests/{request.id}/reject")
    assert response.status_code == 403
