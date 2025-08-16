## CoinCraft Backend: Architecture, Endpoints, and Auth (JWT)

### High-level Architecture
- **Framework**: FastAPI with async SQLAlchemy
- **Entry**: `backend/main.py`
  - Creates app with lifespan that runs `create_db_and_tables()`
  - CORS enabled for localhost dev ports
  - Mounts multiple routers under `/api` (see below)
  - Serves OpenAPI YAML at `/openapi.yaml` and a custom docs page at `/docs`
- **Auth**: FastAPI Users with JWT (Bearer tokens)
  - Config in `backend/auth.py`
  - Token lifetime: 7 days
  - Secret: `JWT_SECRET` env var (falls back to a placeholder default)
- **DB**: Async SQLAlchemy + SQLite by default (`sqlite+aiosqlite:///./coincraft.db`)
- **Models**: See `backend/models.py`
- **Validation Schemas**: See `backend/schemas.py`

### JWT Authentication Flow
- Login endpoint (FastAPI Users): `POST /api/auth/jwt/login`
  - Body: `application/x-www-form-urlencoded` with `username`, `password`
  - Response: `{ access_token, token_type }`
- Register and auto-login (custom): `POST /api/auth/register`
  - Body: JSON `{ email, password, name, role, avatar_url? }`
  - Creates `User` and role profile; returns `{ access_token, token_type: "bearer", user }`
- Logout (client-side):
  - Custom: `POST /api/auth/logout` (no-op server-side; client should delete token)
  - Note: Client currently calls `POST /api/auth/jwt/logout` (FastAPI Users), which may or may not be available depending on version. Prefer the custom endpoint or remove the call and clear token client-side.
- Token usage:
  - Frontend stores token in `localStorage.auth_token`
  - Axios interceptor sets `Authorization: Bearer <token>` for all requests
  - Backends protect routes with `Depends(current_active_user)`

### Routing Overview
- Auth routes
  - `POST /api/auth/jwt/login` (FastAPI Users)
  - `POST /api/auth/register` (custom, returns token + user)
  - `POST /api/auth/logout` (custom; no server invalidation)
  - `POST /api/auth/forgot-password`, `POST /api/auth/reset-password` (FastAPI Users defaults)
  - `POST /api/auth/request-verify-token`, `POST /api/auth/verify` (FastAPI Users defaults)

- Users (`backend/routers/users.py`, prefix `/api/users`)
  - `GET /api/users/me` → current user (`UserRead`)
  - `GET /api/users/{user_id}` → user by id (or `me`) (`UserRead`)
  - `PUT /api/users/{user_id}` → update own profile (`UserRead`)
  - Children management (parent-only):
    - `POST /api/users/{parent_id}/children` → create child account (`UserRead`)
    - `GET  /api/users/{parent_id}/children` → list children (`UserRead[]`)
    - `PUT  /api/users/children/{child_id}` → update a child profile → returns updated `UserRead`
  - Convenience child info:
    - `GET  /api/users/{user_id}/coins` → child coins (int)
    - `POST /api/users/{user_id}/coins` → set child coins (int)
    - `GET  /api/users/{user_id}/transactions` → child transactions (`TransactionRead[]`)
    - `GET  /api/users/{user_id}/goals` → child goals (`GoalRead[]`)
    - `POST /api/users/{user_id}/goals` → create goal (`GoalRead`)

- Goals (`backend/routers/goals.py`, prefix `/api`)
  - `GET    /api/users/{user_id}/goals` → list goals (`GoalRead[]`)
  - `POST   /api/users/{user_id}/goals` → create goal (`GoalRead`)
  - `PUT    /api/users/{user_id}/goals/{goal_id}` → update goal (`GoalRead`)
  - `DELETE /api/users/{user_id}/goals/{goal_id}` → delete goal
  - `POST   /api/users/{user_id}/goals/{goal_id}/contribute` → deduct coins, add to goal; returns `{ goal, transaction, new_coin_balance }`
  - `PUT    /api/goals/{goal_id}/progress` → add amount to `current_amount` (`GoalRead`)
  - `POST   /api/goals/{goal_id}/amount` → set `current_amount` (absolute) (`GoalRead`)
  - `POST   /api/goals/{goal_id}` → partial update (`GoalRead`)

- Transactions (`backend/routers/transactions.py`, prefix `/api`)
  - `GET  /api/users/{user_id}/transactions` → `TransactionList { transactions, total_count, weekly_total, monthly_total }`
  - `POST /api/users/{user_id}/transactions` → create transaction; returns `{ transaction, new_coin_balance }`

- Activities & Learning Modules (`backend/routers/modules.py`, prefix `/api`)
  - `GET  /api/activities?difficulty=&category=&age_group=&completed=` → `ActivityRead[]`
  - `GET  /api/activities/{activity_id}` → module details + `user_progress`
  - `POST /api/activities/{activity_id}/complete` → records progress; if `is_completed`, awards coins
  - `GET  /api/learning-modules?difficulty=&category=&age_group=&created_by=` → `ModuleRead[]` (enriched with progress)
  - `POST /api/learning-modules/{module_id}/complete` → alias of complete activity

