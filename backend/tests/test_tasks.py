import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, Task, ChildProfile
from datetime import datetime

@pytest.mark.asyncio
async def test_get_user_tasks_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    # Add a task assigned by parent
    task = Task(id="task1", title="Do Homework", assigned_by=parent_id, assigned_to="child1", coins_reward=10)
    session.add(task)
    await session.commit()
    response = await client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert any(t["title"] == "Do Homework" for t in data)

@pytest.mark.asyncio
async def test_create_task_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child2", parent_id=parent_id)
    session.add(child)
    await session.commit()
    task_data = {"title": "Clean Room", "assigned_to": "child2", "coins_reward": 15}
    response = await client.post("/api/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Clean Room"
    assert data["coins_reward"] == 15

@pytest.mark.asyncio
async def test_create_task_forbidden(auth_client: dict):
    client = auth_client["client"]
    task_data = {"title": "Forbidden Task", "assigned_to": "child3", "coins_reward": 10}
    response = await client.post("/api/tasks", json=task_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only parents can create tasks"

@pytest.mark.asyncio
async def test_assign_task_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child4", parent_id=parent_id)
    session.add(child)
    await session.commit()
    task_data = {"title": "Read Book", "assigned_to": "child4", "coins_reward": 20}
    response = await client.post(f"/api/tasks/parents/{parent_id}/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Read Book"
    assert data["coins_reward"] == 20

@pytest.mark.asyncio
async def test_assign_task_forbidden(auth_client: dict):
    client = auth_client["client"]
    task_data = {"title": "Forbidden Assign", "assigned_to": "child5", "coins_reward": 10}
    response = await client.post(f"/api/tasks/parents/parentX/tasks", json=task_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only parents can assign tasks"

@pytest.mark.asyncio
async def test_update_task_status_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    child = ChildProfile(user_id="child6", parent_id=parent_id)
    session.add(child)
    await session.commit()
    task = Task(id="task2", title="Math Practice", assigned_by=parent_id, assigned_to="child6", coins_reward=12)
    session.add(task)
    await session.commit()
    update_data = {"status": "completed"}
    response = await client.put(f"/api/tasks/tasks/{task.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"

@pytest.mark.asyncio
async def test_update_task_status_not_found(auth_parent_client: dict):
    client = auth_parent_client["client"]
    update_data = {"status": "completed"}
    response = await client.put(f"/api/tasks/tasks/nonexistent", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

@pytest.mark.asyncio
async def test_delete_task_success(auth_parent_client: dict, session: AsyncSession):
    client = auth_parent_client["client"]
    parent_id = auth_parent_client["user_id"]
    task = Task(id="task3", title="Delete Me", assigned_by=parent_id, assigned_to="child7", coins_reward=5)
    session.add(task)
    await session.commit()
    response = await client.delete(f"/api/tasks/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task deleted successfully"

@pytest.mark.asyncio
async def test_delete_task_not_found(auth_parent_client: dict):
    client = auth_parent_client["client"]
    response = await client.delete(f"/api/tasks/tasks/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
