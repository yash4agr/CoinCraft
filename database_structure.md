## CoinCraft Database Schema (SQLAlchemy Models)

Source: `backend/models.py`

### Base
- Declarative base: `Base = declarative_base()`

### Enums
- `UserRoleEnum`: `parent | teacher | younger_child | older_child`

### Tables
- `users` (extends FastAPI Users `SQLAlchemyBaseUserTable[str]`)
  - id (str, PK, uuid4)
  - email (str, unique, indexed)
  - hashed_password (str)
  - is_active (bool, default True)
  - is_superuser (bool, default False)
  - is_verified (bool, default False)
  - name (str)
  - role (str) — one of UserRoleEnum values
  - avatar_url (str, nullable)
  - created_at (datetime, default now)
  - updated_at (datetime, default now / onupdate)
  - relationships:
    - `child_profile: ChildProfile` (one-to-one)
    - `parent_profile: ParentProfile` (one-to-one)
    - `teacher_profile: TeacherProfile` (one-to-one)
    - `goals: Goal[]`
    - `transactions: Transaction[]`
    - `achievements: UserAchievement[]`
    - `tasks_assigned: Task[]` (as assignee)
    - `tasks_created: Task[]` (as assigner)
    - `redemption_requests: RedemptionRequest[]`

- `child_profiles`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id, unique)
  - age (int)
  - coins (int, default 0)
  - level (int, default 1)
  - streak_days (int, default 0)
  - last_activity_date (datetime, nullable)
  - parent_id (str, FK users.id, nullable)
  - relationships:
    - `user: User`
    - `parent: User`

- `parent_profiles`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id, unique)
  - exchange_rate (float, default 0.10) — $ per coin
  - auto_approval_limit (int, default 500)
  - require_approval (bool, default True)
  - relationships:
    - `user: User`

- `teacher_profiles`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id, unique)
  - school_name (str, nullable)
  - grade_level (str, nullable)
  - subject (str, nullable)
  - relationships:
    - `user: User`
    - `classes: Class[]`

- `goals`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id)
  - title (str, required, max 200 chars)
  - description (text, nullable)
  - target_amount (int, required)
  - current_amount (int, default 0)
  - icon (str, nullable, max 100 chars) — Remix icon class names (e.g., 'ri-bike-line', 'ri-gamepad-line')
  - color (str, nullable, max 50 chars) — CSS color values (e.g., 'blue', 'green', 'purple')
  - deadline (datetime, nullable)
  - is_completed (bool, default False) — Tracks goal completion status
  - created_at (datetime, default now)
  - updated_at (datetime, default now / onupdate)
  - relationships:
    - `user: User`
  
  **Sample Data (Current Database):**
  - 5 total goals across 3 users
  - 2 completed goals (is_completed = 1) for user 'd8a9a61e-7343-43d0-b57a-8b8d23b7a889'
  - 3 active goals for other users
  - Icon system uses Remix icon classes (ri-*)
  - Color system supports standard CSS colors

- `transactions`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id)
  - type (str, required: `earn|spend|save`)
  - amount (int, required)
  - description (str, required)
  - category (str, nullable)
  - source (str, nullable)
  - reference_id (str, nullable)
  - reference_type (str, nullable: `goal|task|activity|shop|redemption`)
  - created_at (datetime, default now)
  - relationships:
    - `user: User`

- `achievements`
  - id (str, PK, uuid4)
  - title (str)
  - description (text)
  - icon (str, nullable)
  - rarity (str, default "common")
  - points_reward (int, default 0)
  - criteria (JSON, nullable)
  - created_at (datetime, default now)
  - relationships:
    - `user_achievements: UserAchievement[]`

- `user_achievements`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id)
  - achievement_id (str, FK achievements.id)
  - earned_at (datetime, default now)
  - relationships:
    - `user: User`
    - `achievement: Achievement`

- `modules`
  - id (str, PK, uuid4)
  - title (str, required)
  - description (text, required)
  - category (str, nullable)
  - difficulty (str, default "easy")
  - estimated_duration (int, nullable)
  - points_reward (int, default 0)
  - created_by (str, FK users.id)
  - is_published (bool, default False)
  - created_at (datetime)
  - updated_at (datetime onupdate)
  - relationships:
    - `sections: ModuleSection[]`
    - `user_progress: UserModuleProgress[]`

- `module_sections`
  - id (str, PK, uuid4)
  - module_id (str, FK modules.id)
  - title (str)
  - type (str: `lesson|quiz|game`)
  - content (text, nullable)
  - order_index (int)
  - points_reward (int, default 0)
  - relationships:
    - `module: Module`
    - `quiz_questions: QuizQuestion[]`

- `quiz_questions`
  - id (str, PK, uuid4)
  - section_id (str, FK module_sections.id)
  - question_text (text)
  - explanation (text, nullable)
  - points (int, default 1)
  - order_index (int)
  - relationships:
    - `section: ModuleSection`
    - `options: QuizOption[]`

- `quiz_options`
  - id (str, PK, uuid4)
  - question_id (str, FK quiz_questions.id)
  - option_text (str)
  - is_correct (bool, default False)
  - order_index (int)
  - relationships:
    - `question: QuizQuestion`

