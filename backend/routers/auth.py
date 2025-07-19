"""Custom authentication endpoints for CoinCraft."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from auth import UserManager, get_user_manager, auth_backend, current_active_user
from models import User, ChildProfile, ParentProfile, TeacherProfile
from schemas import UserCreate, UserRead

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_and_login(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Register a new user and immediately log them in."""
    try:
        # Check if user already exists
        existing_user = await user_manager.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create the user
        user = await user_manager.create(user_data)
        
        # Create role-specific profile
        if user.role == 'parent':
            parent_profile = ParentProfile(
                user_id=user.id,
                exchange_rate=1.0,  # 1 coin = $1 by default
                auto_approval_limit=0.0,  # Require approval for all redemptions
                require_approval=True
            )
            session.add(parent_profile)
        elif user.role == 'teacher':
            teacher_profile = TeacherProfile(
                user_id=user.id,
                school_name="",
                grade_level="",
                subject=""
            )
            session.add(teacher_profile)
        elif user.role in ['younger_child', 'older_child']:
            child_profile = ChildProfile(
                user_id=user.id,
                age=8 if user.role == 'younger_child' else 13,
                coins=0,
                level=1,
                streak_days=0,
                parent_id=None  # Will be set when parent adds child
            )
            session.add(child_profile)
        
        await session.commit()

        # Generate login token
        login_strategy = auth_backend.login_strategy
        token = await login_strategy.write_token(user)

        # Convert user to response format
        user_response = UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user_response
        }

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


# Removed problematic /verify endpoint that was causing import issues


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