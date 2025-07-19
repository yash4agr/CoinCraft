"""Dashboard data router."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc

from database import get_async_session
from auth import current_active_user
from models import (
    User, ChildProfile, Goal, Transaction, UserAchievement, Achievement,
    Module, UserModuleProgress, Task, RedemptionRequest
)
from schemas import DashboardData, ProgressGoal, TransactionRead, GoalRead, AchievementRead

router = APIRouter()


@router.get("/dashboard/{user_role}")
async def get_dashboard_data(
    user_role: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get role-specific dashboard data with appropriate metrics and information."""
    if user_role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role mismatch"
        )
    
    if user_role in ["younger_child", "older_child"]:
        return await get_child_dashboard_data(current_user, session)
    elif user_role == "parent":
        return await get_parent_dashboard_data(current_user, session)
    elif user_role == "teacher":
        return await get_teacher_dashboard_data(current_user, session)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user role"
        )


async def get_child_dashboard_data(current_user: User, session: AsyncSession):
    """Get dashboard data for child users."""
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # User stats
    user_stats = {
        "coins": child_profile.coins,
        "level": child_profile.level,
        "streak": child_profile.streak_days,
        "total_earned": 0,  # Will be calculated from transactions
        "goals_completed": 0,  # Will be calculated from goals
    }
    
    # Calculate total earned from transactions
    earned_stmt = select(func.sum(Transaction.amount)).where(
        and_(Transaction.user_id == current_user.id, Transaction.type == "earn")
    )
    earned_result = await session.execute(earned_stmt)
    total_earned = earned_result.scalar() or 0
    user_stats["total_earned"] = total_earned
    
    # Recent transactions (last 10)
    trans_stmt = select(Transaction).where(
        Transaction.user_id == current_user.id
    ).order_by(desc(Transaction.created_at)).limit(10)
    trans_result = await session.execute(trans_stmt)
    transactions = trans_result.scalars().all()
    recent_transactions = [TransactionRead.model_validate(t) for t in transactions]
    
    # Active goals
    goals_stmt = select(Goal).where(
        and_(Goal.user_id == current_user.id, Goal.is_completed == False)
    ).order_by(desc(Goal.created_at)).limit(5)
    goals_result = await session.execute(goals_stmt)
    goals = goals_result.scalars().all()
    active_goals = [GoalRead.model_validate(g) for g in goals]
    
    # Count completed goals
    completed_goals_stmt = select(func.count(Goal.id)).where(
        and_(Goal.user_id == current_user.id, Goal.is_completed == True)
    )
    completed_goals_result = await session.execute(completed_goals_stmt)
    user_stats["goals_completed"] = completed_goals_result.scalar() or 0
    
    # Recent achievements
    achievements_stmt = select(Achievement, UserAchievement.earned_at).join(
        UserAchievement
    ).where(
        UserAchievement.user_id == current_user.id
    ).order_by(desc(UserAchievement.earned_at)).limit(5)
    achievements_result = await session.execute(achievements_stmt)
    achievement_rows = achievements_result.all()
    
    achievements = []
    for achievement, earned_at in achievement_rows:
        achievement_dict = AchievementRead.model_validate(achievement).model_dump()
        achievement_dict["earned_at"] = earned_at
        achievements.append(AchievementRead(**achievement_dict))
    
    # Learning modules progress
    modules_stmt = select(Module).where(Module.is_published == True).limit(6)
    modules_result = await session.execute(modules_stmt)
    modules = modules_result.scalars().all()
    
    learning_modules = []
    for module in modules:
        # Get user progress
        progress_stmt = select(UserModuleProgress).where(
            and_(
                UserModuleProgress.user_id == current_user.id,
                UserModuleProgress.module_id == module.id
            )
        )
        progress_result = await session.execute(progress_stmt)
        progress = progress_result.scalar_one_or_none()
        
        from schemas import ModuleRead
        module_dict = ModuleRead.model_validate(module).model_dump()
        if progress:
            module_dict["user_progress"] = {
                "progress_percentage": progress.progress_percentage,
                "is_completed": progress.is_completed,
                "score": progress.score,
                "time_spent": progress.time_spent
            }
        learning_modules.append(module_dict)
    
    return DashboardData(
        user_stats=user_stats,
        recent_transactions=recent_transactions,
        active_goals=active_goals,
        achievements=achievements,
        learning_modules=learning_modules
    )


