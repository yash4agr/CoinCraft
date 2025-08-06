import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'

export interface UserProfile {
  id: string
  fullName: string
  email: string
  username: string
  role: 'parent' | 'teacher' | 'younger_child' | 'older_child'
  coins: number
  avatar: string
  level: number
  streak: number
  totalCoinsEarned: number
  goalsCompleted: number
  createdAt: string
  preferences: {
    soundEnabled: boolean
    notificationsEnabled: boolean
    theme: 'light' | 'dark'
  }
}

export interface Goal {
  id: string
  title: string
  description: string
  targetAmount: number
  currentAmount: number
  icon: string
  category: 'saving' | 'spending' | 'wants'
  deadline?: string
  completed: boolean
  createdAt: string
}

export interface ConversionRequest {
  id: string
  childId: string
  amount: number
  coinAmount: number
  reason: string
  status: 'pending' | 'approved' | 'denied'
  requestDate: string
  responseDate?: string
}

export interface Transaction {
  id: string
  type: 'earn' | 'spend' | 'save'
  amount: number
  description: string
  category: string
  timestamp: string
  relatedGoalId?: string
}

export const useUserStore = defineStore('user', () => {
  const profile = ref<UserProfile | null>(null)
  const goals = ref<Goal[]>([])
  const transactions = ref<Transaction[]>([])
  const achievements = ref<any[]>([])
  const conversionRequests = ref<ConversionRequest[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const totalCoins = computed(() => profile.value?.coins || 0)
  const activeGoals = computed(() => goals.value.filter(goal => !goal.completed))
  const completedGoals = computed(() => goals.value.filter(goal => goal.completed))
  const recentTransactions = computed(() => 
    transactions.value.slice(0, 10).sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  )

  const updateProfile = async (updates: Partial<UserProfile>) => {
    if (!profile.value) return
    
    try {
      isLoading.value = true
      profile.value = { ...profile.value, ...updates }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update profile'
    } finally {
      isLoading.value = false
    }
  }

  const addCoins = async (amount: number, description: string, category: string = 'activity') => {
    if (!profile.value) return

    try {
      const transaction: Transaction = {
        id: Date.now().toString(),
        type: 'earn',
        amount,
        description,
        category,
        timestamp: new Date().toISOString()
      }

      transactions.value.unshift(transaction)
      profile.value.coins += amount
      profile.value.totalCoinsEarned += amount

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to add coins'
    }
  }

  const spendCoins = async (amount: number, description: string, category: string = 'purchase') => {
    if (!profile.value || profile.value.coins < amount) {
      error.value = 'Insufficient coins'
      return false
    }

    try {
      const transaction: Transaction = {
        id: Date.now().toString(),
        type: 'spend',
        amount,
        description,
        category,
        timestamp: new Date().toISOString()
      }

      transactions.value.unshift(transaction)
      profile.value.coins -= amount

      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to spend coins'
      return false
    }
  }

  const createGoal = async (goalData: Omit<Goal, 'id' | 'currentAmount' | 'completed' | 'createdAt'>) => {
    try {
      console.log('🎯 [TEEN] Creating new goal:', goalData.title)
      
      // Check if we're in demo mode
      const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
      
      if (isDemoMode || !apiService.isAuthenticated()) {
        // Use mock data for demo mode
        const newGoal: Goal = {
          ...goalData,
          id: Date.now().toString(),
          currentAmount: 0,
          completed: false,
          createdAt: new Date().toISOString()
        }
        goals.value.push(newGoal)
        return newGoal
      }

      // Use real API for teen goals
      const response = await apiService.createGoal({
        user_id: '', // Will be set by backend
        title: goalData.title,
        description: goalData.description,
        target_amount: goalData.targetAmount,
        current_amount: 0,
        icon: goalData.icon,
        color: 'blue'
      })
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        const newGoal: Goal = {
          id: response.data.id,
          title: response.data.title,
          description: response.data.description,
          targetAmount: response.data.target_amount,
          currentAmount: response.data.current_amount,
          icon: response.data.icon,
          category: goalData.category,
          deadline: goalData.deadline,
          completed: false,
          createdAt: response.data.created_at
        }
        goals.value.push(newGoal)
        console.log('✅ [TEEN] Goal created successfully:', newGoal.title)
        return newGoal
      }
    } catch (err) {
      console.error('❌ [TEEN] Failed to create goal:', err)
      error.value = err instanceof Error ? err.message : 'Failed to create goal'
      return null
    }
  }

  const updateGoal = async (goalId: string, updates: Partial<Goal>) => {
    try {
      const goalIndex = goals.value.findIndex(g => g.id === goalId)
      if (goalIndex === -1) return false

      goals.value[goalIndex] = { ...goals.value[goalIndex], ...updates }
      
      if (goals.value[goalIndex].currentAmount >= goals.value[goalIndex].targetAmount) {
        goals.value[goalIndex].completed = true
      }

      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update goal'
      return false
    }
  }

  const contributeToGoal = async (goalId: string, amount: number) => {
    if (!profile.value || profile.value.coins < amount) {
      error.value = 'Insufficient coins'
      return false
    }

    try {
      const goal = goals.value.find(g => g.id === goalId)
      if (!goal) return false

      profile.value.coins -= amount
      goal.currentAmount += amount

      const transaction: Transaction = {
        id: Date.now().toString(),
        type: 'save',
        amount,
        description: `Contributed to ${goal.title}`,
        category: 'goal',
        timestamp: new Date().toISOString(),
        relatedGoalId: goalId
      }

      transactions.value.unshift(transaction)

      if (goal.currentAmount >= goal.targetAmount) {
        goal.completed = true
      }

      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to contribute to goal'
      return false
    }
  }

  const requestMoneyConversion = async (coinAmount: number, dollarAmount: number, reason: string) => {
    if (!profile.value) return false

    try {
      const request: ConversionRequest = {
        id: Date.now().toString(),
        childId: profile.value.id,
        amount: dollarAmount,
        coinAmount,
        reason,
        status: 'pending',
        requestDate: new Date().toISOString()
      }

      conversionRequests.value.push(request)
      return true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create conversion request'
      return false
    }
  }

  const loadUserData = async (userId: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      console.log('👤 [TEEN] Loading user data for:', userId)
      
      // Check if we're in demo mode
      const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
      
      if (isDemoMode || !apiService.isAuthenticated()) {
        // Use mock data for demo mode
        const demoGoals: Goal[] = [
          {
            id: '1',
            title: 'New Gaming Console',
            description: 'Save up for the latest gaming console',
            targetAmount: 500,
            currentAmount: 150,
            icon: 'ri-gamepad-line',
            category: 'wants',
            deadline: '2024-06-01',
            completed: false,
            createdAt: '2024-01-15'
          },
          {
            id: '2',
            title: 'College Fund',
            description: 'Start saving for college expenses',
            targetAmount: 1000,
            currentAmount: 75,
            icon: 'ri-graduation-cap-line',
            category: 'saving',
            deadline: '2024-12-31',
            completed: false,
            createdAt: '2024-01-10'
          }
        ]

        const demoTransactions: Transaction[] = [
          {
            id: '1',
            type: 'earn',
            amount: 25,
            description: 'Completed Advanced Budgeting Module',
            category: 'learning',
            timestamp: '2024-01-20T10:30:00Z'
          },
          {
            id: '2',
            type: 'spend',
            amount: 15,
            description: 'Bought: Movie Tickets',
            category: 'entertainment',
            timestamp: '2024-01-19T18:00:00Z'
          },
          {
            id: '3',
            type: 'save',
            amount: 20,
            description: 'Contributed to College Fund',
            category: 'goal',
            timestamp: '2024-01-18T14:00:00Z',
            relatedGoalId: '2'
          }
        ]

        goals.value = demoGoals
        transactions.value = demoTransactions
        
        console.log('✅ [TEEN] Demo user data loaded successfully')
        return
      }

      // Use real API for role-specific dashboard
      const userRole = profile.value?.role || localStorage.getItem('user_role') || 'older_child'
      console.log(`📊 [USER] Loading dashboard for role: ${userRole}`)
      
      const response = await apiService.getDashboardData(userRole)
      
      if (response.error) {
        if (response.status === 403) {
          console.warn(`⚠️ [USER] Access denied for role ${userRole} - skipping dashboard load`)
          return
        }
        throw new Error(response.error)
      }

      if (response.data) {
        console.log('📊 [TEEN] Dashboard response:', response.data)
        
        // Update profile with real data
        profile.value = {
          id: response.data.user.id,
          fullName: response.data.user.name,
          email: response.data.user.email,
          username: response.data.user.email.split('@')[0],
          role: response.data.user.role,
          coins: response.data.stats.total_coins,
          avatar: response.data.user.avatar_url,
          level: response.data.stats.level,
          streak: response.data.stats.streak_days,
          totalCoinsEarned: response.data.stats.total_coins,
          goalsCompleted: response.data.stats.completed_tasks,
          createdAt: response.data.user.created_at,
          preferences: {
            soundEnabled: true,
            notificationsEnabled: true,
            theme: 'light'
          }
        }
        
        console.log('✅ [TEEN] User data loaded successfully')
      }

    } catch (err) {
      console.error('❌ [TEEN] Failed to load user data:', err)
      error.value = err instanceof Error ? err.message : 'Failed to load user data'
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const setProfile = (userProfile: UserProfile) => {
    profile.value = userProfile
  }

  const $reset = () => {
    profile.value = null
    goals.value = []
    transactions.value = []
    achievements.value = []
    conversionRequests.value = []
    isLoading.value = false
    error.value = null
  }

  return {
    profile,
    goals,
    transactions,
    achievements,
    conversionRequests,
    isLoading,
    error,
    totalCoins,
    activeGoals,
    completedGoals,
    recentTransactions,
    updateProfile,
    addCoins,
    spendCoins,
    createGoal,
    updateGoal,
    contributeToGoal,
    requestMoneyConversion,
    loadUserData,
    clearError,
    setProfile,
    $reset
  }
}) 