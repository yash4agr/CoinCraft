"""CoinCraft FastAPI Backend Application."""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import create_db_and_tables
from backend.auth import auth_backend, fastapi_users
from backend.schemas import UserCreate, UserRead, UserUpdate
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.goals import router as goals_router
from backend.routers.transactions import router as transactions_router
from backend.routers.tasks import router as tasks_router
from backend.routers.modules import router as modules_router
from backend.routers.classes import router as classes_router
from backend.routers.redemptions import router as redemptions_router
from backend.routers.dashboard import router as dashboard_router
from backend.routers.parent import router as parent_router
from backend.routers.teacher import router as teacher_router
from backend.routers.child import router as child_router
from backend.routers.teen import router as teen_router


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
    description="...",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url="/redocs",
)

# CORS Configuration
origins = [
    "http://localhost:3000",  # Vue dev server
    "http://localhost:5173",  # Vite dev server
    "http://localhost:4173",  # Vite preview server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
    "http://localhost:8080",  # Alternative Vue dev server
    "http://127.0.0.1:8080",
    "http://localhost:8000",  # Backend itself (for testing)
    "http://127.0.0.1:8000",
]

# Add environment-specific origins
if os.getenv("ENVIRONMENT") == "production":
    origins.extend(
        [
            "https://coincraft.com",
            "https://www.coincraft.com",
            "https://api.coincraft.com",
        ]
    )

# For development, allow all origins to fix CORS issues
import traceback
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"❌ Exception caught: {str(e)}")
        print(f"❌ Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"},
            headers={
                "Access-Control-Allow-Origin": "http://localhost:5173",
                "Access-Control-Allow-Credentials": "true",
            }
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Specific origins
    allow_credentials=True,  # Now this is valid
    allow_methods=["*"],
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


@app.get("/api/test", tags=["test"])
def test_api():
    """Simple test endpoint to verify API is working."""
    return {"message": "API is working", "timestamp": "2025-01-01T00:00:00Z"}


@app.get("/api/status", tags=["test"])
def get_status():
    """Get backend status and environment configuration."""
    return {
        "status": "OK",
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "database_type": "SQLite"
        if "sqlite" in os.getenv("DATABASE_URL", "")
        else "Other",
        "secret_key_configured": bool(os.getenv("SECRET_KEY")),
        "algorithm": os.getenv("ALGORITHM", "HS256"),
    }


@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse("swagger.yaml", media_type="application/x-yaml")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
      <title>CoinCraft API Docs</title>
      <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
      <script>
        SwaggerUIBundle({
          url: '/openapi.yaml',
          dom_id: '#swagger-ui'
        });
      </script>
    </body>
    </html>
    """)


# Authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
)

# Custom auth routes (includes registration with auto-login)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

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
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/api/users",
    tags=["users"],
)

# API routes
app.include_router(users_router, prefix="/api/users", tags=["User Management"])
app.include_router(goals_router, prefix="/api", tags=["Goals"])
app.include_router(transactions_router, prefix="/api", tags=["Transactions"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])
app.include_router(modules_router, prefix="/api", tags=["Activities & Learning"])
app.include_router(classes_router, prefix="/api", tags=["Teachers"])
app.include_router(redemptions_router, prefix="/api", tags=["Redemptions"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(parent_router, prefix="/api/parent", tags=["Parent"])
app.include_router(teacher_router, prefix="/api/teacher", tags=["Teacher"])
app.include_router(child_router, prefix="/api/child", tags=["Child"])
app.include_router(teen_router, prefix="/api/teen", tags=["Teen"])
app.include_router(shop_router, prefix="/api", tags=["Shop"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
