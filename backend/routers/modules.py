"""Learning modules and activities router."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import get_async_session
from auth import current_active_user
from models import User, Activity, UserActivity, ChildProfile, Transaction
from schemas import ActivityRead, ModuleRead, ModuleCreate, ModuleUpdate, ModuleResponse

router = APIRouter()


@router.get("/activities", response_model=List[ActivityRead])
async def get_activities(
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    color_scheme: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all activities/adventures for children."""
    filters = []
    if difficulty:
        filters.append(Activity.difficulty == difficulty)
    if color_scheme:
        filters.append(Activity.color_scheme == color_scheme)
    stmt = select(Activity).where(and_(*filters)) if filters else select(Activity)
    result = await session.execute(stmt)
    activities = result.scalars().all()
    user_activity_ids = set()
    if current_user.role in ["younger_child", "older_child"]:
        ua_stmt = select(UserActivity.activity_id).where(UserActivity.user_id == current_user.id)
        ua_result = await session.execute(ua_stmt)
        user_activity_ids = set([row[0] for row in ua_result.fetchall()])
    response = []
    for activity in activities:
        completed = activity.id in user_activity_ids
        response.append(ActivityRead(
            id=activity.id,
            title=activity.title,
            description=activity.description or "",
            difficulty=activity.difficulty,
            coins=activity.coins,
            color_scheme=activity.color_scheme,
            emoji=activity.emoji,
            button_text=activity.button_text,
            path=activity.path,
            completed=completed
        ))
    return response


@router.get("/activities/{activity_id}", response_model=ActivityRead)
async def get_activity(
    activity_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get details for a specific activity/adventure."""
    activity = await session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    completed = False
    if current_user.role in ["younger_child", "older_child"]:
        ua_stmt = select(UserActivity).where(
            UserActivity.user_id == current_user.id,
            UserActivity.activity_id == activity_id
        )
        ua_result = await session.execute(ua_stmt)
        completed = ua_result.scalar_one_or_none() is not None
    return ActivityRead(
        id=activity.id,
        title=activity.title,
        description=activity.description or "",
        difficulty=activity.difficulty,
        coins=activity.coins,
        color_scheme=activity.color_scheme,
        emoji=activity.emoji,
        button_text=activity.button_text,
        path=activity.path,
        completed=completed
    )


@router.post("/activities/{activity_id}/complete")
async def complete_activity(
    activity_id: int,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Mark an activity as completed for the current user."""
    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(status_code=403, detail="Only children can complete activities")
    activity = await session.get(Activity, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    ua_stmt = select(UserActivity).where(
        UserActivity.user_id == current_user.id,
        UserActivity.activity_id == activity_id
    )
    ua_result = await session.execute(ua_stmt)
    user_activity = ua_result.scalar_one_or_none()
    if not user_activity:
        user_activity = UserActivity(user_id=current_user.id, activity_id=activity_id)
        session.add(user_activity)
        # Optionally award coins here
        child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
        child_result = await session.execute(child_stmt)
        child_profile = child_result.scalar_one_or_none()
        if child_profile:
            child_profile.coins += activity.coins
            transaction = Transaction(
                user_id=current_user.id,
                type="earn",
                amount=activity.coins,
                description=f"Completed activity: {activity.title}",
                category="activity",
                reference_id=str(activity_id),
                reference_type="activity"
            )
            session.add(transaction)
    await session.commit()
    return {"success": True, "activity_id": activity_id}


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
