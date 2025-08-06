"""Dashboard data router."""

from typing import List, Union
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc

from backend.database import get_async_session
from backend.auth import current_active_user
from backend.models import (
    User,
    ChildProfile,
    Goal,
    Transaction,
    UserAchievement,
    Achievement,
    Module,
    UserModuleProgress,
    Task,
    RedemptionRequest,
)
from backend.schemas import (
    ProgressGoal,
    TransactionRead,
    GoalRead,
    AchievementRead,
    ChildDashboardResponse,
    ParentDashboardResponse,
    TeacherDashboardResponse,
    DashboardStats,
    UserRead,
    TaskRead,
    RedemptionRequestRead,
)

router = APIRouter()


@router.get("/dashboard/{user_role}")
async def get_dashboard_data(
    user_role: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get role-specific dashboard data with appropriate metrics and information."""
    if user_role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Role mismatch"
        )

    if user_role in ["younger_child", "older_child"]:
        return await get_child_dashboard_data(current_user, session)
    elif user_role == "parent":
        return await get_parent_dashboard_data(current_user, session)
    elif user_role == "teacher":
        return await get_teacher_dashboard_data(current_user, session)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user role"
        )


async def get_child_dashboard_data(
    current_user: User, session: AsyncSession
) -> ChildDashboardResponse:
    """Get dashboard data for child users."""
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found"
        )

    # Create UserRead object
    user_read = UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        avatar_url=current_user.avatar_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        is_verified=current_user.is_verified,
    )

    # Get completed goals count
    completed_goals_stmt = select(func.count(Goal.id)).where(
        and_(Goal.user_id == current_user.id, ~Goal.is_completed)
    )
    completed_goals_result = await session.execute(completed_goals_stmt)
    goals_completed = completed_goals_result.scalar() or 0

    # Get completed tasks count
    completed_tasks_stmt = select(func.count(Task.id)).where(
        and_(Task.assigned_to == current_user.id, Task.status == "completed")
    )
    completed_tasks_result = await session.execute(completed_tasks_stmt)
    completed_tasks = completed_tasks_result.scalar() or 0

    # Create DashboardStats object
    stats = DashboardStats(
        total_coins=child_profile.coins,
        level=child_profile.level,
        streak_days=child_profile.streak_days,
        goals_count=goals_completed,
        completed_tasks=completed_tasks,
    )

    # Get recent transactions
    trans_stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(desc(Transaction.created_at))
        .limit(10)
    )
    trans_result = await session.execute(trans_stmt)
    transactions = trans_result.scalars().all()
    recent_transactions = [TransactionRead.model_validate(t) for t in transactions]

    # Active goals
    goals_stmt = (
        select(Goal)
        .where(and_(Goal.user_id == current_user.id, ~Goal.is_completed))
        .order_by(desc(Goal.created_at))
        .limit(5)
    )
    goals_result = await session.execute(goals_stmt)
    goals = goals_result.scalars().all()
    active_goals = [GoalRead.model_validate(g) for g in goals]

    # Get pending tasks
    tasks_stmt = (
        select(Task)
        .where(and_(Task.assigned_to == current_user.id, Task.status == "pending"))
        .order_by(desc(Task.created_at))
        .limit(10)
    )
    tasks_result = await session.execute(tasks_stmt)
    tasks = tasks_result.scalars().all()
    pending_tasks = [TaskRead.model_validate(t) for t in tasks]

    # Get achievements
    achievements_stmt = (
        select(Achievement, UserAchievement.earned_at)
        .join(UserAchievement)
        .where(UserAchievement.user_id == current_user.id)
        .order_by(desc(UserAchievement.earned_at))
        .limit(5)
    )
    achievements_result = await session.execute(achievements_stmt)
    achievement_rows = achievements_result.all()

    achievements = []
    for achievement, earned_at in achievement_rows:
        achievement_dict = AchievementRead.model_validate(achievement).model_dump()
        achievement_dict["earned_at"] = earned_at
        achievements.append(AchievementRead(**achievement_dict))

    return ChildDashboardResponse(
        user=user_read,
        stats=stats,
        active_goals=active_goals,
        pending_tasks=pending_tasks,
        recent_transactions=recent_transactions,
        achievements=achievements,
    )


async def get_parent_dashboard_data(
    current_user: User, session: AsyncSession
) -> ParentDashboardResponse:
    """Get dashboard data for parent users."""
    # Create UserRead object
    user_read = UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        avatar_url=current_user.avatar_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        is_verified=current_user.is_verified,
    )

    # Get children
    children_stmt = (
        select(User).join(ChildProfile).where(ChildProfile.parent_id == current_user.id)
    )
    children_result = await session.execute(children_stmt)
    children = children_result.scalars().all()
    children_read = [
        UserRead(
            id=child.id,
            email=child.email,
            name=child.name,
            role=child.role,
            avatar_url=child.avatar_url,
            created_at=child.created_at,
            updated_at=child.updated_at,
            is_active=child.is_active,
            is_superuser=child.is_superuser,
            is_verified=child.is_verified,
        )
        for child in children
    ]

    # Calculate total coins distributed
    total_coins_distributed = 0
    child_ids = [child.id for child in children]
    for child in children:
        earned_stmt = select(func.sum(Transaction.amount)).where(
            and_(Transaction.user_id == child.id, Transaction.type == "earn")
        )
        earned_result = await session.execute(earned_stmt)
        earned = earned_result.scalar() or 0
        total_coins_distributed += earned

    # Count pending tasks
    pending_tasks_stmt = select(func.count(Task.id)).where(
        and_(Task.assigned_by == current_user.id, Task.status == "completed")
    )
    pending_tasks_result = await session.execute(pending_tasks_stmt)
    pending_tasks_count = pending_tasks_result.scalar() or 0

    # Count pending redemptions
    pending_redemptions_count = 0
    if child_ids:
        pending_redemptions_stmt = select(func.count(RedemptionRequest.id)).where(
            and_(
                RedemptionRequest.user_id.in_(child_ids),
                RedemptionRequest.status == "pending",
            )
        )
        pending_redemptions_result = await session.execute(pending_redemptions_stmt)
        pending_redemptions_count = pending_redemptions_result.scalar() or 0

    # Create DashboardStats object
    stats = DashboardStats(
        total_coins=total_coins_distributed,
        level=1,  # Parent level - could be calculated differently
        streak_days=0,  # Parent streak - could be calculated differently
        goals_count=len(children),  # Using children count as goals count
        completed_tasks=pending_tasks_count,
    )

    # Get recent transactions
    recent_transactions = []
    if child_ids:
        trans_stmt = (
            select(Transaction)
            .where(Transaction.user_id.in_(child_ids))
            .order_by(desc(Transaction.created_at))
            .limit(10)
        )
        trans_result = await session.execute(trans_stmt)
        transactions = trans_result.scalars().all()
        recent_transactions = [TransactionRead.model_validate(t) for t in transactions]

    # Get pending redemption requests with full objects
    pending_redemptions = []
    if child_ids:
        redemptions_stmt = (
            select(RedemptionRequest)
            .where(
                and_(
                    RedemptionRequest.user_id.in_(child_ids),
                    RedemptionRequest.status == "pending",
                )
            )
            .order_by(desc(RedemptionRequest.created_at))
            .limit(10)
        )
        redemptions_result = await session.execute(redemptions_stmt)
        redemption_requests = redemptions_result.scalars().all()
        pending_redemptions = [
            RedemptionRequestRead.model_validate(r) for r in redemption_requests
        ]

    return ParentDashboardResponse(
        user=user_read,
        stats=stats,
        children=children_read,
        recent_transactions=recent_transactions,
        pending_redemptions=pending_redemptions,
    )


async def get_teacher_dashboard_data(
    current_user: User, session: AsyncSession
) -> TeacherDashboardResponse:
    """Get dashboard data for teacher users."""
    # Get teacher profile and classes
    from backend.models import TeacherProfile, Class, ClassStudent
    
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()

    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher profile not found"
        )

    # Create UserRead object
    user_read = UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        avatar_url=current_user.avatar_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        is_verified=current_user.is_verified,
    )

    # Get classes
    classes_stmt = select(Class).where(Class.teacher_id == teacher_profile.id)
    classes_result = await session.execute(classes_stmt)
    classes = classes_result.scalars().all()

    # Count total students
    total_students = 0
    for class_obj in classes:
        students_stmt = select(func.count(ClassStudent.id)).where(
            ClassStudent.class_id == class_obj.id
        )
        students_result = await session.execute(students_stmt)
        total_students += students_result.scalar() or 0

    # Count modules created by teacher
    modules_stmt = select(func.count(Module.id)).where(
        Module.created_by == current_user.id
    )
    modules_result = await session.execute(modules_stmt)
    modules_created = modules_result.scalar() or 0

    # User stats
    stats = {
        "total_classes": len(classes),
        "total_students": total_students,
        "modules_created": modules_created,
        "average_performance": 0.0,
    }

    # Classes data
    classes_data = []
    for class_obj in classes:
        students_stmt = select(func.count(ClassStudent.id)).where(
            ClassStudent.class_id == class_obj.id
        )
        students_result = await session.execute(students_stmt)
        student_count = students_result.scalar() or 0

        classes_data.append(
            {
                "id": class_obj.id,
                "name": class_obj.name,
                "teacher_id": class_obj.teacher_id,
                "student_count": student_count,
                "created_at": class_obj.created_at,
            }
        )

    # Recent modules
    recent_modules_stmt = (
        select(Module)
        .where(Module.created_by == current_user.id)
        .order_by(desc(Module.created_at))
        .limit(5)
    )
    recent_modules_result = await session.execute(recent_modules_stmt)
    recent_modules = recent_modules_result.scalars().all()

    recent_modules_data = []
    for module in recent_modules:
        recent_modules_data.append(
            {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "category": module.category,
                "difficulty": module.difficulty,
                "points_reward": module.points_reward,
                "is_published": module.is_published,
                "created_at": module.created_at,
            }
        )

    # Student progress (simplified for now)
    student_progress = []

    return TeacherDashboardResponse(
        user=user_read,
        stats=stats,
        classes=classes_data,
        recent_modules=recent_modules_data,
        student_progress=student_progress,
    )


@router.get("/progress-goals/{user_id}", response_model=List[ProgressGoal])
async def get_todays_goals(
    user_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get daily progress goals and statistics."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        if current_user.role != "parent":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )

    # For children, return daily goals
    if current_user.role in ["younger_child", "older_child"]:
        today = datetime.utcnow().date()

        today_start = datetime.combine(today, datetime.min.time())

        lessons_stmt = select(func.count(UserModuleProgress.id)).where(
            and_(
                UserModuleProgress.user_id == user_id,
                UserModuleProgress.started_at >= today_start,
                UserModuleProgress.progress_percentage > 0,
            )
        )
        lessons_result = await session.execute(lessons_stmt)
        lessons_read = lessons_result.scalar() or 0

        coins_stmt = select(func.sum(Transaction.amount)).where(
            and_(
                Transaction.user_id == user_id,
                Transaction.type == "earn",
                Transaction.created_at >= today_start,
            )
        )
        coins_result = await session.execute(coins_stmt)
        coins_earned = coins_result.scalar() or 0

        games_stmt = select(func.count(UserModuleProgress.id)).where(
            and_(
                UserModuleProgress.user_id == user_id,
                UserModuleProgress.completed_at >= today_start,
                UserModuleProgress.is_completed == True,
            )
        )
        games_result = await session.execute(games_stmt)
        games_completed = games_result.scalar() or 0

        practice_time = min(lessons_read * 5 + games_completed * 3, 20)

        return [
            ProgressGoal(
                id="lessons",
                title="Read Lessons",
                current=min(lessons_read, 3),
                total=3,
                icon="ri-book-open-line",
                color_scheme="orange",
            ),
            ProgressGoal(
                id="coins",
                title="Earn Coins",
                current=min(coins_earned, 50),
                total=50,
                icon="ri-coins-line",
                color_scheme="blue",
            ),
            ProgressGoal(
                id="games",
                title="Complete Games",
                current=min(games_completed, 2),
                total=2,
                icon="ri-gamepad-line",
                color_scheme="green",
            ),
            ProgressGoal(
                id="practice",
                title="Practice Time",
                current=practice_time,
                total=20,
                icon="ri-time-line",
                color_scheme="purple",
            ),
        ]

    return []


@router.put("/progress-goals/{goal_id}/update")
async def update_goal_progress(
    goal_id: str,
    progress_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update progress on a daily goal."""

    current_value = progress_data.get("current", 0)

    return {
        "id": goal_id,
        "current": current_value,
        "is_completed": current_value >= 100,  # Assuming 100 is completion
        "coins_earned": 5 if current_value >= 100 else 0,
    }
