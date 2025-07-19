"""Teen/Older Child management router for CoinCraft."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload

from database import get_async_session
from auth import current_active_user, get_user_manager, UserManager
from models import (
    User, ChildProfile, Goal, Transaction, Module, UserModuleProgress, 
    Achievement, UserAchievement, RedemptionRequest
)
from schemas import UserRead

router = APIRouter()

# Teen-specific data models
class TeenDashboardData:
    def __init__(self, user: User, profile: ChildProfile, goals: List[Goal], 
                 transactions: List[Transaction], budget_allocations: dict):
        self.user = user
        self.profile = profile
        self.goals = goals
        self.transactions = transactions
        self.budget_allocations = budget_allocations

class BudgetAllocation:
    def __init__(self, saving: int, spending: int, wants: int):
        self.saving = saving
        self.spending = spending
        self.wants = wants

@router.get("/dashboard", response_model=dict)
async def get_teen_dashboard(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get teen dashboard data including budget overview and advanced features."""
    
    # Verify user is an older child
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can access this endpoint"
        )
    
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()
    
    if not child_profile:
        # Create child profile for legacy users
        child_profile = ChildProfile(
            user_id=current_user.id,
            age=15,  # Default age for teens
            coins=0,
            level=1,
            streak_days=0
        )
        session.add(child_profile)
        await session.commit()
    
    print(f"🔍 [BACKEND] Teen Dashboard: Loading data for teen {current_user.id}")
    
    # Get teen's goals (categorized)
    goals_stmt = select(Goal).where(
        and_(Goal.user_id == current_user.id, Goal.is_completed == False)
    ).order_by(Goal.created_at.desc())
    goals_result = await session.execute(goals_stmt)
    active_goals = goals_result.scalars().all()
    
    # Get recent transactions
    transactions_stmt = select(Transaction).where(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(10)
    transactions_result = await session.execute(transactions_stmt)
    recent_transactions = transactions_result.scalars().all()
    
    # Get recent achievements
    achievements_stmt = select(UserAchievement, Achievement).join(
        Achievement, UserAchievement.achievement_id == Achievement.id
    ).where(
        UserAchievement.user_id == current_user.id
    ).order_by(UserAchievement.earned_at.desc()).limit(5)
    achievements_result = await session.execute(achievements_stmt)
    achievements_data = achievements_result.all()
    
    # Get available advanced activities/modules
    modules_stmt = select(Module).where(
        and_(Module.is_published == True, Module.difficulty.in_(['medium', 'hard']))
    ).order_by(Module.difficulty, Module.title)
    modules_result = await session.execute(modules_stmt)
    available_modules = modules_result.scalars().all()
    
    # Get teen's module progress
    progress_stmt = select(UserModuleProgress).where(
        UserModuleProgress.user_id == current_user.id
    )
    progress_result = await session.execute(progress_stmt)
    user_progress = {p.module_id: p for p in progress_result.scalars().all()}
    
    # Calculate budget allocations (default 40-35-25 split)
    total_coins = child_profile.coins
    budget_allocations = {
        "saving": int(total_coins * 0.4),
        "spending": int(total_coins * 0.35),
        "wants": int(total_coins * 0.25)
    }
    
    # Prepare categorized goals
    categorized_goals = {
        "saving": [],
        "spending": [],
        "wants": []
    }
    
    for goal in active_goals:
        category = goal.category if hasattr(goal, 'category') else 'saving'
        if category not in categorized_goals:
            category = 'saving'  # Default category
        
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        categorized_goals[category].append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "targetAmount": goal.target_amount,
            "currentAmount": goal.current_amount,
            "icon": goal.icon,
            "category": category,
            "progress_percentage": round(progress_percentage, 1),
            "deadline": goal.deadline.isoformat() if goal.deadline else None
        })
    
    # Prepare advanced activities
    activities = []
    for module in available_modules[:8]:  # Limit to 8 activities
        progress = user_progress.get(module.id)
        completed = progress.is_completed if progress else False
        
        activities.append({
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "category": module.category,
            "difficulty": module.difficulty,
            "duration": module.estimated_duration,
            "coins": module.points_reward,
            "completed": completed,
            "rating": 4.5,  # Mock rating
            "likes": 42,    # Mock likes
            "bookmarked": False
        })
    
    # Prepare achievements
    achievements = []
    for user_achievement, achievement in achievements_data:
        achievements.append({
            "id": achievement.id,
            "title": achievement.title,
            "description": achievement.description,
            "icon": achievement.icon,
            "badge": achievement.rarity,
            "coins": achievement.points_reward,
            "date": user_achievement.earned_at.strftime("%b %d"),
            "colorScheme": "gold" if achievement.rarity == "rare" else "silver"
        })
    
    # Prepare quick actions
    quick_actions = [
        {
            "id": "budget",
            "title": "Budget Manager",
            "description": "Manage your money allocation",
            "icon": "ri-pie-chart-line",
            "iconBg": "bg-blue-100",
            "iconColor": "#3b82f6"
        },
        {
            "id": "goals",
            "title": "Goals",
            "description": "Track your financial goals",
            "icon": "ri-target-line",
            "iconBg": "bg-green-100",
            "iconColor": "#10b981"
        },
        {
            "id": "explore",
            "title": "Explore",
            "description": "Discover new activities",
            "icon": "ri-compass-line",
            "iconBg": "bg-purple-100",
            "iconColor": "#8b5cf6"
        },
        {
            "id": "shop",
            "title": "Shop",
            "description": "Convert coins to rewards",
            "icon": "ri-shopping-bag-line",
            "iconBg": "bg-yellow-100",
            "iconColor": "#f59e0b"
        }
    ]
    
    return {
        "teen": {
            "id": current_user.id,
            "name": current_user.name,
            "fullName": current_user.name,
            "email": current_user.email,
            "avatar": current_user.avatar_url,
            "coins": child_profile.coins,
            "level": child_profile.level,
            "streak_days": child_profile.streak_days,
            "totalCoinsEarned": child_profile.coins,  # Simplified
            "goalsCompleted": len([g for g in active_goals if g.is_completed])
        },
        "budget_overview": {
            "total_coins": total_coins,
            "allocations": budget_allocations,
            "percentages": {
                "saving": 40,
                "spending": 35,
                "wants": 25
            }
        },
        "goals": categorized_goals,
        "activities": activities,
        "achievements": achievements,
        "quick_actions": quick_actions,
        "stats": {
            "total_goals": len(active_goals),
            "completed_activities": len([p for p in user_progress.values() if p.is_completed]),
            "streak_days": child_profile.streak_days,
            "level": child_profile.level
        }
    }

