"""Database models for CoinCraft application."""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
import uuid

Base = declarative_base()


class UserRoleEnum(str, PyEnum):
    PARENT = "parent"
    TEACHER = "teacher"
    YOUNGER_CHILD = "younger_child"
    OLDER_CHILD = "older_child"


class User(SQLAlchemyBaseUserTable[str], Base):
    """User model with role-based functionality."""
    
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # UserRoleEnum values
    avatar_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Role-specific relationships
    child_profile = relationship("ChildProfile", back_populates="user", uselist=False, primaryjoin="User.id == ChildProfile.user_id")
    parent_profile = relationship("ParentProfile", back_populates="user", uselist=False)
    teacher_profile = relationship("TeacherProfile", back_populates="user", uselist=False)
    
    # Activity relationships
    goals = relationship("Goal", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    tasks_assigned = relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee")
    tasks_created = relationship("Task", foreign_keys="Task.assigned_by", back_populates="assigner")
    redemption_requests = relationship("RedemptionRequest", back_populates="user", primaryjoin="User.id == RedemptionRequest.user_id")


class ChildProfile(Base):
    """Child-specific profile data."""
    
    __tablename__ = "child_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    age = Column(Integer, nullable=False)
    coins = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    parent_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    user = relationship("User", back_populates="child_profile", primaryjoin="ChildProfile.user_id == User.id")
    parent = relationship("User", primaryjoin="ChildProfile.parent_id == User.id")


class ParentProfile(Base):
    """Parent-specific profile data."""
    
    __tablename__ = "parent_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    exchange_rate = Column(Float, default=0.10)  # dollars per coin
    auto_approval_limit = Column(Integer, default=500)  # auto-approve under this amount
    require_approval = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="parent_profile")


class TeacherProfile(Base):
    """Teacher-specific profile data."""
    
    __tablename__ = "teacher_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    school_name = Column(String(200), nullable=True)
    grade_level = Column(String(50), nullable=True)
    subject = Column(String(100), nullable=True)
    
    user = relationship("User", back_populates="teacher_profile")
    classes = relationship("Class", back_populates="teacher")


class Goal(Base):
    """Financial goals set by users."""
    
    __tablename__ = "goals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_amount = Column(Integer, nullable=False)
    current_amount = Column(Integer, default=0)
    icon = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    deadline = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="goals")


class Transaction(Base):
    """Financial transactions (earn, spend, save)."""
    
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String(20), nullable=False)  # earn, spend, save
    amount = Column(Integer, nullable=False)
    description = Column(String(500), nullable=False)
    category = Column(String(100), nullable=True)
    source = Column(String(200), nullable=True)
    reference_id = Column(String, nullable=True)  # ID of related goal, task, etc.
    reference_type = Column(String(50), nullable=True)  # goal, task, activity, shop, redemption
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")


class Achievement(Base):
    """Available achievements in the system."""
    
    __tablename__ = "achievements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=True)
    rarity = Column(String(50), default="common")  # common, uncommon, rare, epic, legendary
    points_reward = Column(Integer, default=0)
    criteria = Column(JSON, nullable=True)  # JSON object defining achievement criteria
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """User's earned achievements."""
    
    __tablename__ = "user_achievements"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    achievement_id = Column(String, ForeignKey("achievements.id"))
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class Module(Base):
    """Learning modules created by teachers."""
    
    __tablename__ = "modules"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    difficulty = Column(String(20), default="easy")  # easy, medium, hard
    estimated_duration = Column(Integer, nullable=True)  # minutes
    points_reward = Column(Integer, default=0)
    created_by = Column(String, ForeignKey("users.id"))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sections = relationship("ModuleSection", back_populates="module")
    user_progress = relationship("UserModuleProgress", back_populates="module")


class ModuleSection(Base):
    """Sections within a learning module."""
    
    __tablename__ = "module_sections"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("modules.id"))
    title = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)  # lesson, quiz, game
    content = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    points_reward = Column(Integer, default=0)
    
    module = relationship("Module", back_populates="sections")
    quiz_questions = relationship("QuizQuestion", back_populates="section")


