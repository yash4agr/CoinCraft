# CoinCraft Backend API

A FastAPI-based backend for the CoinCraft financial literacy learning platform.

## Features

- **Authentication**: JWT-based auth with FastAPI Users
- **Role-based Access**: Parent, Teacher, Younger Child, Older Child roles
- **Goals & Transactions**: Financial goal tracking and coin transactions
- **Learning Modules**: Educational content and progress tracking
- **Task Management**: Parent-child task assignments
- **Redemption System**: Coin-to-money conversion requests
- **Class Management**: Teacher classroom and student management

## Quick Start

### Prerequisites

- Python 3.12+
- pip or uv (recommended)

### Installation

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -e .
   ```

2. **Set environment variables:**
   ```bash
   # Create .env file
   DATABASE_URL=sqlite+aiosqlite:///./coincraft.db
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   PORT=8000
   ENVIRONMENT=development
   ```

3. **Seed initial data:**
   ```bash
   python seed_data.py
   ```

4. **Run the server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Demo Login Credentials

| Role | Email | Password | Description |
|------|-------|----------|-------------|
| Parent | parent@demo.com | demo123 | Sarah Johnson |
| Teacher | teacher@demo.com | demo123 | Mrs. Wilson |
| Child (9y) | luna@demo.com | demo123 | Luna Smith |
| Teen (14y) | harry@demo.com | demo123 | Harry Johnson |

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLAlchemy database models  
├── schemas.py           # Pydantic schemas for validation
├── database.py          # Database configuration
├── auth.py              # Authentication setup
├── seed_data.py         # Initial data seeding
├── routers/             # API route handlers
│   ├── auth.py          # Authentication endpoints
│   ├── users.py         # User management
│   ├── goals.py         # Financial goals
│   ├── transactions.py  # Coin transactions
│   ├── tasks.py         # Parent-child tasks
│   ├── modules.py       # Learning content
│   ├── classes.py       # Teacher classrooms
│   ├── redemptions.py   # Money conversion
│   └── dashboard.py     # Dashboard data
└── pyproject.toml       # Project dependencies
```

## Key API Endpoints

### Authentication
- `POST /api/auth/jwt/login` - Login
- `POST /api/auth/register` - Register
- `GET /api/auth/verify` - Verify token

### Users
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/{user_id}` - Update profile
- `GET /api/users/{parent_id}/children` - Get parent's children

### Goals
- `GET /api/users/{user_id}/goals` - Get user goals
- `POST /api/users/{user_id}/goals` - Create goal
- `POST /api/users/{user_id}/goals/{goal_id}/contribute` - Add coins to goal

### Transactions
- `GET /api/users/{user_id}/transactions` - Get transaction history
- `POST /api/users/{user_id}/transactions` - Create transaction

### Dashboard
- `GET /api/dashboard/{user_role}` - Get role-specific dashboard data

## Technologies Used

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM with async support
- **Pydantic**: Data validation
- **FastAPI Users**: Authentication system
- **SQLite**: Database (development)
- **JWT**: Token-based authentication
- **CORS**: Cross-origin resource sharing

## Development

### Database Migrations

The app automatically creates tables on startup. For production, consider using Alembic:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Testing

```bash
# Run with test database
TEST_DATABASE_URL=sqlite+aiosqlite:///./test.db python -m pytest
```

### Production Deployment

1. Set production environment variables
2. Use PostgreSQL instead of SQLite
3. Set strong JWT_SECRET
4. Configure HTTPS
5. Use a production ASGI server like Gunicorn with Uvicorn workers

## Contributing

1. Follow FastAPI and SQLAlchemy best practices
2. Add type hints for all functions
3. Include docstrings for API endpoints
4. Update this README for new features
