"""Authentication router with custom endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_async_session
from auth import current_active_user
from models import User
from schemas import UserRead

router = APIRouter()


@router.get("/verify", response_model=dict)
async def verify_token(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Verify if the current authentication token is valid and return user info.
    
    Used for maintaining sessions and checking authentication state.
    """
    # Get user with all profile data
    stmt = select(User).where(User.id == current_user.id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "user": UserRead.model_validate(user),
        "valid": True
    }


@router.post("/logout")
async def logout_user():
    """
    Logout user.
    
    Note: In JWT-based auth, logout is typically handled client-side
    by removing the token. This endpoint exists for API consistency.
    """
    return {
        "success": True,
        "message": "Successfully logged out"
    } 