class QuizQuestion(Base):
    """Quiz questions within module sections."""
    
    __tablename__ = "quiz_questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    section_id = Column(String, ForeignKey("module_sections.id"))
    question_text = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1)
    order_index = Column(Integer, nullable=False)
    
    section = relationship("ModuleSection", back_populates="quiz_questions")
    options = relationship("QuizOption", back_populates="question")


class QuizOption(Base):
    """Options for quiz questions."""
    
    __tablename__ = "quiz_options"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String, ForeignKey("quiz_questions.id"))
    option_text = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)
    order_index = Column(Integer, nullable=False)
    
    question = relationship("QuizQuestion", back_populates="options")


class UserModuleProgress(Base):
    """User progress through learning modules."""
    
    __tablename__ = "user_module_progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    module_id = Column(String, ForeignKey("modules.id"))
    progress_percentage = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    score = Column(Float, nullable=True)
    time_spent = Column(Integer, default=0)  # minutes
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User")
    module = relationship("Module", back_populates="user_progress")


class Task(Base):
    """Tasks assigned by parents to children."""
    
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    assigned_by = Column(String, ForeignKey("users.id"))
    assigned_to = Column(String, ForeignKey("users.id"))
    coins_reward = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, approved, rejected
    requires_approval = Column(Boolean, default=True)
    completed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assigner = relationship("User", foreign_keys=[assigned_by], back_populates="tasks_created")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="tasks_assigned")


class Class(Base):
    """Teacher's classes."""
    
    __tablename__ = "classes"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    teacher_id = Column(String, ForeignKey("teacher_profiles.id"))
    description = Column(Text, nullable=True)
    class_code = Column(String(20), unique=True)  # for students to join
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    teacher = relationship("TeacherProfile", back_populates="classes")
    students = relationship("ClassStudent", back_populates="class_obj")


class ClassStudent(Base):
    """Students enrolled in classes."""
    
    __tablename__ = "class_students"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    class_id = Column(String, ForeignKey("classes.id"))
    student_id = Column(String, ForeignKey("users.id"))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    
    class_obj = relationship("Class", back_populates="students")
    student = relationship("User")


class RedemptionRequest(Base):
    """Requests to convert coins to real money."""
    
    __tablename__ = "redemption_requests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    coins_amount = Column(Integer, nullable=False)
    cash_amount = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="redemption_requests", primaryjoin="RedemptionRequest.user_id == User.id")
    approver = relationship("User", primaryjoin="RedemptionRequest.approved_by == User.id")


class PurchaseRequest(Base):
    """Requests by children to purchase shop items (requires parent approval)."""
    
    __tablename__ = "purchase_requests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    shop_item_id = Column(String, ForeignKey("shop_items.id"), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")  # pending, approved, rejected
    approved_by = Column(String, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", primaryjoin="PurchaseRequest.user_id == User.id")
    approver = relationship("User", primaryjoin="PurchaseRequest.approved_by == User.id")
    item = relationship("ShopItem")

class BudgetCategory(Base):
    """Budget categories for teen users."""
    
    __tablename__ = "budget_categories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    budget_amount = Column(Integer, nullable=False)
    spent_amount = Column(Integer, default=0)
    icon = Column(String(100), nullable=True)
    color = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")

class UserOwnedItem(Base):
    __tablename__ = "user_owned_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    shop_item_id = Column(String, ForeignKey("shop_items.id", ondelete="CASCADE"), nullable=False)
    acquired_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to ShopItem
    shop_item = relationship("ShopItem", back_populates="owners")

class ShopItem(Base):
    """Virtual shop items."""
    
    __tablename__ = "shop_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)
    category = Column(String(100), nullable=True)
    emoji = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 
    owners = relationship("UserOwnedItem", back_populates="shop_item", cascade="all, delete")