async def get_parent_dashboard_data(current_user: User, session: AsyncSession):
    """Get dashboard data for parent users."""
    # Get children
    children_stmt = select(User).join(ChildProfile).where(
        ChildProfile.parent_id == current_user.id
    )
    children_result = await session.execute(children_stmt)
    children = children_result.scalars().all()
    
    # User stats
    user_stats = {
        "total_children": len(children),
        "total_coins_distributed": 0,
        "pending_tasks": 0,
        "pending_redemptions": 0,
    }
    
    # Calculate total coins distributed
    for child in children:
        earned_stmt = select(func.sum(Transaction.amount)).where(
            and_(Transaction.user_id == child.id, Transaction.type == "earn")
        )
        earned_result = await session.execute(earned_stmt)
        earned = earned_result.scalar() or 0
        user_stats["total_coins_distributed"] += earned
    
    # Count pending tasks
    pending_tasks_stmt = select(func.count(Task.id)).where(
        and_(Task.assigned_by == current_user.id, Task.status == "completed")
    )
    pending_tasks_result = await session.execute(pending_tasks_stmt)
    user_stats["pending_tasks"] = pending_tasks_result.scalar() or 0
    
    # Count pending redemptions
    child_ids = [child.id for child in children]
    if child_ids:
        pending_redemptions_stmt = select(func.count(RedemptionRequest.id)).where(
            and_(
                RedemptionRequest.user_id.in_(child_ids),
                RedemptionRequest.status == "pending"
            )
        )
        pending_redemptions_result = await session.execute(pending_redemptions_stmt)
        user_stats["pending_redemptions"] = pending_redemptions_result.scalar() or 0
    
    # Recent transactions from all children
    if child_ids:
        trans_stmt = select(Transaction).where(
            Transaction.user_id.in_(child_ids)
        ).order_by(desc(Transaction.created_at)).limit(10)
        trans_result = await session.execute(trans_stmt)
        transactions = trans_result.scalars().all()
        recent_transactions = [TransactionRead.model_validate(t) for t in transactions]
    else:
        recent_transactions = []
    
    # Children's active goals
    active_goals = []
    if child_ids:
        goals_stmt = select(Goal).where(
            and_(Goal.user_id.in_(child_ids), Goal.is_completed == False)
        ).order_by(desc(Goal.created_at)).limit(5)
        goals_result = await session.execute(goals_stmt)
        goals = goals_result.scalars().all()
        active_goals = [GoalRead.model_validate(g) for g in goals]
    
    # No achievements or learning modules for parents
    achievements = []
    learning_modules = []
    
    return DashboardData(
        user_stats=user_stats,
        recent_transactions=recent_transactions,
        active_goals=active_goals,
        achievements=achievements,
        learning_modules=learning_modules
    )


