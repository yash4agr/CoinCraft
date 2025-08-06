import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# Import your FastAPI application
# Assuming your main FastAPI app instance is in backend/main.py
# You might need to adjust this import based on your actual app structure
from backend.main import app # Adjust this import if your main app is elsewhere (e.g., from ..main import app) 

# Import your database models and base
from backend.database import Base, get_async_session
from backend.auth import auth_backend, get_user_manager
from backend.models import User, ChildProfile, ParentProfile, TeacherProfile
from backend.schemas import UserCreate, UserRead

# Use an in-memory SQLite database for testing
# This ensures tests are isolated and don't affect your development database
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create an async engine for the test database
engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL, 
    echo=False,  # Set to True to see SQL queries in tests
    connect_args={"check_same_thread": False} # Required for SQLite
)

# Create a sessionmaker for the test database
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

@pytest.fixture(name="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a clean, independent database session for each test.
    All tables are created before each test and dropped after.
    """
    async with engine.begin() as conn:
        # Drop and create tables for a clean slate
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Yield a new session for the test
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        # Close the session after the test
        await db_session.close()

@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provides an asynchronous test client for the FastAPI application.
    Overrides the database dependency to use the test session.
    """
    # Override the get_async_session dependency to use our testing session
    def override_get_async_session():
        return session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Clean up dependency override
    app.dependency_overrides.clear()

@pytest.fixture(name="user_manager")
async def user_manager_fixture(session: AsyncSession):
    """
    Provides the UserManager instance for tests, configured with the test session.
    """
    return get_user_manager(session)

@pytest.fixture
async def register_user(client: AsyncClient):
    """
    Fixture to register a new user and return their client and token.
    """
    async def _register_user(email: str, password: str, name: str, role: str, age: int = None):
        user_data = {
            "email": email,
            "password": password,
            "name": name,
            "role": role
        }
        if age:
            user_data["age"] = age

        response = await client.post("/api/auth/register", json=user_data)
        assert response.status_code == 201
        data = response.json()
        return {
            "client": client,
            "token": data["access_token"],
            "user_id": data["user"]["id"],
            "user_email": data["user"]["email"],
            "user_role": data["user"]["role"]
        }
    return _register_user

@pytest.fixture
async def auth_client(client: AsyncClient, register_user):
    """
    Fixture that provides an authenticated client for a parent user.
    """
    user_info = await register_user("parent@example.com", "securepassword", "Test Parent", "parent")
    client.headers = {"Authorization": f"Bearer {user_info['token']}"}
    return user_info

@pytest.fixture
async def auth_child_client(client: AsyncClient, register_user):
    """
    Fixture that provides an authenticated client for a child user.
    """
    user_info = await register_user("child@example.com", "childpassword", "Test Child", "younger_child", age=8)
    client.headers = {"Authorization": f"Bearer {user_info['token']}"}
    return user_info

@pytest.fixture
async def auth_teacher_client(client: AsyncClient, register_user):
    """
    Fixture that provides an authenticated client for a teacher user.
    """
    user_info = await register_user("teacher@example.com", "teacherpassword", "Test Teacher", "teacher")
    client.headers = {"Authorization": f"Bearer {user_info['token']}"}
    return user_info