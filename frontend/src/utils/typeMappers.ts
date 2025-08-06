/**
 * Type Mappers for converting backend response models to frontend-friendly types
 * Handles ISO string to Date conversions and computed fields
 */

import type { 
  User, Goal, Transaction, Task, Module, Class, RedemptionRequest, 
  Student, ChildProfile,
  ParentDashboardResponse, TeacherDashboardResponse, ChildDashboardResponse
} from '../types'

/**
 * Safely convert ISO string to Date object
 */
const parseISODate = (isoString?: string): Date | undefined => {
  if (!isoString) return undefined
  try {
    return new Date(isoString)
  } catch {
    return undefined
  }
}

/**
 * Extract username from email
 */
const extractUsername = (email: string): string => {
  return email?.split('@')[0] || 'user'
}

/**
 * Map backend User to frontend User with computed fields
 */
export const mapBackendUser = (backendUser: any): User => {
  return {
    ...backendUser,
    // Computed fields for frontend compatibility
    fullName: backendUser.name,
    username: extractUsername(backendUser.email),
    avatar: backendUser.avatar_url,
    createdAt: parseISODate(backendUser.created_at),
    updatedAt: parseISODate(backendUser.updated_at),
    // Add coins and level from child_profile if present
    coins: backendUser.child_profile?.coins,
    level: backendUser.child_profile?.level,
  }
}

/**
 * Map backend Goal to frontend Goal with computed Date fields
 */
export const mapBackendGoal = (backendGoal: any): Goal => {
  return {
    ...backendGoal,
    // Computed Date fields
    createdAt: parseISODate(backendGoal.created_at),
    updatedAt: parseISODate(backendGoal.updated_at),
    deadlineDate: parseISODate(backendGoal.deadline),
  }
}

/**
 * Map backend Transaction to frontend Transaction with computed Date fields
 */
export const mapBackendTransaction = (backendTransaction: any): Transaction => {
  return {
    ...backendTransaction,
    // Computed Date fields
    createdAt: parseISODate(backendTransaction.created_at),
  }
}

/**
 * Map backend Task to frontend Task with computed Date fields
 */
export const mapBackendTask = (backendTask: any): Task => {
  return {
    ...backendTask,
    // Computed Date fields
    createdAt: parseISODate(backendTask.created_at),
    dueDate: parseISODate(backendTask.due_date),
    completedAt: parseISODate(backendTask.completed_at),
    approvedAt: parseISODate(backendTask.approved_at),
  }
}

/**
 * Map backend Module to frontend Module with computed Date fields
 */
export const mapBackendModule = (backendModule: any): Module => {
  return {
    ...backendModule,
    // Computed Date fields
    createdAt: parseISODate(backendModule.created_at),
    updatedAt: parseISODate(backendModule.updated_at),
  }
}

/**
 * Map backend Class to frontend Class with computed Date fields
 */
export const mapBackendClass = (backendClass: any): Class => {
  return {
    ...backendClass,
    // Computed Date fields
    createdAt: parseISODate(backendClass.created_at),
  }
}

/**
 * Map backend RedemptionRequest to frontend RedemptionRequest with computed Date fields
 */
export const mapBackendRedemptionRequest = (backendRequest: any): RedemptionRequest => {
  return {
    ...backendRequest,
    // Computed Date fields
    createdAt: parseISODate(backendRequest.created_at),
    approvedAt: parseISODate(backendRequest.approved_at),
  }
}

/**
 * Map backend Student to frontend Student with computed Date fields
 */
export const mapBackendStudent = (backendStudent: any): Student => {
  return {
    ...backendStudent,
    // Computed Date fields
    lastActivityDate: parseISODate(backendStudent.last_activity_date),
  }
}

/**
 * Map backend ChildProfile to frontend ChildProfile with computed Date fields
 */
export const mapBackendChildProfile = (backendProfile: any): ChildProfile => {
  return {
    ...backendProfile,
    // Note: last_activity_date stays as string to match backend schema
  }
}

/**
 * Map arrays of backend items to frontend items
 */
export const mapBackendUsers = (backendUsers: any[]): User[] => {
  return backendUsers.map(mapBackendUser)
}

export const mapBackendGoals = (backendGoals: any[]): Goal[] => {
  return backendGoals.map(mapBackendGoal)
}

export const mapBackendTransactions = (backendTransactions: any[]): Transaction[] => {
  return backendTransactions.map(mapBackendTransaction)
}

export const mapBackendTasks = (backendTasks: any[]): Task[] => {
  return backendTasks.map(mapBackendTask)
}

export const mapBackendModules = (backendModules: any[]): Module[] => {
  return backendModules.map(mapBackendModule)
}

export const mapBackendClasses = (backendClasses: any[]): Class[] => {
  return backendClasses.map(mapBackendClass)
}

export const mapBackendRedemptionRequests = (backendRequests: any[]): RedemptionRequest[] => {
  return backendRequests.map(mapBackendRedemptionRequest)
}

export const mapBackendStudents = (backendStudents: any[]): Student[] => {
  return backendStudents.map(mapBackendStudent)
}

/**
 * Map backend dashboard responses to frontend dashboard responses
 */
export const mapBackendParentDashboard = (backendResponse: any): ParentDashboardResponse => {
  return {
    user: mapBackendUser(backendResponse.user),
    stats: backendResponse.stats, // DashboardStats doesn't need mapping
    children: mapBackendUsers(backendResponse.children || []),
    recent_transactions: mapBackendTransactions(backendResponse.recent_transactions || []),
  }
}

export const mapBackendTeacherDashboard = (backendResponse: any): TeacherDashboardResponse => {
  return {
    user: mapBackendUser(backendResponse.user),
    stats: backendResponse.stats,
    classes: mapBackendClasses(backendResponse.classes || []),
    recent_activities: backendResponse.recent_activities || [], // Activities don't need date mapping
  }
}

export const mapBackendChildDashboard = (backendResponse: any): ChildDashboardResponse => {
  return {
    user: mapBackendUser(backendResponse.user),
    stats: backendResponse.stats,
    goals: mapBackendGoals(backendResponse.goals || []),
    activities: backendResponse.activities || [],
    achievements: backendResponse.achievements || [],
    learning_modules: mapBackendModules(backendResponse.learning_modules || []),
  }
}

/**
 * Runtime type validation helpers
 */
export const validateUser = (data: any): data is User => {
  return data && 
    typeof data.id === 'string' && 
    typeof data.email === 'string' && 
    typeof data.name === 'string' &&
    ['parent', 'teacher', 'younger_child', 'older_child'].includes(data.role)
}

export const validateGoal = (data: any): data is Goal => {
  return data && 
    typeof data.id === 'string' && 
    typeof data.user_id === 'string' &&
    typeof data.title === 'string' &&
    typeof data.target_amount === 'number'
}

export const validateTransaction = (data: any): data is Transaction => {
  return data && 
    typeof data.id === 'string' && 
    typeof data.user_id === 'string' &&
    ['earn', 'spend', 'save'].includes(data.type) &&
    typeof data.amount === 'number' &&
    typeof data.description === 'string'
}

export const validateTask = (data: any): data is Task => {
  return data && 
    typeof data.id === 'string' && 
    typeof data.title === 'string' &&
    typeof data.coins_reward === 'number' &&
    typeof data.assigned_by === 'string' &&
    typeof data.assigned_to === 'string' &&
    ['pending', 'in_progress', 'completed', 'approved', 'rejected'].includes(data.status)
}
