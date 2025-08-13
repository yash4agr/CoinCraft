"""Parent management router for CoinCraft."""

from typing import List, Optional
from datetime import datetime, timedelta
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from database import get_async_session
from auth import current_active_user, get_user_manager, UserManager
from models import (
    User,
    ChildProfile,
    ParentProfile,
    Task,
    Goal,
    Transaction,
    Achievement,
    UserAchievement,
    Module,
    UserModuleProgress,
)
from schemas import (
    UserRead,
    ChildProfileRead,
    TaskRead,
    TaskCreate,
    TaskUpdate,
    GoalRead,
    TransactionRead,
    RedemptionRequestRead,
    DashboardData,
    ParentDashboardResponse,
    DashboardStats,
    ChildCreateResponse,
    TaskCreateResponse,
    TaskApprovalResponse,
    ChildProgressResponse,
    ParentSettingsResponse,
    ActivityRead,
    AchievementRead,
)

router = APIRouter()


class ChildSummary:
    def __init__(self, child: User, profile: ChildProfile):
        self.id = child.id
        self.name = child.name
        self.email = child.email
        self.age = profile.age
        self.coins = profile.coins
        self.level = profile.level
        self.streak_days = profile.streak_days
        self.avatar_url = child.avatar_url
        self.created_at = child.created_at


class FamilyStats:
    def __init__(self):
        self.total_children = 0
        self.total_coins_earned = 0
        self.completed_tasks = 0
        self.active_goals = 0
        self.total_coins = 0
        self.level = 1
        self.streak_days = 0
        self.goals_count = 0


@router.get("/dashboard", response_model=ParentDashboardResponse)
async def get_parent_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get parent dashboard data including children overview and family stats."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can access this endpoint",
        )

    # Ensure parent profile exists
    parent_stmt = select(ParentProfile).where(ParentProfile.user_id == current_user.id)
    parent_result = await session.execute(parent_stmt)
    parent_profile = parent_result.scalar_one_or_none()

    if not parent_profile:
        parent_profile = ParentProfile(
            user_id=current_user.id,
            exchange_rate=0.10,
            auto_approval_limit=500,
            require_approval=True,
        )
        session.add(parent_profile)
        await session.commit()

    # Get children with their profiles
    children_stmt = (
        select(User, ChildProfile)
        .join(ChildProfile, User.id == ChildProfile.user_id)
        .where(ChildProfile.parent_id == current_user.id)
    )
    children_result = await session.execute(children_stmt)
    children_data = children_result.all()

    print(f"[BACKEND] Dashboard: Found {len(children_data)} children for parent {current_user.id}")
    
    # Initialize aggregated stats
    total_coins = 0
    total_completed_tasks = 0
    total_active_goals = 0
    max_level = 1
    max_streak = 0
    
    # Prepare children list as UserRead objects
    children_list = []
    for user, child_profile in children_data:
        # Calculate stats for this child
        goals_stmt = select(func.count(Goal.id)).where(
            and_(Goal.user_id == user.id, Goal.is_completed == False)
        )
        goals_result = await session.execute(goals_stmt)
        active_goals = goals_result.scalar() or 0

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        tasks_stmt = select(func.count(Task.id)).where(
            and_(
                Task.assigned_to == user.id,
                Task.status == "completed",
                Task.completed_at >= thirty_days_ago,
            )
        )
        tasks_result = await session.execute(tasks_stmt)
        completed_tasks = tasks_result.scalar() or 0

        # Aggregate family stats
        total_coins += child_profile.coins
        total_completed_tasks += completed_tasks
        total_active_goals += active_goals
        max_level = max(max_level, child_profile.level)
        max_streak = max(max_streak, child_profile.streak_days)

        # Add child as UserRead object
        children_list.append(UserRead.model_validate(user))

    # Get recent transactions for the family
    if children_data:
        children_ids = [user.id for user, _ in children_data]
        recent_transactions_stmt = (
            select(Transaction)
            .where(Transaction.user_id.in_(children_ids))
            .order_by(Transaction.created_at.desc())
            .limit(10)
        )
        recent_transactions_result = await session.execute(recent_transactions_stmt)
        recent_transactions = recent_transactions_result.scalars().all()
        recent_transactions_list = [TransactionRead.model_validate(t) for t in recent_transactions]
    else:
        recent_transactions_list = []

    # Get pending redemption requests
    from models import RedemptionRequest
    if children_data:
        redemptions_stmt = (
            select(RedemptionRequest)
            .where(and_(
                RedemptionRequest.user_id.in_(children_ids),
                RedemptionRequest.status == "pending"
            ))
            .order_by(RedemptionRequest.created_at.desc())
        )
        redemptions_result = await session.execute(redemptions_stmt)
        redemptions = redemptions_result.scalars().all()
        pending_redemptions_list = [RedemptionRequestRead.model_validate(r) for r in redemptions]
    else:
        pending_redemptions_list = []

    # Create DashboardStats object
    dashboard_stats = DashboardStats(
        total_coins=total_coins,
        level=max_level,
        streak_days=max_streak,
        goals_count=total_active_goals,
        completed_tasks=total_completed_tasks
    )

    # Return proper ParentDashboardResponse
    return ParentDashboardResponse(
        user=UserRead.model_validate(current_user),
        stats=dashboard_stats,
        children=children_list,
        recent_transactions=recent_transactions_list,
        pending_redemptions=pending_redemptions_list
    )


