import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, ChildProfile, Goal, Transaction
from datetime import datetime

@pytest.mark.asyncio
async def test_get_user_goals_self_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful retrieval of a user's own goals using 'me'.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]

    goal1 = Goal(user_id=child_id, title="Vacation Fund", target_amount=500, current_amount=100)
    goal2 = Goal(user_id=child_id, title="New Shoes", target_amount=80, current_amount=20, is_completed=True)
    session.add_all([goal1, goal2])
    await session.commit()

    response = await client.get("/api/users/me/goals")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert any(g["title"] == "Vacation Fund" for g in data)
    assert any(g["title"] == "New Shoes" for g in data)

@pytest.mark.asyncio
async def test_get_user_goals_parent_viewing_child_success(auth_client: dict, register_user, session: AsyncSession):
    """
    Test successful retrieval of a child's goals by their parent.
    """
    parent_client = auth_client["client"]
    parent_id = auth_client["user_id"]

    # Create a child linked to this parent
    child_info = await register_user("child_for_parent@example.com", "childpass", "Child For Parent", "younger_child", age=9)
    child_id = child_info["user_id"]

    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child_id))
    child_profile = child_profile.scalar_one()
    child_profile.parent_id = parent_id
    session.add(child_profile)

    # Create a goal for the child
    child_goal = Goal(user_id=child_id, title="Gaming Console", target_amount=300, current_amount=50)
    session.add(child_goal)
    await session.commit()

    response = await parent_client.get(f"/api/users/{child_id}/goals")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Gaming Console"
    assert data[0]["user_id"] == child_id

@pytest.mark.asyncio
async def test_get_user_goals_forbidden(auth_client: dict, register_user):
    """
    Test that a user cannot view another user's goals without proper permissions.
    """
    client = auth_client["client"] # This is a parent client
    
    # Register a random child not linked to this parent
    random_child_info = await register_user("random_child@example.com", "randompass", "Random Child", "younger_child", age=7)
    random_child_id = random_child_info["user_id"]

    response = await client.get(f"/api/users/{random_child_id}/goals")
    assert response.status_code == 403
    assert response.json()["detail"] == "Insufficient permissions"

@pytest.mark.asyncio
async def test_create_goal_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful creation of a new goal for the current user.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    goal_data = {
        "title": "New Bike",
        "description": "Save up for a cool new mountain bike.",
        "target_amount": 250,
        "icon": "bike",
        "color": "green",
        "deadline": "2025-12-31"
    }
    response = await client.post(f"/api/users/{user_id}/goals", json=goal_data)
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == goal_data["title"]
    assert data["target_amount"] == goal_data["target_amount"]
    assert data["current_amount"] == 0
    assert data["is_completed"] is False
    assert data["user_id"] == user_id

    # Verify in database
    goal = await session.execute(select(Goal).where(Goal.id == data["id"]))
    goal = goal.scalar_one_or_none()
    assert goal is not None
    assert goal.title == goal_data["title"]

