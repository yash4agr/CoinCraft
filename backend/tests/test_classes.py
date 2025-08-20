import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models import User, TeacherProfile, Class, ClassStudent, ChildProfile, UserModuleProgress
from datetime import datetime

@pytest.mark.asyncio
async def test_get_teacher_classes_success(auth_teacher_client: dict, session: AsyncSession):
    """
    Test successful retrieval of classes managed by a teacher.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    # Get the teacher's profile ID
    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    # Create some classes for the teacher
    class1 = Class(name="Math 101", teacher_id=teacher_profile.id, class_code="MATH001")
    class2 = Class(name="Science Basics", teacher_id=teacher_profile.id, class_code="SCI001")
    session.add_all([class1, class2])
    await session.commit()

    response = await client.get(f"/api/teachers/{teacher_id}/classes")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert any(c["name"] == "Math 101" for c in data)
    assert any(c["name"] == "Science Basics" for c in data)
    assert all(c["students_count"] == 0 for c in data) # Initially no students

@pytest.mark.asyncio
async def test_get_teacher_classes_forbidden_role(auth_child_client: dict):
    """
    Test that a non-teacher user cannot view teacher classes.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    response = await client.get(f"/api/teachers/{child_id}/classes")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can view classes"

@pytest.mark.asyncio
async def test_get_teacher_classes_unauthorized_teacher(auth_teacher_client: dict, register_user):
    """
    Test that a teacher cannot view another teacher's classes.
    """
    client = auth_teacher_client["client"]
    # Register a second teacher
    second_teacher_info = await register_user("teacher2@example.com", "pass123", "Teacher Two", "teacher")
    second_teacher_id = second_teacher_info["user_id"]

    response = await client.get(f"/api/teachers/{second_teacher_id}/classes")
    assert response.status_code == 403
    assert response.json()["detail"] == "Can only view your own classes"

