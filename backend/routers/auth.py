"""Custom authentication endpoints for CoinCraft."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_async_session
from backend.auth import UserManager, get_user_manager, auth_backend, current_active_user
from backend.models import User, ChildProfile, ParentProfile, TeacherProfile
from backend.schemas import UserCreate, UserRead, AuthResponse

router = APIRouter()


@router.post("/register", response_model=AuthResponse)
async def register_and_login(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session),
    user_manager: UserManager = Depends(get_user_manager),
):
    """Register a new user and immediately log them in."""
    try:
        print(
            f"[AUTH] Registration attempt for email: {user_data.email}, role: {user_data.role}"
        )

        # Validate required fields
        if not user_data.email or not user_data.email.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email is required"
            )

        if not user_data.password or len(user_data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long",
            )

        if not user_data.name or not user_data.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required"
            )

        if user_data.role not in ["parent", "teacher", "younger_child", "older_child"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role specified"
            )

        print(f"[AUTH] Input validation passed")

        try:
            print(f"[AUTH] Checking if user exists with email: {user_data.email}")

            from sqlalchemy import select
            from models import User as UserModel

            stmt = select(UserModel).where(UserModel.email == user_data.email)
            result = await session.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print(f"[AUTH] User already exists: {user_data.email}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            print(f"[AUTH] Email is available, proceeding with registration")

        except HTTPException:
            raise
        except Exception as e:
            print(f"[AUTH] Error checking existing user: {type(e).__name__}: {str(e)}")
            print(f"[AUTH] Exception details: {repr(e)}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error during user lookup: {str(e)}",
            )

        # Create the user
        print(f"[AUTH] Creating user with email: {user_data.email}")
        print(f"[AUTH] User data: name={user_data.name}, role={user_data.role}")
        try:
            user = await user_manager.create(user_data)
            print(f"[AUTH] User created successfully with ID: {user.id}")
        except Exception as user_error:
            print(
                f" [AUTH] Failed to create user: {type(user_error).__name__}: {str(user_error)}"
            )
            print(f"[AUTH] User creation exception details: {repr(user_error)}")

            error_str = str(user_error).lower()
            if (
                "already exists" in error_str
                or "unique" in error_str
                or "duplicate" in error_str
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists",
                )
            elif "validation" in error_str or "invalid" in error_str:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid user data provided",
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user: {str(user_error)}",
            )

        # Create role-specific profile
        if user.role == "parent":
            print(f"[AUTH] Creating parent profile for user: {user.id}")
            parent_profile = ParentProfile(
                user_id=user.id,
                exchange_rate=1.0,
                auto_approval_limit=0.0,
                require_approval=True,
            )
            session.add(parent_profile)
        elif user.role == "teacher":
            print(f"[AUTH] Creating teacher profile for user: {user.id}")
            teacher_profile = TeacherProfile(
                user_id=user.id, school_name="", grade_level="", subject=""
            )
            session.add(teacher_profile)
        elif user.role in ["younger_child", "older_child"]:
            print(f"[AUTH] Creating child profile for user: {user.id}")
            child_profile = ChildProfile(
                user_id=user.id,
                age=8 if user.role == "younger_child" else 13,
                coins=0,
                level=1,
                streak_days=0,
                parent_id=None,  # Will be set when parent adds child
            )
            session.add(child_profile)

        try:
            print(f"[AUTH] Committing profile to database...")
            await session.commit()
            print(f"[AUTH] Profile committed successfully")
        except Exception as commit_error:
            print(f"[AUTH] Error committing profile: {str(commit_error)}")
            await session.rollback()

            print(f"[AUTH] Rolling back user creation...")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create user profile: {str(commit_error)}",
            )

        # Generate login token
        print(f"[AUTH] Generating login token...")
        login_strategy = auth_backend.get_strategy()
        token = await login_strategy.write_token(user)
        print(f"[AUTH] Token generated successfully")

        user_response = UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            is_verified=user.is_verified,
        )

        print(f"[AUTH] Registration and login successful for user: {user.id}")
        return AuthResponse(access_token=token, token_type="bearer", user=user_response)

    except HTTPException as http_ex:
        print(f"[AUTH] HTTP exception during registration: {http_ex.detail}")
        await session.rollback()
        raise
    except Exception as e:
        print(
            f"[AUTH] Unexpected error during registration: {type(e).__name__}: {str(e)}"
        )
        print(f"[AUTH] Full exception details: {repr(e)}")
        print(f"[AUTH] Exception traceback:")
        import traceback

        traceback.print_exc()

        await session.rollback()

        if "ValidationError" in type(e).__name__:
            error_detail = "Invalid user data provided. Please check your input."
        elif "IntegrityError" in type(e).__name__ or "unique" in str(e).lower():
            error_detail = "User with this email already exists"
        elif (
            "DatabaseError" in type(e).__name__
            or "OperationalError" in type(e).__name__
        ):
            error_detail = "Database connection issue. Please try again later."
        else:
            error_detail = f"Registration failed: {str(e)}"

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail
        )


@router.post("/logout")
async def logout_user():
    """
    Logout user.

    Note: In JWT-based auth, logout is typically handled client-side
    by removing the token. This endpoint exists for API consistency.
    """
    return {"success": True, "message": "Successfully logged out"}