@router.post("/children", response_model=ChildCreateResponse)
async def add_child(
    child_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager),
):
    """Add a new child to the parent's account."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can add children",
        )

    username = f"{child_data['name'].lower().replace(' ', '')}{child_data['age']}"
    email = child_data.get("email", f"{username}@family.local")

    # Create child user account
    from schemas import UserCreate
    import secrets
    import string

    password = "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(8)
    )

    user_data = UserCreate(
        email=email,
        password=password,
        name=child_data["name"],
        role="younger_child" if child_data["age"] < 11 else "older_child",
        avatar_url=child_data.get(
            "avatar_url", "👶" if child_data["age"] < 11 else "🧒"
        ),
    )

    try:
        child_user = await user_manager.create(user_data)
        print(f"[BACKEND] Created child user: {child_user.id} - {child_user.name}")
    except Exception as e:
        print(f"[BACKEND] Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create child user: {str(e)}",
        )

    # Create child profile
    try:
        child_profile = ChildProfile(
            user_id=child_user.id,
            age=child_data["age"],
            coins=0,
            level=1,
            streak_days=0,
            parent_id=current_user.id,
        )

        session.add(child_profile)
        await session.commit()
        print(f"[BACKEND] Child profile committed to database: {child_profile.user_id}")
    except Exception as e:
        print(f"[BACKEND] Error creating child profile: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create child profile: {str(e)}",
        )

    # Verify child was created successfully
    verify_stmt = (
        select(User, ChildProfile)
        .join(ChildProfile, User.id == ChildProfile.user_id)
        .where(
            and_(User.id == child_user.id, ChildProfile.parent_id == current_user.id)
        )
    )
    verify_result = await session.execute(verify_stmt)
    verified_child = verify_result.first()

    if not verified_child:
        print(f"[BACKEND] ERROR: Child not found after creation!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create child - database verification failed",
        )

    print(f"[BACKEND] Child verified in database: {verified_child[0].name}")

    # Store password for parent temporarily (in real app, send via secure channel)
    print(f"[BACKEND] Generated password for child {child_user.name}: {password}")

    # Return proper ChildCreateResponse
    return ChildCreateResponse(
        success=True,
        message=f"Child account created successfully for {child_user.name}",
        child=UserRead.model_validate(child_user)
    )


@router.get("/children/{child_id}/progress", response_model=dict)
async def get_child_progress(
    child_id: str,
    timeframe: str = "month",
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get detailed progress information for a specific child."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view child progress",
        )

    # Verify child belongs to parent
    child_stmt = (
        select(User, ChildProfile)
        .join(ChildProfile, User.id == ChildProfile.user_id)
        .where(and_(User.id == child_id, ChildProfile.parent_id == current_user.id))
    )
    child_result = await session.execute(child_stmt)
    child_data = child_result.first()

    if not child_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found or not associated with your account",
        )

    child_user, child_profile = child_data

    # Calculate timeframe dates
    now = datetime.utcnow()
    if timeframe == "week":
        start_date = now - timedelta(days=7)
    elif timeframe == "month":
        start_date = now - timedelta(days=30)
    elif timeframe == "quarter":
        start_date = now - timedelta(days=90)
    else:  # year
        start_date = now - timedelta(days=365)

    # Get statistics

    rewards_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == child_id,
            Transaction.type == "earn",
            Transaction.created_at >= start_date,
        )
    )
    rewards_result = await session.execute(rewards_stmt)
    total_rewards = rewards_result.scalar() or 0

    # Completed lessons/modules
    lessons_stmt = select(func.count(UserModuleProgress.id)).where(
        and_(
            UserModuleProgress.user_id == child_id,
            UserModuleProgress.is_completed == True,
            UserModuleProgress.completed_at >= start_date,
        )
    )
    lessons_result = await session.execute(lessons_stmt)
    lessons_completed = lessons_result.scalar() or 0

    # Goals achieved
    goals_stmt = select(func.count(Goal.id)).where(
        and_(
            Goal.user_id == child_id,
            Goal.is_completed == True,
            Goal.updated_at >= start_date,
        )
    )
    goals_result = await session.execute(goals_stmt)
    goals_achieved = goals_result.scalar() or 0

    # Recent activities
    activities_stmt = (
        select(Transaction)
        .where(
            and_(Transaction.user_id == child_id, Transaction.created_at >= start_date)
        )
        .order_by(Transaction.created_at.desc())
        .limit(10)
    )
    activities_result = await session.execute(activities_stmt)
    recent_activities = activities_result.scalars().all()

    # Active goals
    active_goals_stmt = select(Goal).where(
        and_(Goal.user_id == child_id, Goal.is_completed == False)
    )
    active_goals_result = await session.execute(active_goals_stmt)
    active_goals = active_goals_result.scalars().all()

    # Recent achievements
    achievements_stmt = (
        select(Achievement, UserAchievement.earned_at)
        .join(UserAchievement, Achievement.id == UserAchievement.achievement_id)
        .where(
            and_(
                UserAchievement.user_id == child_id,
                UserAchievement.earned_at >= start_date,
            )
        )
        .order_by(UserAchievement.earned_at.desc())
        .limit(5)
    )
    achievements_result = await session.execute(achievements_stmt)
    achievements_data = achievements_result.all()

    return {
        "child": {
            "id": child_user.id,
            "name": child_user.name,
            "age": child_profile.age,
            "current_coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days,
        },
        "stats": {
            "total_rewards": total_rewards,
            "lessons_completed": lessons_completed,
            "goals_achieved": goals_achieved,
            "current_streak": child_profile.streak_days,
        },
        "recent_activities": [
            {
                "id": activity.id,
                "type": activity.type,
                "amount": activity.amount,
                "description": activity.description,
                "created_at": activity.created_at.isoformat(),
            }
            for activity in recent_activities
        ],
        "active_goals": [
            {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "progress_percentage": (goal.current_amount / goal.target_amount * 100)
                if goal.target_amount > 0
                else 0,
                "deadline": goal.deadline.isoformat() if goal.deadline else None,
            }
            for goal in active_goals
        ],
        "recent_achievements": [
            {
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "icon": achievement.icon,
                "rarity": achievement.rarity,
                "earned_at": earned_at.isoformat(),
            }
            for achievement, earned_at in achievements_data
        ],
    }


@router.post("/tasks", response_model=TaskCreateResponse)
async def create_task(
    task_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new task for children."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create tasks",
        )

    # Handle single child assignment (expected by frontend)
    assigned_to = task_data.get("assigned_to")
    if not assigned_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="assigned_to field is required",
        )

    # Verify child belongs to parent
    child_stmt = select(ChildProfile.user_id).where(
        and_(
            ChildProfile.user_id == assigned_to,
            ChildProfile.parent_id == current_user.id,
        )
    )
    child_result = await session.execute(child_stmt)
    valid_child = child_result.scalar_one_or_none()

    if not valid_child:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Child does not belong to your account",
        )

    # Create task
    due_date = None
    if task_data.get("due_date"):
        try:
            # Handle ISO format with timezone info
            due_date_str = task_data["due_date"]
            if due_date_str.endswith('Z'):
                due_date_str = due_date_str[:-1] + '+00:00'
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError as e:
            print(f"[BACKEND] Warning: Invalid due_date format '{task_data['due_date']}': {e}")
            # Continue without due date rather than failing
            due_date = None
    
    task = Task(
        title=task_data["title"],
        description=task_data.get("description", ""),
        assigned_to=assigned_to,
        assigned_by=current_user.id,
        coins_reward=task_data.get("coins_reward", 10),
        due_date=due_date,
        requires_approval=task_data.get("requires_approval", True),
    )
    session.add(task)
    await session.commit()

    # Return proper TaskCreateResponse
    return TaskCreateResponse(
        success=True,
        task=TaskRead.model_validate(task),
        message=f"Task '{task.title}' created successfully"
    )


@router.get("/tasks", response_model=List[TaskRead])
async def get_family_tasks(
    status: Optional[str] = None,
    child_id: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all tasks for the family with optional filtering."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view family tasks",
        )

    children_stmt = select(ChildProfile.user_id).where(
        ChildProfile.parent_id == current_user.id
    )
    children_result = await session.execute(children_stmt)
    children_ids = [row[0] for row in children_result.all()]

    # Build query
    tasks_stmt = (
        select(Task, User.name.label("child_name"))
        .join(User, Task.assigned_to == User.id)
        .where(Task.assigned_to.in_(children_ids))
    )

    # Apply filters
    if status:
        if status == "completed":
            tasks_stmt = tasks_stmt.where(Task.status == "completed")
        elif status == "pending":
            tasks_stmt = tasks_stmt.where(Task.status == "pending")
        elif status == "overdue":
            tasks_stmt = tasks_stmt.where(
                and_(Task.status == "pending", Task.due_date < datetime.utcnow())
            )

    if child_id:
        tasks_stmt = tasks_stmt.where(Task.assigned_to == child_id)

    tasks_stmt = tasks_stmt.order_by(Task.created_at.desc())

    tasks_result = await session.execute(tasks_stmt)
    tasks_data = tasks_result.all()

    return [TaskRead.model_validate(task) for task, child_name in tasks_data]


@router.put("/tasks/{task_id}/approve", response_model=TaskApprovalResponse)
async def approve_task(
    task_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Approve a completed task and award coins."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can approve tasks",
        )

    # Get task and verify it belongs to parent's child
    task_stmt = (
        select(Task, ChildProfile)
        .join(ChildProfile, Task.assigned_to == ChildProfile.user_id)
        .where(and_(Task.id == task_id, ChildProfile.parent_id == current_user.id))
    )
    task_result = await session.execute(task_stmt)
    task_data = task_result.first()

    if not task_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not associated with your children",
        )

    task, child_profile = task_data

    if task.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task must be completed before approval",
        )

    if task.status == "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Task already approved"
        )

    # Approve task and award coins
    task.status = "approved"
    task.approved_at = datetime.utcnow()

    # Award coins to child
    child_profile.coins += task.coins_reward

    # Create transaction record
    transaction = Transaction(
        user_id=task.assigned_to,
        type="earn",
        amount=task.coins_reward,
        description=f"Task completed: {task.title}",
        category="task",
        source="parent_approval",
        reference_id=task.id,
        reference_type="task",
    )
    session.add(transaction)

    await session.commit()

    # Return proper TaskApprovalResponse
    return TaskApprovalResponse(
        success=True,
        task=TaskRead.model_validate(task),
        coins_awarded=task.coins_reward,
        message=f"Task '{task.title}' approved successfully"
    )


@router.get("/redemptions", response_model=List[RedemptionRequestRead])
async def get_redemption_requests(
    status: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get redemption requests from children."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view redemption requests",
        )

    # Get all children of this parent
    children_stmt = select(ChildProfile.user_id).where(
        ChildProfile.parent_id == current_user.id
    )
    children_result = await session.execute(children_stmt)
    children_ids = [row[0] for row in children_result.all()]

    if not children_ids:
        return []

    # Get redemption requests for these children
    from models import RedemptionRequest
    redemptions_stmt = (
        select(RedemptionRequest, User.name)
        .join(User, RedemptionRequest.user_id == User.id)
        .where(RedemptionRequest.user_id.in_(children_ids))
        .order_by(RedemptionRequest.created_at.desc())
    )

    # Apply status filter if provided
    if status:
        redemptions_stmt = redemptions_stmt.where(RedemptionRequest.status == status)

    redemptions_result = await session.execute(redemptions_stmt)
    redemptions_data = redemptions_result.all()

    # Build response with child information
    redemptions_list = []
    for redemption, child_name in redemptions_data:
        redemption_dict = RedemptionRequestRead.model_validate(redemption).model_dump()
        redemption_dict["child"] = {
            "name": child_name,
            "id": redemption.user_id
        }
        redemptions_list.append(RedemptionRequestRead(**redemption_dict))

    return redemptions_list


@router.put("/settings", response_model=dict)
async def update_parent_settings(
    settings_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update parent settings like exchange rate and approval requirements."""

    if current_user.role != "parent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can update settings",
        )

    # Get parent profile
    parent_stmt = select(ParentProfile).where(ParentProfile.user_id == current_user.id)
    parent_result = await session.execute(parent_stmt)
    parent_profile = parent_result.scalar_one_or_none()

    if not parent_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parent profile not found"
        )

    # Update settings
    if "exchange_rate" in settings_data:
        parent_profile.exchange_rate = settings_data["exchange_rate"]

    if "require_approval" in settings_data:
        parent_profile.require_approval = settings_data["require_approval"]

    if "auto_approval_limit" in settings_data:
        parent_profile.auto_approval_limit = settings_data["auto_approval_limit"]

    await session.commit()

    return {
        "message": "Settings updated successfully",
        "settings": {
            "exchange_rate": parent_profile.exchange_rate,
            "require_approval": parent_profile.require_approval,
            "auto_approval_limit": parent_profile.auto_approval_limit,
        },
    }
