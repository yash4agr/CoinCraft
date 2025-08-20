#!/usr/bin/env python3
"""
Seed Users Script for CoinCraft Development
This script creates sample teachers, parents, and children for development and testing.
"""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# Import your models and database
from database import get_async_session
from models import User, TeacherProfile, ParentProfile, ChildProfile, UserRoleEnum
from auth import get_user_manager, UserManager

# Database URL - adjust if needed
DATABASE_URL = "sqlite+aiosqlite:///coincraft.db"

async def create_user_manager():
    """Create a user manager instance for user creation."""
    # This is a simplified version - you might need to adjust based on your auth setup
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    return engine, async_session

async def seed_users():
    """Seed the database with sample users."""
    print("🌱 Starting user seeding process...")
    
    engine, async_session = await create_user_manager()
    
    async with async_session() as session:
        try:
            # ===================
            # CREATE TEACHERS
            # ===================
            print("\n👨‍🏫 Creating teachers...")
            
            teachers_data = [
                {
                    "name": "Sarah Johnson",
                    "email": "sarah.johnson@school.edu",
                    "password": "teacher123",
                    "role": UserRoleEnum.TEACHER
                },
                {
                    "name": "Michael Chen",
                    "email": "michael.chen@school.edu", 
                    "password": "teacher123",
                    "role": UserRoleEnum.TEACHER
                }
            ]
            
            created_teachers = []
            for teacher_data in teachers_data:
                # Create user
                teacher_user = User(
                    id=str(uuid.uuid4()),
                    name=teacher_data["name"],
                    email=teacher_data["email"],
                    role=teacher_data["role"],
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                
                # Hash password using bcrypt (compatible with FastAPI Users)
                import bcrypt
                salt = bcrypt.gensalt()
                teacher_user.hashed_password = bcrypt.hashpw(teacher_data["password"].encode('utf-8'), salt).decode('utf-8')
                
                session.add(teacher_user)
                await session.flush()  # Get the user ID
                
                # Create teacher profile
                teacher_profile = TeacherProfile(
                    id=str(uuid.uuid4()),
                    user_id=teacher_user.id,
                    school_name="Maple Elementary School",
                    grade_level="3rd-5th Grade",
                    subject="Financial Literacy"
                )
                
                session.add(teacher_profile)
                created_teachers.append(teacher_user)
                print(f"✅ Created teacher: {teacher_data['name']} ({teacher_data['email']})")
            
            # ===================
            # CREATE PARENTS
            # ===================
            print("\n👨‍👩‍👧‍👦 Creating parents...")
            
            parents_data = [
                {
                    "name": "Emily Rodriguez",
                    "email": "emily.rodriguez@email.com",
                    "password": "parent123",
                    "role": UserRoleEnum.PARENT
                },
                {
                    "name": "David Thompson",
                    "email": "david.thompson@email.com",
                    "password": "parent123", 
                    "role": UserRoleEnum.PARENT
                },
                {
                    "name": "Lisa Wang",
                    "email": "lisa.wang@email.com",
                    "password": "parent123",
                    "role": UserRoleEnum.PARENT
                },
                {
                    "name": "James Wilson",
                    "email": "james.wilson@email.com",
                    "password": "parent123",
                    "role": UserRoleEnum.PARENT
                }
            ]
            
            created_parents = []
            for parent_data in parents_data:
                # Create user
                parent_user = User(
                    id=str(uuid.uuid4()),
                    name=parent_data["name"],
                    email=parent_data["email"],
                    role=parent_data["role"],
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                
                # Hash password using bcrypt
                import bcrypt
                salt = bcrypt.gensalt()
                parent_user.hashed_password = bcrypt.hashpw(parent_data["password"].encode('utf-8'), salt).decode('utf-8')
                
                session.add(parent_user)
                await session.flush()
                
                # Create parent profile
                parent_profile = ParentProfile(
                    id=str(uuid.uuid4()),
                    user_id=parent_user.id,
                    exchange_rate=0.10,  # 10 cents per coin
                    auto_approval_limit=500,
                    require_approval=True
                )
                
                session.add(parent_profile)
                created_parents.append(parent_user)
                print(f"✅ Created parent: {parent_data['name']} ({parent_data['email']})")
            
            # ===================
            # CREATE CHILDREN
            # ===================
            print("\n👶 Creating children...")
            
            children_data = [
                # Younger children (8-10 years) - first 2 parents
                {
                    "name": "Sophia Rodriguez",
                    "email": "sophia.rodriguez@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.YOUNGER_CHILD,
                    "age": 8,
                    "parent_index": 0
                },
                {
                    "name": "Lucas Rodriguez", 
                    "email": "lucas.rodriguez@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.YOUNGER_CHILD,
                    "age": 10,
                    "parent_index": 0
                },
                {
                    "name": "Emma Thompson",
                    "email": "emma.thompson@email.com", 
                    "password": "child123",
                    "role": UserRoleEnum.YOUNGER_CHILD,
                    "age": 9,
                    "parent_index": 1
                },
                {
                    "name": "Noah Thompson",
                    "email": "noah.thompson@email.com",
                    "password": "child123", 
                    "role": UserRoleEnum.YOUNGER_CHILD,
                    "age": 8,
                    "parent_index": 1
                },
                
                # Older children (11-14 years) - last 2 parents
                {
                    "name": "Aiden Wang",
                    "email": "aiden.wang@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.OLDER_CHILD, 
                    "age": 12,
                    "parent_index": 2
                },
                {
                    "name": "Zoe Wang",
                    "email": "zoe.wang@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.OLDER_CHILD,
                    "age": 14,
                    "parent_index": 2
                },
                {
                    "name": "Mia Wilson",
                    "email": "mia.wilson@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.OLDER_CHILD,
                    "age": 11,
                    "parent_index": 3
                },
                {
                    "name": "Ethan Wilson",
                    "email": "ethan.wilson@email.com",
                    "password": "child123",
                    "role": UserRoleEnum.OLDER_CHILD,
                    "age": 13,
                    "parent_index": 3
                }
            ]
            
            created_children = []
            for child_data in children_data:
                # Create user
                child_user = User(
                    id=str(uuid.uuid4()),
                    name=child_data["name"],
                    email=child_data["email"],
                    role=child_data["role"],
                    is_active=True,
                    is_verified=True,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                )
                
                # Hash password using bcrypt
                import bcrypt
                salt = bcrypt.gensalt()
                child_user.hashed_password = bcrypt.hashpw(child_data["password"].encode('utf-8'), salt).decode('utf-8')
                
                session.add(child_user)
                await session.flush()
                
                # Get parent user
                parent_user = created_parents[child_data["parent_index"]]
                
                # Create child profile
                child_profile = ChildProfile(
                    id=str(uuid.uuid4()),
                    user_id=child_user.id,
                    age=child_data["age"],
                    coins=100,  # Start with 100 coins
                    level=1,
                    streak_days=0,
                    last_activity_date=datetime.now(timezone.utc) - timedelta(days=2),
                    parent_id=parent_user.id
                )
                
                session.add(child_profile)
                created_children.append(child_user)
                
                age_group = "8-10" if child_data["age"] <= 10 else "11-14"
                print(f"✅ Created child: {child_data['name']} (Age: {child_data['age']}, Group: {age_group})")
            
            # Commit all changes
            await session.commit()
            
            print(f"\n🎉 Successfully seeded database!")
            print(f"📊 Summary:")
            print(f"   👨‍🏫 Teachers: {len(created_teachers)}")
            print(f"   👨‍👩‍👧‍👦 Parents: {len(created_parents)}")
            print(f"   👶 Children: {len(created_children)}")
            print(f"\n🔑 Login Credentials:")
            print(f"   Teachers: sarah.johnson@school.edu / michael.chen@school.edu (password: teacher123)")
            print(f"   Parents: emily.rodriguez@email.com, david.thompson@email.com, etc. (password: parent123)")
            print(f"   Children: sophia.rodriguez@email.com, aiden.wang@email.com, etc. (password: child123)")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {str(e)}")
            raise
        finally:
            await engine.dispose()

async def main():
    """Main function to run the seeding process."""
    try:
        await seed_users()
    except Exception as e:
        print(f"❌ Failed to seed database: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
