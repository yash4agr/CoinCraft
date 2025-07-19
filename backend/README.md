# CoinCraft Backend API

FastAPI backend for the CoinCraft financial literacy education platform with AI-powered module generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Install in development mode**
```bash
pip install -e .
```

Or with uv (recommended):
```bash
uv pip install -e .
```

3. **Install dependencies**
```bash
# If using pip
pip install fastapi uvicorn sqlalchemy asyncpg fastapi-users

# If using uv (automatically handles dependencies)
uv sync
```

### 🔧 Configuration


### 🗄️ Database Setup

```bash
# Run database migrations and seed data
python seed_data.py
```

### 🏃 Running the Server

```bash
# Development server with auto-reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using uvicorn directly
uvicorn main:app --reload
```

Server will start at: `http://localhost:8000`

## 📚 API Documentation

### Swagger UI (Interactive)
```
http://localhost:8000/docs
```

### ReDoc (Alternative Documentation)
```
http://localhost:8000/redoc
```

### OpenAPI Schema
```
http://localhost:8000/openapi.json
```

## 🔐 Authentication

The API uses JWT tokens for authentication. Available user roles:
- `teacher` - Create modules, manage classes
- `parent` - Monitor children, manage tasks
- `younger_child` - Ages 8-11, simplified interface
- `older_child` - Ages 12+, advanced features

### Demo Accounts
```
Teacher: teacher@demo.com / demo123
Parent: parent@demo.com / demo123
Child: child@demo.com / demo123
```

## 🛠️ API Endpoints

### Core Endpoints
- **Authentication**: `/api/auth/`
- **Users**: `/api/users/`
- **Dashboard**: `/api/dashboard/`

### Teacher Endpoints
- **Modules**: `/api/teacher/modules`
- **Classes**: `/api/teacher/classes`
- **Analytics**: `/api/teacher/analytics`

### Learning Endpoints
- **Activities**: `/api/modules/activities`
- **Progress**: `/api/modules/progress`

### Financial Endpoints
- **Goals**: `/api/goals/`
- **Transactions**: `/api/transactions/`
- **Achievements**: `/api/achievements/`

## 🤖 AI Module Generation

Enhanced modules with sections, activities, and quizzes powered by Cerebras AI.

### Features
- Automatic content generation based on topic and age group
- Interactive sections (lessons, readings, videos, discussions)
- Learning activities (exercises, simulations, projects)
- Auto-generated quiz questions with explanations

### API Usage
```bash
POST /api/teacher/modules
{
  "title": "Budgeting Basics",
  "description": "Learn fundamental budgeting skills",
  "sections": [...],
  "activities": [...],
  "quiz": [...]
}
```

## 🗃️ Database Schema

### Core Models
- **Users** - Authentication and profiles
- **Modules** - Learning content
- **ModuleSections** - Content sections
- **QuizQuestions** - Assessment questions
- **UserModuleProgress** - Learning progress tracking

### Relationships
```
Users -> TeacherProfile/ParentProfile/ChildProfile
Modules -> ModuleSections -> QuizQuestions -> QuizOptions
Users -> UserModuleProgress -> Modules
```

## 🔧 Development

### Project Structure
```
backend/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── auth.py             # Authentication logic
├── database.py         # Database configuration
├── routers/            # API route handlers
│   ├── auth.py
│   ├── teacher.py
│   ├── modules.py
│   └── ...
├── seed_data.py        # Database seeding
└── pyproject.toml      # Dependencies
```

### Adding New Endpoints
1. Define schemas in `schemas.py`
2. Add database models in `models.py`
3. Create router in `routers/`
4. Include router in `main.py`

## 🐛 Troubleshooting

### Common Issues

**Database locked error:**
```bash
rm coincraft.db
python seed_data.py
```

**Import errors:**
```bash
pip install -e .
```

**CORS errors:**
Check `FRONTEND_URL` in `.env` matches your frontend URL

### Logs
Server logs include SQL queries and API requests for debugging.

## 🚀 Production Deployment

### Environment Variables
Set production values for:
- `DATABASE_URL` (PostgreSQL recommended)
- `SECRET_KEY` (generate secure key)
- `FRONTEND_URL` (production domain)

### Database Migration
```bash
# Run migrations
alembic upgrade head

# Seed production data
python seed_data.py --production
```

---

**Need help?** Check the [API documentation](http://localhost:8000/docs) or review the codebase structure.
