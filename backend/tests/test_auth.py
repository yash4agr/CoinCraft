import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models import User, ChildProfile, ParentProfile, TeacherProfile
from sqlalchemy import select

# Assuming 'app' is imported from your main FastAPI application file (e.g., main.py)
# and 'auth_backend' is available from your auth module.
# You might need to adjust these imports based on your actual project structure.
from backend.main import app
from backend.auth import auth_backend

@pytest.mark.asyncio
async def test_register_parent_success(client: AsyncClient, session: AsyncSession):
    """
    Test successful registration of a new parent user.
    Verifies HTTP status, response data, and database entry.
    """
    user_data = {
        "email": "testparent@example.com",
        "password": "securepassword123",
        "name": "Test Parent",
        "role": "parent"
    }
    response = await client.post("/api/auth/register", json=user_data) # Use the client directly

    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]
    assert data["user"]["name"] == user_data["name"]
    assert data["user"]["role"] == user_data["role"]
    assert data["user"]["is_active"] is True

    # Verify user in database
    user = await session.execute(select(User).where(User.email == user_data["email"]))
    user = user.scalar_one_or_none()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.role == user_data["role"]

    # Verify parent profile in database
    parent_profile = await session.execute(select(ParentProfile).where(ParentProfile.user_id == user.id))
    parent_profile = parent_profile.scalar_one_or_none()
    assert parent_profile is not None
    assert parent_profile.user_id == user.id
    assert parent_profile.exchange_rate == 1.0 # Default value
    assert parent_profile.require_approval is True # Default value

@pytest.mark.asyncio
async def test_register_teacher_success(client: AsyncClient, session: AsyncSession):
    """
    Test successful registration of a new teacher user.
    Verifies HTTP status, response data, and database entry.
    """
    user_data = {
        "email": "testteacher@example.com",
        "password": "securepassword123",
        "name": "Test Teacher",
        "role": "teacher",
        "school_name": "Test School",
        "grade_level": "5th Grade",
        "subject": "Math"
    }
    response = await client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]
    assert data["user"]["name"] == user_data["name"]
    assert data["user"]["role"] == user_data["role"]

    # Verify user in database
    user = await session.execute(select(User).where(User.email == user_data["email"]))
    user = user.scalar_one_or_none()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.role == user_data["role"]

    # Verify teacher profile in database
    teacher_profile = await session.execute(select(TeacherProfile).where(TeacherProfile.user_id == user.id))
    teacher_profile = teacher_profile.scalar_one_or_none()
    assert teacher_profile is not None
    assert teacher_profile.user_id == user.id
    assert teacher_profile.school_name == "" # Default empty string from auth.py
    assert teacher_profile.grade_level == "" # Default empty string from auth.py
    assert teacher_profile.subject == "" # Default empty string from auth.py

@pytest.mark.asyncio
async def test_register_child_success(client: AsyncClient, session: AsyncSession):
    """
    Test successful registration of a new child user (younger_child).
    Verifies HTTP status, response data, and database entry.
    """
    user_data = {
        "email": "testchild@example.com",
        "password": "childpassword123",
        "name": "Test Child",
        "role": "younger_child",
        "age": 8
    }
    response = await client.post("/api/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == user_data["email"]
    assert data["user"]["name"] == user_data["name"]
    assert data["user"]["role"] == user_data["role"]

    # Verify user in database
    user = await session.execute(select(User).where(User.email == user_data["email"]))
    user = user.scalar_one_or_none()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.role == user_data["role"]

    # Verify child profile in database
    child_profile = await session.execute(select(ChildProfile).where(ChildProfile.user_id == user.id))
    child_profile = child_profile.scalar_one_or_none()
    assert child_profile is not None
    assert child_profile.user_id == user.id
    assert child_profile.age == 8 # Age from input, if provided, otherwise default by role
    assert child_profile.coins == 0
    assert child_profile.level == 1

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, register_user_helper):
    """
    Test registration with an email that already exists.
    """
    # Use the helper to register the first user
    await register_user_helper("duplicate@example.com", "password123", "First User", "parent")

    user_data = {
        "email": "duplicate@example.com",
        "password": "anotherpassword",
        "name": "Second User",
        "role": "parent"
    }
    response = await client.post("/api/auth/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists"

@pytest.mark.asyncio
async def test_register_missing_fields(client: AsyncClient):
    """
    Test registration with missing required fields.
    """
    # Missing email
    user_data = {
        "password": "password123",
        "name": "Test User",
        "role": "parent"
    }
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"

    # Missing password
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "role": "parent"
    }
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 6 characters long"

    # Missing name
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "role": "parent"
    }
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Name is required"

    # Missing role (will be a 422 Unprocessable Entity by Pydantic)
    user_data = {
        "email": "test_no_role@example.com",
        "password": "password123",
        "name": "Test User No Role"
    }
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert any("field required" in err["msg"] for err in response.json()["detail"])

