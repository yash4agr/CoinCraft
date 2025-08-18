"""Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from fastapi_users import schemas


class UserRoleEnum(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    YOUNGER_CHILD = "younger_child"
    OLDER_CHILD = "older_child"


# User Schemas
class UserRead(schemas.BaseUser[str]):
    id: str
    name: str
    role: UserRoleEnum
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_superuser: bool
    is_verified: bool
class ChildSummaryRead(UserRead):
    age: Optional[int] = None



# Extended user schema with profile data (for endpoints that explicitly load profiles)
class UserWithProfilesRead(UserRead):
    # Role-specific profile data
    child_profile: Optional["ChildProfileRead"] = None
    parent_profile: Optional["ParentProfileRead"] = None
    teacher_profile: Optional["TeacherProfileRead"] = None


class UserCreate(schemas.BaseUserCreate):
    name: str
    role: UserRoleEnum
    avatar_url: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    name: Optional[str] = None
    avatar_url: Optional[str] = None


# Profile Schemas
class ChildProfileRead(BaseModel):
    """Child profile data for reading."""
    
    id: str
    user_id: str
    age: int
    coins: int
    level: int
    streak_days: int
    last_activity_date: Optional[datetime] = None
    parent_id: Optional[str] = None
    temporary_password: Optional[str] = None  # Include password for parent visibility

    class Config:
        from_attributes = True


class ChildProfileCreate(BaseModel):
    age: int = Field(..., ge=6, le=18)
    parent_id: Optional[str] = None


class ChildProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=6, le=18)
    coins: Optional[int] = None
    level: Optional[int] = None
    streak_days: Optional[int] = None
    last_activity_date: Optional[datetime] = None


class ParentProfileRead(BaseModel):
    id: str
    user_id: str
    exchange_rate: float = 0.10
    auto_approval_limit: int = 500
    require_approval: bool = True

    class Config:
        from_attributes = True


class ParentProfileUpdate(BaseModel):
    exchange_rate: Optional[float] = Field(None, ge=0.01, le=1.0)
    auto_approval_limit: Optional[int] = Field(None, ge=0)
    require_approval: Optional[bool] = None


class TeacherProfileRead(BaseModel):
    id: str
    user_id: str
    school_name: Optional[str] = None
    grade_level: Optional[str] = None
    subject: Optional[str] = None

    class Config:
        from_attributes = True


class TeacherProfileUpdate(BaseModel):
    school_name: Optional[str] = None
    grade_level: Optional[str] = None
    subject: Optional[str] = None


# Goal Schemas
class GoalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    target_amount: int = Field(..., gt=0)
    icon: Optional[str] = None
    color: Optional[str] = None
    deadline: Optional[datetime] = None


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    target_amount: Optional[int] = Field(None, gt=0)
    icon: Optional[str] = None
    color: Optional[str] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None


class GoalRead(GoalBase):
    id: str
    user_id: str
    current_amount: int = 0
    is_completed: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GoalContribution(BaseModel):
    amount: int = Field(..., gt=0)


# Transaction Schemas
class TransactionBase(BaseModel):
    type: str = Field(..., pattern="^(earn|spend|save)$")
    amount: int = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = None
    source: Optional[str] = None
    reference_id: Optional[str] = None
    reference_type: Optional[str] = Field(
        None, pattern="^(goal|task|activity|shop|redemption)$"
    )


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    transactions: List[TransactionRead]
    total_count: int
    weekly_total: int
    monthly_total: int


# Achievement Schemas
class AchievementRead(BaseModel):
    id: str
    title: str
    description: str
    icon: Optional[str] = None
    rarity: str = "common"
    points_reward: int = 0
    earned_at: Optional[datetime] = None  # Only populated for user achievements

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    coins_reward: int = Field(..., gt=0)
    due_date: Optional[datetime] = None
    requires_approval: bool = True


class TaskCreate(TaskBase):
    assigned_to: str


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    coins_reward: Optional[int] = Field(None, gt=0)
    due_date: Optional[datetime] = None
    requires_approval: Optional[bool] = None
    status: Optional[str] = Field(
        None, pattern="^(pending|in_progress|completed|approved|rejected)$"
    )


class TaskRead(TaskBase):
    id: str
    assigned_by: str
    assigned_to: str
    status: str = "pending"
    completed_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Module Schemas
class ModuleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str
    category: Optional[str] = None
    difficulty: str = Field("easy", pattern="^(easy|medium|hard)$")
    estimated_duration: Optional[int] = None
    points_reward: int = 0


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    estimated_duration: Optional[int] = None
    points_reward: Optional[int] = None
    is_published: Optional[bool] = None


class ModuleRead(ModuleBase):
    id: str
    created_by: str
    is_published: bool = False
    created_at: datetime
    updated_at: datetime
    user_progress: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ClassResponse(BaseModel):
    id: str
    name: str
    teacher_id: str
    student_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ModuleResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    difficulty: str
    points_reward: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Class Schemas
class ClassBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    age_group: str = Field(..., pattern="^(8-10|11-14)$")  # Only allow "8-10" or "11-14"


class ClassCreate(ClassBase):
    pass


class ClassUpdate(ClassBase):
    is_active: Optional[bool] = None


class ClassRead(ClassBase):
    id: str
    teacher_id: str
    class_code: str
    is_active: bool = True
    created_at: datetime
    students_count: Optional[int] = 0
    average_performance: Optional[float] = 0.0

    class Config:
        from_attributes = True


# Student Schema for class management
class StudentRead(BaseModel):
    user_id: str
    name: str
    email: str
    avatar_url: Optional[str] = None
    age: Optional[int] = None
    level: Optional[int] = None
    performance_score: Optional[float] = None
    needs_support: Optional[bool] = None
    last_activity_date: Optional[datetime] = None
    modules_completed: Optional[int] = None
    total_time_spent: Optional[int] = None
    progress: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Redemption Schemas
class RedemptionRequestBase(BaseModel):
    coins_amount: int = Field(..., gt=0)
    description: Optional[str] = None


class RedemptionRequestCreate(RedemptionRequestBase):
    pass


class RedemptionRequestRead(RedemptionRequestBase):
    id: str
    user_id: str
    cash_amount: float
    status: str = "pending"
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    # Child info for parent view
    child: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# Budget Schemas
class BudgetCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    budget_amount: int = Field(..., ge=0)
    icon: Optional[str] = None
    color: Optional[str] = None


class BudgetCategoryCreate(BudgetCategoryBase):
    pass


class BudgetCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    budget_amount: Optional[int] = Field(None, ge=0)
    spent_amount: Optional[int] = Field(None, ge=0)
    icon: Optional[str] = None
    color: Optional[str] = None


class BudgetCategoryRead(BudgetCategoryBase):
    id: str
    user_id: str
    spent_amount: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BudgetAllocation(BaseModel):
    saving: int = Field(..., ge=0, le=100)
    spending: int = Field(..., ge=0, le=100)
    wants: int = Field(..., ge=0, le=100)

    def validate_total(self):
        total = self.saving + self.spending + self.wants
        if total != 100:
            raise ValueError("Budget allocation percentages must sum to 100")
        return self


# Shop Schemas
class ShopItemRead(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: int
    category: Optional[str] = None
    emoji: Optional[str] = None
    available: bool = True

    class Config:
        from_attributes = True
class ShopItemRequest(BaseModel):
    item_id: str

class PurchaseRequestRead(BaseModel):
    id: str
    user_id: str
    shop_item_id: str
    price: int
    status: str = "pending"
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    item_info: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    total_coins: int
    level: int
    streak_days: int
    goals_count: int
    completed_tasks: int


class ParentDashboardResponse(BaseModel):
    user: UserRead
    stats: DashboardStats
    children: List[ChildSummaryRead]
    recent_transactions: List[TransactionRead]
    pending_redemptions: List[RedemptionRequestRead]

    class Config:
        from_attributes = True


class TeacherDashboardResponse(BaseModel):
    user: UserRead
    stats: Dict[str, Any]
    classes: List[Dict[str, Any]]
    recent_modules: List[Dict[str, Any]]
    student_progress: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class ChildDashboardResponse(BaseModel):
    user: UserRead
    stats: DashboardStats
    active_goals: List[GoalRead]
    pending_tasks: List[TaskRead]
    recent_transactions: List[TransactionRead]
    achievements: List[AchievementRead]

    class Config:
        from_attributes = True


# Legacy Dashboard Schema (keeping for backward compatibility)
class DashboardData(BaseModel):
    user_stats: Dict[str, Any]
    recent_transactions: List[TransactionRead]
    active_goals: List[GoalRead]
    achievements: List[AchievementRead]
    learning_modules: Optional[List[ModuleRead]] = None


class ProgressGoal(BaseModel):
    id: str
    title: str
    current: int
    total: int
    icon: str
    color_scheme: str


class ActivityRead(BaseModel):
    id: str
    title: str
    description: str
    type: str
    difficulty: str
    coins: int
    duration: int
    completed: bool
    icon: str
    category: str
    age_group: str

    class Config:
        from_attributes = True


# Auth Response Schema
class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

    class Config:
        from_attributes = True


# Legacy AuthResponse with refresh_token (keeping for compatibility)
class AuthResponseWithRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserRead

    class Config:
        from_attributes = True


# Error Schemas
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    status_code: int


class ValidationErrorResponse(BaseModel):
    detail: List[Dict[str, Any]]


# Parent-specific response models
class ChildCreateResponse(BaseModel):
    success: bool
    message: str
    child: UserRead
    # Returned only at creation time so parent can note credentials
    password: Optional[str] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True


class TaskCreateResponse(BaseModel):
    success: bool
    task: TaskRead
    message: str

    class Config:
        from_attributes = True


class TaskApprovalResponse(BaseModel):
    success: bool
    task: TaskRead
    coins_awarded: int
    message: str

    class Config:
        from_attributes = True


class ChildProgressResponse(BaseModel):
    child: UserRead
    stats: DashboardStats
    goals: List[GoalRead]
    recent_activities: List[ActivityRead]
    achievements: List[AchievementRead]

    class Config:
        from_attributes = True


class ParentSettingsResponse(BaseModel):
    success: bool
    message: str
    settings: Dict[str, Any]

    class Config:
        from_attributes = True


# Update forward references
UserRead.model_rebuild()
ChildProfileRead.model_rebuild()
ParentProfileRead.model_rebuild()
TeacherProfileRead.model_rebuild()
