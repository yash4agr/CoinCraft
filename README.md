# CoinCraft - Financial Literacy Learning Platform

A comprehensive financial education platform designed for children and teens, featuring AI-powered learning modules, gamified learning experiences, and parental oversight tools.

## 🚀 Quick Setup

### Prerequisites
- **Python 3.12+** (required for backend)
- **Node.js 18+** (required for frontend)
- **uv** package manager (recommended for Python)
- **npm** (comes with Node.js)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies using uv (recommended)
uv sync

# Or using pip if uv is not available
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your configuration

# Initialize database
python seed_data.py

# Start the backend server
uv run main.py
# Or alternatively: python -m uvicorn main:app --reload --port 8000
```

**Backend will run at:** `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will run at:** `http://localhost:5173`

### 3. Cerebras AI API Setup

The platform uses [Cerebras AI](https://cloud.cerebras.ai/) for generating intelligent learning modules.

1. **Visit** [https://cloud.cerebras.ai/](https://cloud.cerebras.ai/)
2. **Sign up** for an account
3. **Generate an API key** from your dashboard
4. **Add the API key** to your backend `.env` file:

```env
CEREBRAS_API_KEY=your_api_key_here
```

## 🏗️ Project Structure

```
soft-engg-project-may-2025-se-May-15/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── models.py           # Database models
│   ├── routers/            # API endpoints
│   ├── schemas.py          # Data validation
│   └── pyproject.toml      # Python dependencies
├── frontend/               # Vue.js frontend
│   ├── src/                # Source code
│   ├── components/         # Vue components
│   ├── views/              # Page views
│   └── package.json        # Node dependencies
└── README.md               # This file
```

## 🔧 Development Commands

### Backend
```bash
cd backend

# Run with auto-reload
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest

# Database operations
python seed_data.py          # Initialize/reset database
python -m alembic upgrade    # Run migrations
```

### Frontend
```bash
cd frontend

# Development
npm run dev                  # Start dev server
npm run build               # Build for production
npm run preview             # Preview production build

# Testing
npm run test                # Run tests
npm run lint                # Lint code
```

## 🌐 API Documentation

Once the backend is running, you can access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## 👥 User Roles & Demo Accounts

The platform supports multiple user types:

- **Teacher:** Create modules, manage classes, track progress
- **Parent:** Monitor children, approve transactions, set goals
- **Child (8-11):** Simplified learning interface
- **Teen (12+):** Advanced features and budgeting tools

### Demo Login Credentials
```
Teacher: teacher@demo.com / demo123
Parent:  parent@demo.com  / demo123
Child:   child@demo.com   / demo123
```

## 🎯 Key Features

- **AI-Powered Learning:** Generate custom modules with Cerebras AI
- **Gamified Experience:** Earn coins, complete tasks, unlock achievements
- **Progress Tracking:** Monitor learning progress and financial literacy
- **Parental Controls:** Oversight and approval systems
- **Multi-Age Support:** Different interfaces for different age groups
- **Real-time Updates:** Live progress tracking and notifications

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version (must be 3.12+)
python --version

# Reinstall dependencies
cd backend
uv sync --reinstall
```

**Frontend won't start:**
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Database errors:**
```bash
cd backend
rm coincraft.db
python seed_data.py
```

**CORS errors:**
- Ensure backend is running on port 8000
- Check frontend is running on port 5173
- Verify CORS settings in backend `.env`

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///coincraft.db

# Security
SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cerebras AI
CEREBRAS_API_KEY=your_cerebras_api_key

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173
```

## 📚 Additional Resources

- **Backend Documentation:** [backend/README.md](backend/README.md)
- **Database Schema:** [database_structure.md](database_structure.md)
- **API Endpoints:** [backend_endpoint.md](backend_endpoint.md)
- **Frontend-Backend Connection:** [frontend_store_connection_with_backend.md](frontend_store_connection_with_backend.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest` (backend) and `npm run test` (frontend)
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Need help?** Check the API documentation at http://localhost:8000/docs or review the troubleshooting section above.
