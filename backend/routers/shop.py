"""Shop and redemption router for CoinCraft."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_async_session
from auth import current_active_user
from models import User, ShopItem, ChildProfile, Transaction, UserOwnedItem, PurchaseRequest
from schemas import ShopItemRead, ShopItemRequest, PurchaseRequestRead

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

    # Create a pending purchase request instead of immediate purchase
    purchase_request = PurchaseRequest(
        user_id=current_user.id,
        shop_item_id=shop_item.id,
        price=shop_item.price,
        status="pending",
    )
    session.add(purchase_request)
    await session.commit()

    return {
        "success": True,
        "message": f"Purchase request created for {shop_item.name}",
        "request": {
            "id": purchase_request.id,
            "user_id": purchase_request.user_id,
            "shop_item_id": purchase_request.shop_item_id,
            "price": purchase_request.price,
            "status": purchase_request.status,
            "created_at": purchase_request.created_at,
            "item_info": {
                "id": shop_item.id,
                "name": shop_item.name,
                "price": shop_item.price,
                "emoji": shop_item.emoji,
                "category": shop_item.category
            }
        }
    }

@router.get('/shop/purchase_requests', response_model=List[PurchaseRequestRead])
async def get_purchase_requests(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    """Get all purchase requests for the current user."""
    
    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can view purchase requests"
        )
    
    stmt = select(PurchaseRequest).where(PurchaseRequest.user_id == current_user.id)
    result = await session.execute(stmt)
    purchase_requests = result.scalars().all()
    
    return [PurchaseRequestRead.model_validate(req) for req in purchase_requests]


@router.get("/shop/{user_id}/transactions", response_model=List[dict])
async def get_shop_transactions(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    """Get all shop-related transactions for a specific user."""
    
    # Verify the user is requesting their own transactions or is authorized
    if current_user.id != user_id and current_user.role not in ["parent", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own transactions"
        )
    
    # Get shop transactions (spend type with shop category)
    stmt = select(Transaction).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.category == "shop",
            Transaction.type == "spend"
        )
    ).order_by(Transaction.created_at.desc())
    
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    
    # Format transactions for frontend
    shop_transactions = []
    for transaction in transactions:
        shop_transactions.append({
            "id": transaction.id,
            "type": transaction.type,
            "amount": transaction.amount,
            "description": transaction.description,
            "category": transaction.category,
            "source": transaction.source,
            "reference_id": transaction.reference_id,
            "reference_type": transaction.reference_type,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None
        })
    
    return shop_transactions

@router.put('/shop/purchase_requests/{request_id}/approve', response_model=PurchaseRequestRead)
async def approve_purchase_request(
    request_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    if current_user.role != 'parent':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only parents can approve')

    # Load request and verify it's for this parent's child
    from models import ChildProfile
    stmt = select(PurchaseRequest, ChildProfile).join(ChildProfile, PurchaseRequest.user_id == ChildProfile.user_id).where(PurchaseRequest.id == request_id)
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail='Request not found')
    req, child_profile = row
    if child_profile.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not your child')
    if req.status != 'pending':
        raise HTTPException(status_code=400, detail='Request already processed')

    # Verify coins
    if child_profile.coins < req.price:
        raise HTTPException(status_code=400, detail='Insufficient coins')

    # Deduct coins and grant item
    child_profile.coins -= req.price
    session.add(child_profile)
    session.add(UserOwnedItem(user_id=req.user_id, shop_item_id=req.shop_item_id))
    session.add(Transaction(
        user_id=req.user_id,
        type='spend',
        amount=req.price,
        description='Purchased item',
        category='shop',
        reference_id=req.shop_item_id,
        reference_type='shop',
    ))

    # Mark approved
    from datetime import datetime as _dt
    req.status = 'approved'
    req.approved_by = current_user.id
    req.approved_at = _dt.utcnow()
    await session.commit()
    await session.refresh(req)
    return {
        "id": req.id,
        "user_id": req.user_id,
        "shop_item_id": req.shop_item_id,
        "price": req.price,
        "status": req.status,
        "approved_by": req.approved_by,
        "approved_at": req.approved_at,
        "created_at": req.created_at,
    }

@router.put('/shop/purchase_requests/{request_id}/reject', response_model=PurchaseRequestRead)
async def reject_purchase_request(
    request_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    if current_user.role != 'parent':
        raise HTTPException(status_code=403, detail='Only parents can reject')
    from models import ChildProfile
    stmt = select(PurchaseRequest, ChildProfile).join(ChildProfile, PurchaseRequest.user_id == ChildProfile.user_id).where(PurchaseRequest.id == request_id)
    result = await session.execute(stmt)
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail='Request not found')
    req, child_profile = row
    if child_profile.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail='Not your child')
    if req.status != 'pending':
        raise HTTPException(status_code=400, detail='Request already processed')
    req.status = 'rejected'
    await session.commit()
    await session.refresh(req)
    return {
        "id": req.id,
        "user_id": req.user_id,
        "shop_item_id": req.shop_item_id,
        "price": req.price,
        "status": req.status,
        "approved_by": req.approved_by,
        "approved_at": req.approved_at,
        "created_at": req.created_at,
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