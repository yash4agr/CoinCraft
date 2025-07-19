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
    User, ChildProfile, ParentProfile, Task, Goal, Transaction, 
    Achievement, UserAchievement, Module, UserModuleProgress
)
from schemas import (
    UserRead, ChildProfileRead, TaskRead, TaskCreate, TaskUpdate,
    GoalRead, TransactionRead, RedemptionRequestRead, DashboardData
)

router = APIRouter()

# Parent-specific data models
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

@router.get("/dashboard", response_model=dict)
async def get_parent_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get parent dashboard data including children overview and family stats."""
    
    # Verify user is a parent
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can access this endpoint"
        )
    
    # Get parent profile (create if doesn't exist for legacy users)
    parent_stmt = select(ParentProfile).where(ParentProfile.user_id == current_user.id)
    parent_result = await session.execute(parent_stmt)
    parent_profile = parent_result.scalar_one_or_none()
    
    if not parent_profile:
        # Create parent profile for legacy users who don't have one
        parent_profile = ParentProfile(
            user_id=current_user.id,
            exchange_rate=1.0,  # 1 coin = $1 by default
            auto_approval_limit=0.0,  # Require approval for all redemptions
            require_approval=True
        )
        session.add(parent_profile)
        await session.commit()
    
    # Get children
    children_stmt = select(User, ChildProfile).join(
        ChildProfile, User.id == ChildProfile.user_id
    ).where(ChildProfile.parent_id == current_user.id)
    
    children_result = await session.execute(children_stmt)
    children_data = children_result.all()
    
    print(f"🔍 [BACKEND] Dashboard: Found {len(children_data)} children for parent {current_user.id}")
    for user, profile in children_data:
        print(f"  - Child: {user.name} (ID: {user.id}, Age: {profile.age})")
    
    children = []
    family_stats = FamilyStats()
    family_stats.total_children = len(children_data)
    
    for user, child_profile in children_data:
        # Get child's active goals
        goals_stmt = select(func.count(Goal.id)).where(
            and_(Goal.user_id == user.id, Goal.is_completed == False)
        )
        goals_result = await session.execute(goals_stmt)
        active_goals = goals_result.scalar() or 0
        
        # Get child's completed tasks (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        tasks_stmt = select(func.count(Task.id)).where(
            and_(
                Task.assigned_to == user.id,
                Task.status == "completed",
                Task.completed_at >= thirty_days_ago
            )
        )
        tasks_result = await session.execute(tasks_stmt)
        completed_tasks = tasks_result.scalar() or 0
        
        # Get recent activity (last 5 transactions)
        activity_stmt = select(Transaction).where(
            Transaction.user_id == user.id
        ).order_by(Transaction.created_at.desc()).limit(5)
        activity_result = await session.execute(activity_stmt)
        recent_transactions = activity_result.scalars().all()
        
        child_data = {
            "id": user.id,
            "name": user.name,
            "age": child_profile.age,
            "coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days,
            "avatar_url": user.avatar_url,
            "active_goals": active_goals,
            "completed_tasks": completed_tasks,
            "username": f"{user.name.lower().replace(' ', '')}{child_profile.age}",
            "email": user.email,
            "recent_activity": [
                {
                    "id": t.id,
                    "type": t.type,
                    "amount": t.amount,
                    "description": t.description,
                    "created_at": t.created_at.isoformat()
                } for t in recent_transactions
            ]
        }
        children.append(child_data)
        
        # Update family stats
        family_stats.total_coins_earned += child_profile.coins
        family_stats.completed_tasks += completed_tasks
        family_stats.active_goals += active_goals
    
    return {
        "parent": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "exchange_rate": parent_profile.exchange_rate,
            "require_approval": parent_profile.require_approval
        },
        "children": children,
        "family_stats": {
            "total_children": family_stats.total_children,
            "total_coins_earned": family_stats.total_coins_earned,
            "completed_tasks": family_stats.completed_tasks,
            "active_goals": family_stats.active_goals
        }
    }

@router.post("/children", response_model=dict)
async def add_child(
    child_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Add a new child to the parent's account."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can add children"
        )
    
    # Generate child credentials
    username = f"{child_data['name'].lower().replace(' ', '')}{child_data['age']}"
    email = child_data.get('email', f"{username}@family.local")
    
    # Create child user account
    from schemas import UserCreate
    import secrets
    import string
    
    # Generate a simple password for the child
    password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
    
    user_data = UserCreate(
        email=email,
        password=password,
        name=child_data['name'],
        role='younger_child' if child_data['age'] < 11 else 'older_child',
        avatar_url=child_data.get('avatar_url', '👶' if child_data['age'] < 11 else '🧒')
    )
    
    # Create child user account
    try:
        child_user = await user_manager.create(user_data)
        print(f"🔍 [BACKEND] Created child user: {child_user.id} - {child_user.name}")
    except Exception as e:
        print(f"❌ [BACKEND] Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create child user: {str(e)}"
        )
    
    # Create child profile
    try:
        child_profile = ChildProfile(
            user_id=child_user.id,
            age=child_data['age'],
            coins=0,
            level=1,
            streak_days=0,
            parent_id=current_user.id
        )
        
        session.add(child_profile)
        await session.commit()
        print(f"✅ [BACKEND] Child profile committed to database: {child_profile.user_id}")
    except Exception as e:
        print(f"❌ [BACKEND] Error creating child profile: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create child profile: {str(e)}"
        )
    
    # Verify the child was saved by querying it back
    verify_stmt = select(User, ChildProfile).join(
        ChildProfile, User.id == ChildProfile.user_id
    ).where(
        and_(User.id == child_user.id, ChildProfile.parent_id == current_user.id)
    )
    verify_result = await session.execute(verify_stmt)
    verified_child = verify_result.first()
    
    if not verified_child:
        print(f"❌ [BACKEND] ERROR: Child not found after creation!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create child - database verification failed"
        )
    
    print(f"✅ [BACKEND] Child verified in database: {verified_child[0].name}")
    
    return {
        "message": "Child added successfully",
        "child": {
            "id": child_user.id,
            "name": child_user.name,
            "email": child_user.email,
            "username": username,
            "password": password,  # Return for parent to share with child
            "age": child_profile.age,
            "role": child_user.role
        }
    }

@router.get("/children/{child_id}/progress", response_model=dict)
async def get_child_progress(
    child_id: str,
    timeframe: str = "month",
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get detailed progress information for a specific child."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view child progress"
        )
    
    # Verify child belongs to parent
    child_stmt = select(User, ChildProfile).join(
        ChildProfile, User.id == ChildProfile.user_id
    ).where(
        and_(User.id == child_id, ChildProfile.parent_id == current_user.id)
    )
    child_result = await session.execute(child_stmt)
    child_data = child_result.first()
    
    if not child_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found or not associated with your account"
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
    # Total rewards/coins earned
    rewards_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.user_id == child_id,
            Transaction.type == 'earn',
            Transaction.created_at >= start_date
        )
    )
    rewards_result = await session.execute(rewards_stmt)
    total_rewards = rewards_result.scalar() or 0
    
    # Completed lessons/modules
    lessons_stmt = select(func.count(UserModuleProgress.id)).where(
        and_(
            UserModuleProgress.user_id == child_id,
            UserModuleProgress.is_completed == True,
            UserModuleProgress.completed_at >= start_date
        )
    )
    lessons_result = await session.execute(lessons_stmt)
    lessons_completed = lessons_result.scalar() or 0
    
    # Goals achieved
    goals_stmt = select(func.count(Goal.id)).where(
        and_(
            Goal.user_id == child_id,
            Goal.is_completed == True,
            Goal.updated_at >= start_date
        )
    )
    goals_result = await session.execute(goals_stmt)
    goals_achieved = goals_result.scalar() or 0
    
    # Recent activities
    activities_stmt = select(Transaction).where(
        and_(
            Transaction.user_id == child_id,
            Transaction.created_at >= start_date
        )
    ).order_by(Transaction.created_at.desc()).limit(10)
    activities_result = await session.execute(activities_stmt)
    recent_activities = activities_result.scalars().all()
    
    # Active goals
    active_goals_stmt = select(Goal).where(
        and_(Goal.user_id == child_id, Goal.is_completed == False)
    )
    active_goals_result = await session.execute(active_goals_stmt)
    active_goals = active_goals_result.scalars().all()
    
    # Recent achievements
    achievements_stmt = select(Achievement, UserAchievement.earned_at).join(
        UserAchievement, Achievement.id == UserAchievement.achievement_id
    ).where(
        and_(
            UserAchievement.user_id == child_id,
            UserAchievement.earned_at >= start_date
        )
    ).order_by(UserAchievement.earned_at.desc()).limit(5)
    achievements_result = await session.execute(achievements_stmt)
    achievements_data = achievements_result.all()
    
    return {
        "child": {
            "id": child_user.id,
            "name": child_user.name,
            "age": child_profile.age,
            "current_coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days
        },
        "stats": {
            "total_rewards": total_rewards,
            "lessons_completed": lessons_completed,
            "goals_achieved": goals_achieved,
            "current_streak": child_profile.streak_days
        },
        "recent_activities": [
            {
                "id": activity.id,
                "type": activity.type,
                "amount": activity.amount,
                "description": activity.description,
                "created_at": activity.created_at.isoformat()
            } for activity in recent_activities
        ],
        "active_goals": [
            {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "target_amount": goal.target_amount,
                "current_amount": goal.current_amount,
                "progress_percentage": (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0,
                "deadline": goal.deadline.isoformat() if goal.deadline else None
            } for goal in active_goals
        ],
        "recent_achievements": [
            {
                "id": achievement.id,
                "title": achievement.title,
                "description": achievement.description,
                "icon": achievement.icon,
                "rarity": achievement.rarity,
                "earned_at": earned_at.isoformat()
            } for achievement, earned_at in achievements_data
        ]
    }

@router.post("/tasks", response_model=dict)
async def create_task(
    task_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new task for children."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create tasks"
        )
    
    # Verify children belong to parent
    children_ids = task_data.get('assigned_to', [])
    if children_ids:
        children_stmt = select(ChildProfile.user_id).where(
            and_(
                ChildProfile.user_id.in_(children_ids),
                ChildProfile.parent_id == current_user.id
            )
        )
        children_result = await session.execute(children_stmt)
        valid_children = [row[0] for row in children_result.all()]
        
        if len(valid_children) != len(children_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more children do not belong to your account"
            )
    
    # Create tasks for each assigned child
    created_tasks = []
    for child_id in children_ids:
        task = Task(
            title=task_data['title'],
            description=task_data.get('description', ''),
            assigned_to=child_id,
            assigned_by=current_user.id,
            coin_reward=task_data.get('coin_reward', 10),
            due_date=datetime.fromisoformat(task_data['due_date']) if task_data.get('due_date') else None,
            requires_approval=task_data.get('requires_approval', True),
            is_recurring=task_data.get('is_recurring', False),
            priority=task_data.get('priority', 'medium')
        )
        session.add(task)
        created_tasks.append(task)
    
    await session.commit()
    
    return {
        "message": f"Created {len(created_tasks)} task(s) successfully",
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "assigned_to": task.assigned_to,
                "coin_reward": task.coins_reward,
                "due_date": task.due_date.isoformat() if task.due_date else None
            } for task in created_tasks
        ]
    }

@router.get("/tasks", response_model=List[dict])
async def get_family_tasks(
    status: Optional[str] = None,
    child_id: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all tasks for the family with optional filtering."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view family tasks"
        )
    
    # Get all children of this parent
    children_stmt = select(ChildProfile.user_id).where(ChildProfile.parent_id == current_user.id)
    children_result = await session.execute(children_stmt)
    children_ids = [row[0] for row in children_result.all()]
    
    # Build query
    tasks_stmt = select(Task, User.name.label('child_name')).join(
        User, Task.assigned_to == User.id
    ).where(Task.assigned_to.in_(children_ids))
    
    # Apply filters
    if status:
        if status == 'completed':
            tasks_stmt = tasks_stmt.where(Task.status == "completed")
        elif status == 'pending':
            tasks_stmt = tasks_stmt.where(Task.status == "pending")
        elif status == 'overdue':
            tasks_stmt = tasks_stmt.where(
                and_(Task.status == "pending", Task.due_date < datetime.utcnow())
            )
    
    if child_id:
        tasks_stmt = tasks_stmt.where(Task.assigned_to == child_id)
    
    tasks_stmt = tasks_stmt.order_by(Task.created_at.desc())
    
    tasks_result = await session.execute(tasks_stmt)
    tasks_data = tasks_result.all()
    
    return [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "child_id": task.assigned_to,
            "child_name": child_name,
            "coin_reward": task.coins_reward,
            "is_completed": task.status == "completed",
            "requires_approval": task.requires_approval,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "created_at": task.created_at.isoformat()
        } for task, child_name in tasks_data
    ]

@router.put("/tasks/{task_id}/approve", response_model=dict)
async def approve_task(
    task_id: str,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Approve a completed task and award coins."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can approve tasks"
        )
    
    # Get task and verify it belongs to parent's child
    task_stmt = select(Task, ChildProfile).join(
        ChildProfile, Task.assigned_to == ChildProfile.user_id
    ).where(
        and_(Task.id == task_id, ChildProfile.parent_id == current_user.id)
    )
    task_result = await session.execute(task_stmt)
    task_data = task_result.first()
    
    if not task_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not associated with your children"
        )
    
    task, child_profile = task_data
    
    if task.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task must be completed before approval"
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
        type='earn',
        amount=task.coins_reward,
        description=f"Task completed: {task.title}",
        category='task',
        source='parent_approval',
        reference_id=task.id,
        reference_type='task'
    )
    session.add(transaction)
    
    await session.commit()
    
    return {
        "message": "Task approved successfully",
        "coins_awarded": task.coins_reward,
        "child_total_coins": child_profile.coins
    }

@router.get("/redemptions", response_model=List[dict])
async def get_redemption_requests(
    status: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get redemption requests from children."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can view redemption requests"
        )
    
    # Get all children of this parent
    children_stmt = select(ChildProfile.user_id).where(ChildProfile.parent_id == current_user.id)
    children_result = await session.execute(children_stmt)
    children_ids = [row[0] for row in children_result.all()]
    
    # Get redemption requests (this would be a separate model in a real app)
    # For now, return empty list as the RedemptionRequest model isn't defined
    return []

@router.put("/settings", response_model=dict)
async def update_parent_settings(
    settings_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update parent settings like exchange rate and approval requirements."""
    
    if current_user.role != 'parent':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can update settings"
        )
    
    # Get parent profile
    parent_stmt = select(ParentProfile).where(ParentProfile.user_id == current_user.id)
    parent_result = await session.execute(parent_stmt)
    parent_profile = parent_result.scalar_one_or_none()
    
    if not parent_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent profile not found"
        )
    
    # Update settings
    if 'exchange_rate' in settings_data:
        parent_profile.exchange_rate = settings_data['exchange_rate']
    
    if 'require_approval' in settings_data:
        parent_profile.require_approval = settings_data['require_approval']
    
    if 'auto_approval_limit' in settings_data:
        parent_profile.auto_approval_limit = settings_data['auto_approval_limit']
    
    await session.commit()
    
    return {
        "message": "Settings updated successfully",
        "settings": {
            "exchange_rate": parent_profile.exchange_rate,
            "require_approval": parent_profile.require_approval,
            "auto_approval_limit": parent_profile.auto_approval_limit
        }
    } 