// Type definitions for CoinCraft application 
// Updated to match backend schemas.py response models

// User Role Enum - matches backend UserRoleEnum
export type UserRole = 'parent' | 'teacher' | 'younger_child' | 'older_child'

// Core User Interface - aligned with backend UserRead schema
export interface User {
  id: string
  name: string                    // Backend field (not fullName)
  email: string
  role: UserRole
  avatar_url?: string            // Backend field (not avatar)
  created_at: string             // ISO string from backend (not Date)
  updated_at: string             // ISO string from backend (not Date)
  is_active: boolean
  is_superuser: boolean
  is_verified: boolean
  
  // Computed/derived fields for frontend compatibility
  fullName?: string              // Computed from name
  username?: string              // Computed from email
  avatar?: string               // Alias for avatar_url
  coins?: number                // From child_profile if present
  level?: number                // From child_profile if present
  createdAt?: Date              // Computed Date object from created_at
  updatedAt?: Date              // Computed Date object from updated_at
}

// User with profiles - matches backend UserWithProfilesRead
export interface UserWithProfiles extends User {
  child_profile?: ChildProfile
  parent_profile?: ParentProfile
  teacher_profile?: TeacherProfile
}

// Profile Interfaces - aligned with backend schemas
export interface ChildProfile {
  id: string
  user_id: string
  age: number
  coins: number                  // Default 0 in backend
  level: number                  // Default 1 in backend
  streak_days: number            // Default 0 in backend
  last_activity_date?: string    // ISO string from backend (not Date)
  parent_id?: string
}

export interface ParentProfile {
  id: string
  user_id: string
  exchange_rate: number          // Default 0.10 in backend
  auto_approval_limit: number    // Default 500 in backend
  require_approval: boolean      // Default true in backend
}

export interface TeacherProfile {
  id: string
  user_id: string
  school_name?: string
  grade_level?: string
  subject?: string
}

export interface TeacherProfile {
  id: string
  user_id: string
  school_name?: string
  grade_level?: string
  subject?: string
}

// Legacy interfaces for backward compatibility (will be removed later)
export interface Child extends User {
  age: number
  coins: number
  level: number
  parentId: string
  classId?: string
  avatarColor?: string
  password?:string
}

export interface Parent extends User {
  children: string[] // child IDs
}

export interface Teacher extends User {
  classes: string[] // class IDs
}

// Transaction Interface - aligned with backend TransactionRead schema
export interface Transaction {
  id: string
  user_id?: string
  type: 'earn' | 'spend' | 'save'    // Backend uses pattern validation
  amount: number                      // Must be > 0 in backend
  description: string                 // Required in backend
  category?: string
  source?: string
  reference_id?: string
  reference_type?: 'goal' | 'task' | 'activity' | 'shop' | 'redemption'  // Backend pattern validation
  created_at: string                  // ISO string from backend (not Date)
  
  // Computed fields for frontend compatibility
  createdAt?: Date                    // Computed Date object
}

// Transaction List - matches backend TransactionList schema
export interface TransactionList {
  transactions: Transaction[]
  total_count: number
  weekly_total: number
  monthly_total: number
}

// Goal Interface - aligned with backend GoalRead schema
export interface Goal {
  id: string
  user_id: string
  title: string
  description?: string
  target_amount: number
  current_amount: number         // Default 0 in backend
  icon?: string
  color?: string
  deadline?: string              // ISO string from backend (not Date)
  is_completed: boolean          // Default false in backend
  created_at: string             // ISO string from backend (not Date)
  updated_at: string             // ISO string from backend (not Date)
  
  // Computed fields for frontend compatibility
  createdAt?: Date               // Computed Date object
  updatedAt?: Date               // Computed Date object
  deadlineDate?: Date            // Computed Date object from deadline
  unit?: string
}

