import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'
import type { User, Goal, Task, RedemptionRequest, ChildProgress, DashboardStats, Activity, Module, Achievement } from '../types'

// Child interface extending User with additional parent-specific fields
export interface Child extends User {
  // These fields come from child_profile in backend
  age?: number
  coins?: number
  level?: number
  streak_days?: number
  password?: string
  
  // Computed fields for parent dashboard
  goalsActive?: number
  lastActivity?: Date
  completedTasks?: number
  recentActivity?: any[]
  currentGoals?: Goal[]
}

// Parent task interface extending Task
export interface ParentTask extends Task {
  childId?: string
  childName?: string
  assigned_to_name?: string  // Child name for display
}

// Family statistics interface
export interface FamilyStats {
  totalChildren: number
  totalCoinsEarned: number
  completedTasks: number
  activeGoals: number
}

// Error interface for structured error handling
interface ParentError {
  message: string
  code?: string
  timestamp: Date
}

export const useParentStore = defineStore('parent', () => {
  // State
  const children = ref<Child[]>([])
  const tasks = ref<ParentTask[]>([])
  const redemptionRequests = ref<RedemptionRequest[]>([])
  const childProgress = ref<ChildProgress>({
    stats: {} as DashboardStats,
    recent_activities: [] as Activity[],
    active_goals: [] as Goal[],
    completed_goals: [] as Goal[],
    achievements: [] as Achievement[],
    learning_modules: [] as Module[],
  })
  const familyStats = ref<FamilyStats>({
    totalChildren: 0,
    totalCoinsEarned: 0,
    completedTasks: 0,
    activeGoals: 0
  })
  const isLoading = ref(false)
  const error = ref<ParentError | null>(null)

  // Getters
  const pendingTasks = computed(() => 
    tasks.value.filter(task => task.status === 'pending')
  )
  const completedTasks = computed(() => 
    tasks.value.filter(task => task.status === 'completed')
  )
  const pendingRedemptions = computed(() => 
    redemptionRequests.value.filter(req => req.status === 'pending')
  )

  // Actions
  const loadDashboard = async (): Promise<void> => {
    console.log('📊 [PARENT] Loading parent dashboard...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getParentDashboard()
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No dashboard data received')
      }

      const dashboardData = response.data
      
      // Update family stats from dashboard response
      if (dashboardData.stats) {
        familyStats.value = {
          totalChildren: dashboardData.children?.length || 0,
          totalCoinsEarned: dashboardData.stats.total_coins || 0,
          completedTasks: dashboardData.stats.completed_tasks || 0,
          activeGoals: dashboardData.stats.goals_count || 0
        }
      }

      // Update children list
      if (dashboardData.children) {
        children.value = dashboardData.children.map((child: User) => ({
          ...child,
          goalsActive: 0,
          lastActivity: new Date(),
          completedTasks: 0
        }))
      }

      console.log('✅ [PARENT] Dashboard loaded successfully')

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to load dashboard:', err.message)
      error.value = {
        message: err.message,
        code: 'DASHBOARD_LOAD_ERROR',
        timestamp: new Date()
      }
    } finally {
      isLoading.value = false
    }
  }

  const createChild = async (childData: {
    name: string
    email: string
    password: string
    age: number
    role: 'younger_child' | 'older_child'
  }): Promise<Child | null> => {
    console.log('👶 [PARENT] Creating new child account...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.createChild(childData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No user data received')
      }

      const newChild: Child = {
        ...response.data,
        age: childData.age,
        password: childData.password, // Store password for parent visibility
        goalsActive: 0,
        lastActivity: new Date(),
        completedTasks: 0
      }
      
      children.value.push(newChild)
      familyStats.value.totalChildren = children.value.length
      
      console.log('✅ [PARENT] Child created successfully:', newChild.name)
      return newChild

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to create child:', err.message)
      error.value = {
        message: err.message,
        code: 'CHILD_CREATE_ERROR',
        timestamp: new Date()
      }
      return null
    } finally {
      isLoading.value = false
    }
  }

  const loadTasks = async (): Promise<void> => {
    console.log('📋 [PARENT] Loading parent tasks...')
    
    try {
      const response = await apiService.getParentTasks()
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        tasks.value = response.data.map((task: Task) => ({
          ...task,
          childName: getChildName(task.assigned_to),
          assigned_to_name: getChildName(task.assigned_to)
        }))
      }

      console.log('✅ [PARENT] Tasks loaded successfully')

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to load tasks:', err.message)
      error.value = {
        message: err.message,
        code: 'TASKS_LOAD_ERROR',
        timestamp: new Date()
      }
    }
  }

  const createTask = async (taskData: {
    title: string
    description?: string
    coins_reward: number
    assigned_to: string
    due_date?: string
    requires_approval?: boolean
  }): Promise<Task | null> => {
    console.log('📝 [PARENT] Creating new task...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.createParentTask(taskData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No task data received')
      }

      const newTask: ParentTask = {
        ...response.data,
        childName: getChildName(taskData.assigned_to),
        assigned_to_name: getChildName(taskData.assigned_to)
      }
      
      tasks.value.push(newTask)
      
      console.log('✅ [PARENT] Task created successfully:', newTask.title)
      return newTask

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to create task:', err.message)
      error.value = {
        message: err.message,
        code: 'TASK_CREATE_ERROR',
        timestamp: new Date()
      }
      return null
    } finally {
      isLoading.value = false
    }
  }

  const approveTask = async (taskId: string): Promise<boolean> => {
    console.log('✅ [PARENT] Approving task:', taskId)
    
    try {
      const response = await apiService.approveTask(taskId)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        // Update task in local state
        const taskIndex = tasks.value.findIndex(t => t.id === taskId)
        if (taskIndex !== -1) {
          tasks.value[taskIndex] = {
            ...tasks.value[taskIndex],
            ...response.data,
            status: 'approved'
          }
        }
      }

      console.log('✅ [PARENT] Task approved successfully')
      return true

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to approve task:', err.message)
      error.value = {
        message: err.message,
        code: 'TASK_APPROVE_ERROR',
        timestamp: new Date()
      }
      return false
    }
  }

  const loadRedemptions = async (): Promise<void> => {
    console.log('💰 [PARENT] Loading redemption requests...')
    
    try {
      const response = await apiService.getRedemptionRequests()
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        redemptionRequests.value = response.data.map((req: RedemptionRequest) => ({
          ...req,
          childName: getChildName(req.user_id)
        }))
      }

      console.log('✅ [PARENT] Redemptions loaded successfully')

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to load redemptions:', err.message)
      error.value = {
        message: err.message,
        code: 'REDEMPTIONS_LOAD_ERROR',
        timestamp: new Date()
      }
    }
  }

  const approveRedemption = async (requestId: string): Promise<boolean> => {
    console.log('✅ [PARENT] Approving redemption:', requestId)
    
    try {
      const response = await apiService.approveRedemption(requestId)
      
      if (response.error) {
        throw new Error(response.error)
      }

      // Update redemption in local state
      const reqIndex = redemptionRequests.value.findIndex(r => r.id === requestId)
      if (reqIndex !== -1 && redemptionRequests.value[reqIndex]) {
        redemptionRequests.value[reqIndex].status = 'approved'
      }

      console.log('✅ [PARENT] Redemption approved successfully')
      return true

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to approve redemption:', err.message)
      error.value = {
        message: err.message,
        code: 'REDEMPTION_APPROVE_ERROR',
        timestamp: new Date()
      }
      return false
    }
  }

  const rejectRedemption = async (requestId: string): Promise<boolean> => {
    console.log('❌ [PARENT] Rejecting redemption:', requestId)
    
    try {
      const response = await apiService.rejectRedemption(requestId)
      
      if (response.error) {
        throw new Error(response.error)
      }

      // Update redemption in local state
      const reqIndex = redemptionRequests.value.findIndex(r => r.id === requestId)
      if (reqIndex !== -1 && redemptionRequests.value[reqIndex]) {
        redemptionRequests.value[reqIndex].status = 'rejected'
      }

      console.log('✅ [PARENT] Redemption rejected successfully')
      return true

    } catch (err: any) {
      console.error('❌ [PARENT] Failed to reject redemption:', err.message)
      error.value = {
        message: err.message,
        code: 'REDEMPTION_REJECT_ERROR',
        timestamp: new Date()
      }
      return false
    }
  }

  const clearError = (): void => {
    error.value = null
  }

  const refreshData = async (): Promise<void> => {
    await Promise.all([
      loadDashboard(),
      loadTasks(),
      loadRedemptions()
    ])
  }

  // Helper function to get child name by ID
  const getChildName = (childId: string): string => {
    const child = children.value.find(c => c.id === childId)
    return child?.name || 'Unknown Child'
  }

  const getChildProgress = async (childId: string): Promise<void> => {
    const response = await apiService.getChildProgress(childId)
    const data = response.data
    childProgress.value = {
      child: data.child,
      stats: data.stats,
      recent_activities: data.recent_activities,
      active_goals: data.active_goals,
      completed_goals: data.completed_goals,
      achievements: data.achievements || [],
      learning_modules: data.learning_modules || [],
    }
    
  }

  return {
    // State
    children,
    tasks,
    redemptionRequests,
    familyStats,
    isLoading,
    error,
    childProgress,
    
    // Getters
    pendingTasks,
    completedTasks,
    pendingRedemptions,
    
    // Actions
    loadDashboard,
    createChild,
    loadTasks,
    createTask,
    approveTask,
    loadRedemptions,
    approveRedemption,
    rejectRedemption,
    clearError,
    refreshData,
    getChildName,
    getChildProgress
  }
})
