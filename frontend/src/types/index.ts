// Type definitions for CoinCraft application 

// User Role Enum (matches backend exactly)
export type UserRole = 'parent' | 'teacher' | 'younger_child' | 'older_child'

// Core User Interface
export interface User {
  id: string
  name: string
  email: string
  role: UserRole
  avatar_url?: string
  created_at: Date
  updated_at: Date
  is_active: boolean
  is_superuser: boolean
  is_verified: boolean
}

// User with profiles
export interface UserWithProfiles extends User {
  child_profile?: ChildProfile
  parent_profile?: ParentProfile
  teacher_profile?: TeacherProfile
}

// Profile Interfaces
export interface ChildProfile {
  id: string
  user_id: string
  age: number
  coins: number
  level: number
  streak_days: number
  last_activity_date?: Date
  parent_id?: string
}

export interface ParentProfile {
  id: string
  user_id: string
  exchange_rate: number
  auto_approval_limit: number
  require_approval: boolean
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

// Transaction Interface 
export interface Transaction {
  id: string
  user_id: string
  type: 'earn' | 'spend' | 'save'
  amount: number
  description: string
  category?: string
  source?: string
  reference_id?: string
  reference_type?: 'goal' | 'task' | 'activity' | 'shop' | 'redemption'
  created_at: Date
}

// Goal Interface
export interface Goal {
  id: string
  user_id: string
  title: string
  description?: string
  target_amount: number
  current_amount: number
  icon?: string
  color?: string
  deadline?: Date
  is_completed: boolean
  created_at: Date
  updated_at: Date
}

// Task Interface 
export interface Task {
  id: string
  title: string
  description?: string
  coins_reward: number
  assigned_by: string
  assigned_to: string
  status: 'pending' | 'in_progress' | 'completed' | 'approved' | 'rejected'
  due_date?: Date
  requires_approval: boolean
  completed_at?: Date
  approved_at?: Date
  created_at: Date
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

// Module Interface 
export interface Module {
  id: string
  title: string
  description: string
  category?: string
  difficulty: 'easy' | 'medium' | 'hard'
  estimated_duration?: number
  points_reward: number
  created_by: string
  is_published: boolean
  created_at: Date
  updated_at: Date
  user_progress?: Record<string, any>
}

// Class Interface 
export interface Class {
  id: string
  name: string
  description?: string
  teacher_id: string
  class_code: string
  is_active: boolean
  created_at: Date
  students_count: number
  average_performance: number
}

// ShopItem Interface 
export interface ShopItem {
  id: string
  name: string
  description?: string
  price: number
  category?: string
  emoji?: string
  available: boolean
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

// Redemption Request Interface 
export interface RedemptionRequest {
  id: string
  user_id: string
  coins_amount: number
  cash_amount: number
  description?: string
  status: 'pending' | 'approved' | 'rejected'
  approved_by?: string
  approved_at?: Date
  created_at: Date
  child?: Record<string, any>
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

// Student Interface
export interface Student {
  user_id: string
  name: string
  email: string
  avatar_url?: string
  age?: number
  level?: number
  performance_score?: number
  needs_support?: boolean
  last_activity_date?: Date
  modules_completed?: number
  total_time_spent?: number
  progress?: Record<string, any>
}

// Dashboard Data Interface
export interface DashboardData {
  user_stats: Record<string, any>
  recent_transactions: Transaction[]
  active_goals: Goal[]
  achievements: Achievement[]
  learning_modules?: Module[]
}

// Activity Interface 
export interface Activity {
  id: string
  title: string
  description: string
  type: string
  difficulty: string
  coins: number
  duration: number
  completed: boolean
  icon: string
  category: string
  age_group: string
}

// Auth Response Interface 
export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
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