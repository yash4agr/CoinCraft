"""Shop and redemption router for CoinCraft."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_async_session
from auth import current_active_user
from models import User, ShopItem, ChildProfile, Transaction
from schemas import ShopItemRead

router = APIRouter()


@router.get("/shop/items", response_model=List[ShopItemRead])
async def get_shop_items(session: AsyncSession = Depends(get_async_session)):
    """Get available shop items."""
    # Query shop items from database
    stmt = select(ShopItem).where(ShopItem.available)
    result = await session.execute(stmt)
    shop_items = result.scalars().all()

    if not shop_items:
        # Create default shop items if none exist
        default_items = [
            ShopItem(
                id="1",
                name="Small Toy",
                description="A fun small toy",
                price=100,
                category="toys",
                emoji="🧸",
                available=True,
            ),
            ShopItem(
                id="2",
                name="Book",
                description="An educational book",
                price=200,
                category="education",
                emoji="📚",
                available=True,
            ),
            ShopItem(
                id="3",
                name="Game Time",
                description="30 minutes of extra game time",
                price=150,
                category="privileges",
                emoji="🎮",
                available=True,
            ),
            ShopItem(
                id="4",
                name="Movie Night",
                description="Family movie night choice",
                price=300,
                category="privileges",
                emoji="🎬",
                available=True,
            ),
            ShopItem(
                id="5",
                name="Art Supplies",
                description="Drawing and coloring supplies",
                price=250,
                category="creative",
                emoji="🎨",
                available=True,
            ),
        ]

        for item in default_items:
            session.add(item)
        await session.commit()
        shop_items = default_items

    return [ShopItemRead.model_validate(item) for item in shop_items]


@router.post("/shop/purchase", response_model=dict)
async def purchase_item(
    item_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    """Purchase an item from the shop."""

    # Get the shop item from database
    stmt = select(ShopItem).where(ShopItem.id == item_id)
    result = await session.execute(stmt)
    shop_item = result.scalar_one_or_none()

    if not shop_item or not shop_item.available:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or not available",
        )

    # Get user's child profile to check coins
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Child profile not found"
        )

    # Check if user has enough coins
    if child_profile.coins < shop_item.price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient coins"
        )

    # Deduct coins from child profile
    child_profile.coins -= shop_item.price

    # Create transaction record
    transaction = Transaction(
        user_id=current_user.id,
        type="spend",
        amount=shop_item.price,
        description=f"Purchased {shop_item.name}",
        category="shop",
        reference_id=shop_item.id,
        reference_type="shop",
    )
    session.add(transaction)

    await session.commit()

    return {
        "success": True,
        "message": f"Successfully purchased {shop_item.name}",
        "item": {"id": shop_item.id, "name": shop_item.name, "price": shop_item.price},
        "remaining_coins": child_profile.coins,
    }
