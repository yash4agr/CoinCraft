"""Seed initial data for CoinCraft application."""

import asyncio
from datetime import datetime, timedelta

from database import create_db_and_tables, get_async_session
from models import (
    User, ChildProfile, ParentProfile, TeacherProfile, Goal, Transaction,
    Achievement, Module, ShopItem
)
from auth import get_user_db, get_user_manager
from schemas import UserCreate
from fastapi_users import exceptions


async def seed_data():
    """Seed initial data for development."""
    print("Creating database tables...")
    await create_db_and_tables()
    
    async for session in get_async_session():
        try:
            print("Seeding initial data...")
            
            # Get user manager
            user_db = await get_user_db(session).__anext__()
            user_manager = await get_user_manager(user_db).__anext__()
            
            # Create demo users
            
            # 1. Parent user
            try:
                parent_user = await user_manager.create(UserCreate(
                    email="parent@demo.com",
                    password="demo123",
                    name="Sarah Johnson",
                    role="parent",
                    avatar_url="👩‍💼"
                ))
                print("✅ Created parent user")
            except exceptions.UserAlreadyExists:
                print("ℹ️  Parent user already exists, skipping...")
                parent_user = await user_manager.get_by_email("parent@demo.com")
            
            # Create parent profile
            parent_profile = ParentProfile(
                user_id=parent_user.id,
                exchange_rate=0.10,
                auto_approval_limit=50,
                require_approval=True
            )
            session.add(parent_profile)
            
            # 2. Teacher user
            try:
                teacher_user = await user_manager.create(UserCreate(
                    email="teacher@demo.com",
                    password="demo123",
                    name="Mrs. Wilson",
                    role="teacher",
                    avatar_url="👩‍🏫"
                ))
                print("✅ Created teacher user")
            except exceptions.UserAlreadyExists:
                print("ℹ️  Teacher user already exists, skipping...")
                teacher_user = await user_manager.get_by_email("teacher@demo.com")
            
            # Create teacher profile
            teacher_profile = TeacherProfile(
                user_id=teacher_user.id,
                school_name="Financial Literacy Academy",
                grade_level="4-6",
                subject="Financial Education"
            )
            session.add(teacher_profile)
            
            # 3. Younger child user
            try:
                child1_user = await user_manager.create(UserCreate(
                    email="luna@demo.com",
                    password="demo123",
                    name="Luna Smith",
                    role="younger_child",
                    avatar_url="🦸‍♀️"
                ))
                print("✅ Created younger child user")
            except exceptions.UserAlreadyExists:
                print("ℹ️  Younger child user already exists, skipping...")
                child1_user = await user_manager.get_by_email("luna@demo.com")
            
            # Create child profile
            child1_profile = ChildProfile(
                user_id=child1_user.id,
                age=9,
                coins=135,
                level=3,
                streak_days=7,
                parent_id=parent_user.id,
                last_activity_date=datetime.utcnow()
            )
            session.add(child1_profile)
            
            # 4. Older child user
            try:
                child2_user = await user_manager.create(UserCreate(
                    email="harry@demo.com",
                    password="demo123",
                    name="Harry Johnson",
                    role="older_child",
                    avatar_url="🧙‍♂️"
                ))
                print("✅ Created older child user")
            except exceptions.UserAlreadyExists:
                print("ℹ️  Older child user already exists, skipping...")
                child2_user = await user_manager.get_by_email("harry@demo.com")
            
            # Create child profile
            child2_profile = ChildProfile(
                user_id=child2_user.id,
                age=14,
                coins=245,
                level=5,
                streak_days=12,
                parent_id=parent_user.id,
                last_activity_date=datetime.utcnow()
            )
            session.add(child2_profile)
            
            # Create some goals
            goals_data = [
                {
                    "user_id": child1_user.id,
                    "title": "New Bike",
                    "description": "Save for a cool new bicycle",
                    "target_amount": 100,
                    "current_amount": 35,
                    "icon": "ri-bike-line",
                    "color": "blue"
                },
                {
                    "user_id": child1_user.id,
                    "title": "Video Game",
                    "description": "New adventure game",
                    "target_amount": 60,
                    "current_amount": 10,
                    "icon": "ri-gamepad-line",
                    "color": "green"
                },
                {
                    "user_id": child2_user.id,
                    "title": "Laptop",
                    "description": "Save for a laptop for school",
                    "target_amount": 500,
                    "current_amount": 120,
                    "icon": "ri-computer-line",
                    "color": "purple"
                }
            ]
            
            for goal_data in goals_data:
                goal = Goal(**goal_data)
                session.add(goal)
            
            # Create some achievements
            achievements_data = [
                {
                    "title": "First Steps",
                    "description": "Completed your first lesson!",
                    "icon": "ri-foot-print-line",
                    "rarity": "common",
                    "points_reward": 10
                },
                {
                    "title": "Coin Collector",
                    "description": "Earned your first 50 coins",
                    "icon": "ri-coins-line",
                    "rarity": "uncommon",
                    "points_reward": 20
                },
                {
                    "title": "Smart Saver",
                    "description": "Saved money for 7 days straight",
                    "icon": "ri-save-line",
                    "rarity": "rare",
                    "points_reward": 50
                }
            ]
            
            for achievement_data in achievements_data:
                achievement = Achievement(**achievement_data)
                session.add(achievement)
            
            # Create some learning modules
            modules_data = [
                {
                    "title": "Money Basics",
                    "description": "Learn about different types of money and how to count them.",
                    "category": "Financial Literacy",
                    "difficulty": "easy",
                    "estimated_duration": 15,
                    "points_reward": 20,
                    "created_by": teacher_user.id,
                    "is_published": True
                },
                {
                    "title": "Saving Goals",
                    "description": "Set and achieve your first savings goal.",
                    "category": "Financial Literacy",
                    "difficulty": "easy",
                    "estimated_duration": 20,
                    "points_reward": 25,
                    "created_by": teacher_user.id,
                    "is_published": True
                },
                {
                    "title": "Smart Spending",
                    "description": "Learn how to make smart choices when spending money.",
                    "category": "Financial Literacy",
                    "difficulty": "medium",
                    "estimated_duration": 25,
                    "points_reward": 30,
                    "created_by": teacher_user.id,
                    "is_published": True
                },
                {
                    "title": "Investment Basics",
                    "description": "Learn the basics of investing and growing your money.",
                    "category": "Investing",
                    "difficulty": "hard",
                    "estimated_duration": 35,
                    "points_reward": 40,
                    "created_by": teacher_user.id,
                    "is_published": True
                }
            ]
            
            for module_data in modules_data:
                module = Module(**module_data)
                session.add(module)
            
            # Create some transactions
            transactions_data = [
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 15,
                    "description": "Completed Money Basics module",
                    "category": "learning",
                    "source": "module_completion"
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 10,
                    "description": "Daily streak bonus",
                    "category": "bonus",
                    "source": "streak"
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 20,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution"
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 25,
                    "description": "Completed Investment Basics",
                    "category": "learning",
                    "source": "module_completion"
                }
            ]
            
            for transaction_data in transactions_data:
                transaction = Transaction(**transaction_data)
                session.add(transaction)
            
            # Create some shop items
            shop_items_data = [
                {
                    "name": "Star Sticker",
                    "description": "Shiny gold star for your collection",
                    "price": 5,
                    "category": "stickers",
                    "emoji": "⭐",
                    "available": True
                },
                {
                    "name": "Rainbow Badge",
                    "description": "Beautiful rainbow achievement badge",
                    "price": 15,
                    "category": "badges",
                    "emoji": "🌈",
                    "available": True
                },
                {
                    "name": "Virtual Pet",
                    "description": "Adopt a cute virtual pet",
                    "price": 50,
                    "category": "pets",
                    "emoji": "🐱",
                    "available": True
                },
                {
                    "name": "Magic Wand",
                    "description": "Magical wand for special effects",
                    "price": 30,
                    "category": "tools",
                    "emoji": "🪄",
                    "available": True
                }
            ]
            
            for item_data in shop_items_data:
                shop_item = ShopItem(**item_data)
                session.add(shop_item)
            
            await session.commit()
            print("✅ Data seeding completed successfully!")
            
            print("\n🔑 Demo Login Credentials:")
            print("Parent: parent@demo.com / demo123")
            print("Teacher: teacher@demo.com / demo123") 
            print("Child (9y): luna@demo.com / demo123")
            print("Teen (14y): harry@demo.com / demo123")
            
        except Exception as e:
            print(f"❌ Error seeding data: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(seed_data()) 