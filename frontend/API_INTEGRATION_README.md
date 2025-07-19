# CoinCraft Frontend API Integration

## Overview
The frontend has been successfully integrated with the FastAPI backend using a hybrid approach:

- **Demo Mode**: Mock data for unauthenticated users and demo pages
- **Authenticated Mode**: Real API calls for logged-in users
- **Fallback**: Mock data if API is unavailable or fails

## API Service Layer

### Location: `src/services/api.ts`
- **Comprehensive API client** with all endpoints
- **Automatic token management** (JWT)
- **Error handling** and response formatting
- **TypeScript interfaces** for all data types

### Key Features:
- ✅ **Authentication**: Login, register, logout with JWT
- ✅ **User Management**: Profile updates, current user
- ✅ **Goals**: CRUD operations for savings goals
- ✅ **Transactions**: Financial transaction tracking
- ✅ **Tasks**: Task management and completion
- ✅ **Modules**: Learning module progress
- ✅ **Redemptions**: Coin redemption requests
- ✅ **Dashboard**: Role-specific dashboard data

## Updated Stores

### 1. Auth Store (`src/stores/auth.ts`)
**Changes Made:**
- ✅ Replaced mock login with real API calls
- ✅ Added JWT token management
- ✅ Updated user session handling
- ✅ Fixed demo login credentials

**Demo Credentials:**
```typescript
// Updated demo login mapping
const demoCredentials = {
  parent: { username: 'parent@demo.com', password: 'demo123' },
  teacher: { username: 'teacher@demo.com', password: 'demo123' },
  younger_child: { username: 'luna@demo.com', password: 'demo123' },
  older_child: { username: 'harry@demo.com', password: 'demo123' }
}
```

### 2. Dashboard Store (`src/stores/dashboard.ts`)
**Changes Made:**
- ✅ Hybrid approach: Mock data for demo, real API for authenticated users
- ✅ Automatic detection of authentication status
- ✅ Fallback to mock data if API fails
- ✅ Dynamic activity loading based on user role
- ✅ Live achievements and goals (when authenticated)

### 3. Child Store (`src/stores/child.ts`)
**Changes Made:**
- ✅ Hybrid approach: Mock data for demo, real API for authenticated users
- ✅ Demo mode detection via localStorage
- ✅ Real goal creation and updates (when authenticated)
- ✅ Live transaction tracking (when authenticated)
- ✅ API-driven progress updates (when authenticated)

## Environment Configuration

**IMPORTANT**: You must create a `.env` file in the frontend directory. See `SETUP_INSTRUCTIONS.md` for detailed setup steps.

```env
# API Configuration
VITE_API_URL=http://localhost:8000

# Development settings
VITE_APP_TITLE=CoinCraft
VITE_DEBUG=true
```

**Note**: The API service uses relative imports (`../services/api`) instead of path aliases to avoid configuration issues.

## API Endpoints Used

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout
- `GET /users/me` - Get current user

### Dashboard
- `GET /dashboard/{role}` - Role-specific dashboard data

### Goals
- `GET /goals/` - Get user goals
- `POST /goals/` - Create new goal
- `PUT /goals/{id}` - Update goal
- `POST /goals/{id}/progress` - Update goal progress

### Transactions
- `GET /transactions/` - Get transaction history
- `POST /transactions/` - Create new transaction

### Tasks
- `GET /tasks/` - Get user tasks
- `POST /tasks/` - Create new task
- `POST /tasks/{id}/complete` - Complete task

### Modules
- `GET /modules/` - Get learning modules
- `GET /modules/{id}` - Get specific module
- `POST /modules/{id}/progress` - Update module progress

### Redemptions
- `GET /redemptions/` - Get redemption requests
- `POST /redemptions/` - Create redemption request
- `POST /redemptions/{id}/approve` - Approve request

## Error Handling

The API service includes comprehensive error handling:

```typescript
// Example error handling
const response = await apiService.login(credentials)
if (response.error) {
  throw new Error(response.error)
}
```

**Error Types Handled:**
- ✅ Network errors
- ✅ Authentication failures (401)
- ✅ Validation errors
- ✅ Server errors
- ✅ Token expiration

## Token Management

JWT tokens are automatically managed:

```typescript
// Automatic token storage
apiService.login(credentials) // Token saved automatically

// Automatic token inclusion in requests
apiService.getGoals() // Token included in Authorization header

// Automatic token cleanup
apiService.logout() // Token removed from storage
```

## Data Transformation

The API service handles data transformation between frontend and backend formats:

```typescript
// Frontend format -> API format
const apiGoal = {
  title: goal.name,           // Frontend: name
  target_amount: goal.targetAmount,  // Frontend: targetAmount
  current_amount: goal.currentAmount // Frontend: currentAmount
}

// API format -> Frontend format
const localGoal = {
  name: apiGoal.title,        // API: title
  targetAmount: apiGoal.target_amount,  // API: target_amount
  currentAmount: apiGoal.current_amount // API: current_amount
}
```

## Testing the Integration

### 1. Start the Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

### 3. Test Login
- Use demo credentials: `luna@demo.com` / `demo123`
- Check browser dev tools for JWT token
- Verify API calls in Network tab

### 4. Test Features
- Create new goals
- Complete activities
- Check transaction history
- Verify dashboard data updates

## Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Ensure backend is running on `http://localhost:8000`
   - Check CORS configuration in backend

2. **Authentication Errors**
   - Verify JWT token in localStorage
   - Check token expiration
   - Ensure correct credentials

3. **API Connection Errors**
   - Verify `VITE_API_URL` in environment
   - Check backend server status
   - Review network connectivity

4. **Data Format Errors**
   - Check API response format
   - Verify data transformation logic
   - Review TypeScript interfaces

### Debug Mode:
Enable debug logging by setting `VITE_DEBUG=true` in your `.env` file.

## Next Steps

1. **Complete Store Updates**: Update remaining stores (parent, teacher)
2. **Add Loading States**: Implement loading indicators
3. **Error Boundaries**: Add Vue error boundaries
4. **Offline Support**: Add service worker for offline functionality
5. **Testing**: Add unit tests for API integration

## Files Modified

- ✅ `src/services/api.ts` - New API service layer with enhanced error handling
- ✅ `src/stores/auth.ts` - Updated with real API calls and proper token management
- ✅ `src/stores/dashboard.ts` - Updated with real API calls, removed mock data
- ✅ `src/stores/child.ts` - Updated with real API calls
- ✅ `API_INTEGRATION_README.md` - This documentation
- ✅ `SETUP_INSTRUCTIONS.md` - Detailed setup instructions

## Recent Fixes Applied

- ✅ **Fixed import paths**: Changed from `@/services/api` to `../services/api` for compatibility
- ✅ **Hybrid approach**: Mock data for demo pages, real API for authenticated users
- ✅ **Enhanced error handling**: Added network error detection and better error messages
- ✅ **Environment setup**: Created detailed setup instructions
- ✅ **Token management**: Improved JWT token handling and error recovery
- ✅ **Demo mode**: Added `mockDemoLogin` for demo pages without backend

## Demo Mode vs Authenticated Mode

### Demo Mode (Before Login)
- Uses mock data for immediate demo experience
- No backend required for basic functionality
- Perfect for showcasing the UI/UX
- Access via `mockDemoLogin()` function

### Authenticated Mode (After Login)
- Uses real API calls for full functionality
- Requires backend to be running
- Full data persistence and user management
- Access via `demoLogin()` or regular login

The frontend now provides the best of both worlds: instant demo experience and full backend integration! 