"""Learning modules and activities router."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_async_session
from auth import current_active_user
from models import User, Module, UserModuleProgress, ChildProfile, Transaction
from schemas import ModuleRead, ModuleCreate, ModuleUpdate, ActivityRead, ModuleResponse

router = APIRouter()


@router.get("/activities", response_model=List[ActivityRead])
async def get_activities(
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    category: Optional[str] = None,
    age_group: Optional[str] = Query(None, pattern="^(younger_child|older_child)$"),
    completed: Optional[bool] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get learning activities and modules with filtering options."""

    filters = [Module.is_published == True]

    if difficulty:
        filters.append(Module.difficulty == difficulty)
    if category:
        filters.append(Module.category == category)

    stmt = select(Module).where(and_(*filters)).order_by(Module.created_at.desc())
    result = await session.execute(stmt)
    modules = result.scalars().all()

    activities = []
    for module in modules:
        if current_user.role in ["younger_child", "older_child"]:
            progress_stmt = select(UserModuleProgress).where(
                and_(
                    UserModuleProgress.user_id == current_user.id,
                    UserModuleProgress.module_id == module.id,
                )
            )
            progress_result = await session.execute(progress_stmt)
            progress = progress_result.scalar_one_or_none()
            is_completed = progress.is_completed if progress else False
        else:
            is_completed = False

        if completed is not None and is_completed != completed:
            continue

        module_age_group = (
            "younger_child" if module.difficulty == "easy" else "older_child"
        )
        if age_group and module_age_group != age_group:
            continue

        activity = ActivityRead(
            id=module.id,
            title=module.title,
            description=module.description,
            type="module",
            difficulty=module.difficulty,
            coins=module.points_reward,
            duration=module.estimated_duration or 15,
            completed=is_completed,
            icon="ri-book-line",
            category=module.category or "financial_literacy",
            age_group=module_age_group,
        )
        activities.append(activity)

    return activities


@router.get("/activities/{activity_id}")
async def get_activity(
    activity_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get detailed information about a specific learning activity or module."""

    stmt = select(Module).where(Module.id == activity_id)
    result = await session.execute(stmt)
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )

    user_progress = None
    if current_user.role in ["younger_child", "older_child"]:
        progress_stmt = select(UserModuleProgress).where(
            and_(
                UserModuleProgress.user_id == current_user.id,
                UserModuleProgress.module_id == activity_id,
            )
        )
        progress_result = await session.execute(progress_stmt)
        progress = progress_result.scalar_one_or_none()

        if progress:
            user_progress = {
                "progress_percentage": progress.progress_percentage,
                "is_completed": progress.is_completed,
                "score": progress.score,
                "time_spent": progress.time_spent,
            }

    module_dict = ModuleRead.model_validate(module).model_dump()
    module_dict["user_progress"] = user_progress

    return module_dict


@router.post("/activities/{activity_id}/complete")
async def complete_activity(
    activity_id: str,
    progress_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Record progress and mark an activity as completed."""
    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can complete activities",
        )

    # Get module
    stmt = select(Module).where(Module.id == activity_id)
    result = await session.execute(stmt)
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )

    progress_stmt = select(UserModuleProgress).where(
        and_(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == activity_id,
        )
    )
    progress_result = await session.execute(progress_stmt)
    progress = progress_result.scalar_one_or_none()

    if not progress:
        progress = UserModuleProgress(user_id=current_user.id, module_id=activity_id)
        session.add(progress)

    progress.progress_percentage = progress_data.get("progress_percentage", 100.0)
    progress.score = progress_data.get("score", 0.0)
    progress.time_spent = progress_data.get("time_spent", 0)
    progress.is_completed = progress_data.get("is_completed", False)

    if progress.is_completed and not progress.completed_at:
        progress.completed_at = datetime.utcnow()

        child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
        child_result = await session.execute(child_stmt)
        child_profile = child_result.scalar_one()

        coins_earned = module.points_reward
        child_profile.coins += coins_earned

        transaction = Transaction(
            user_id=current_user.id,
            type="earn",
            amount=coins_earned,
            description=f"Completed activity: {module.title}",
            category="activity",
            reference_id=activity_id,
            reference_type="activity",
        )
        session.add(transaction)

        await session.commit()
        await session.refresh(child_profile)

        return {
            "progress": {
                "progress_percentage": progress.progress_percentage,
                "is_completed": progress.is_completed,
                "score": progress.score,
                "time_spent": progress.time_spent,
            },
            "coins_earned": coins_earned,
            "new_coin_balance": child_profile.coins,
        }

    await session.commit()

    return {
        "progress": {
            "progress_percentage": progress.progress_percentage,
            "is_completed": progress.is_completed,
            "score": progress.score,
            "time_spent": progress.time_spent,
        },
        "coins_earned": 0,
        "new_coin_balance": None,
    }


@router.get("/learning-modules", response_model=List[ModuleRead])
async def get_learning_modules(
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    category: Optional[str] = None,
    age_group: Optional[str] = Query(None, pattern="^(younger_child|older_child)$"),
    created_by: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all learning modules with optional filters."""

    filters = [Module.is_published == True]

    if difficulty:
        filters.append(Module.difficulty == difficulty)
    if category:
        filters.append(Module.category == category)
    if created_by:
        filters.append(Module.created_by == created_by)

    stmt = select(Module).where(and_(*filters)).order_by(Module.created_at.desc())
    result = await session.execute(stmt)
    modules = result.scalars().all()

    enriched_modules = []
    for module in modules:
        module_dict = ModuleRead.model_validate(module).model_dump()

        if current_user.role in ["younger_child", "older_child"]:
            progress_stmt = select(UserModuleProgress).where(
                and_(
                    UserModuleProgress.user_id == current_user.id,
                    UserModuleProgress.module_id == module.id,
                )
            )
            progress_result = await session.execute(progress_stmt)
            progress = progress_result.scalar_one_or_none()

            if progress:
                module_dict["user_progress"] = {
                    "progress_percentage": progress.progress_percentage,
                    "is_completed": progress.is_completed,
                    "score": progress.score,
                    "time_spent": progress.time_spent,
                }

        enriched_modules.append(ModuleRead(**module_dict))

    return enriched_modules


@router.post("/learning-modules/{module_id}/complete")
async def complete_module(
    module_id: str,
    completion_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Record completion of a learning module."""
    return await complete_activity(module_id, completion_data, current_user, session)