@router.get("/budget", response_model=dict)
async def get_teen_budget(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get teen's budget allocation and management data."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can access budget management"
        )
    
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Get recent transactions by category
    transactions_stmt = select(Transaction).where(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(20)
    transactions_result = await session.execute(transactions_stmt)
    transactions = transactions_result.scalars().all()
    
    # Calculate budget allocations
    total_coins = child_profile.coins
    budget_allocations = {
        "saving": int(total_coins * 0.4),
        "spending": int(total_coins * 0.35),
        "wants": int(total_coins * 0.25)
    }
    
    # Categorize transactions
    categorized_transactions = {
        "saving": [],
        "spending": [],
        "wants": []
    }
    
    for transaction in transactions:
        category = transaction.category if transaction.category else 'spending'
        if category not in categorized_transactions:
            category = 'spending'
        
        categorized_transactions[category].append({
            "id": transaction.id,
            "type": transaction.type,
            "amount": transaction.amount,
            "description": transaction.description,
            "timestamp": transaction.created_at.isoformat(),
            "category": category
        })
    
    return {
        "budget_allocations": budget_allocations,
        "percentages": {
            "saving": 40,
            "spending": 35,
            "wants": 25
        },
        "total_coins": total_coins,
        "transactions": categorized_transactions,
        "history": [
            {
                "date": "2024-01-15",
                "saving": 40,
                "spending": 35,
                "wants": 25
            },
            {
                "date": "2024-01-08",
                "saving": 45,
                "spending": 30,
                "wants": 25
            }
        ]
    }

@router.put("/budget", response_model=dict)
async def update_teen_budget(
    budget_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update teen's budget allocation."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can update budget"
        )
    
    # Validate budget percentages
    saving = budget_data.get('saving', 40)
    spending = budget_data.get('spending', 35)
    wants = budget_data.get('wants', 25)
    
    total = saving + spending + wants
    if total != 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget percentages must total 100%"
        )
    
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Update budget allocations (in a real app, you'd store this in a separate table)
    total_coins = child_profile.coins
    new_allocations = {
        "saving": int(total_coins * (saving / 100)),
        "spending": int(total_coins * (spending / 100)),
        "wants": int(total_coins * (wants / 100))
    }
    
    print(f"✅ [BACKEND] Updated teen budget: {saving}% saving, {spending}% spending, {wants}% wants")
    
    return {
        "message": "Budget updated successfully",
        "budget_allocations": new_allocations,
        "percentages": {
            "saving": saving,
            "spending": spending,
            "wants": wants
        }
    }

@router.get("/goals", response_model=List[dict])
async def get_teen_goals(
    category: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get teen's goals with advanced filtering."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can access goals"
        )
    
    # Build query
    query = select(Goal).where(Goal.user_id == current_user.id)
    
    if status == "active":
        query = query.where(Goal.is_completed == False)
    elif status == "completed":
        query = query.where(Goal.is_completed == True)
    
    if category:
        query = query.where(Goal.category == category)
    
    query = query.order_by(Goal.created_at.desc())
    
    goals_result = await session.execute(query)
    goals = goals_result.scalars().all()
    
    goals_data = []
    for goal in goals:
        progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
        days_remaining = None
        if goal.deadline:
            days_remaining = (goal.deadline - datetime.utcnow()).days
        
        goals_data.append({
            "id": goal.id,
            "title": goal.title,
            "description": goal.description,
            "targetAmount": goal.target_amount,
            "currentAmount": goal.current_amount,
            "icon": goal.icon,
            "category": getattr(goal, 'category', 'saving'),
            "deadline": goal.deadline.isoformat() if goal.deadline else None,
            "daysRemaining": days_remaining,
            "progress_percentage": round(progress_percentage, 1),
            "is_completed": goal.is_completed,
            "createdAt": goal.created_at.isoformat()
        })
    
    return goals_data

@router.post("/goals", response_model=dict)
async def create_teen_goal(
    goal_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new goal for the teen with advanced features."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can create goals"
        )
    
    # Validate category
    category = goal_data.get('category', 'saving')
    if category not in ['saving', 'spending', 'wants']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category. Must be 'saving', 'spending', or 'wants'"
        )
    
    # Create goal
    new_goal = Goal(
        user_id=current_user.id,
        title=goal_data['title'],
        description=goal_data.get('description', goal_data['title']),
        target_amount=goal_data['targetAmount'],
        current_amount=goal_data.get('currentAmount', 0),
        icon=goal_data.get('icon', 'ri-target-line'),
        color=goal_data.get('color', 'blue'),
        is_completed=False
    )
    
    # Add category attribute (you might need to add this to your Goal model)
    # new_goal.category = category
    
    # Add deadline if provided
    if goal_data.get('deadline'):
        new_goal.deadline = datetime.fromisoformat(goal_data['deadline'].replace('Z', '+00:00'))
    
    session.add(new_goal)
    await session.commit()
    
    print(f"✅ [BACKEND] Created teen goal: {new_goal.title} (Category: {category})")
    
    return {
        "message": "Goal created successfully",
        "goal": {
            "id": new_goal.id,
            "title": new_goal.title,
            "description": new_goal.description,
            "targetAmount": new_goal.target_amount,
            "currentAmount": new_goal.current_amount,
            "icon": new_goal.icon,
            "category": category,
            "deadline": new_goal.deadline.isoformat() if new_goal.deadline else None,
            "createdAt": new_goal.created_at.isoformat()
        }
    }