@pytest.mark.asyncio
async def test_register_invalid_role(client: AsyncClient):
    """
    Test registration with an invalid role.
    """
    user_data = {
        "email": "invalidrole@example.com",
        "password": "password123",
        "name": "Invalid Role User",
        "role": "admin" # Invalid role according to schema
    }
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid role specified"

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, register_user_helper):
    """
    Test successful user login.
    """
    user_email = "loginuser@example.com"
    user_password = "loginpassword123"
    await register_user_helper(user_email, user_password, "Login User", "parent")

    login_data = {
        "username": user_email,
        "password": user_password
    }
    response = await client.post("/api/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == user_email

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, register_user_helper):
    """
    Test login with incorrect password.
    """
    user_email = "badlogin@example.com"
    await register_user_helper(user_email, "correctpassword", "Bad Login User", "parent")

    login_data = {
        "username": user_email,
        "password": "wrongpassword"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

@pytest.mark.asyncio
async def test_login_non_existent_user(client: AsyncClient):
    """
    Test login with a non-existent email.
    """
    login_data = {
        "username": "nonexistent@example.com",
        "password": "anypassword"
    }
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

@pytest.mark.asyncio
async def test_logout_success(auth_parent_client: dict):
    """
    Test successful user logout.
    """
    client = auth_parent_client["client"] # Access the client from the dictionary
    response = await client.post("/api/auth/logout")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["message"] == "Successfully logged out"

@pytest.mark.asyncio
async def test_logout_unauthenticated(client: AsyncClient):
    """
    Test logout when no user is authenticated.
    """
    # Ensure no Authorization header is set
    client.headers = {}
    response = await client.post("/api/auth/logout")
    # FastAPI Users logout endpoint doesn't actually require auth, it just returns success.
    # This is a design choice for JWT-based auth where client-side token removal is key.
    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_verify_token_success(auth_parent_client: dict):
    """
    Test token verification with a valid token.
    """
    client = auth_parent_client["client"] # Access the client from the dictionary
    response = await client.get("/api/auth/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["user"]["id"] == auth_parent_client["user_id"]
    assert data["user"]["email"] == auth_parent_client["user_email"]

@pytest.mark.asyncio
async def test_verify_token_invalid(client: AsyncClient):
    """
    Test token verification with an invalid token.
    """
    client.headers = {"Authorization": "Bearer invalidtoken123"}
    response = await client.get("/api/auth/verify")
    assert response.status_code == 401
    assert response.json()["detail"] == "UNAUTHORIZED"

@pytest.mark.asyncio
async def test_verify_token_no_token(client: AsyncClient):
    """
    Test token verification with no token provided.
    """
    # Ensure no Authorization header is set
    client.headers = {}
    response = await client.get("/api/auth/verify")
    assert response.status_code == 401
    assert response.json()["detail"] == "UNAUTHORIZED"
