import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile, Goal, Transaction, Module, UserModuleProgress, Achievement, UserAchievement
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_get_child_dashboard_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of child dashboard data.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    # Manually add some data for the child to ensure the dashboard has content
    # Add a goal
    goal = Goal(
        user_id=child_id,
        title="Buy a Toy",
        description="Save for a new toy car",
        target_amount=100,
        current_amount=50,
        icon="toy",
        color="blue"
    )
    session.add(goal)

    # Add a transaction
    transaction = Transaction(
        user_id=child_id,
        type="earn",
        amount=20,
        description="Earned from chores",
        category="task"
    )
    session.add(transaction)

    # Add a completed module progress
    module = Module(
        title="Money Basics",
        description="Introduction to money",
        category="finance",
        difficulty="easy",
        estimated_duration=15,
        points_reward=10,
        is_published=True,
        created_by="system"
    )
    session.add(module)
    await session.commit() # Commit module first to get its ID

    user_module_progress = UserModuleProgress(
        user_id=child_id,
        module_id=module.id,
        is_completed=True,
        score=100,
        time_spent=10,
        completed_at=datetime.utcnow()
    )
    session.add(user_module_progress)

    # Add an achievement
    achievement = Achievement(
        title="First Saver",
        description="Saved your first coins",
        icon="star",
        rarity="common",
        points_reward=5,
        criteria={}
    )
    session.add(achievement)
    await session.commit() # Commit achievement first to get its ID

    user_achievement = UserAchievement(
        user_id=child_id,
        achievement_id=achievement.id,
        earned_at=datetime.utcnow()
    )
    session.add(user_achievement)

    await session.commit()
    await session.refresh(goal)
    await session.refresh(transaction)
    await session.refresh(module)
    await session.refresh(user_module_progress)
    await session.refresh(achievement)
    await session.refresh(user_achievement)

    response = await client.get("/api/child/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert "child" in data
    assert data["child"]["id"] == child_id
    assert data["child"]["coins"] >= 0 # Initial 0 + earned 20 - spent on goal 50 (if any)

    assert "todays_goals" in data
    assert len(data["todays_goals"]) > 0
    assert data["todays_goals"][0]["id"] == str(goal.id)

    assert "adventures" in data
    assert len(data["adventures"]) > 0
    assert data["adventures"][0]["id"] == str(module.id)
    assert data["adventures"][0]["completed"] is True

    assert "achievements" in data
    assert len(data["achievements"]) > 0
    assert data["achievements"][0]["id"] == str(achievement.id)

    assert "learning_journey" in data
    assert len(data["learning_journey"]) > 0

    assert "stats" in data
    assert data["stats"]["total_goals"] >= 1
    assert data["stats"]["total_coins"] >= 0


@pytest.mark.asyncio
async def test_get_child_dashboard_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot access the child dashboard.
    """
    client = auth_client["client"] # This is a parent client
    response = await client.get("/api/child/dashboard")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can access this endpoint"

@pytest.mark.asyncio
async def test_get_child_goals_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of a child's goals.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    goal1 = Goal(user_id=child_id, title="Bike", target_amount=200, current_amount=50, is_completed=False)
    goal2 = Goal(user_id=child_id, title="Book", target_amount=50, current_amount=50, is_completed=True)
    session.add_all([goal1, goal2])
    await session.commit()

    response = await client.get("/api/child/goals")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(g["name"] == "Bike" for g in data)
    assert any(g["name"] == "Book" for g in data)

@pytest.mark.asyncio
async def test_get_child_goals_filter_active(auth_child_client: dict, session: AsyncSession):
    """
    Test filtering child goals by 'active' status.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    goal1 = Goal(user_id=child_id, title="Bike", target_amount=200, current_amount=50, is_completed=False)
    goal2 = Goal(user_id=child_id, title="Book", target_amount=50, current_amount=50, is_completed=True)
    session.add_all([goal1, goal2])
    await session.commit()

    response = await client.get("/api/child/goals?status=active")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Bike"
    assert data[0]["is_completed"] is False

@pytest.mark.asyncio
async def test_create_child_goal_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful creation of a new goal for a child.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    goal_data = {
        "name": "New Toy",
        "targetAmount": 150,
        "description": "Save for a cool new toy",
        "icon": "toy-icon",
        "color": "red"
    }
    response = await client.post("/api/child/goals", json=goal_data)
    assert response.status_code == 200 # Note: The endpoint returns 200, not 201
    data = response.json()

    assert "message" in data
    assert "goal" in data
    assert data["goal"]["name"] == goal_data["name"]
    assert data["goal"]["targetAmount"] == goal_data["targetAmount"]

    # Verify in database
    goal = await session.execute(select(Goal).where(Goal.user_id == child_id, Goal.title == goal_data["name"]))
    goal = goal.scalar_one_or_none()
    assert goal is not None
    assert goal.target_amount == goal_data["targetAmount"]
    assert goal.is_completed is False

@pytest.mark.asyncio
async def test_create_child_goal_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot create goals.
    """
    client = auth_client["client"]
    goal_data = {
        "name": "Forbidden Goal",
        "targetAmount": 100
    }
    response = await client.post("/api/child/goals", json=goal_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can create goals"

@pytest.mark.asyncio
async def test_update_goal_progress_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful update of a child's goal progress.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    # Create a goal and give child some coins
    goal = Goal(user_id=child_id, title="New Gadget", target_amount=200, current_amount=0, is_completed=False)
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 100
    session.add_all([goal, child_profile])
    await session.commit()

    progress_data = {"amount": 50}
    response = await client.put(f"/api/child/goals/{goal.id}/progress", json=progress_data)
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Goal progress updated successfully"
    assert data["goal"]["currentAmount"] == 50
    assert data["coins_remaining"] == 50 # 100 - 50

    # Verify in database
    await session.refresh(goal)
    await session.refresh(child_profile)
    assert goal.current_amount == 50
    assert child_profile.coins == 50

    # Test completing the goal
    progress_data = {"amount": 150} # Remaining 50 + 150 = 200 (target)
    response = await client.put(f"/api/child/goals/{goal.id}/progress", json=progress_data)
    assert response.status_code == 200
    data = response.json()
    assert data["goal"]["currentAmount"] == 200
    assert data["goal"]["is_completed"] is True
    assert data["coins_remaining"] == 0 # 50 - 150 = -100, but coins cannot go negative, so it would be 0.

    await session.refresh(goal)
    await session.refresh(child_profile)
    assert goal.current_amount == 200
    assert goal.is_completed is True
    assert child_profile.coins == 0

@pytest.mark.asyncio
async def test_update_goal_progress_insufficient_coins(auth_child_client: dict, session: AsyncSession):
    """
    Test updating goal progress with insufficient coins.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    goal = Goal(user_id=child_id, title="Expensive Item", target_amount=500, current_amount=0)
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 10 # Only 10 coins
    session.add_all([goal, child_profile])
    await session.commit()

    progress_data = {"amount": 50} # Trying to add 50 coins
    response = await client.put(f"/api/child/goals/{goal.id}/progress", json=progress_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Not enough coins"

@pytest.mark.asyncio
async def test_update_goal_progress_goal_not_found(auth_child_client: dict):
    """
    Test updating progress for a non-existent goal.
    """
    client = auth_child_client["client"]
    non_existent_goal_id = "00000000-0000-0000-0000-000000000001"
    progress_data = {"amount": 10}
    response = await client.put(f"/api/child/goals/{non_existent_goal_id}/progress", json=progress_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"

@pytest.mark.asyncio
async def test_update_goal_progress_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot update goal progress.
    """
    client = auth_client["client"] # Parent client
    # Create a dummy goal for a child
    child_user_id = "00000000-0000-0000-0000-000000000002"
    goal = Goal(user_id=child_user_id, title="Dummy Goal", target_amount=100, current_amount=0)
    session.add(goal)
    await session.commit()

    progress_data = {"amount": 10}
    response = await client.put(f"/api/child/goals/{goal.id}/progress", json=progress_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can update goals"

@pytest.mark.asyncio
async def test_get_child_activities_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of child activities.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    module1 = Module(title="Budgeting 101", description="Learn budgeting", category="finance", difficulty="easy", points_reward=20, is_published=True, created_by="system")
    module2 = Module(title="Investing Basics", description="Intro to investing", category="investing", difficulty="medium", points_reward=30, is_published=True, created_by="system")
    session.add_all([module1, module2])
    await session.commit()

    # Mark module1 as completed for the child
    progress1 = UserModuleProgress(user_id=child_id, module_id=module1.id, is_completed=True, score=100)
    session.add(progress1)
    await session.commit()

    response = await client.get("/api/child/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(a["name"] == "Budgeting 101" and a["completed"] is True for a in data)
    assert any(a["name"] == "Investing Basics" and a["completed"] is False for a in data)

@pytest.mark.asyncio
async def test_get_child_activities_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot access child activities.
    """
    client = auth_client["client"]
    response = await client.get("/api/child/activities")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can access activities"

@pytest.mark.asyncio
async def test_complete_activity_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful completion of an activity and coin award.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    module = Module(title="Saving Smart", description="How to save money", category="finance", difficulty="easy", points_reward=25, is_published=True, created_by="system")
    session.add(module)
    await session.commit()

    # Get initial coins
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    initial_coins = child_profile.coins

    completion_data = {"score": 90, "time_spent": 12}
    response = await client.post(f"/api/child/activities/{module.id}/complete", json=completion_data)
    assert response.status_code == 200
    data = response.json()

    expected_coins_earned = int((completion_data["score"] / 100) * module.points_reward)

    assert data["message"] == "Activity completed successfully"
    assert data["activity"]["id"] == str(module.id)
    assert data["activity"]["score"] == completion_data["score"]
    assert data["activity"]["coins_earned"] == expected_coins_earned
    assert data["total_coins"] == initial_coins + expected_coins_earned

    # Verify in database
    await session.refresh(child_profile)
    assert child_profile.coins == initial_coins + expected_coins_earned
    progress = await session.execute(select(UserModuleProgress).where(UserModuleProgress.user_id == child_id, UserModuleProgress.module_id == module.id))
    progress = progress.scalar_one_or_none()
    assert progress is not None
    assert progress.is_completed is True
    assert progress.score == completion_data["score"]

@pytest.mark.asyncio
async def test_complete_activity_already_completed(auth_child_client: dict, session: AsyncSession):
    """
    Test attempting to complete an activity that is already completed.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    module = Module(title="Advanced Finance", description="Advanced topics", category="finance", difficulty="hard", points_reward=50, is_published=True, created_by="system")
    session.add(module)
    await session.commit()

    # Mark as completed
    progress = UserModuleProgress(user_id=child_id, module_id=module.id, is_completed=True, score=100)
    session.add(progress)
    await session.commit()

    completion_data = {"score": 80, "time_spent": 15}
    response = await client.post(f"/api/child/activities/{module.id}/complete", json=completion_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity already completed"

@pytest.mark.asyncio
async def test_complete_activity_not_found(auth_child_client: dict):
    """
    Test completing a non-existent activity.
    """
    client = auth_child_client["client"]
    non_existent_activity_id = "00000000-0000-0000-0000-000000000001"
    completion_data = {"score": 100, "time_spent": 10}
    response = await client.post(f"/api/child/activities/{non_existent_activity_id}/complete", json=completion_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

@pytest.mark.asyncio
async def test_complete_activity_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot complete activities.
    """
    client = auth_client["client"] # Parent client
    module = Module(title="Parent Module", description="For parents", category="parenting", difficulty="easy", points_reward=10, is_published=True, created_by="system")
    session.add(module)
    await session.commit()

    completion_data = {"score": 100, "time_spent": 5}
    response = await client.post(f"/api/child/activities/{module.id}/complete", json=completion_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can complete activities"

@pytest.mark.asyncio
async def test_get_child_transactions_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of child's transaction history.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    transaction1 = Transaction(user_id=child_id, type="earn", amount=10, description="Allowance", category="allowance")
    transaction2 = Transaction(user_id=child_id, type="spend", amount=5, description="Candy", category="food")
    session.add_all([transaction1, transaction2])
    await session.commit()

    response = await client.get("/api/child/transactions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert any(t["description"] == "Allowance" for t in data)
    assert any(t["description"] == "Candy" for t in data)

@pytest.mark.asyncio
async def test_get_child_transactions_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot view child transactions.
    """
    client = auth_client["client"]
    response = await client.get("/api/child/transactions")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can view transactions"

@pytest.mark.asyncio
async def test_get_child_stats_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of child's statistics.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    # Add some data to ensure stats are meaningful
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 100
    child_profile.level = 5
    child_profile.streak_days = 7
    session.add(child_profile)

    goal1 = Goal(user_id=child_id, title="Game", target_amount=100, current_amount=100, is_completed=True)
    goal2 = Goal(user_id=child_id, title="Tablet", target_amount=500, current_amount=50, is_completed=False)
    session.add_all([goal1, goal2])

    module = Module(title="Financial Fun", description="Fun with money", category="finance", difficulty="easy", points_reward=10, is_published=True, created_by="system")
    session.add(module)
    await session.commit()

    progress = UserModuleProgress(user_id=child_id, module_id=module.id, is_completed=True, score=100)
    session.add(progress)

    transaction_earn = Transaction(user_id=child_id, type="earn", amount=50, description="Bonus", category="bonus")
    transaction_spend = Transaction(user_id=child_id, type="spend", amount=20, description="Snacks", category="food")
    session.add_all([transaction_earn, transaction_spend])
    await session.commit()

    response = await client.get("/api/child/stats")
    assert response.status_code == 200
    data = response.json()

    assert "profile" in data
    assert data["profile"]["coins"] == 100
    assert data["profile"]["level"] == 5
    assert data["profile"]["streak_days"] == 7

    assert "goals" in data
    assert data["goals"]["active"] == 1
    assert data["goals"]["completed"] == 1
    assert data["goals"]["total"] == 2

    assert "activities" in data
    assert data["activities"]["completed"] == 1

    assert "transactions" in data
    assert data["transactions"]["total_earned"] == 50
    assert data["transactions"]["total_spent"] == 20
    assert data["transactions"]["net_balance"] == 30

@pytest.mark.asyncio
async def test_get_child_stats_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot view child statistics.
    """
    client = auth_client["client"]
    response = await client.get("/api/child/stats")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can view stats"