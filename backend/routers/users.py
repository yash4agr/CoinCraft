"""User management router."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_async_session
from auth import current_active_user
from models import User, ChildProfile, ParentProfile, TeacherProfile
from schemas import (
    UserRead, UserUpdate, ChildProfileRead, ChildProfileCreate, ChildProfileUpdate,
    ParentProfileUpdate, TeacherProfileUpdate
)

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(
    current_user: User = Depends(current_active_user)
):
    """Get current user's profile (basic info only)."""
    try:
        return UserRead(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            role=current_user.role,
            avatar_url=current_user.avatar_url,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            is_active=current_user.is_active,
            is_superuser=current_user.is_superuser,
            is_verified=current_user.is_verified
        )
    except Exception as e:
        print(f"Error in get_current_user_profile: {e}")
        return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_profile(
    user_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get user profile with role-specific data."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        if current_user.role not in ["parent", "teacher"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
    

    stmt = select(User).options(
        selectinload(User.child_profile),
        selectinload(User.parent_profile),
        selectinload(User.teacher_profile)
    ).where(User.id == user_id)
    
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserRead.model_validate(user)


@router.put("/{user_id}", response_model=UserRead)
async def update_user_profile(
    user_id: str,
    user_update: UserUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update user profile information."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Get user
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await session.commit()
    await session.refresh(user)
    
    return UserRead.model_validate(user)


@router.post("/{parent_id}/children", response_model=UserRead)
async def create_child_account(
    parent_id: str,
    child_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new child account linked to a parent."""
    if parent_id != current_user.id or current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create child accounts"
        )
    

    age = child_data.get("age", 10)
    child_role = "younger_child" if age < 13 else "older_child"
    
    # Create new user
    from auth import get_user_db, get_user_manager
    from schemas import UserCreate
    

    user_db = await anext(get_user_db(session))
    user_manager = await anext(get_user_manager(user_db))
    
    user_create = UserCreate(
        email=child_data["email"],
        password=child_data["password"],
        name=child_data["name"],
        role=child_role,
        avatar_url=child_data.get("avatar_url"),
        age=age
    )
    
    new_user = await user_manager.create(user_create)
  
    child_profile = ChildProfile(
        user_id=new_user.id,
        age=age,
        parent_id=parent_id
    )
    session.add(child_profile)
    
    await session.commit()
    await session.refresh(new_user)
    
    return UserRead.model_validate(new_user)


@router.get("/{parent_id}/children", response_model=List[UserRead])
async def get_parent_children(
    parent_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get children accounts associated with a parent."""
    if parent_id != current_user.id or current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view their children"
        )
    
    # Get children
    stmt = select(User).join(ChildProfile).where(
        ChildProfile.parent_id == parent_id
    ).options(selectinload(User.child_profile))
    
    result = await session.execute(stmt)
    children = result.scalars().all()
    
    return [UserRead.model_validate(child) for child in children]


@router.put("/children/{child_id}", response_model=UserRead)
async def update_child_info(
    child_id: str,
    child_update: ChildProfileUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update a child's profile information."""

    stmt = select(ChildProfile).where(ChildProfile.user_id == child_id)
    result = await session.execute(stmt)
    child_profile = result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
 
    if child_profile.parent_id != current_user.id and child_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
  
    update_data = child_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(child_profile, field, value)
    
    await session.commit()
    

    stmt = select(User).options(selectinload(User.child_profile)).where(User.id == child_id)
    result = await session.execute(stmt)
    user = result.scalar_one()
    
    return UserRead.model_validate(user) 