"""Seed initial data for CoinCraft application."""

import asyncio
from datetime import datetime, timedelta, timezone

from database import create_db_and_tables, get_async_session, engine
from models import (
    User, ChildProfile, ParentProfile, TeacherProfile, Goal, Transaction,
    Achievement, Module, ShopItem, UserOwnedItem, Activity, UserActivity, TeenShopItem
)
from sqlalchemy import delete, select
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
                    email="sarah@demo.com",
                    password="demo123",
                    name="Sarah Johnson",
                    role="parent",
                    avatar_url="👩‍💼"
                ))
                print("Created parent user")
            except exceptions.UserAlreadyExists:
                print("Parent user already exists, skipping...")
                parent_user = await user_manager.get_by_email("sarah@demo.com")
            
            # Create parent profile if it doesn't exist
            existing_profile_stmt = select(ParentProfile).where(ParentProfile.user_id == parent_user.id)
            existing_profile_result = await session.execute(existing_profile_stmt)
            existing_parent_profile = existing_profile_result.scalar_one_or_none()
            
            if not existing_parent_profile:
                parent_profile = ParentProfile(
                    user_id=parent_user.id,
                    exchange_rate=0.10,
                    auto_approval_limit=50,
                    require_approval=True
                )
                session.add(parent_profile)
                print("Created parent profile")
            else:
                print("Parent profile already exists, skipping...")
            
            # 2. Teacher user
            try:
                teacher_user = await user_manager.create(UserCreate(
                    email="teacher@demo.com",
                    password="demo123",
                    name="Mrs. Wilson",
                    role="teacher",
                    avatar_url="👩‍🏫"
                ))
                print("Created teacher user")
            except exceptions.UserAlreadyExists:
                print("Teacher user already exists, skipping...")
                teacher_user = await user_manager.get_by_email("teacher@demo.com")
            
            # Create teacher profile if it doesn't exist
            existing_teacher_stmt = select(TeacherProfile).where(TeacherProfile.user_id == teacher_user.id)
            existing_teacher_result = await session.execute(existing_teacher_stmt)
            existing_teacher_profile = existing_teacher_result.scalar_one_or_none()
            
            if not existing_teacher_profile:
                teacher_profile = TeacherProfile(
                    user_id=teacher_user.id,
                    school_name="Financial Literacy Academy",
                    grade_level="4-6",
                    subject="Financial Education"
                )
                session.add(teacher_profile)
                print("Created teacher profile")
            else:
                print("Teacher profile already exists, skipping...")
            
            # 3. Younger child user
            try:
                child1_user = await user_manager.create(UserCreate(
                    email="luna@demo.com",
                    password="demo123",
                    name="Luna Smith",
                    role="younger_child",
                    avatar_url="🦸‍♀️"
                ))
                print("Created younger child user")
            except exceptions.UserAlreadyExists:
                print("Younger child user already exists, skipping...")
                child1_user = await user_manager.get_by_email("luna@demo.com")
            
            # Create child profile if it doesn't exist
            existing_child1_stmt = select(ChildProfile).where(ChildProfile.user_id == child1_user.id)
            existing_child1_result = await session.execute(existing_child1_stmt)
            existing_child1_profile = existing_child1_result.scalar_one_or_none()
            
            if not existing_child1_profile:
                child1_profile = ChildProfile(
                    user_id=child1_user.id,
                    age=9,
                    coins=135,
                    level=3,
                    streak_days=7,
                    parent_id=parent_user.id,
                    last_activity_date=datetime.now(timezone.utc)
                )
                session.add(child1_profile)
                print("Created child1 profile (Luna)")
            else:
                print("ℹChild1 profile (Luna) already exists, skipping...")
            
            # 4. Older child user
            try:
                child2_user = await user_manager.create(UserCreate(
                    email="harry@demo.com",
                    password="demo123",
                    name="Harry Johnson",
                    role="older_child",
                    avatar_url="🧙‍♂️"
                ))
                print("Created older child user")
            except exceptions.UserAlreadyExists:
                print("Older child user already exists, skipping...")
                child2_user = await user_manager.get_by_email("harry@demo.com")
            
            # Create child profile if it doesn't exist
            existing_child2_stmt = select(ChildProfile).where(ChildProfile.user_id == child2_user.id)
            existing_child2_result = await session.execute(existing_child2_stmt)
            existing_child2_profile = existing_child2_result.scalar_one_or_none()
            
            if not existing_child2_profile:
                child2_profile = ChildProfile(
                    user_id=child2_user.id,
                    age=14,
                    coins=245,
                    level=5,
                    streak_days=12,
                    parent_id=parent_user.id,
                    last_activity_date=datetime.now(timezone.utc)
                )
                session.add(child2_profile)
                print("Created child2 profile (Harry)")
            else:
                print("Child2 profile (Harry) already exists, skipping...")
            
            await session.execute(delete(Goal))
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
            
            await session.execute(delete(Achievement))
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
            
            await session.execute(delete(Module))
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
            
            await session.execute(delete(Transaction))
            # Create some transactions
            transactions_data = [
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 15,
                    "description": "Completed Money Basics module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-08-01T10:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 10,
                    "description": "Daily streak bonus",
                    "category": "bonus",
                    "source": "streak",
                    "created_at": datetime.fromisoformat("2025-08-02T08:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 20,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-08-03T12:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 25,
                    "description": "Completed Investment Basics",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-08-10T14:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 12,
                    "description": "Completed Saving Goals module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-07-01T09:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "save",
                    "amount": 30,
                    "description": "Saved for laptop",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-02T11:30:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "spend",
                    "amount": 8,
                    "description": "Bought Animal Stickers",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-03T15:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 18,
                    "description": "Daily streak bonus",
                    "category": "bonus",
                    "source": "streak",
                    "created_at": datetime.fromisoformat("2025-07-04T08:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 20,
                    "description": "Completed Smart Spending module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-07-06T13:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "spend",
                    "amount": 20,
                    "description": "Bought Toy Car",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-07T16:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 15,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-09T12:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 22,
                    "description": "Completed Money Basics module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-07-10T10:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "spend",
                    "amount": 10,
                    "description": "Bought Rainbow Stickers",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-12T17:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "save",
                    "amount": 40,
                    "description": "Saved for laptop",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-13T11:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 14,
                    "description": "Daily streak bonus",
                    "category": "bonus",
                    "source": "streak",
                    "created_at": datetime.fromisoformat("2025-07-15T08:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "spend",
                    "amount": 30,
                    "description": "Bought Teddy Bear",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-16T18:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 25,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-18T12:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 16,
                    "description": "Completed Smart Spending module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-07-19T13:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "spend",
                    "amount": 6,
                    "description": "Bought Heart Stickers",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-21T15:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "save",
                    "amount": 35,
                    "description": "Saved for laptop",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-22T11:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 18,
                    "description": "Completed Investment Basics",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-07-24T14:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "spend",
                    "amount": 15,
                    "description": "Bought Bouncy Ball",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-25T16:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 10,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-07-27T12:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 20,
                    "description": "Daily streak bonus",
                    "category": "bonus",
                    "source": "streak",
                    "created_at": datetime.fromisoformat("2025-07-28T08:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "spend",
                    "amount": 12,
                    "description": "Bought Crayons",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-07-30T17:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "save",
                    "amount": 50,
                    "description": "Saved for laptop",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-08-04T11:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "earn",
                    "amount": 16,
                    "description": "Completed Saving Goals module",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-08-05T09:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "spend",
                    "amount": 18,
                    "description": "Bought Comic Book",
                    "category": "shop",
                    "source": "shop_purchase",
                    "created_at": datetime.fromisoformat("2025-08-07T18:00:00Z")
                },
                {
                    "user_id": child1_user.id,
                    "type": "save",
                    "amount": 30,
                    "description": "Added to bike fund",
                    "category": "goal",
                    "source": "goal_contribution",
                    "created_at": datetime.fromisoformat("2025-08-09T12:00:00Z")
                },
                {
                    "user_id": child2_user.id,
                    "type": "earn",
                    "amount": 24,
                    "description": "Completed Investment Basics",
                    "category": "learning",
                    "source": "module_completion",
                    "created_at": datetime.fromisoformat("2025-08-11T14:00:00Z")
                }
            ]
            
            for transaction_data in transactions_data:
                transaction = Transaction(**transaction_data)
                session.add(transaction)
            
            await session.execute(delete(ShopItem))
    
    # Insert fresh catalog
            shop_items_data = [
                # Stickers
                {"name": "Star Stickers", "description": "Shiny gold stars!", "price": 5, "category": "stickers", "emoji": "⭐"},
                {"name": "Animal Stickers", "description": "Cute animal friends", "price": 8, "category": "stickers", "emoji": "🐱"},
                {"name": "Rainbow Stickers", "description": "Colorful rainbows", "price": 10, "category": "stickers", "emoji": "🌈"},
                {"name": "Heart Stickers", "description": "Pretty pink hearts", "price": 6, "category": "stickers", "emoji": "💖"},

                # Toys
                {"name": "Magic Wand", "description": "Cast magical spells!", "price": 25, "category": "toys", "emoji": "🪄"},
                {"name": "Toy Car", "description": "Zoom zoom race car", "price": 20, "category": "toys", "emoji": "🚗"},
                {"name": "Teddy Bear", "description": "Soft cuddly friend", "price": 30, "category": "toys", "emoji": "🧸"},
                {"name": "Bouncy Ball", "description": "Super bouncy fun!", "price": 15, "category": "toys", "emoji": "⚽"},

                # Art Supplies
                {"name": "Crayons", "description": "Colorful drawing fun", "price": 12, "category": "art", "emoji": "🖍️"},
                {"name": "Paint Set", "description": "Make beautiful art", "price": 18, "category": "art", "emoji": "🎨"},
                {"name": "Sticker Book", "description": "Fill with stickers!", "price": 14, "category": "art", "emoji": "📖"},

                # Books
                {"name": "Adventure Book", "description": "Exciting stories!", "price": 22, "category": "books", "emoji": "📚"},
                {"name": "Puzzle Book", "description": "Fun brain games", "price": 16, "category": "books", "emoji": "🧩"},
                {"name": "Comic Book", "description": "Funny superhero stories", "price": 18, "category": "books", "emoji": "📖"}
            ]
            for item_data in shop_items_data:
                shop_item = ShopItem(**item_data)
                session.add(shop_item)
            
            await session.commit()

            # Create some owned shop items for child_1 and child_2
            await session.execute(delete(UserOwnedItem))
            owned_items_data = [
                # child_1 owns two items
                {
                    "user_id": child1_user.id,
                    "shop_item_id": "1",  # Star Stickers
                    "acquired_at": datetime.now(timezone.utc),
                },
                {
                    "user_id": child1_user.id,
                    "shop_item_id": "5",  # Magic Wand
                    "acquired_at": datetime.now(timezone.utc),
                },
                # child_2 owns one item
                {
                    "user_id": child2_user.id,
                    "shop_item_id": "2",  # Animal Stickers
                    "acquired_at": datetime.now(timezone.utc),
                },
            ]
            for owned_item in owned_items_data:
                session.add(UserOwnedItem(**owned_item))
            await session.commit()

            await session.commit()
            await session.execute(delete(TeenShopItem))
            teen_shop_items_data = [
                # Digital Rewards
                {"name": "Spotify Premium", "description": "1 month subscription", "price": 100, "emoji": "🎵", "category": "digital", "bg_color": "from-green-400 to-green-500"},
                {"name": "Netflix Credit", "description": "$10 streaming credit", "price": 100, "emoji": "📺", "category": "digital", "bg_color": "from-red-400 to-red-500"},
                {"name": "Gaming Credit", "description": "$5 game store credit", "price": 50, "emoji": "🎮", "category": "digital", "bg_color": "from-blue-400 to-blue-500"},
                {"name": "App Store Credit", "description": "$10 app store credit", "price": 100, "emoji": "📱", "category": "digital", "bg_color": "from-purple-400 to-purple-500"},
                # Learning Tools
                {"name": "Online Course", "description": "Udemy course of choice", "price": 200, "emoji": "🎓", "category": "education", "bg_color": "from-indigo-400 to-indigo-500"},
                {"name": "E-Book Credit", "description": "$15 book store credit", "price": 150, "emoji": "📚", "category": "education", "bg_color": "from-orange-400 to-orange-500"},
                {"name": "Language App", "description": "3 months premium access", "price": 180, "emoji": "🗣️", "category": "education", "bg_color": "from-teal-400 to-teal-500"},
                # Experiences
                {"name": "Movie Tickets", "description": "2 movie theater tickets", "price": 250, "emoji": "🎬", "category": "experiences", "bg_color": "from-yellow-400 to-yellow-500"},
                {"name": "Restaurant Voucher", "description": "$20 dining credit", "price": 200, "emoji": "🍕", "category": "experiences", "bg_color": "from-red-400 to-orange-500"},
                {"name": "Activity Pass", "description": "Local activity center pass", "price": 300, "emoji": "🎯", "category": "experiences", "bg_color": "from-pink-400 to-pink-500"},
                # Tech Accessories
                {"name": "Phone Case", "description": "Premium protective case", "price": 150, "emoji": "📱", "category": "tech", "bg_color": "from-gray-400 to-gray-600"},
                {"name": "Wireless Earbuds", "description": "Bluetooth earbuds", "price": 500, "emoji": "🎧", "category": "tech", "bg_color": "from-blue-500 to-purple-600"},
                {"name": "Power Bank", "description": "Portable phone charger", "price": 200, "emoji": "🔋", "category": "tech", "bg_color": "from-green-400 to-blue-500"},
            ]
            for item_data in teen_shop_items_data:
                item = TeenShopItem(**item_data)
                session.add(item)
            print("Seeded TeenShop items")


            await session.commit()
            await session.execute(delete(Activity))
            await session.execute(delete(UserActivity))
            # Seed activities
            activities_data = [
                {
                    "title": "Piggy Bank Adventure",
                    "description": "Learn how to save money with your digital piggy bank!",
                    "emoji": "🐷",
                    "difficulty": "easy",
                    "coins": 10,
                    "color_scheme": "pink",
                    "button_text": "Start Saving!",
                    "path": "/child/games/piggy-bank-adventure"
                },
                {
                    "title": "Needs vs Wants Game",
                    "description": "Discover the difference between things you need and want.",
                    "emoji": "🤔",
                    "difficulty": "easy",
                    "coins": 15,
                    "color_scheme": "teal",
                    "button_text": "Start Game",
                    "path": "/child/games/needs-vs-wants"
                },
                {
                    "title": "Coin Counting Challenge",
                    "description": "Practice counting coins and making change!",
                    "emoji": "🪙",
                    "difficulty": "medium",
                    "coins": 20,
                    "color_scheme": "blue",
                    "button_text": "Begin Challenge",
                    "path": "/child/games/coin-counting-challenge"
                },
                {
                    "title": "Budget Builder",
                    "description": "Create your first budget and learn to plan ahead.",
                    "emoji": "📊",
                    "difficulty": "medium",
                    "coins": 25,
                    "color_scheme": "green",
                    "button_text": "Start Budget",
                    "path": "/child/games/budget-builder"
                },
                {
                    "title": "Shopping Smart",
                    "description": "Learn smart shopping tips and compare prices.",
                    "emoji": "🛒",
                    "difficulty": "hard",
                    "coins": 30,
                    "color_scheme": "yellow",
                    "button_text": "Shop Smart",
                    "path": "/child/games/shopping-smart"
                },
                {
                    "title": "Goal Setting Quest",
                    "description": "Set and achieve your financial goals step by step.",
                    "emoji": "🎯",
                    "difficulty": "hard",
                    "coins": 35,
                    "color_scheme": "purple",
                    "button_text": "Begin Quest",
                    "path": "/child/games/goal-setting-quest"
                }
            ]
            activity_objs = []
            for activity_data in activities_data:
                activity = Activity(**activity_data)
                session.add(activity)
                activity_objs.append(activity)
            await session.commit()
            # Mark Piggy Bank Adventure as completed for Luna
            piggy_bank_activity = await session.execute(select(Activity).where(Activity.title == "Piggy Bank Adventure"))
            piggy_bank = piggy_bank_activity.scalar_one_or_none()
            if piggy_bank:
                user_activity = UserActivity(user_id=child1_user.id, activity_id=piggy_bank.id)
                session.add(user_activity)
                await session.commit()
            
            print("Data seeding completed successfully!")
            
            print("\n Demo Login Credentials:")
            print("Parent: parent@demo.com / demo123")
            print("Teacher: teacher@demo.com / demo123") 
            print("Child (9y): luna@demo.com / demo123")
            print("Teen (14y): harry@demo.com / demo123")
            
        except Exception as e:
            print(f"Error seeding data: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

        
if __name__ == "__main__":
    asyncio.run(seed_data())