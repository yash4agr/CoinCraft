"""Transactions management router."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from database import get_async_session
from auth import current_active_user
from models import User, Transaction, ChildProfile
from schemas import TransactionRead, TransactionCreate, TransactionList

router = APIRouter()


@router.get("/users/{user_id}/transactions", response_model=TransactionList)
async def get_user_transactions(
    user_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    type: Optional[str] = Query(None, pattern="^(earn|spend|save)$"),
    category: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get user transactions with optional filters."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        if current_user.role == "parent":
            from models import ChildProfile
            stmt = select(ChildProfile).where(
                and_(ChildProfile.user_id == user_id, ChildProfile.parent_id == current_user.id)
            )
            result = await session.execute(stmt)
            child_profile = result.scalar_one_or_none()
            if not child_profile:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
    

    filters = [Transaction.user_id == user_id]
    
    if type:
        filters.append(Transaction.type == type)
    if category:
        filters.append(Transaction.category == category)
    if start_date:
        filters.append(Transaction.created_at >= start_date)
    if end_date:
        filters.append(Transaction.created_at <= end_date)
    

    stmt = select(Transaction).where(and_(*filters)).order_by(
        Transaction.created_at.desc()
    ).offset(offset).limit(limit)
    
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    
  
    count_stmt = select(func.count(Transaction.id)).where(and_(*filters))
    count_result = await session.execute(count_stmt)
    total_count = count_result.scalar()
    

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    

    weekly_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == "earn",
            Transaction.created_at >= week_ago
        )
    )
    weekly_result = await session.execute(weekly_stmt)
    weekly_total = weekly_result.scalar() or 0
    

    monthly_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == "earn",
            Transaction.created_at >= month_ago
        )
    )
    monthly_result = await session.execute(monthly_stmt)
    monthly_total = monthly_result.scalar() or 0
    
    return TransactionList(
        transactions=[TransactionRead.model_validate(t) for t in transactions],
        total_count=total_count,
        weekly_total=weekly_total,
        monthly_total=monthly_total
    )


@router.post("/users/{user_id}/transactions", response_model=dict)
async def create_transaction(
    user_id: str,
    transaction_data: TransactionCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new transaction."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:

        if current_user.role != "parent":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
  
        stmt = select(ChildProfile).where(
            and_(ChildProfile.user_id == user_id, ChildProfile.parent_id == current_user.id)
        )
        result = await session.execute(stmt)
        child_profile = result.scalar_one_or_none()
        if not child_profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
    

    stmt = select(ChildProfile).where(ChildProfile.user_id == user_id)
    result = await session.execute(stmt)
    child_profile = result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User profile not found"
        )
    

    if transaction_data.type == "spend" and child_profile.coins < transaction_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient coins for spending"
        )
    

    transaction = Transaction(
        user_id=user_id,
        **transaction_data.model_dump()
    )
    session.add(transaction)
    

    if transaction_data.type == "earn":
        child_profile.coins += transaction_data.amount
    elif transaction_data.type == "spend":
        child_profile.coins -= transaction_data.amount

    
    await session.commit()
    await session.refresh(transaction)
    await session.refresh(child_profile)
    
    return {
        "id": transaction.id,
        "new_coin_balance": child_profile.coins
    } 