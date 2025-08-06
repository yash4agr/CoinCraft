"""Child management router for CoinCraft."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from backend.database import get_async_session
from backend.auth import current_active_user, get_user_manager, UserManager
from backend.models import (
    User,
    ChildProfile,
    Goal,
    Transaction,
    Module,
    UserModuleProgress,
    Achievement,
    UserAchievement,
    RedemptionRequest,
)
from backend.schemas import UserRead

router = APIRouter()


# Child-specific data models
class ChildDashboardData:
    def __init__(
        self,
        user: User,
        profile: ChildProfile,
        goals: List[Goal],
        transactions: List[Transaction],
        achievements: List[UserAchievement],
    ):
        self.user = user
        self.profile = profile
        self.goals = goals
        self.transactions = transactions
        self.achievements = achievements


class ActivitySummary:
    def __init__(self, module: Module, progress: Optional[UserModuleProgress]):
        self.id = module.id
        self.title = module.title
        self.description = module.description
        self.difficulty = module.difficulty
        self.duration = module.estimated_duration
        self.coins = module.points_reward
        self.completed = progress.is_completed if progress else False
        self.icon = f"ri-{module.category.lower()}-line"


@router.get("/dashboard", response_model=dict)
async def get_child_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get child dashboard data including goals, activities, and progress."""

    # Verify user is a child
    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can access this endpoint",
        )

    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        child_profile = ChildProfile(
            user_id=current_user.id,
            age=10,  # Default age
            coins=0,
            level=1,
            streak_days=0,
        )
        session.add(child_profile)
        await session.commit()

    print(f"[BACKEND] Child Dashboard: Loading data for child {current_user.id}")

    # Get child's goals
    goals_stmt = (
        select(Goal)
        .where(and_(Goal.user_id == current_user.id, Goal.is_completed == False))
        .order_by(Goal.created_at.desc())
    )
    goals_result = await session.execute(goals_stmt)
    active_goals = goals_result.scalars().all()

    # Get completed goals
    completed_goals_stmt = (
        select(Goal)
        .where(and_(Goal.user_id == current_user.id, Goal.is_completed == True))
        .order_by(Goal.updated_at.desc())
        .limit(5)
    )
    completed_goals_result = await session.execute(completed_goals_stmt)
    completed_goals = completed_goals_result.scalars().all()

    # Get recent transactions
    transactions_stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .limit(10)
    )
    transactions_result = await session.execute(transactions_stmt)
    recent_transactions = transactions_result.scalars().all()

    # Get recent achievements
    achievements_stmt = (
        select(UserAchievement, Achievement)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .where(UserAchievement.user_id == current_user.id)
        .order_by(UserAchievement.earned_at.desc())
        .limit(5)
    )
    achievements_result = await session.execute(achievements_stmt)
    achievements_data = achievements_result.all()

    # Get available activities/modules
    modules_stmt = (
        select(Module)
        .where(
            and_(Module.is_published == True, Module.difficulty.in_(["easy", "medium"]))
        )
        .order_by(Module.difficulty, Module.title)
    )
    modules_result = await session.execute(modules_stmt)
    available_modules = modules_result.scalars().all()

    # Get child's module progress
    progress_stmt = select(UserModuleProgress).where(
        UserModuleProgress.user_id == current_user.id
    )
    progress_result = await session.execute(progress_stmt)
    user_progress = {p.module_id: p for p in progress_result.scalars().all()}

    todays_goals = []
    for goal in active_goals[:4]:  # Limit to 4 goals
        progress_percentage = (
            (goal.current_amount / goal.target_amount * 100)
            if goal.target_amount > 0
            else 0
        )
        todays_goals.append(
            {
                "id": goal.id,
                "title": goal.title,
                "current": goal.current_amount,
                "total": goal.target_amount,
                "icon": goal.icon,
                "colorScheme": "green" if progress_percentage > 50 else "yellow",
            }
        )

    adventures = []
    for module in available_modules[:6]:  # Limit to 6 activities
        progress = user_progress.get(module.id)
        completed = progress.is_completed if progress else False

        adventures.append(
            {
                "id": module.id,
                "title": module.title,
                "description": module.description,
                "emoji": "🎮",  # Default emoji
                "difficulty": module.difficulty,
                "coins": module.points_reward,
                "completed": completed,
                "colorScheme": "blue" if completed else "purple",
                "buttonText": "Play Again" if completed else "Start Adventure!",
            }
        )

    # Prepare achievements
    achievements = []
    for user_achievement, achievement in achievements_data:
        achievements.append(
            {
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "icon": achievement.icon,
                "badge": achievement.rarity,
                "coins": achievement.points_reward,
                "date": user_achievement.earned_at.strftime("%b %d"),
                "colorScheme": "gold" if achievement.rarity == "rare" else "silver",
            }
        )

    # Prepare learning journey
    learning_journey = [
        {
            "id": "1",
            "title": "Piggy Bank Basics",
            "description": "Learn how to save money",
            "status": "completed"
            if any(p.is_completed for p in user_progress.values())
            else "available",
            "icon": "ri-piggy-bank-line",
        },
        {
            "id": "2",
            "title": "Needs vs Wants",
            "description": "Understand the difference",
            "status": "available",
            "icon": "ri-scales-line",
        },
        {
            "id": "3",
            "title": "Smart Shopping",
            "description": "Learn to shop wisely",
            "status": "locked",
            "icon": "ri-shopping-cart-line",
        },
    ]

    return {
        "child": {
            "id": current_user.id,
            "name": current_user.name,
            "avatar": current_user.avatar_url,
            "coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days,
        },
        "todays_goals": todays_goals,
        "adventures": adventures,
        "achievements": achievements,
        "learning_journey": learning_journey,
        "stats": {
            "total_goals": len(active_goals),
            "completed_goals": len(completed_goals),
            "total_coins": child_profile.coins,
            "streak_days": child_profile.streak_days,
        },
    }


