"""Goals management router."""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_async_session
from auth import current_active_user
from models import User, Goal, Transaction, ChildProfile
from schemas import GoalRead, GoalCreate, GoalUpdate, GoalContribution, TransactionRead

router = APIRouter()


@router.get("/users/{user_id}/goals", response_model=List[GoalRead])
async def get_user_goals(
    user_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all goals for a user."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        if current_user.role == "parent":
            stmt = select(ChildProfile).where(
                and_(
                    ChildProfile.user_id == user_id,
                    ChildProfile.parent_id == current_user.id,
                )
            )
            result = await session.execute(stmt)
            child_profile = result.scalar_one_or_none()
            if not child_profile:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )

    stmt = select(Goal).where(Goal.user_id == user_id).order_by(Goal.created_at.desc())
    result = await session.execute(stmt)
    goals = result.scalars().all()

    return [GoalRead.model_validate(goal) for goal in goals]


@router.post("/users/{user_id}/goals", response_model=GoalRead)
async def create_goal(
    user_id: str,
    goal_data: GoalCreate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new financial goal."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only create goals for yourself",
        )

    goal = Goal(user_id=user_id, **goal_data.model_dump())
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    return GoalRead.model_validate(goal)


@router.put("/users/{user_id}/goals/{goal_id}", response_model=GoalRead)
async def update_goal(
    user_id: str,
    goal_id: str,
    goal_update: GoalUpdate,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update an existing financial goal."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own goals",
        )

    stmt = select(Goal).where(and_(Goal.id == goal_id, Goal.user_id == user_id))
    result = await session.execute(stmt)
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )

    update_data = goal_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)

    goal.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(goal)

    return GoalRead.model_validate(goal)


@router.delete("/users/{user_id}/goals/{goal_id}")
async def delete_goal(
    user_id: str,
    goal_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a financial goal."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only delete your own goals",
        )

    # Get goal
    stmt = select(Goal).where(and_(Goal.id == goal_id, Goal.user_id == user_id))
    result = await session.execute(stmt)
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )

    await session.delete(goal)
    await session.commit()

    return {"message": "Goal deleted successfully"}


@router.post("/users/{user_id}/goals/{goal_id}/contribute")
async def contribute_to_goal(
    user_id: str,
    goal_id: str,
    contribution: GoalContribution,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Add coins to a financial goal."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only contribute to your own goals",
        )

    # Get goal and user profile
    goal_stmt = select(Goal).where(and_(Goal.id == goal_id, Goal.user_id == user_id))
    goal_result = await session.execute(goal_stmt)
    goal = goal_result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )

    profile_stmt = select(ChildProfile).where(ChildProfile.user_id == user_id)
    profile_result = await session.execute(profile_stmt)
    child_profile = profile_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only children can contribute to goals",
        )

    if child_profile.coins < contribution.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient coins"
        )

    goal.current_amount += contribution.amount
    child_profile.coins -= contribution.amount

    if goal.current_amount >= goal.target_amount:
        goal.is_completed = True

    goal.updated_at = datetime.utcnow()

    transaction = Transaction(
        user_id=user_id,
        type="save",
        amount=contribution.amount,
        description=f"Contributed to goal: {goal.title}",
        category="goal",
        reference_id=goal_id,
        reference_type="goal",
    )
    session.add(transaction)

    await session.commit()
    await session.refresh(goal)
    await session.refresh(child_profile)
    await session.refresh(transaction)

    return {
        "goal": GoalRead.model_validate(goal),
        "transaction": TransactionRead.model_validate(transaction),
        "new_coin_balance": child_profile.coins,
    }


@router.put("/goals/{goal_id}/progress", response_model=GoalRead)
async def update_goal_progress(
    goal_id: str,
    contribution: GoalContribution,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    """Update goal progress by adding a contribution amount."""
    # Fetch goal
    stmt = select(Goal).where(Goal.id == goal_id, Goal.user_id == current_user.id)
    result = await session.execute(stmt)
    goal = result.scalar_one_or_none()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    # Update current amount
    goal.current_amount += contribution.amount
    if goal.current_amount >= goal.target_amount:
        goal.is_completed = True

    goal.updated_at = datetime.utcnow()

    # Create transaction record
    transaction = Transaction(
        user_id=current_user.id,
        type="save",
        amount=contribution.amount,
        description=f"Progress towards goal: {goal.title}",
        reference_id=goal.id,
        reference_type="goal",
    )
    session.add(transaction)

    await session.commit()
    await session.refresh(goal)

    return goal
