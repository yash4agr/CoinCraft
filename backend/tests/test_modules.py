import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Module, UserModuleProgress


@pytest.mark.asyncio
async def test_get_activities_forbidden(auth_client: dict):
    """
    Test that a non-child user cannot access activities.
    """
    client = auth_client["client"]
    response = await client.get("/api/modules/activities")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can access activities"


@pytest.mark.asyncio
async def test_get_activity_not_found(auth_child_client: dict):
    """
    Test getting details for a non-existent activity.
    """
    client = auth_child_client["client"]
    non_existent_id = "00000000-0000-0000-0000-000000000001"
    response = await client.get(f"/api/modules/activities/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


@pytest.mark.asyncio
async def test_complete_activity_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot complete activities.
    """
    client = auth_client["client"]
    module = Module(title="Parent Module", description="For parents", category="parenting", difficulty="easy", points_reward=10, is_published=True, created_by="system")
    session.add(module)
    await session.commit()
    completion_data = {"score": 100, "time_spent": 5, "is_completed": True}
    response = await client.post(f"/api/modules/activities/{module.id}/complete", json=completion_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can complete activities"


@pytest.mark.asyncio
async def test_complete_activity_not_found(auth_child_client: dict):
    """
    Test completing a non-existent activity.
    """
    client = auth_child_client["client"]
    non_existent_id = "00000000-0000-0000-0000-000000000002"
    completion_data = {"score": 100, "time_spent": 10, "is_completed": True}
    response = await client.post(f"/api/modules/activities/{non_existent_id}/complete", json=completion_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


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
    progress = UserModuleProgress(user_id=child_id, module_id=module.id, is_completed=True, score=100)
    session.add(progress)
    await session.commit()
    completion_data = {"score": 80, "time_spent": 15, "is_completed": True}
    response = await client.post(f"/api/modules/activities/{module.id}/complete", json=completion_data)
    assert response.status_code == 400
    # The actual error message may need to match your implementation


@pytest.mark.asyncio
async def test_get_learning_modules_forbidden(auth_client: dict):
    """
    Test that a non-child user can still get learning modules (should be allowed, but no progress info).
    """
    client = auth_client["client"]
    response = await client.get("/api/modules/learning-modules")
    assert response.status_code == 200
    # Should not have user_progress in returned modules
    for module in response.json():
        assert "user_progress" not in module or module["user_progress"] is None


@pytest.mark.asyncio
async def test_complete_module_forbidden(auth_client: dict, session: AsyncSession):
    """
    Test that a non-child user cannot complete modules.
    """
    client = auth_client["client"]
    module = Module(title="Parent Module", description="For parents", category="parenting", difficulty="easy", points_reward=10, is_published=True, created_by="system")
    session.add(module)
    await session.commit()
    completion_data = {"score": 100, "time_spent": 5, "is_completed": True}
    response = await client.post(f"/api/modules/learning-modules/{module.id}/complete", json=completion_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only children can complete activities"


@pytest.mark.asyncio
async def test_complete_module_not_found(auth_child_client: dict):
    """
    Test completing a non-existent module.
    """
    client = auth_child_client["client"]
    non_existent_id = "00000000-0000-0000-0000-000000000003"
    completion_data = {"score": 100, "time_spent": 10, "is_completed": True}
    response = await client.post(f"/api/modules/learning-modules/{non_existent_id}/complete", json=completion_data)
    assert response.status_code == 404
    # The actual error message may need to match your implementation