export interface ChildProgress {
  child?: User 
  stats: DashboardStats 
  recent_activities: Activity[] 
  active_goals: Goal[] 
  completed_goals: Goal[] 
  achievements: Achievement[] 
  learning_modules: Module[] 
}

// Task Interface - aligned with backend TaskRead schema
export interface Task {
  id: string
  title: string                       // Required, min 1 max 200 chars
  description?: string
  coins_reward: number                // Must be > 0 in backend
  assigned_by: string
  assigned_to: string
  status: 'pending' | 'in_progress' | 'completed' | 'approved' | 'rejected'  // Backend pattern validation
  due_date?: string                   // ISO string from backend (not Date)
  requires_approval: boolean          // Default true in backend
  completed_at?: string               // ISO string from backend (not Date)
  approved_at?: string                // ISO string from backend (not Date)
  created_at: string                  // ISO string from backend (not Date)
  
  // Computed fields for frontend compatibility
  createdAt?: Date                    // Computed Date object
  dueDate?: Date                      // Computed Date object from due_date
  completedAt?: Date                  // Computed Date object
  approvedAt?: Date                   // Computed Date object

  // optional fields
  type?: string
  priority?: string
  recurring?: boolean
  allow_partial_completion?: boolean
  notify_on_due?: boolean
  photo_required?: boolean
  bonus_available?: boolean
  recurring_frequency?: string
  recurring_end?: string
}

// Notification Interface 
export interface Notification {
  id: string
  user_id: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  read: boolean
  action_url?: string
  created_at: Date
}

// Module Interface - aligned with backend ModuleRead schema
export interface Module {
  id: string
  title: string                       // Required, min 1 max 200 chars
  description: string                 // Required in backend
  category?: string
  difficulty: 'easy' | 'medium' | 'hard'  // Backend pattern validation, default 'easy'
  estimated_duration?: number
  points_reward: number               // Default 0 in backend
  created_by: string
  is_published: boolean               // Default false in backend
  created_at: string                  // ISO string from backend (not Date)
  updated_at: string                  // ISO string from backend (not Date)
  user_progress?: Record<string, any> // Optional user progress data
  
  // Computed fields for frontend compatibility
  createdAt?: Date                    // Computed Date object
  updatedAt?: Date                    // Computed Date object
}

// Class Interface - aligned with backend ClassRead schema
export interface Class {
  id: string
  name: string                        // Required, min 1 max 200 chars
  description?: string
  teacher_id: string
  class_code: string
  is_active: boolean                  // Default true in backend
  created_at: string                  // ISO string from backend (not Date)
  students_count?: number             // Default 0 in backend
  average_performance?: number        // Default 0.0 in backend
  
  // Computed fields for frontend compatibility
  createdAt?: Date                    // Computed Date object
}

// ShopItem Interface - aligned with backend ShopItemRead schema
export interface ShopItem {
  id: string
  name: string
  description?: string
  price: number                       // Required in backend
  category?: string
  emoji?: string
  available: boolean                  // Default true in backend
}

// Budget Interface 
export interface Budget {
  id: string
  user_id: string
  saving: number
  spending: number
  wants: number
  total_amount: number
  updated_at: Date
}

// ActivityProgress Interface 
export interface ActivityProgress {
  id: string
  user_id: string
  module_id: string
  progress: number
  completed: boolean
  score?: number
  time_spent: number
  started_at: Date
  completed_at?: Date
}

export interface FilterOptions {
  dateRange?: {
    start: Date
    end: Date
  }
  category?: string
  type?: string
  amount?: {
    min: number
    max: number
  }
}

export interface SortOptions {
  field: string
  direction: 'asc' | 'desc'
}

export interface PaginationOptions {
  page: number
  limit: number
  total: number
}


// Achievement Interface 
export interface Achievement {
  id: string
  title: string
  description: string
  icon?: string
  rarity: string
  points_reward: number
  earned_at?: Date
}

