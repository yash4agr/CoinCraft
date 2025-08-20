## Frontend–Backend Integration (Vue 3 + Pinia + Axios → FastAPI)

### Overview
- **Frontend**: Vue 3 + TypeScript + Pinia
- **HTTP**: Axios instance in `frontend/src/services/http.ts`
- **API layer**: `frontend/src/services/api.ts` centralizes calls
- **State**: Pinia stores under `frontend/src/stores/*`
- **Types & mappers**: `frontend/src/types/index.ts`, `frontend/src/utils/typeMappers.ts`
- **Routing/guards**: `frontend/src/router/index.ts`

### HTTP Client & JWT Flow
- `httpClient` base URL: `import.meta.env.VITE_API_URL` (default `http://localhost:8000`)
- Interceptors:
  - Request: reads `localStorage.auth_token`, sets `Authorization: Bearer <token>`
  - Response: on 401, clears token and redirects to `/login`
- Token manager (`tokenManager`): helper to get/set/remove token in `localStorage`

### Authentication (Pinia `auth` store)
File: `frontend/src/stores/auth.ts`
- `login({ username, password })`:
  - Calls `apiService.login()` → `POST /api/auth/jwt/login` with URL-encoded form
  - Stores `access_token` in `localStorage.auth_token`
  - Calls `getCurrentUser()` to populate `user` (mapped via `mapBackendUser`)
  - If role is child/teen, calls `getCoins(user.id)` and annotates `user.coins`
- `register({ email, password, name, role, avatar_url? })`:
  - Calls `POST /api/auth/register` (custom backend) → returns token + user
  - Stores token and user, similar to login flow
- `checkAuth()`:
  - Validates token by calling `GET /api/users/me` and refreshes `user`
- `logout()`:
  - Calls `apiService.logout()` then clears all client-side state and `localStorage`
- `initializeAuth()`:
  - Restores `token` and `user` from `localStorage` on app start, then calls `checkAuth()`

Frontend storage keys used:
- `auth_token`: JWT token
- `auth_user`: serialized user object

### API Service (`apiService`)
File: `frontend/src/services/api.ts`
- Auth
  - `login` → `POST /api/auth/jwt/login` (form), then `GET /api/users/me`
  - `register` → `POST /api/auth/register`
  - `logout` → `POST /api/auth/jwt/logout` (try/catch) and remove token
- Users
  - `getCurrentUser` → `GET /api/users/me`
  - `getUserProfile(id)` → `GET /api/users/{id}`
  - `updateUserProfile(id, data)` → `PUT /api/users/{id}`
  - `getCoins(userId)` → `GET /api/users/{userId}/coins`
  - `updateUserCoins(userId, coins)` → `POST /api/users/{userId}/coins`
- Goals
  - `getGoals(userId)` → `GET /api/users/{userId}/goals`
  - `createGoal(userId, goalData)` → `POST /api/users/{userId}/goals`
  - `updateGoal(goalId, updates)` → `POST /api/goals/{goalId}` (partial)
  - `updateGoalAmount(goalId, amount)` → `POST /api/goals/{goalId}/amount`
  - `deleteGoal(goalId)` → `DELETE /api/goals/{goalId}`
  - `addGoalProgress(goalId, amount)` → `PUT /api/goals/{goalId}/progress`
  - `contributeToGoal(userId, goalId, amount)` → `POST /api/users/{userId}/goals/{goalId}/contribute`
- Transactions
  - `getTransactions(userId)` → `GET /api/users/{userId}/transactions` (note: in `transactions.py` shape is `TransactionList`)
  - `createTransaction(userId, data)` → `POST /api/users/{userId}/transactions`