@router.get("/goals", response_model=List[dict])
async def get_child_goals(
    status: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get child's goals."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can access this endpoint",
        )

    query = select(Goal).where(Goal.user_id == current_user.id)

    if status == "active":
        query = query.where(Goal.is_completed == False)
    elif status == "completed":
        query = query.where(Goal.is_completed == True)

    query = query.order_by(Goal.created_at.desc())

    goals_result = await session.execute(query)
    goals = goals_result.scalars().all()

    goals_data = []
    for goal in goals:
        progress_percentage = (
            (goal.current_amount / goal.target_amount * 100)
            if goal.target_amount > 0
            else 0
        )
        goals_data.append(
            {
                "id": goal.id,
                "name": goal.title,
                "targetAmount": goal.target_amount,
                "currentAmount": goal.current_amount,
                "icon": goal.icon,
                "createdAt": goal.created_at.isoformat(),
                "progress_percentage": round(progress_percentage, 1),
                "is_completed": goal.is_completed,
            }
        )

    return goals_data


@router.post("/goals", response_model=dict)
async def create_child_goal(
    goal_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new goal for the child."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can create goals",
        )

    # Create goal
    new_goal = Goal(
        user_id=current_user.id,
        title=goal_data["name"],
        description=goal_data.get("description", goal_data["name"]),
        target_amount=goal_data["targetAmount"],
        current_amount=goal_data.get("currentAmount", 0),
        icon=goal_data.get("icon", "ri-target-line"),
        color=goal_data.get("color", "blue"),
        is_completed=False,
    )

    session.add(new_goal)
    await session.commit()

    print(f"[BACKEND] Created goal: {new_goal.title} (ID: {new_goal.id})")

    return {
        "message": "Goal created successfully",
        "goal": {
            "id": new_goal.id,
            "name": new_goal.title,
            "targetAmount": new_goal.target_amount,
            "currentAmount": new_goal.current_amount,
            "icon": new_goal.icon,
            "createdAt": new_goal.created_at.isoformat(),
        },
    }


@router.put("/goals/{goal_id}/progress", response_model=dict)
async def update_goal_progress(
    goal_id: str,
    progress_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update goal progress by adding coins."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can update goals",
        )

    # Get goal
    goal_stmt = select(Goal).where(
        and_(Goal.id == goal_id, Goal.user_id == current_user.id)
    )
    goal_result = await session.execute(goal_stmt)
    goal = goal_result.scalar_one_or_none()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found"
        )

    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found"
        )

    amount = progress_data.get("amount", 0)

    if amount > child_profile.coins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough coins"
        )

    goal.current_amount = min(goal.current_amount + amount, goal.target_amount)

    if goal.current_amount >= goal.target_amount:
        goal.is_completed = True
        goal.updated_at = datetime.utcnow()

    child_profile.coins -= amount

    transaction = Transaction(
        user_id=current_user.id,
        type="spend",
        amount=amount,
        description=f"Added to goal: {goal.title}",
        category="goal",
        reference_id=goal.id,
        reference_type="goal",
    )

    session.add(transaction)
    await session.commit()

    print(f"[BACKEND] Updated goal progress: {goal.title} (+{amount} coins)")

    return {
        "message": "Goal progress updated successfully",
        "goal": {
            "id": goal.id,
            "name": goal.title,
            "targetAmount": goal.target_amount,
            "currentAmount": goal.current_amount,
            "is_completed": goal.is_completed,
        },
        "coins_remaining": child_profile.coins,
    }