@router.get("/explore", response_model=List[dict])
async def get_teen_activities(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    duration: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get advanced activities for teens with filtering and search."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can access explore activities"
        )
    
    # Build query
    query = select(Module).where(Module.is_published == True)
    
    if category:
        query = query.where(Module.category == category)
    
    if difficulty:
        query = query.where(Module.difficulty == difficulty)
    
    if duration:
        if duration == "short":
            query = query.where(Module.estimated_duration < 15)
        elif duration == "medium":
            query = query.where(and_(Module.estimated_duration >= 15, Module.estimated_duration <= 30))
        elif duration == "long":
            query = query.where(Module.estimated_duration > 30)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Module.title.ilike(search_term),
                Module.description.ilike(search_term)
            )
        )
    
    query = query.order_by(Module.difficulty, Module.title)
    
    modules_result = await session.execute(query)
    modules = modules_result.scalars().all()
    
    # Get user's progress
    progress_stmt = select(UserModuleProgress).where(
        UserModuleProgress.user_id == current_user.id
    )
    progress_result = await session.execute(progress_stmt)
    user_progress = {p.module_id: p for p in progress_result.scalars().all()}
    
    activities = []
    for module in modules:
        progress = user_progress.get(module.id)
        completed = progress.is_completed if progress else False
        
        activities.append({
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "category": module.category,
            "difficulty": module.difficulty,
            "duration": module.estimated_duration,
            "coins": module.points_reward,
            "completed": completed,
            "rating": 4.5,  # Mock rating
            "likes": 42,    # Mock likes
            "bookmarked": False,
            "tags": [module.category, module.difficulty],
            "thumbnail": f"https://picsum.photos/300/200?random={module.id}"
        })
    
    return activities

