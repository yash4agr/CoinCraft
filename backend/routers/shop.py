"""Shop and redemption router for CoinCraft."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_async_session
from auth import current_active_user
from models import User, ShopItem, ChildProfile, Transaction, UserOwnedItem
from schemas import ShopItemRead, ShopItemRequest

router = APIRouter()


@router.get("/shop/items", response_model=List[ShopItemRead])
async def get_shop_items(session: AsyncSession = Depends(get_async_session)):
    """Get all shop items."""
    stmt = select(ShopItem)
    result = await session.execute(stmt)
    shop_items = result.scalars().all()
    return [ShopItemRead.model_validate(item) for item in shop_items]


@router.post("/shop/{user_id}/purchase", response_model=dict)
async def purchase_item(
    user_id: str,
    request: ShopItemRequest,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    # This function now uses user_id and item_id, removes the deprecated 'available' clause, and checks ownership via UserOwnedItem.

    """Purchase an item from the shop."""

    # Get the shop item from database
    stmt = select(ShopItem).where(ShopItem.id == request.item_id)
    result = await session.execute(stmt)
    shop_item = result.scalar_one_or_none()

    if not shop_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    # Check if user already owns the item
    owned_stmt = select(UserOwnedItem).where(
        UserOwnedItem.user_id == current_user.id,
        UserOwnedItem.shop_item_id == shop_item.id
    )
    owned_result = await session.execute(owned_stmt)
    owned_item = owned_result.scalar_one_or_none()
    if owned_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already owns this item"
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
    session.add(child_profile)

    # Add item to user's owned items
    user_owned_item = UserOwnedItem(
        user_id=current_user.id,
        shop_item_id=shop_item.id
    )
    session.add(user_owned_item)

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

@router.get('/shop/owned_items', response_model=List[ShopItemRead])
async def get_owned_items(session: AsyncSession = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    """Get all owned items."""
    print("I HAVE ENTERED THE FUNCTION")
    stmt = select(ShopItem).join(UserOwnedItem, ShopItem.id == UserOwnedItem.shop_item_id).where(UserOwnedItem.user_id == current_user.id)
    result = await session.execute(stmt)
    owned_shop_items = result.scalars().all()
    # Return the actual shop items owned by the user
    return [ShopItemRead.model_validate(item) for item in owned_shop_items]