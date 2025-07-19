"""CoinCraft FastAPI Backend Application."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_db_and_tables
from auth import auth_backend, fastapi_users
from schemas import UserCreate, UserRead
import routers.auth as auth_router
import routers.users as users_router
import routers.goals as goals_router
import routers.transactions as transactions_router
import routers.tasks as tasks_router
import routers.modules as modules_router
import routers.classes as classes_router
import routers.redemptions as redemptions_router
import routers.dashboard as dashboard_router


class HealthCheck(BaseModel):
    """Response model for health check."""
    status: str = "OK"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown
    pass


# Create FastAPI app
app = FastAPI(
    title="CoinCraft API",
    description="Financial literacy learning platform API for children, teens, parents, and teachers.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Vue dev server
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://localhost:8080",  # Alternative Vue dev server
    "http://127.0.0.1:8080",
]

# Add environment-specific origins
if os.getenv("ENVIRONMENT") == "production":
    origins.extend([
        "https://coincraft.com",
        "https://www.coincraft.com",
        "https://api.coincraft.com",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on.

    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


# Authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)

# API routes
app.include_router(auth_router.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router.router, prefix="/api/users", tags=["User Management"])
app.include_router(goals_router.router, prefix="/api", tags=["Goals"])
app.include_router(transactions_router.router, prefix="/api", tags=["Transactions"])
app.include_router(tasks_router.router, prefix="/api", tags=["Tasks"])
app.include_router(modules_router.router, prefix="/api", tags=["Activities & Learning"])
app.include_router(classes_router.router, prefix="/api", tags=["Teachers"])
app.include_router(redemptions_router.router, prefix="/api", tags=["Redemptions"])
app.include_router(dashboard_router.router, prefix="/api", tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
