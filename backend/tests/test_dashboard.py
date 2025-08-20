import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile, ParentProfile, TeacherProfile, Goal, Transaction, Module, UserModuleProgress, Achievement, UserAchievement, Class, ClassStudent
from datetime import datetime, timedelta, timezone

@pytest.mark.asyncio
async def test_get_dashboard_data_child_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of dashboard data for a child user.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    # Add some data for the child
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 150
    child_profile.level = 3
    child_profile.streak_days = 5
    session.add(child_profile)

    # Add a completed goal
    goal = Goal(user_id=child_id, title="New Bike", target_amount=200, current_amount=200, is_completed=True)
    session.add(goal)

    # Add transactions
    transaction1 = Transaction(user_id=child_id, type="earn", amount=50, description="Allowance", created_at=datetime.now(timezone.utc) - timedelta(days=1))
    transaction2 = Transaction(user_id=child_id, type="spend", amount=20, description="Candy", created_at=datetime.now(timezone.utc) - timedelta(days=2))
    session.add_all([transaction1, transaction2])

    # Add a completed module
    module = Module(title="Money Management", description="Learn to manage money", category="finance", difficulty="easy", points_reward=20, is_published=True, created_by="system")
    session.add(module)
    await session.commit()
    user_module_progress = UserModuleProgress(user_id=child_id, module_id=module.id, is_completed=True, score=100, completed_at=datetime.now(timezone.utc) - timedelta(days=3))
    session.add(user_module_progress)

    # Add an achievement
    achievement = Achievement(title="Saving Star", description="Achieved a saving goal", icon="star", rarity="rare", points_reward=10, criteria={})
    session.add(achievement)
    await session.commit()
    user_achievement = UserAchievement(user_id=child_id, achievement_id=achievement.id, earned_at=datetime.now(timezone.utc) - timedelta(days=4))
    session.add(user_achievement)

    await session.commit()

    response = await client.get(f"/api/dashboard/{auth_child_client['user_role']}")
    assert response.status_code == 200
    data = response.json()

    assert data["user_stats"]["coins"] == 150
    assert data["user_stats"]["level"] == 3
    assert data["user_stats"]["streak"] == 5
    assert data["user_stats"]["goals_completed"] == 1
    assert data["user_stats"]["total_earned"] == 50 # Only the 'earn' transaction

    assert len(data["recent_transactions"]) == 2
    assert data["recent_transactions"][0]["description"] == "Allowance"

    assert len(data["active_goals"]) == 0 # We added a completed goal
    assert len(data["achievements"]) == 1
    assert data["achievements"][0]["title"] == "Saving Star"

    assert len(data["learning_modules"]) > 0
    assert any(m["title"] == "Money Management" and m["user_progress"]["is_completed"] is True for m in data["learning_modules"])

@pytest.mark.asyncio
async def test_get_dashboard_data_parent_success(auth_client: dict, session: AsyncSession, register_user):
    """
    Test successful retrieval of dashboard data for a parent user.
    """
    client = auth_client["client"]
    parent_id = auth_client["user_id"]

    # Add a child to the parent
    child1_info = await register_user("child1@example.com", "pass123", "Child One", "younger_child", age=7)
    child1_user = await session.execute(select(User).where(User.id == child1_info["user_id"]))
    child1_user = child1_user.scalar_one()
    child1_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child1_info["user_id"]))
    child1_profile = child1_profile.scalar_one()
    child1_profile.parent_id = parent_id
    child1_profile.coins = 75
    session.add(child1_profile)

    child2_info = await register_user("child2@example.com", "pass123", "Child Two", "older_child", age=13)
    child2_user = await session.execute(select(User).where(User.id == child2_info["user_id"]))
    child2_user = child2_user.scalar_one()
    child2_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child2_info["user_id"]))
    child2_profile = child2_profile.scalar_one()
    child2_profile.parent_id = parent_id
    child2_profile.coins = 125
    session.add(child2_profile)

    # Add tasks for children
    from models import Task
    task1 = Task(title="Clean Room", assigned_by=parent_id, assigned_to=child1_info["user_id"], coins_reward=10, status="completed")
    task2 = Task(title="Do Dishes", assigned_by=parent_id, assigned_to=child2_info["user_id"], coins_reward=15, status="pending")
    session.add_all([task1, task2])

    # Add a pending redemption request
    from models import RedemptionRequest
    redemption_request = RedemptionRequest(user_id=child1_info["user_id"], coins_amount=50, cash_amount=5.0, status="pending")
    session.add(redemption_request)

    # Add a goal for child1
    goal = Goal(user_id=child1_info["user_id"], title="New Game", target_amount=100, current_amount=20, is_completed=False)
    session.add(goal)

    await session.commit()

    response = await client.get(f"/api/dashboard/{auth_client['user_role']}")
    assert response.status_code == 200
    data = response.json()

    assert data["user_stats"]["total_children"] == 2
    assert data["user_stats"]["total_coins_distributed"] == 0 # This needs to be calculated from transactions, not child_profile.coins
    assert data["user_stats"]["pending_tasks"] == 1 # Only 'completed' tasks are pending approval
    assert data["user_stats"]["pending_redemptions"] == 1

    assert len(data["recent_transactions"]) == 0 # No transactions yet for children via this flow
    assert len(data["active_goals"]) == 1
    assert data["active_goals"][0]["title"] == "New Game"