- `user_module_progress`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id)
  - module_id (str, FK modules.id)
  - progress_percentage (float, default 0)
  - is_completed (bool, default False)
  - score (float, nullable)
  - time_spent (int, default 0)
  - started_at (datetime, default now)
  - completed_at (datetime, nullable)
  - relationships:
    - `user: User`
    - `module: Module`

- `tasks`
  - id (str, PK, uuid4)
  - title (str)
  - description (text, nullable)
  - assigned_by (str, FK users.id)
  - assigned_to (str, FK users.id)
  - coins_reward (int)
  - due_date (datetime, nullable)
  - status (str, default `pending`)
  - requires_approval (bool, default True)
  - completed_at (datetime, nullable)
  - approved_at (datetime, nullable)
  - created_at (datetime, default now)
  - relationships:
    - `assigner: User`
    - `assignee: User`

- `classes`
  - id (str, PK, uuid4)
  - name (str)
  - teacher_id (str, FK teacher_profiles.id)
  - description (text, nullable)
  - class_code (str, unique)
  - is_active (bool, default True)
  - created_at (datetime, default now)
  - relationships:
    - `teacher: TeacherProfile`
    - `students: ClassStudent[]`

- `class_students`
  - id (str, PK, uuid4)
  - class_id (str, FK classes.id)
  - student_id (str, FK users.id)
  - enrolled_at (datetime, default now)
  - relationships:
  - `class_obj: Class`
  - `student: User`

- `redemption_requests`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id)
  - coins_amount (int)
  - cash_amount (float)
  - description (str, nullable)
  - status (str, default `pending`)
  - approved_by (str, FK users.id, nullable)
  - approved_at (datetime, nullable)
  - created_at (datetime, default now)
  - relationships:
    - `user: User`
    - `approver: User`

- `shop_items`
  - id (str, PK, uuid4)
  - name (str)
  - description (text, nullable)
  - price (int)
  - category (str, nullable)
  - emoji (str, nullable)
  - created_at (datetime, default now)
  - relationships:
    - `owners: UserOwnedItem[]` (cascade on delete)

- `user_owned_items`
  - id (str, PK, uuid4)
  - user_id (str, FK users.id, ondelete CASCADE)
  - shop_item_id (str, FK shop_items.id, ondelete CASCADE)
  - acquired_at (datetime, default now)
  - relationships:
    - `shop_item: ShopItem`

### Notes / Inconsistencies to Address
- `Class` model lacks a `grade` column, but several teacher endpoints reference `class_obj.grade`. Either add this column or remove usages.
- Ensure `difficulty` values in modules are one of `easy|medium|hard` across code paths.

## Current Database State (Last Updated: 2025-08-16)

### Goals Table Status
- **Total Goals**: 5
- **Completed Goals**: 2 (40% completion rate)
- **Active Goals**: 3
- **Users with Goals**: 3 unique users

### Recent Goal Completions
1. **Goal ID**: `99bf7bcd-c800-4934-95bb-07c4266c2811`
   - Title: "New"
   - User: `d8a9a61e-7343-43d0-b57a-8b8d23b7a889` (hello)
   - Completed: 2025-08-16 12:58:48
   - Target: 10 coins

2. **Goal ID**: `4c21c325-c547-4871-b8cd-41f0fe47455c`
   - Title: "asd"
   - User: `d8a9a61e-7343-43d0-b57a-8b8d23b7a889` (hello)
   - Completed: 2025-08-16 12:45:54
   - Target: 10 coins

### Database Schema Validation
- ✅ All required fields present
- ✅ Foreign key constraints working
- ✅ Boolean fields properly implemented
- ✅ Datetime fields with proper defaults
- ✅ Icon and color systems functional

### Current User Relationships
**Family 1: Johnson Family**
- Parent: `b5383341-4eee-45fb-8762-a6d1f2a48118` (Johnson)
- Children: 6 children including:
  - `d8a9a61e-7343-43d0-b57a-8b8d23b7a889` (hello) - Has 2 completed goals
  - `2fd5b20c-09a6-438c-a473-86841ef25917` (bob)
  - `1714f3c7-a8f8-4af1-b728-eac792ec0a37` (alan)
  - `155088ca-98a9-4bfc-bd11-ab33c48174f0` (bob22)
  - `1180068d-c8a7-4fcb-bf5c-b8101769bf16` (lol)
  - `a9ad4830-f2f6-4f0b-87cc-442ead1d6b9a` (mary)

**Family 2: Sarah Johnson Family**
- Parent: `7599ee27-7394-46fe-87f8-4478885c3f76` (Sarah Johnson)
- Children: 4 children including:
  - `345efb1f-91f4-4b71-a9a4-2b913a5073f7` (Luna Smith) - Has 2 active goals
  - `6b135010-e00f-455e-a732-9172f86cfdf6` (Harry Johnson) - Has 1 active goal
  - `43f02e05-30c8-4cab-92d0-4d83ebede844` (Child 1)
  - `11746b1d-b831-4a75-ab85-22ba2b5a4669` (newChild)
  - `abd29874-61ae-4044-a138-109d950483bd` (abcd)

**Other Families:**
- Multiple other parent-child relationships exist
- Some test users without family connections