async def get_teacher_dashboard_data(current_user: User, session: AsyncSession):
    """Get dashboard data for teacher users."""
    # Get teacher profile and classes
    from models import TeacherProfile, Class, ClassStudent
    
    teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == current_user.id)
    teacher_result = await session.execute(teacher_stmt)
    teacher_profile = teacher_result.scalar_one_or_none()
    
    if not teacher_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher profile not found"
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
    
    # User stats
    user_stats = {
        "total_classes": len(classes),
        "total_students": total_students,
        "modules_created": 0,
        "average_performance": 0.0,
    }
    
    # Count modules created by teacher
    modules_stmt = select(func.count(Module.id)).where(Module.created_by == current_user.id)
    modules_result = await session.execute(modules_stmt)
    user_stats["modules_created"] = modules_result.scalar() or 0
    
    # No transactions, goals, or achievements for teachers
    recent_transactions = []
    active_goals = []
    achievements = []
    
    # Show available modules
    modules_stmt = select(Module).where(Module.is_published == True).limit(6)
    modules_result = await session.execute(modules_stmt)
    modules = modules_result.scalars().all()
    
    from schemas import ModuleRead
    learning_modules = [ModuleRead.model_validate(m).model_dump() for m in modules]
    
    return DashboardData(
        user_stats=user_stats,
        recent_transactions=recent_transactions,
        active_goals=active_goals,
        achievements=achievements,
        learning_modules=learning_modules
    )


@router.get("/progress-goals/{user_id}", response_model=List[ProgressGoal])
async def get_todays_goals(
    user_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get daily progress goals and statistics."""
    if user_id == "me":
        user_id = current_user.id
    elif user_id != current_user.id:
        # Parents can view their children's progress
        if current_user.role != "parent":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
    
    # For children, return daily goals
    if current_user.role in ["younger_child", "older_child"]:
        today = datetime.utcnow().date()
        
        # Calculate daily progress
        today_start = datetime.combine(today, datetime.min.time())
        
        # Lessons read today
        lessons_stmt = select(func.count(UserModuleProgress.id)).where(
            and_(
                UserModuleProgress.user_id == user_id,
                UserModuleProgress.started_at >= today_start,
                UserModuleProgress.progress_percentage > 0
            )
        )
        lessons_result = await session.execute(lessons_stmt)
        lessons_read = lessons_result.scalar() or 0
        
        # Coins earned today
        coins_stmt = select(func.sum(Transaction.amount)).where(
            and_(
                Transaction.user_id == user_id,
                Transaction.type == "earn",
                Transaction.created_at >= today_start
            )
        )
        coins_result = await session.execute(coins_stmt)
        coins_earned = coins_result.scalar() or 0
        
        # Games completed today
        games_stmt = select(func.count(UserModuleProgress.id)).where(
            and_(
                UserModuleProgress.user_id == user_id,
                UserModuleProgress.completed_at >= today_start,
                UserModuleProgress.is_completed == True
            )
        )
        games_result = await session.execute(games_stmt)
        games_completed = games_result.scalar() or 0
        
        # Practice time (simplified)
        practice_time = min(lessons_read * 5 + games_completed * 3, 20)
        
        return [
            ProgressGoal(
                id="lessons",
                title="Read Lessons",
                current=min(lessons_read, 3),
                total=3,
                icon="ri-book-open-line",
                color_scheme="orange"
            ),
            ProgressGoal(
                id="coins",
                title="Earn Coins",
                current=min(coins_earned, 50),
                total=50,
                icon="ri-coins-line",
                color_scheme="blue"
            ),
            ProgressGoal(
                id="games",
                title="Complete Games",
                current=min(games_completed, 2),
                total=2,
                icon="ri-gamepad-line",
                color_scheme="green"
            ),
            ProgressGoal(
                id="practice",
                title="Practice Time",
                current=practice_time,
                total=20,
                icon="ri-time-line",
                color_scheme="purple"
            )
        ]
    
    return []


@router.put("/progress-goals/{goal_id}/update")
async def update_goal_progress(
    goal_id: str,
    progress_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update progress on a daily goal."""
    # This is mainly for tracking daily goal completion
    # In a real implementation, this would update progress tracking
    current_value = progress_data.get("current", 0)
    
    # Return updated progress (simplified)
    return {
        "id": goal_id,
        "current": current_value,
        "is_completed": current_value >= 100,  # Assuming 100 is completion
        "coins_earned": 5 if current_value >= 100 else 0
    } 