@pytest.mark.asyncio
async def test_create_class_success(auth_teacher_client: dict, session: AsyncSession):
    """
    Test successful creation of a new class by a teacher.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    class_data = {
        "name": "History 201",
        "description": "Advanced history class",
        "grade_level": "High School"
    }
    response = await client.post(f"/api/teachers/{teacher_id}/classes", json=class_data)
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == class_data["name"]
    assert "id" in data
    assert "class_code" in data
    assert data["students_count"] == 0 # Newly created class has no students

    # Verify in database
    class_obj = await session.execute(select(Class).where(Class.id == data["id"]))
    class_obj = class_obj.scalar_one_or_none()
    assert class_obj is not None
    assert class_obj.name == class_data["name"]

@pytest.mark.asyncio
async def test_create_class_forbidden_role(auth_child_client: dict):
    """
    Test that a non-teacher user cannot create classes.
    """
    client = auth_child_client["client"]
    child_id = auth_child_client["user_id"]
    class_data = {"name": "Forbidden Class"}
    response = await client.post(f"/api/teachers/{child_id}/classes", json=class_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can create classes"

@pytest.mark.asyncio
async def test_update_class_success(auth_teacher_client: dict, session: AsyncSession):
    """
    Test successful update of an existing class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="Old Name", teacher_id=teacher_profile.id, class_code="OLDCODE")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    update_data = {
        "name": "New Class Name",
        "description": "Updated description"
    }
    response = await client.put(f"/api/classes/{class_obj.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()

    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

    # Verify in database
    await session.refresh(class_obj)
    assert class_obj.name == update_data["name"]
    assert class_obj.description == update_data["description"]

@pytest.mark.asyncio
async def test_update_class_forbidden_role(auth_child_client: dict, session: AsyncSession):
    """
    Test that a non-teacher user cannot update classes.
    """
    client = auth_child_client["client"]
    # Create a dummy class for a teacher
    teacher_profile = TeacherProfile(user_id="00000000-0000-0000-0000-000000000001")
    session.add(teacher_profile)
    await session.commit()
    dummy_class = Class(name="Dummy Class", teacher_id=teacher_profile.id, class_code="DUMMY")
    session.add(dummy_class)
    await session.commit()

    update_data = {"name": "Attempted Update"}
    response = await client.put(f"/api/classes/{dummy_class.id}", json=update_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can update classes"

@pytest.mark.asyncio
async def test_update_class_not_found(auth_teacher_client: dict):
    """
    Test updating a non-existent class.
    """
    client = auth_teacher_client["client"]
    non_existent_class_id = "00000000-0000-0000-0000-000000000001"
    update_data = {"name": "Non Existent"}
    response = await client.put(f"/api/classes/{non_existent_class_id}", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Class not found or insufficient permissions"

@pytest.mark.asyncio
async def test_delete_class_success(auth_teacher_client: dict, session: AsyncSession):
    """
    Test successful deletion of a class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_to_delete = Class(name="Delete Me", teacher_id=teacher_profile.id, class_code="DELME")
    session.add(class_to_delete)
    await session.commit()
    await session.refresh(class_to_delete)

    response = await client.delete(f"/api/classes/{class_to_delete.id}")
    assert response.status_code == 204 # No Content

    # Verify in database
    class_obj = await session.execute(select(Class).where(Class.id == class_to_delete.id))
    class_obj = class_obj.scalar_one_or_none()
    assert class_obj is None

@pytest.mark.asyncio
async def test_delete_class_forbidden_role(auth_child_client: dict, session: AsyncSession):
    """
    Test that a non-teacher user cannot delete classes.
    """
    client = auth_child_client["client"]
    # Create a dummy class
    teacher_profile = TeacherProfile(user_id="00000000-0000-0000-0000-000000000001")
    session.add(teacher_profile)
    await session.commit()
    dummy_class = Class(name="Dummy Class", teacher_id=teacher_profile.id, class_code="DUMMY")
    session.add(dummy_class)
    await session.commit()

    response = await client.delete(f"/api/classes/{dummy_class.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can delete classes"

@pytest.mark.asyncio
async def test_delete_class_not_found(auth_teacher_client: dict):
    """
    Test deleting a non-existent class.
    """
    client = auth_teacher_client["client"]
    non_existent_class_id = "00000000-0000-0000-0000-000000000001"
    response = await client.delete(f"/api/classes/{non_existent_class_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Class not found or insufficient permissions"

@pytest.mark.asyncio
async def test_get_class_students_success(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test successful retrieval of students in a class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="My Class", teacher_id=teacher_profile.id, class_code="MYCLASS")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    # Register child users
    child1_info = await register_user("student1@example.com", "pass123", "Student One", "younger_child", age=8)
    child2_info = await register_user("student2@example.com", "pass123", "Student Two", "older_child", age=12)

    # Add children to the class
    class_student1 = ClassStudent(class_id=class_obj.id, student_id=child1_info["user_id"])
    class_student2 = ClassStudent(class_id=class_obj.id, student_id=child2_info["user_id"])
    session.add_all([class_student1, class_student2])
    await session.commit()

    response = await client.get(f"/api/classes/{class_obj.id}/students")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert any(s["name"] == "Student One" for s in data)
    assert any(s["name"] == "Student Two" for s in data)
    assert all("email" in s and "age" in s and "level" in s for s in data)

@pytest.mark.asyncio
async def test_get_class_students_forbidden_role(auth_child_client: dict, session: AsyncSession):
    """
    Test that a non-teacher user cannot view class students.
    """
    client = auth_child_client["client"]
    # Create a dummy class
    teacher_profile = TeacherProfile(user_id="00000000-0000-0000-0000-000000000001")
    session.add(teacher_profile)
    await session.commit()
    dummy_class = Class(name="Dummy Class", teacher_id=teacher_profile.id, class_code="DUMMY")
    session.add(dummy_class)
    await session.commit()

    response = await client.get(f"/api/classes/{dummy_class.id}/students")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can view class students"

@pytest.mark.asyncio
async def test_get_class_students_class_not_found(auth_teacher_client: dict):
    """
    Test retrieving students from a non-existent class.
    """
    client = auth_teacher_client["client"]
    non_existent_class_id = "00000000-0000-0000-0000-000000000001"
    response = await client.get(f"/api/classes/{non_existent_class_id}/students")
    assert response.status_code == 404
    assert response.json()["detail"] == "Class not found or insufficient permissions"

@pytest.mark.asyncio
async def test_add_student_to_class_success(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test successful addition of a student to a class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="New Student Class", teacher_id=teacher_profile.id, class_code="NEWSTUD")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    child_info = await register_user("newstudent@example.com", "pass123", "New Student", "younger_child", age=7)
    student_id = child_info["user_id"]

    add_data = {"student_id": student_id}
    response = await client.post(f"/api/classes/{class_obj.id}/students", json=add_data)
    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] == student_id
    assert data["name"] == "New Student"

    # Verify in database
    class_student = await session.execute(select(ClassStudent).where(ClassStudent.class_id == class_obj.id, ClassStudent.student_id == student_id))
    class_student = class_student.scalar_one_or_none()
    assert class_student is not None

@pytest.mark.asyncio
async def test_add_student_to_class_already_in_class(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test adding a student who is already in the class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="Existing Student Class", teacher_id=teacher_profile.id, class_code="EXISTING")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    child_info = await register_user("existingstudent@example.com", "pass123", "Existing Student", "younger_child", age=9)
    student_id = child_info["user_id"]

    # Add student initially
    class_student = ClassStudent(class_id=class_obj.id, student_id=student_id)
    session.add(class_student)
    await session.commit()

    add_data = {"student_id": student_id}
    response = await client.post(f"/api/classes/{class_obj.id}/students", json=add_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already in class"

@pytest.mark.asyncio
async def test_add_student_to_class_student_not_found(auth_teacher_client: dict, session: AsyncSession):
    """
    Test adding a non-existent student to a class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="Non Existent Student Class", teacher_id=teacher_profile.id, class_code="NONEXIST")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    non_existent_student_id = "00000000-0000-0000-0000-000000000001"
    add_data = {"student_id": non_existent_student_id}
    response = await client.post(f"/api/classes/{class_obj.id}/students", json=add_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"

@pytest.mark.asyncio
async def test_add_student_to_class_forbidden_role(auth_child_client: dict, session: AsyncSession):
    """
    Test that a non-teacher user cannot add students to classes.
    """
    client = auth_child_client["client"]
    # Create a dummy class
    teacher_profile = TeacherProfile(user_id="00000000-0000-0000-0000-000000000001")
    session.add(teacher_profile)
    await session.commit()
    dummy_class = Class(name="Dummy Class", teacher_id=teacher_profile.id, class_code="DUMMY")
    session.add(dummy_class)
    await session.commit()

    add_data = {"student_id": auth_child_client["user_id"]}
    response = await client.post(f"/api/classes/{dummy_class.id}/students", json=add_data)
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can add students to classes"

@pytest.mark.asyncio
async def test_remove_student_from_class_success(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test successful removal of a student from a class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="Remove Student Class", teacher_id=teacher_profile.id, class_code="REMOVE")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    child_info = await register_user("removestudent@example.com", "pass123", "Remove Student", "younger_child", age=10)
    student_id = child_info["user_id"]

    class_student = ClassStudent(class_id=class_obj.id, student_id=student_id)
    session.add(class_student)
    await session.commit()

    response = await client.delete(f"/api/classes/{class_obj.id}/students/{student_id}")
    assert response.status_code == 204

    # Verify in database
    class_student = await session.execute(select(ClassStudent).where(ClassStudent.class_id == class_obj.id, ClassStudent.student_id == student_id))
    class_student = class_student.scalar_one_or_none()
    assert class_student is None

@pytest.mark.asyncio
async def test_remove_student_from_class_student_not_in_class(auth_teacher_client: dict, session: AsyncSession, register_user):
    """
    Test removing a student who is not in the specified class.
    """
    client = auth_teacher_client["client"]
    teacher_id = auth_teacher_client["user_id"]

    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == teacher_id))
    teacher_profile = teacher_profile.scalar_one()

    class_obj = Class(name="No Such Student Class", teacher_id=teacher_profile.id, class_code="NOSUCH")
    session.add(class_obj)
    await session.commit()
    await session.refresh(class_obj)

    child_info = await register_user("notinstudent@example.com", "pass123", "Not In Class Student", "younger_child", age=11)
    student_id = child_info["user_id"]

    response = await client.delete(f"/api/classes/{class_obj.id}/students/{student_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in class"

@pytest.mark.asyncio
async def test_remove_student_from_class_forbidden_role(auth_child_client: dict, session: AsyncSession):
    """
    Test that a non-teacher user cannot remove students from classes.
    """
    client = auth_child_client["client"]
    # Create a dummy class and student
    teacher_profile = TeacherProfile(user_id="00000000-0000-0000-0000-000000000001")
    session.add(teacher_profile)
    await session.commit()
    dummy_class = Class(name="Dummy Class", teacher_id=teacher_profile.id, class_code="DUMMY")
    session.add(dummy_class)
    await session.commit()

    dummy_student_id = "00000000-0000-0000-0000-000000000002" # Just a dummy ID, not a real user
    response = await client.delete(f"/api/classes/{dummy_class.id}/students/{dummy_student_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Only teachers can remove students from classes"