@pytest.mark.asyncio
async def test_get_dashboard_data_teacher_success(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test successful retrieval of dashboard data for a teacher user.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    # Create classes for the teacher
    class1 = Class(name="Grade 3 Math", teacher_id=teacher_profile.id, class_code="G3MATH")
    class2 = Class(name="Art Class", teacher_id=teacher_profile.id, class_code="ART101")
    session.add_all([class1, class2])
    await session.commit()
    await session.refresh(class1)
    await session.refresh(class2)

    # Add students to classes
    child1_info = await register_user("student_a@example.com", "pass123", "Student A", "younger_child", age=8)
    child2_info = await register_user("student_b@example.com", "pass123", "Student B", "younger_child", age=9)
    session.add(ClassStudent(class_id=class1.id, student_id=child1_info["user_id"]))
    session.add(ClassStudent(class_id=class1.id, student_id=child2_info["user_id"]))
    await session.commit()

    # Create a module by this teacher
    module = Module(title="Teacher Created Module", description="My own module", category="education", difficulty="easy", points_reward=10, is_published=True, created_by=teacher_id)
    session.add(module)
    await session.commit()


    response = await client.get(f"/api/dashboard/{auth_teacher_client['user_role']}")
    assert response.status_code == 200
    data = response.json()

    assert data["user_stats"]["total_classes"] == 2
    assert data["user_stats"]["total_students"] == 2
    assert data["user_stats"]["modules_created"] == 1

    assert len(data["recent_transactions"]) == 0
    assert len(data["active_goals"]) == 0
    assert len(data["achievements"]) == 0
    assert len(data["learning_modules"]) > 0
    assert any(m["title"] == "Teacher Created Module" for m in data["learning_modules"])


@pytest.mark.asyncio
async def test_get_dashboard_data_role_mismatch(auth_client: dict):
    """
    Test accessing dashboard data with a role mismatch in the path.
    """
    client = auth_client["client"] # This is a parent client
    response = await client.get("/api/dashboard/teacher") # Trying to access teacher dashboard
    assert response.status_code == 403
    assert response.json()["detail"] == "Role mismatch"

@pytest.mark.asyncio
async def test_get_todays_goals_child_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of today's progress goals for a child.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    # Add some activity and transactions for today
    today = datetime.now(timezone.utc).date()
    module = Module(title="Daily Lesson", description="Quick read", category="lesson", difficulty="easy", points_reward=5, is_published=True, created_by="system")
    session.add(module)
    await session.commit()

    # Simulate progress for "Read Lessons" and "Complete Games"
    progress1 = UserModuleProgress(user_id=child_id, module_id=module.id, progress_percentage=50, started_at=datetime.now(timezone.utc))
    progress2 = UserModuleProgress(user_id=child_id, module_id=module.id, is_completed=True, completed_at=datetime.now(timezone.utc))
    session.add_all([progress1, progress2])

    # Simulate "Earn Coins"
    transaction = Transaction(user_id=child_id, type="earn", amount=30, description="Daily task", created_at=datetime.now(timezone.utc))
    session.add(transaction)
    await session.commit()

    response = await client.get(f"/api/progress-goals/{child_id}")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 4 # lessons, coins, games, practice

    lessons_goal = next(item for item in data if item["id"] == "lessons")
    assert lessons_goal["current"] >= 1 # At least one lesson started

    coins_goal = next(item for item in data if item["id"] == "coins")
    assert coins_goal["current"] >= 30

    games_goal = next(item for item in data if item["id"] == "games")
    assert games_goal["current"] >= 1 # At least one game completed

    practice_goal = next(item for item in data if item["id"] == "practice")
    assert practice_goal["current"] > 0

@pytest.mark.asyncio
async def test_get_todays_goals_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot access today's goals.
    """
    client = auth_client["client"] # Parent client
    dummy_child_id = "00000000-0000-0000-0000-000000000001"
    response = await client.get(f"/api/progress-goals/{dummy_child_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"

@pytest.mark.asyncio
async def test_update_goal_progress_dashboard_success(auth_child_client: dict):
    """
    Test successful update of a daily progress goal (dashboard endpoint).
    """
    client = auth_child_client["client"]
    
    # This endpoint doesn't interact with the database in the provided code,
    # it just returns a mock response based on the input.
    goal_id = "lessons"
    update_data = {"current": 2}
    response = await client.put(f"/api/progress-goals/{goal_id}/update", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == goal_id
    assert data["current"] == 2
    assert data["is_completed"] is False
    assert data["coins_earned"] == 0

    # Test completion
    update_data = {"current": 100}
    response = await client.put(f"/api/progress-goals/{goal_id}/update", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["current"] == 100
    assert data["is_completed"] is True
    assert data["coins_earned"] == 5