@router.get("/activities", response_model=List[dict])
async def get_child_activities(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get available activities/games for the child."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can access activities",
        )

    modules_stmt = (
        select(Module)
        .where(
            and_(Module.is_published == True, Module.difficulty.in_(["easy", "medium"]))
        )
        .order_by(Module.difficulty, Module.title)
    )
    modules_result = await session.execute(modules_stmt)
    modules = modules_result.scalars().all()

    progress_stmt = select(UserModuleProgress).where(
        UserModuleProgress.user_id == current_user.id
    )
    progress_result = await session.execute(progress_stmt)
    user_progress = {p.module_id: p for p in progress_result.scalars().all()}

    activities = []
    for module in modules:
        progress = user_progress.get(module.id)
        completed = progress.is_completed if progress else False

        activities.append(
            {
                "id": module.id,
                "name": module.title,
                "description": module.description,
                "coins": module.points_reward,
                "duration": module.estimated_duration,
                "difficulty": module.difficulty,
                "completed": completed,
                "icon": f"ri-{module.category.lower()}-line",
            }
        )

    return activities


@router.post("/activities/{activity_id}/complete", response_model=dict)
async def complete_activity(
    activity_id: str,
    completion_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Complete an activity and earn coins."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can complete activities",
        )

    module_stmt = select(Module).where(Module.id == activity_id)
    module_result = await session.execute(module_stmt)
    module = module_result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found"
        )

    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found"
        )

    progress_stmt = select(UserModuleProgress).where(
        and_(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.module_id == activity_id,
        )
    )
    progress_result = await session.execute(progress_stmt)
    existing_progress = progress_result.scalar_one_or_none()

    if existing_progress and existing_progress.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Activity already completed"
        )

    score = completion_data.get("score", 100)
    coins_earned = int((score / 100) * module.points_reward)

    if existing_progress:
        existing_progress.is_completed = True
        existing_progress.score = score
        existing_progress.completed_at = datetime.utcnow()
        existing_progress.time_spent = completion_data.get("time_spent", 0)
    else:
        new_progress = UserModuleProgress(
            user_id=current_user.id,
            module_id=activity_id,
            is_completed=True,
            score=score,
            completed_at=datetime.utcnow(),
            time_spent=completion_data.get("time_spent", 0),
        )
        session.add(new_progress)

    child_profile.coins += coins_earned

    transaction = Transaction(
        user_id=current_user.id,
        type="earn",
        amount=coins_earned,
        description=f"Completed: {module.title}",
        category="activity",
        source="module_completion",
        reference_id=activity_id,
        reference_type="module",
    )

    session.add(transaction)
    await session.commit()

    print(f"[BACKEND] Activity completed: {module.title} (+{coins_earned} coins)")

    return {
        "message": "Activity completed successfully",
        "activity": {
            "id": module.id,
            "name": module.title,
            "score": score,
            "coins_earned": coins_earned,
        },
        "total_coins": child_profile.coins,
    }


@router.get("/transactions", response_model=List[dict])
async def get_child_transactions(
    limit: int = 20,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get child's transaction history."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only children can view transactions",
        )

    transactions_stmt = (
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc())
        .limit(limit)
    )

    transactions_result = await session.execute(transactions_stmt)
    transactions = transactions_result.scalars().all()

    transactions_data = []
    for transaction in transactions:
        transactions_data.append(
            {
                "id": transaction.id,
                "type": transaction.type,
                "amount": transaction.amount,
                "description": transaction.description,
                "timestamp": transaction.created_at.isoformat(),
                "category": transaction.category,
            }
        )

    return transactions_data


@router.get("/stats", response_model=dict)
async def get_child_stats(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get child's statistics and progress."""

    if current_user.role not in ["younger_child", "older_child"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only children can view stats"
        )

    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()

    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found"
        )

    # Get goals stats
    goals_stmt = select(Goal).where(Goal.user_id == current_user.id)
    goals_result = await session.execute(goals_stmt)
    goals = goals_result.scalars().all()

    active_goals = [g for g in goals if not g.is_completed]
    completed_goals = [g for g in goals if g.is_completed]

    # Get module/activity stats
    modules_stmt = select(Module).where(Module.is_published)
    modules_result = await session.execute(modules_stmt)
    total_modules = modules_result.scalars().all()

    progress_stmt = select(UserModuleProgress).where(
        and_(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.is_completed,
        )
    )
    progress_result = await session.execute(progress_stmt)
    completed_activities = progress_result.scalars().all()

    # Get transaction stats
    transactions_stmt = select(Transaction).where(
        Transaction.user_id == current_user.id
    )
    transactions_result = await session.execute(transactions_stmt)
    transactions = transactions_result.scalars().all()

    total_earned = sum(t.amount for t in transactions if t.type == "earn")
    total_spent = sum(t.amount for t in transactions if t.type == "spend")

    return {
        "profile": {
            "coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days,
        },
        "goals": {
            "active": len(active_goals),
            "completed": len(completed_goals),
            "total": len(goals),
        },
        "activities": {
            "completed": len(completed_activities),
            "total_available": len(total_modules),
        },
        "transactions": {
            "total_earned": total_earned,
            "total_spent": total_spent,
            "net_balance": total_earned - total_spent,
        },
    }