- Parent dashboards & actions
  - `getParentDashboard()` → `GET /api/parent/dashboard`
  - `createChild()` → `POST /api/parent/children`
  - `getChildProgress(childId)` → `GET /api/parent/children/{childId}/progress`
  - `getParentTasks()` → `GET /api/parent/tasks`
  - `createParentTask()` → `POST /api/parent/tasks`
  - `approveTask(taskId)` → `PUT /api/parent/tasks/{taskId}/approve`
  - Redemptions: `getRedemptionRequests()`, `approveRedemption(id)`, `rejectRedemption(id)`
- Teacher dashboards & classes/modules
  - `getTeacherDashboard()` → `GET /api/teacher/dashboard`
  - Classes: `getTeacherClasses()`, `createClass()`, `getClassDetails(id)`, `addStudentToClass()`, `removeStudentFromClass()`, `updateClass()`
  - Modules: `getTeacherModules()`, `createModule()`, `getModules()` alias
  - Analytics: `getPerformanceAnalytics()`
- Teen
  - Goals/Budget/Analytics and conversion requests under `/api/teen/*`
- Activities & Learning Modules
  - `getActivities()`, `getActivityDetails(id)`, `getLearningModules()`, `completeLearningModule(id)`, `completeActivity(id)`
- Generic `request(url, options)` helper for legacy calls

### Pinia Stores and Their Backend Connections

1) `auth` store
- Handles login/register/logout, token storage, user loading, and token validation
- Calls: `/api/auth/jwt/login`, `/api/auth/register`, `/api/users/me`, `/api/users/{id}/coins`

2) `user` store
- Child/Teen oriented profile, goals, transactions, shop
- Calls: `createTransaction`, `updateUserCoins`, `createGoal`, `updateGoal`, `updateGoalAmount`
- Uses computed helpers, persists portions to localStorage for UX

3) `parent` store
- Family dashboard, children, tasks, redemptions
- Calls: `/api/parent/dashboard`, `/api/parent/children`, `/api/parent/tasks`, `/api/parent/redemptions`, approval endpoints

4) `teacher` store
- Classes, analytics, modules
- Calls: `/api/teacher/dashboard`, classes CRUD endpoints under teacher and generic classes router, teacher modules endpoints
- Note: Current backend lacks `grade` column on `Class`; teacher store maps `grade` if present in responses

5) `dashboard` store
- Unified child/teen activity view (mix of mock and server data)
- Calls: `getDashboardData(userRole)` → role mapping to `/api/parent|teacher|child|teen/dashboard`
- Also loads activities/modules via `getModules()` (teacher modules) as a proxy for available activities

### Router Guards and Store Bootstrapping
File: `frontend/src/router/index.ts`
- On navigation, restores auth, verifies role-based access, redirects to correct dashboard
- If authenticated, sets profile into `user` store and loads user/dashboard data as needed

### Type Mappers
File: `frontend/src/utils/typeMappers.ts`
- Convert backend ISO strings to Date objects where needed
- Enrich `User` with `fullName`, `username`, `coins`, `level`
- Normalize arrays via dedicated `mapBackend*` helpers

### What’s Connected Today vs Mocked
- Fully connected:
  - Auth login/register/me
  - Parent dashboard, children management, tasks, redemptions
  - Goals CRUD, contributions, progress updates
  - Activities/modules listing and completion
  - Shop items, owned items, purchases
  - Teen budget/goals (per teen router)
- Partially/Mocked:
  - `dashboard` store uses mock data for unauthenticated/demo mode
  - Teacher analytics aggregates are computed server-side but with basic heuristics

### Integration Gaps / Fix List
- Align logout to use a single endpoint or go pure client-side token removal
- Standardize transactions GET shape (array vs `TransactionList`) and update callers
- Add `grade` column to `Class` model or remove its usage in teacher endpoints/stores
- Ensure `difficulty` values are one of `easy|medium|hard` end-to-end
- Avoid duplicate user-goals/transactions implementations across routers to reduce drift

### Environment
- Frontend reads `VITE_API_URL`; create `.env`:
```
VITE_API_URL=http://localhost:8000
```


