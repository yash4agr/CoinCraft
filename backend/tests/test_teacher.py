import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, TeacherProfile, Class

@pytest.mark.asyncio
async def test_get_teacher_dashboard_success(auth_teacher_client: dict, session: AsyncSession):
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]
    profile = TeacherProfile(user_id=teacher_id, school_name="Test School", grade_level="5", subject="Math")
    session.add(profile)
    await session.commit()
    response = await client.get("/api/teacher/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "teacher" in data
    assert "classes" in data
    assert "analytics" in data

@pytest.mark.asyncio
async def test_create_class_success(auth_teacher_client: dict, session: AsyncSession):
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]
    profile = TeacherProfile(user_id=teacher_id)
    session.add(profile)
    await session.commit()
    class_data = {"name": "Math Class", "description": "Algebra lessons"}
    response = await client.post("/api/teacher/classes", json=class_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Class created successfully"
    assert "class" in data
    assert data["class"]["name"] == "Math Class"

@pytest.mark.asyncio
async def test_get_teacher_classes_success(auth_teacher_client: dict, session: AsyncSession):
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]
    profile = TeacherProfile(user_id=teacher_id)
    session.add(profile)
    await session.commit()
    class_obj = Class(id="class1", name="Science Class", teacher_id=profile.id)
    session.add(class_obj)
    await session.commit()
    response = await client.get("/api/teacher/classes")
    assert response.status_code == 200
    data = response.json()
    assert any(c["name"] == "Science Class" for c in data)

@pytest.mark.asyncio
async def test_get_class_details_success(auth_teacher_client: dict, session: AsyncSession):
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]
    profile = TeacherProfile(user_id=teacher_id)
    session.add(profile)
    await session.commit()
    class_obj = Class(id="class2", name="History Class", teacher_id=profile.id)
    session.add(class_obj)
    await session.commit()
    response = await client.get(f"/api/teacher/classes/{class_obj.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "History Class"

@pytest.mark.asyncio
async def test_get_teacher_dashboard_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get("/api/teacher/dashboard")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_create_class_forbidden(auth_client: dict):
    client = auth_client["client"]
    class_data = {"name": "Forbidden Class"}
    response = await client.post("/api/teacher/classes", json=class_data)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_teacher_classes_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get("/api/teacher/classes")
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_class_details_forbidden(auth_client: dict):
    client = auth_client["client"]
    response = await client.get("/api/teacher/classes/classX")
    assert response.status_code == 403
