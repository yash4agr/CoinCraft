import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ShopItem, ChildProfile, Transaction

@pytest.mark.asyncio
async def test_get_shop_items_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of shop items.
    """
    client = auth_child_client["client"]
    # Add a shop item
    item = ShopItem(id="item1", name="Test Toy", description="A toy", price=50, category="toys", emoji="🧸", available=True)
    session.add(item)
    await session.commit()
    response = await client.get("/api/shop/items")
    assert response.status_code == 200
    data = response.json()
    assert any(i["name"] == "Test Toy" for i in data)

@pytest.mark.asyncio
async def test_purchase_item_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful purchase of a shop item.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    item = ShopItem(id="item2", name="Book", description="A book", price=30, category="education", emoji="📚", available=True)
    session.add(item)
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 100
    session.add(child_profile)
    await session.commit()
    response = await client.post(f"/api/shop/purchase?item_id={item.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["item"]["name"] == "Book"
    assert data["remaining_coins"] == 70

@pytest.mark.asyncio
async def test_purchase_item_insufficient_coins(auth_child_client: dict, session: AsyncSession):
    """
    Test purchasing an item with insufficient coins.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    item = ShopItem(id="item3", name="Expensive Toy", description="Expensive", price=200, category="toys", emoji="🧸", available=True)
    session.add(item)
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 50
    session.add(child_profile)
    await session.commit()
    response = await client.post(f"/api/shop/purchase?item_id={item.id}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient coins"

@pytest.mark.asyncio
async def test_purchase_item_not_found(auth_child_client: dict, session: AsyncSession):
    """
    Test purchasing a non-existent item.
    """
    client = auth_child_client["client"]
    response = await client.post("/api/shop/purchase?item_id=nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found or not available"

@pytest.mark.asyncio
async def test_purchase_item_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot purchase shop items.
    """
    client = auth_client["client"]
    item = ShopItem(id="item4", name="Parent Item", description="For parents", price=10, category="parenting", emoji="👨‍👩‍👧", available=True)
    session.add(item)
    await session.commit()
    response = await client.post(f"/api/shop/purchase?item_id={item.id}")
    assert response.status_code == 400 or response.status_code == 403