// Redemption Request Interface - aligned with backend RedemptionRequestRead schema
export interface RedemptionRequest {
  id: string
  user_id: string
  coins_amount: number                // Must be > 0 in backend
  cash_amount: number                 // Calculated by backend
  description?: string
  status: 'pending' | 'approved' | 'rejected' | 'completed'  // Default 'pending' in backend
  approved_by?: string
  approved_at?: string                // ISO string from backend (not Date)
  created_at: string                  // ISO string from backend (not Date)
  child?: Record<string, any>         // Child info for parent view
  
  // Computed fields for frontend compatibility
  createdAt?: Date                    // Computed Date object
  approvedAt?: Date                   // Computed Date object
}

// Redemption Settings Interface - aligned with backend RedemptionSettings schema
export interface RedemptionSettings {
  exchange_rate: number
  currency: string
  auto_approval_limit: number
  require_approval: boolean
  notify_on_request: boolean
  processing_time: string
  daily_limit: number
  weekly_limit: number
  monthly_limit: number
  allow_savings_override: boolean
  track_spending_categories: boolean
}

// Budget Category Interface 
export interface BudgetCategory {
  id: string
  user_id: string
  name: string
  budget_amount: number
  spent_amount: number
  icon?: string
  color?: string
  created_at: Date
  updated_at: Date
}

// Budget Allocation Interface 
export interface BudgetAllocation {
  saving: number
  spending: number
  wants: number
}

// Student Interface - aligned with backend StudentRead schema
export interface Student {
  user_id: string
  name: string
  email: string
  avatar_url?: string
  age?: number
  level?: number
  performance_score?: number
  needs_support?: boolean
  last_activity_date?: string         // ISO string from backend (not Date)
  modules_completed?: number
  total_time_spent?: number
  progress?: Record<string, any>
  
  // Computed fields for frontend compatibility
  lastActivityDate?: Date             // Computed Date object
}

// Dashboard Stats - matches backend DashboardStats schema
export interface DashboardStats {
  total_coins: number
  level: number
  streak_days: number
  goals_count: number
  completed_tasks: number
}

// Dashboard Response Types - aligned with backend response schemas
export interface ParentDashboardResponse {
  user: User
  stats: DashboardStats
  children: User[]
  recent_transactions: Transaction[]
}

export interface TeacherDashboardResponse {
  user: User
  stats: DashboardStats
  classes: Class[]
  recent_activities: Activity[]
}

export interface ChildDashboardResponse {
  user: User
  stats: DashboardStats
  goals: Goal[]
  activities: Activity[]
  achievements: Achievement[]
  learning_modules: Module[]
}

// Legacy Dashboard Data Interface (for backward compatibility)
export interface DashboardData {
  user_stats?: Record<string, any>
  stats?: DashboardStats | Record<string, any>
  recent_transactions?: Transaction[]
  transactions?: Transaction[]
  active_goals?: Goal[]
  goals?: Goal[]
  achievements?: Achievement[]
  learning_modules?: Module[]
  pending_tasks?: Task[]
  tasks?: Task[]
  activities?: Activity[]
  children?: User[]
  classes?: Class[]
  [key: string]: any // Allow additional properties
}

// Activity Interface - aligned with backend ActivityRead schema
export interface Activity {
  id: number
  title: string
  description: string
  difficulty: string
  coins: number
  color_scheme?: string | null
  emoji?: string | null
  button_text: string
  path?: string | null
  completed: boolean
}

// Auth Response Interface - aligned with backend AuthResponse schema
export interface AuthResponse {
  access_token: string
  token_type: string                  // Usually "bearer"
  user: User
}

// Legacy AuthResponse with refresh token (keeping for compatibility)
export interface AuthResponseWithRefresh extends AuthResponse {
  refresh_token: string
}

// Error Response Interfaces
export interface ErrorResponse {
  detail: string
  error_code?: string
  status_code: number
}

export interface ValidationErrorResponse {
  detail: Array<Record<string, any>>
}