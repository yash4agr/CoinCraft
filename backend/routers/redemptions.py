"""Redemption requests management router."""

from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_async_session
from auth import current_active_user
from models import User, RedemptionRequest, ChildProfile, ParentProfile
from schemas import RedemptionRequestRead, RedemptionRequestCreate

router = APIRouter()


@router.get("/users/{user_id}/conversion-requests", response_model=List[RedemptionRequestRead])
async def get_conversion_requests(
    user_id: str,
    status: str = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get money conversion (redemption) requests for a user."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    

    filters = [RedemptionRequest.user_id == user_id]
    if status:
        filters.append(RedemptionRequest.status == status)
    
    stmt = select(RedemptionRequest).where(and_(*filters)).order_by(
        RedemptionRequest.created_at.desc()
    )
    result = await session.execute(stmt)
    requests = result.scalars().all()
    
    return [RedemptionRequestRead.model_validate(req) for req in requests]


@router.post("/users/{user_id}/conversion-requests", response_model=dict)
async def create_conversion_request(
    user_id: str,
    request_data: RedemptionRequestCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new request to convert virtual coins to real money."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only create conversion requests for yourself"
        )
    
  
    stmt = select(ChildProfile).where(ChildProfile.user_id == user_id)
    result = await session.execute(stmt)
    child_profile = result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only children can request money conversion"
        )
    
  
    if child_profile.coins < request_data.coins_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient coins"
        )
    

    parent_stmt = select(ParentProfile).where(ParentProfile.user_id == child_profile.parent_id)
    parent_result = await session.execute(parent_stmt)
    parent_profile = parent_result.scalar_one()
    

    cash_amount = request_data.coins_amount * parent_profile.exchange_rate
    

    redemption_request = RedemptionRequest(
        user_id=user_id,
        coins_amount=request_data.coins_amount,
        cash_amount=cash_amount,
        description=request_data.description
    )
    session.add(redemption_request)
    

    child_profile.coins -= request_data.coins_amount
    
    await session.commit()
    await session.refresh(redemption_request)
    await session.refresh(child_profile)
    
    return {
        **RedemptionRequestRead.model_validate(redemption_request).model_dump(),
        "remaining_coins": child_profile.coins
    }


@router.get("/parents/{parent_id}/redemption-requests", response_model=List[RedemptionRequestRead])
async def get_parent_redemption_requests(
    parent_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get redemption requests from a parent's children."""
    if parent_id != current_user.id or current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view their children's redemption requests"
        )
    

    stmt = select(RedemptionRequest).join(ChildProfile).where(
        ChildProfile.parent_id == parent_id
    ).order_by(RedemptionRequest.created_at.desc())
    
    result = await session.execute(stmt)
    requests = result.scalars().all()
    
    # Add child info to each request
    enriched_requests = []
    for req in requests:

        child_stmt = select(User).join(ChildProfile).where(ChildProfile.user_id == req.user_id)
        child_result = await session.execute(child_stmt)
        child = child_result.scalar_one()
        
        req_dict = RedemptionRequestRead.model_validate(req).model_dump()
        req_dict["child"] = {
            "name": child.name,
            "avatar_url": child.avatar_url,
            "age": child.child_profile.age
        }
        enriched_requests.append(RedemptionRequestRead(**req_dict))
    
    return enriched_requests


@router.put("/redemption-requests/{request_id}/approve", response_model=RedemptionRequestRead)
async def approve_redemption_request(
    request_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Approve a redemption request."""
    # Get request
    stmt = select(RedemptionRequest).where(RedemptionRequest.id == request_id)
    result = await session.execute(stmt)
    redemption_request = result.scalar_one_or_none()
    
    if not redemption_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Redemption request not found"
        )
    

    child_stmt = select(ChildProfile).where(ChildProfile.user_id == redemption_request.user_id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one()
    
    if child_profile.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the parent can approve redemption requests"
        )
    
    # Update request
    redemption_request.status = "approved"
    redemption_request.approved_by = current_user.id
    redemption_request.approved_at = datetime.now(timezone.utc)
    
    await session.commit()
    await session.refresh(redemption_request)
    
    return RedemptionRequestRead.model_validate(redemption_request)


@router.put("/redemption-requests/{request_id}/reject", response_model=RedemptionRequestRead)
async def reject_redemption_request(
    request_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Reject a redemption request."""
    # Get request
    stmt = select(RedemptionRequest).where(RedemptionRequest.id == request_id)
    result = await session.execute(stmt)
    redemption_request = result.scalar_one_or_none()
    
    if not redemption_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Redemption request not found"
        )
    
 
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == redemption_request.user_id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one()
    
    if child_profile.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the parent can reject redemption requests"
        )
    
  
    redemption_request.status = "rejected"
    redemption_request.approved_by = current_user.id
    redemption_request.approved_at = datetime.now(timezone.utc)
    
    
    child_profile.coins += redemption_request.coins_amount
    
    await session.commit()
    await session.refresh(redemption_request)
    
    return RedemptionRequestRead.model_validate(redemption_request) 