@router.post("/conversion-requests", response_model=dict)
async def create_conversion_request(
    request_data: dict,
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a coin-to-money conversion request."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can create conversion requests"
        )
    
    # Get child profile
    child_stmt = select(ChildProfile).where(ChildProfile.user_id == current_user.id)
    child_result = await session.execute(child_stmt)
    child_profile = child_result.scalar_one_or_none()
    
    if not child_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    coin_amount = request_data.get('coinAmount', 0)
    dollar_amount = request_data.get('dollarAmount', 0)
    reason = request_data.get('reason', '')
    
    # Validate amounts
    if coin_amount <= 0 or dollar_amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid amounts"
        )
    
    # Check if child has enough coins
    if coin_amount > child_profile.coins:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient coins"
        )
    
    # Create redemption request
    redemption_request = RedemptionRequest(
        user_id=current_user.id,
        item_name=f"Coin Conversion: {coin_amount} coins",
        coins_cost=coin_amount,
        status='pending',
        description=reason
    )
    
    session.add(redemption_request)
    await session.commit()
    
    print(f"✅ [BACKEND] Created conversion request: {coin_amount} coins for ${dollar_amount}")
    
    return {
        "message": "Conversion request created successfully",
        "request": {
            "id": redemption_request.id,
            "coinAmount": coin_amount,
            "dollarAmount": dollar_amount,
            "reason": reason,
            "status": "pending",
            "requestDate": redemption_request.created_at.isoformat()
        }
    }

@router.get("/conversion-requests", response_model=List[dict])
async def get_conversion_requests(
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get teen's conversion request history."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can view conversion requests"
        )
    
    # Get redemption requests
    requests_stmt = select(RedemptionRequest).where(
        RedemptionRequest.user_id == current_user.id
    ).order_by(RedemptionRequest.created_at.desc())
    
    requests_result = await session.execute(requests_stmt)
    requests = requests_result.scalars().all()
    
    requests_data = []
    for request in requests:
        requests_data.append({
            "id": request.id,
            "coinAmount": request.coins_cost,
            "dollarAmount": request.coins_cost * 0.01,  # Mock conversion rate
            "reason": request.description or "Coin conversion",
            "status": request.status,
            "requestDate": request.created_at.isoformat(),
            "responseDate": request.updated_at.isoformat() if request.status != 'pending' else None
        })
    
    return requests_data

@router.get("/analytics", response_model=dict)
async def get_teen_analytics(
    timeframe: str = "month",
    current_user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get comprehensive analytics for teen's financial behavior."""
    
    if current_user.role != 'older_child':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only older children can view analytics"
        )
    
    # Calculate timeframe
    now = datetime.utcnow()
    if timeframe == "week":
        start_date = now - timedelta(days=7)
    elif timeframe == "month":
        start_date = now - timedelta(days=30)
    elif timeframe == "quarter":
        start_date = now - timedelta(days=90)
    else:  # year
        start_date = now - timedelta(days=365)
    
    # Get transactions in timeframe
    transactions_stmt = select(Transaction).where(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.created_at >= start_date
        )
    )
    transactions_result = await session.execute(transactions_stmt)
    transactions = transactions_result.scalars().all()
    
    # Calculate analytics
    total_earned = sum(t.amount for t in transactions if t.type == 'earn')
    total_spent = sum(t.amount for t in transactions if t.type == 'spend')
    total_saved = sum(t.amount for t in transactions if t.type == 'save')
    
    # Get goals analytics
    goals_stmt = select(Goal).where(Goal.user_id == current_user.id)
    goals_result = await session.execute(goals_stmt)
    goals = goals_result.scalars().all()
    
    active_goals = [g for g in goals if not g.is_completed]
    completed_goals = [g for g in goals if g.is_completed]
    
    # Get activities analytics
    progress_stmt = select(UserModuleProgress).where(
        and_(
            UserModuleProgress.user_id == current_user.id,
            UserModuleProgress.completed_at >= start_date
        )
    )
    progress_result = await session.execute(progress_stmt)
    completed_activities = progress_result.scalars().all()
    
    return {
        "timeframe": timeframe,
        "financial_summary": {
            "total_earned": total_earned,
            "total_spent": total_spent,
            "total_saved": total_saved,
            "net_change": total_earned - total_spent - total_saved
        },
        "goals_analytics": {
            "active_goals": len(active_goals),
            "completed_goals": len(completed_goals),
            "completion_rate": len(completed_goals) / len(goals) * 100 if goals else 0
        },
        "activities_analytics": {
            "completed_activities": len(completed_activities),
            "total_coins_earned": sum(p.score or 0 for p in completed_activities)
        },
        "spending_patterns": {
            "by_category": {
                "saving": total_saved,
                "spending": total_spent,
                "wants": 0  # Would need to track this separately
            }
        }
    } 