- Shop (`backend/routers/shop.py`, prefix `/api`)
  - `GET  /api/shop/items` → shop items
  - `GET  /api/shop/owned_items` → items owned by current user
  - `POST /api/shop/{user_id}/purchase` → purchase by id; validates coins/ownership

- Dashboard (`backend/routers/dashboard.py`, prefix `/api`)
  - `GET  /api/dashboard/{user_role}` → role-specific dashboard
  - `GET  /api/progress-goals/{user_id}` → daily goals (children)
  - `PUT  /api/progress-goals/{goal_id}/update` → update daily goal progress (simple response)

- Parent (`backend/routers/parent.py`, prefix `/api/parent`)
  - `GET  /api/parent/dashboard` → `ParentDashboardResponse`
  - `POST /api/parent/children` → create child (returns `ChildCreateResponse`)
  - `GET  /api/parent/children/{child_id}/progress` → rich progress object
  - `GET  /api/parent/tasks` → tasks for all children
  - `POST /api/parent/tasks` → create a task (returns `TaskCreateResponse`)
  - `PUT  /api/parent/tasks/{task_id}/approve` → approve task; awards coins (`TaskApprovalResponse`)
  - `GET  /api/parent/redemptions` → redemption requests for children
  - `PUT  /api/parent/settings` → update parent settings

- Teacher (`backend/routers/teacher.py`, prefix `/api/teacher`)
  - `GET  /api/teacher/dashboard` → composite analytics + classes overview
  - `POST /api/teacher/classes` → create class (random 6-char `class_code`)
  - `GET  /api/teacher/classes` → list classes (teacher-owned)
  - `GET  /api/teacher/classes/{class_id}` → class details + student progress
  - `POST /api/teacher/classes/{class_id}/students` → add student by email
  - `POST /api/teacher/modules` → create module (sections + quiz supported)
  - `GET  /api/teacher/modules` → list modules created by teacher (with stats)
  - `GET  /api/teacher/analytics/performance` → aggregated performance metrics

- Classes (generic) (`backend/routers/classes.py`, prefix `/api`)
  - `GET  /api/teachers/{teacher_id}/classes` → list classes for teacher id
  - `POST /api/teachers/{teacher_id}/classes` → create class for teacher id
  - `PUT  /api/classes/{class_id}` → update class
  - `DELETE /api/classes/{class_id}` → delete class
  - `GET  /api/classes/{class_id}/students` → list students for class
  - `POST /api/classes/{class_id}/students` → add student by email
  - `DELETE /api/classes/{class_id}/students/{student_id}` → remove student

- Redemptions (`backend/routers/redemptions.py`, prefix `/api`)
  - `GET  /api/users/{user_id}/conversion-requests`
  - `POST /api/users/{user_id}/conversion-requests`
  - `GET  /api/parents/{parent_id}/redemption-requests`
  - `PUT  /api/redemption-requests/{request_id}/approve`
  - `PUT  /api/redemption-requests/{request_id}/reject`

- Child (`backend/routers/child.py`, prefix `/api/child`) and Teen (`backend/routers/teen.py`, prefix `/api/teen`)
  - Both provide dashboard, goals, activities, transactions, stats (child) and budget (teen) flows tailored for the role.

### Important Response Models (schemas)
- Users: `UserRead`, `UserWithProfilesRead`
- Goals: `GoalRead`, `GoalCreate`, `GoalUpdate`, `GoalContribution`
- Transactions: `TransactionRead`, `TransactionList`
- Tasks: `TaskRead`, `TaskCreate`, `TaskUpdate`
- Modules/Activities: `ModuleRead`, `ActivityRead`
- Dashboards: `ChildDashboardResponse`, `ParentDashboardResponse`, `TeacherDashboardResponse`, `DashboardStats`
- Redemptions: `RedemptionRequestRead`, `RedemptionRequestCreate`
- Auth: `AuthResponse`

### Known Integration Risks / Mismatches to Fix
- **Duplicate endpoints**: `/api/users/{id}/goals` and `/api/users/{id}/transactions` exist in both `users.py` and dedicated routers (`goals.py`, `transactions.py`) with the same paths. Unify to a single implementation to avoid conflicts and schema drift.
- **Teacher `Class` model vs usage**: `teacher.py` references `class_obj.grade`, but `models.Class` has no `grade` column. Either add the column or remove references to `grade`.
- **Module difficulty values**: `teacher.py` sets `difficulty="beginner"`; schema and filters expect one of `easy|medium|hard`. Use those values consistently.
- **Logout endpoint**: Frontend calls `/api/auth/jwt/logout`; the custom route is `/api/auth/logout`. Align or remove server call and only clear token client-side.
- **Transactions shape**: `transactions.py` `GET` returns `TransactionList`; `users.py` `GET` returns `TransactionRead[]`. Frontend expects an array in some places. Standardize the API and update the client accordingly.

### Health and Docs
- `GET /health` → `{ status: "OK" }`
- `GET /openapi.yaml` → OpenAPI YAML
- `GET /docs` → Swagger UI (serves `/openapi.yaml`)


