import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'
import { useAuthStore } from './auth'
import { 
  mapBackendGoals,
  mapBackendTransactions,
  mapBackendTasks 
} from '../utils/typeMappers'
import type { Goal, Transaction, Task, Module } from '../types'

export interface Activity extends Module {
  completed?: boolean
  progress?: number
  coins?: number
}

export interface ChildStats {
  coins: number
  level: number
  streak_days: number
  goals_count: number
  completed_tasks: number
}

export interface ConversionRequest {
  id: string
  coins_amount: number
  cash_amount: number
  description?: string
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
}

export interface BudgetAllocation {
  saving: number
  spending: number
  wants: number
}

export const useChildStore = defineStore('child', () => {
  // State
  const goals = ref<Goal[]>([])
  const activities = ref<Activity[]>([])
  const transactions = ref<Transaction[]>([])
  const tasks = ref<Task[]>([])
  const stats = ref<ChildStats>({
    coins: 0,
    level: 1,
    streak_days: 0,
    goals_count: 0,
    completed_tasks: 0
  })
  const achievements = ref<any[]>([])
  const conversionRequests = ref<ConversionRequest[]>([])
  const budgetAllocation = ref<BudgetAllocation>({
    saving: 30,
    spending: 50,
    wants: 20
  })
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const availableGoals = computed(() => 
    goals.value.filter(goal => !goal.is_completed)
  )
  const completedGoals = computed(() => 
    goals.value.filter(goal => goal.is_completed)
  )
  const pendingTasks = computed(() => 
    tasks.value.filter(task => task.status === 'pending')
  )
  const completedTasks = computed(() => 
    tasks.value.filter(task => task.status === 'completed')
  )
  const recentTransactions = computed(() => 
    transactions.value.slice(0, 10)
  )
  const totalEarnings = computed(() => 
    transactions.value
      .filter(t => t.type === 'earn')
      .reduce((sum, t) => sum + t.amount, 0)
  )

  // Actions
  const loadDashboard = async (): Promise<void> => {
    console.log('📊 [CHILD] Loading child dashboard...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const userRole = authStore.user?.role
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      let dashboardResponse
      
      // Call appropriate dashboard endpoint based on user role
      if (userRole === 'older_child') {
        dashboardResponse = await apiService.getTeenDashboard()
      } else {
        dashboardResponse = await apiService.getChildDashboard()
      }
      
      if (!dashboardResponse.data) {
        throw new Error(dashboardResponse.error || 'Failed to load dashboard')
      }

      const dashboardData = dashboardResponse.data
      
      // Update stats using backend data structure
      stats.value = {
        coins: dashboardData.coins || 0,
        level: dashboardData.level || 1,
        streak_days: dashboardData.streak_days || 0,
        goals_count: dashboardData.goals_count || 0,
        completed_tasks: dashboardData.completed_tasks || 0
      }

      // Update goals with mapping
      if (dashboardData.active_goals) {
        goals.value = mapBackendGoals(dashboardData.active_goals)
      }

      // Update transactions with mapping
      if (dashboardData.recent_transactions || dashboardData.transactions) {
        const transactionData = dashboardData.recent_transactions || dashboardData.transactions || []
        transactions.value = mapBackendTransactions(transactionData)
      }

      // Update achievements
      if (dashboardData.achievements) {
        achievements.value = dashboardData.achievements || []
      }

      // Update tasks with mapping
      if (dashboardData.pending_tasks || dashboardData.tasks) {
        const taskData = dashboardData.pending_tasks || dashboardData.tasks || []
        tasks.value = mapBackendTasks(taskData)
      }

      console.log('✅ [CHILD] Dashboard loaded successfully')

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load dashboard:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const loadActivities = async (): Promise<void> => {
    console.log('🎯 [CHILD] Loading activities...')
    
    isLoading.value = true
    error.value = null

    try {
      const activitiesData = await apiService.getActivities()
      activities.value = activitiesData.map((activity: any) => ({
        ...activity,
        completed: activity.completed ?? false,
        progress: activity.progress ?? 0,
        coins: activity.coins ?? activity.points_reward ?? 10
      }))
      console.log('✅ [CHILD] Activities loaded successfully:', activities.value.length)
    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load activities:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const completeActivity = async (activityId: string): Promise<boolean> => {
    console.log('✨ [CHILD] Completing activity:', activityId)
    
    try {
      const result = await apiService.completeActivity(activityId)
      
      // Update local activity status
      const activityIndex = activities.value.findIndex(a => a.id === activityId)
      if (activityIndex !== -1 && activities.value[activityIndex]) {
        activities.value[activityIndex].completed = true
      }

      // Update stats
      if (result && result.coins_earned) {
        stats.value.coins += result.coins_earned
      }

      console.log('✅ [CHILD] Activity completed successfully')
      return true

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to complete activity:', err.message)
      error.value = err.message
      return false
    }
  }

  const loadGoals = async (): Promise<void> => {
    console.log('🎯 [CHILD] Loading goals...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const userId = authStore.user?.id
      
      if (!userId) {
        throw new Error('User not authenticated')
      }

      const goalsData = await apiService.getGoals(userId)
      goals.value = mapBackendGoals(goalsData)
      
      console.log('✅ [CHILD] Goals loaded successfully:', goals.value.length)

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load goals:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const createGoal = async (goalData: {
    title: string
    description?: string
    target_amount: number
    category?: string
  }): Promise<Goal | null> => {
    console.log('✨ [CHILD] Creating new goal...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const userId = authStore.user?.id
      
      if (!userId) {
        throw new Error('User not authenticated')
      }

      const response = await apiService.createGoal(userId, goalData)
      
      if ('error' in response && response.error) {
        throw new Error(response.error)
      }

      if ('data' in response && response.data) {
        const newGoal: Goal = response.data
        goals.value.push(newGoal)
        
        console.log('✅ [CHILD] Goal created successfully:', newGoal.title)
        return newGoal
      }

      // If response is a Goal directly (not wrapped in ApiResponse)
      if ('id' in response && 'title' in response) {
        goals.value.push(response as Goal)
        console.log('✅ [CHILD] Goal created successfully:', (response as Goal).title)
        return response as Goal
      }

      return null

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to create goal:', err.message)
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  const addGoalProgress = async (goalId: string, amount: number): Promise<boolean> => {
    console.log('📈 [CHILD] Adding progress to goal:', goalId, amount)
    
    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      const response = await apiService.addGoalProgress(goalId, amount)
      
      if (response.error) {
        throw new Error(response.error)
      }

      // Update local goal progress if API call was successful
      if (response.data) {
        const goalIndex = goals.value.findIndex(g => g.id === goalId)
        if (goalIndex !== -1 && goals.value[goalIndex]) {
          goals.value[goalIndex] = response.data
        }
      }

      // Update user coins
      stats.value.coins = Math.max(0, stats.value.coins - amount)

      console.log('✅ [CHILD] Goal progress updated successfully')
      return true

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to update goal progress:', err.message)
      error.value = err.message
      return false
    }
  }

  const loadTransactions = async (): Promise<void> => {
    console.log('💰 [CHILD] Loading transactions...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      const userId = authStore.user?.id
      
      if (!userId) {
        throw new Error('User not authenticated')
      }

      const transactionsData = await apiService.getTransactions(userId)
      transactions.value = transactionsData
      
      console.log('✅ [CHILD] Transactions loaded successfully:', transactions.value.length)

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load transactions:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const loadConversionRequests = async (): Promise<void> => {
    console.log('💱 [CHILD] Loading conversion requests...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      // Only teens can have conversion requests
      if (authStore.user?.role !== 'older_child') {
        console.log('💱 [CHILD] User is not a teen, skipping conversion requests')
        conversionRequests.value = []
        return
      }

      const requestsData = await apiService.getConversionRequests()
      conversionRequests.value = requestsData || []
      
      console.log('✅ [CHILD] Conversion requests loaded successfully:', conversionRequests.value.length)

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load conversion requests:', err.message)
      error.value = err.message
      conversionRequests.value = []
    } finally {
      isLoading.value = false
    }
  }

  const createConversionRequest = async (requestData: {
    coins_amount: number
    cash_amount: number
    description?: string
  }): Promise<boolean> => {
    console.log('💱 [CHILD] Creating conversion request...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      // Only teens can create conversion requests
      if (authStore.user?.role !== 'older_child') {
        throw new Error('Only teens can create conversion requests')
      }

      // Check if user has enough coins
      if (requestData.coins_amount > stats.value.coins) {
        throw new Error('Insufficient coins for conversion request')
      }

      const result = await apiService.createConversionRequest(requestData)
      
      // Add to local requests if creation was successful
      if (result && result.id) {
        const newRequest: ConversionRequest = {
          id: result.id,
          coins_amount: requestData.coins_amount,
          cash_amount: requestData.cash_amount,
          description: requestData.description,
          status: 'pending',
          created_at: new Date().toISOString()
        }
        conversionRequests.value.push(newRequest)
      }

      console.log('✅ [CHILD] Conversion request created successfully')
      return true

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to create conversion request:', err.message)
      error.value = err.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  const updateBudgetAllocation = async (allocation: BudgetAllocation): Promise<void> => {
    console.log('📊 [CHILD] Updating budget allocation...')
    
    // Ensure percentages add up to 100
    const total = allocation.saving + allocation.spending + allocation.wants
    if (total !== 100) {
      console.warn('Budget allocation percentages do not add up to 100:', total)
    }

    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      // Only teens have budget allocation features
      if (authStore.user?.role === 'older_child') {
        // TODO: When teen budget API is implemented, call it here
        // await apiService.updateTeenBudget(allocation)
      }

      budgetAllocation.value = allocation
      console.log('✅ [CHILD] Budget allocation updated successfully')

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to update budget allocation:', err.message)
      error.value = err.message
      // Still update local state even if API fails
      budgetAllocation.value = allocation
    }
  }

  // Additional methods for task management
  const loadTasks = async (): Promise<void> => {
    console.log('📋 [CHILD] Loading tasks...')
    
    isLoading.value = true
    error.value = null

    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      // Load tasks specific to child/teen role
      if (authStore.user?.role === 'older_child') {
        // For teens, load from teen-specific endpoint if available
        // Otherwise fallback to generic tasks endpoint
        const tasksData = await apiService.getTasks()
        tasks.value = tasksData || []
      } else if (authStore.user?.role === 'younger_child') {
        // For children, load from child-specific endpoint if available
        // Otherwise fallback to generic tasks endpoint
        const tasksData = await apiService.getTasks()
        tasks.value = tasksData || []
      }
      
      console.log('✅ [CHILD] Tasks loaded successfully:', tasks.value.length)

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to load tasks:', err.message)
      error.value = err.message
      tasks.value = []
    } finally {
      isLoading.value = false
    }
  }

  const completeTask = async (taskId: string): Promise<boolean> => {
    console.log('✅ [CHILD] Completing task:', taskId)
    
    try {
      const authStore = useAuthStore()
      
      if (!authStore.isAuthenticated) {
        throw new Error('User not authenticated')
      }

      // Find the task
      const taskIndex = tasks.value.findIndex(t => t.id === taskId)
      if (taskIndex === -1) {
        throw new Error('Task not found')
      }

      const task = tasks.value[taskIndex]
      if (!task) {
        throw new Error('Task not found')
      }
      
      // Update task status locally
      tasks.value[taskIndex] = {
        ...task,
        status: 'completed' as const
      }

      // Update stats (add coins earned)
      if (task.coins_reward) {
        stats.value.coins += task.coins_reward
        stats.value.completed_tasks += 1
      }

      console.log('✅ [CHILD] Task completed successfully')
      return true

    } catch (err: any) {
      console.error('❌ [CHILD] Failed to complete task:', err.message)
      error.value = err.message
      return false
    }
  }

  return {
    // State
    goals,
    activities,
    transactions,
    tasks,
    stats,
    achievements,
    conversionRequests,
    budgetAllocation,
    isLoading,
    error,

    // Getters
    availableGoals,
    completedGoals,
    pendingTasks,
    completedTasks,
    recentTransactions,
    totalEarnings,

    // Actions
    loadDashboard,
    loadActivities,
    completeActivity,
    loadGoals,
    createGoal,
    addGoalProgress,
    loadTransactions,
    loadConversionRequests,
    createConversionRequest,
    updateBudgetAllocation,
    loadTasks,
    completeTask
  }
})