@pytest.mark.asyncio
async def test_create_goal_forbidden(auth_client: dict):
    """
    Test that a user cannot create goals for another user.
    """
    client = auth_client["client"] # Parent client
    dummy_child_id = "00000000-0000-0000-0000-000000000001"
    goal_data = {
        "title": "Forbidden Goal",
        "target_amount": 100
    }
    response = await client.post(f"/api/users/{dummy_child_id}/goals", json=goal_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Can only create goals for yourself"

@pytest.mark.asyncio
async def test_update_goal_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful update of an existing goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    goal = Goal(user_id=user_id, title="Old Title", target_amount=100, current_amount=10)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    update_data = {
        "title": "Updated Title",
        "target_amount": 150,
        "description": "New description",
        "is_completed": True
    }
    response = await client.put(f"/api/users/{user_id}/goals/{goal.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == update_data["title"]
    assert data["target_amount"] == update_data["target_amount"]
    assert data["description"] == update_data["description"]
    assert data["is_completed"] is True

    # Verify in database
    await session.refresh(goal)
    assert goal.title == update_data["title"]
    assert goal.target_amount == update_data["target_amount"]
    assert goal.is_completed is True

@pytest.mark.asyncio
async def test_update_goal_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a user cannot update another user's goal.
    """
    client = auth_client["client"] # Parent client
    # Create a dummy goal for a non-parent user
    dummy_user_id = "00000000-0000-0000-0000-000000000001"
    goal = Goal(user_id=dummy_user_id, title="Other User's Goal", target_amount=50)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    update_data = {"title": "Attempted Update"}
    response = await client.put(f"/api/users/{dummy_user_id}/goals/{goal.id}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Can only update your own goals"

@pytest.mark.asyncio
async def test_update_goal_not_found(auth_child_client: dict):
    """
    Test updating a non-existent goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]
    non_existent_goal_id = "00000000-0000-0000-0000-000000000001"
    update_data = {"title": "Non Existent"}
    response = await client.put(f"/api/users/{user_id}/goals/{non_existent_goal_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"

@pytest.mark.asyncio
async def test_delete_goal_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful deletion of a goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    goal_to_delete = Goal(user_id=user_id, title="Delete This", target_amount=50)
    session.add(goal_to_delete)
    await session.commit()
    await session.refresh(goal_to_delete)

    response = await client.delete(f"/api/users/{user_id}/goals/{goal_to_delete.id}")
    assert response.status_code == 204 # No Content

    # Verify in database
    goal = await session.execute(select(Goal).where(Goal.id == goal_to_delete.id))
    goal = goal.scalar_one_or_none()
    assert goal is None

@pytest.mark.asyncio
async def test_delete_goal_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a user cannot delete another user's goal.
    """
    client = auth_client["client"] # Parent client
    # Create a dummy goal for a non-parent user
    dummy_user_id = "00000000-0000-0000-0000-000000000001"
    goal = Goal(user_id=dummy_user_id, title="Other User's Goal", target_amount=50)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    response = await client.delete(f"/api/users/{dummy_user_id}/goals/{goal.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Can only delete your own goals"

@pytest.mark.asyncio
async def test_delete_goal_not_found(auth_child_client: dict):
    """
    Test deleting a non-existent goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]
    non_existent_goal_id = "00000000-0000-0000-0000-000000000001"
    response = await client.delete(f"/api/users/{user_id}/goals/{non_existent_goal_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"

@pytest.mark.asyncio
async def test_contribute_to_goal_success(auth_child_client: dict, session: AsyncSession):
    """
    Test successful contribution of coins to a goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    # Give child some coins
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == user_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 100
    session.add(child_profile)

    # Create a goal
    goal = Goal(user_id=user_id, title="Dream Gadget", target_amount=200, current_amount=50)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    await session.refresh(child_profile)

    contribution_data = {"amount": 30}
    response = await client.post(f"/api/users/{user_id}/goals/{goal.id}/contribute", json=contribution_data)
    assert response.status_code == 200
    data = response.json()

    assert data["goal"]["current_amount"] == 80 # 50 + 30
    assert data["new_coin_balance"] == 70 # 100 - 30
    assert data["transaction"]["amount"] == 30
    assert data["transaction"]["type"] == "save"

    # Verify in database
    await session.refresh(goal)
    await session.refresh(child_profile)
    assert goal.current_amount == 80
    assert child_profile.coins == 70
    transaction = await session.execute(select(Transaction).where(Transaction.reference_id == goal.id, Transaction.type == "save"))
    transaction = transaction.scalar_one_or_none()
    assert transaction is not None
    assert transaction.amount == 30

@pytest.mark.asyncio
async def test_contribute_to_goal_completes_goal(auth_child_client: dict, session: AsyncSession):
    """
    Test that contributing to a goal marks it as completed if target is reached.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == user_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 50
    session.add(child_profile)

    goal = Goal(user_id=user_id, title="Small Goal", target_amount=50, current_amount=30, is_completed=False)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    await session.refresh(child_profile)

    contribution_data = {"amount": 20} # 30 + 20 = 50 (target)
    response = await client.post(f"/api/users/{user_id}/goals/{goal.id}/contribute", json=contribution_data)
    assert response.status_code == 200
    data = response.json()

    assert data["goal"]["current_amount"] == 50
    assert data["goal"]["is_completed"] is True
    assert data["new_coin_balance"] == 30 # 50 - 20

    # Verify in database
    await session.refresh(goal)
    assert goal.is_completed is True

@pytest.mark.asyncio
async def test_contribute_to_goal_insufficient_coins(auth_child_client: dict, session: AsyncSession):
    """
    Test contributing to a goal with insufficient coins.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]

    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == user_id))
    child_profile = child_profile.scalar_one()
    child_profile.coins = 5 # Only 5 coins
    session.add(child_profile)

    goal = Goal(user_id=user_id, title="Big Purchase", target_amount=100, current_amount=0)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)
    await session.refresh(child_profile)

    contribution_data = {"amount": 10}
    response = await client.post(f"/api/users/{user_id}/goals/{goal.id}/contribute", json=contribution_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient coins"

@pytest.mark.asyncio
async def test_contribute_to_goal_not_a_child(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot contribute to goals.
    """
    client = auth_client["client"] # Parent client
    user_id = auth_client["user_id"] # Parent ID

    # Create a dummy goal for this parent (even though only children can contribute)
    goal = Goal(user_id=user_id, title="Parent's Goal", target_amount=100, current_amount=0)
    session.add(goal)
    await session.commit()
    await session.refresh(goal)

    contribution_data = {"amount": 10}
    response = await client.post(f"/api/users/{user_id}/goals/{goal.id}/contribute", json=contribution_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Only children can contribute to goals"

@pytest.mark.asyncio
async def test_contribute_to_goal_not_found(auth_child_client: dict, session: AsyncSession):
    """
    Test contributing to a non-existent goal.
    """
    client = auth_child_client["client"]
    user_id = auth_child_client["user_id"]
    non_existent_goal_id = "00000000-0000-0000-0000-000000000001"
    contribution_data = {"amount": 10}
    response = await client.post(f"/api/users/{user_id}/goals/{non_existent_goal_id}/contribute", json=contribution_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"

@pytest.mark.asyncio
async def test_contribute_to_goal_forbidden(auth_child_client: dict, register_user, session: AsyncSession):
    """
    Test that a child cannot contribute to another child's goal.
    """
    client = auth_child_client["client"] # Child 1 client
    child1_id = auth_child_client["user_id"]

    # Register a second child
    child2_info = await register_user("child2_for_goal@example.com", "pass123", "Child Two", "younger_child", age=8)
    child2_id = child2_info["user_id"]

    # Give child1 some coins
    child1_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == child1_id))
    child1_profile = child1_profile.scalar_one()
    child1_profile.coins = 50
    session.add(child1_profile)

    # Create a goal for child2
    goal_for_child2 = Goal(user_id=child2_id, title="Child2's Goal", target_amount=100, current_amount=0)
    session.add(goal_for_child2)
    await session.commit()
    await session.refresh(goal_for_child2)

    contribution_data = {"amount": 10}
    response = await client.post(f"/api/users/{child2_id}/goals/{goal_for_child2.id}/contribute", json=contribution_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Can only contribute to your own goals"

