import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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
      const newGoal: Goal = {
        ...goalData,
        id: Date.now().toString(),
        currentAmount: 0,
        completed: false,
        createdAt: new Date().toISOString()
      }

      goals.value.push(newGoal)
      return newGoal
    } catch (err) {
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
      
      const demoGoals: Goal[] = [
        {
          id: '1',
          title: 'New Bike',
          description: 'Save for a new bicycle',
          targetAmount: 100,
          currentAmount: 35,
          icon: 'ri-bike-line',
          category: 'wants',
          deadline: '2024-06-01',
          completed: false,
          createdAt: '2024-01-15'
        },
        {
          id: '2',
          title: 'Emergency Fund',
          description: 'Build an emergency savings fund',
          targetAmount: 50,
          currentAmount: 20,
          icon: 'ri-shield-check-line',
          category: 'saving',
          completed: false,
          createdAt: '2024-01-10'
        },
        {
          id: '3',
          title: 'Birthday Gift',
          description: 'Save for mom\'s birthday gift',
          targetAmount: 25,
          currentAmount: 25,
          icon: 'ri-gift-line',
          category: 'wants',
          deadline: '2024-03-15',
          completed: true,
          createdAt: '2024-01-05'
        }
      ]

      const demoTransactions: Transaction[] = [
        {
          id: '1',
          type: 'earn',
          amount: 10,
          description: 'Completed Piggy Bank Adventure',
          category: 'activity',
          timestamp: '2024-01-20T10:00:00Z'
        },
        {
          id: '2',
          type: 'save',
          amount: 5,
          description: 'Contributed to New Bike',
          category: 'goal',
          timestamp: '2024-01-19T15:30:00Z',
          relatedGoalId: '1'
        },
        {
          id: '3',
          type: 'spend',
          amount: 15,
          description: 'Bought virtual stickers',
          category: 'purchase',
          timestamp: '2024-01-18T14:20:00Z'
        },
        {
          id: '4',
          type: 'earn',
          amount: 20,
          description: 'Weekly allowance',
          category: 'allowance',
          timestamp: '2024-01-17T09:00:00Z'
        }
      ]

      goals.value = demoGoals
      transactions.value = demoTransactions

    } catch (err) {
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