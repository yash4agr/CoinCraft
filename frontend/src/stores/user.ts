import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { apiService } from '@/services/api'
import { useAuthStore } from './auth'
import { isPartOfTypeOnlyImportOrExportDeclaration } from 'typescript'


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
  target_amount: number
  current_amount: number
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
  created_at: string
  relatedGoalId?: string
  reference_type?: 'goal' | 'task' | 'activity' | 'shop' | 'redemption'
}

export const useUserStore = defineStore('user', () => {
  const authStore = useAuthStore()
  const profile = ref<UserProfile | null>(null)
  const goals = ref<Goal[]>([])
  const transactions = ref<Transaction[]>([])
  const achievements = ref<any[]>([])
  const conversionRequests = ref<ConversionRequest[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const shopItems = ref<any[]>([])
  const ownedItems = ref<string[]>([])

  const totalCoins = computed(() => profile.value?.coins || 0)
  const activeGoals = computed(() => goals.value.filter(goal => !goal.completed))
  const completedGoals = computed(() => goals.value.filter(goal => goal.completed))
  const recentTransactions = computed(() => 
    transactions.value.slice(-10).sort((a, b) => 
      new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
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
        created_at: new Date().toISOString()
      }

      transactions.value.push(transaction)
      let response = await apiService.createTransaction(profile.value.id, transaction)
      profile.value.coins += amount
      authStore.user.coins=profile.value.coins
      profile.value.totalCoinsEarned += amount
      await apiService.updateUserCoins(profile.value.id, profile.value.coins)

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
        created_at: new Date().toISOString()
      }
      transactions.value.push(transaction)
      await apiService.createTransaction(profile.value.id, transaction)
      profile.value.coins -= amount
      authStore.user.coins=profile.value.coins
      await apiService.updateUserCoins(profile.value.id, profile.value.coins)
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
      console.log("BREAK 1")
      // Use real API for teen goals
      const response = await apiService.createGoal(profile.value?.id, {
        title: goalData.title,
        description: goalData.description,
        target_amount: goalData.target_amount,
        icon: goalData.icon,
        color: 'blue'
      })
      
      if (response.error) {
        throw new Error(response.error)
      }
      console.log("BREAK 2")
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

      // Update local state first
      goals.value[goalIndex] = { ...goals.value[goalIndex], ...updates }
      if (goals.value[goalIndex].currentAmount >= goals.value[goalIndex].targetAmount) {
        goals.value[goalIndex].completed = true
      }

      // Call backend API to persist changes
      const apiUpdates: any = {}
      if (updates.title !== undefined) apiUpdates.title = updates.title
      if (updates.description !== undefined) apiUpdates.description = updates.description
      if (updates.target_amount !== undefined) apiUpdates.target_amount = updates.target_amount
      if (updates.icon !== undefined) apiUpdates.icon = updates.icon
      if (updates.current_amount !== undefined) apiUpdates.current_amount = updates.current_amount
      if (updates.category !== undefined) apiUpdates.category = updates.category
      // Add other fields as needed

      const response = await apiService.updateGoal(goalId, apiUpdates)
      if (response.error) {
        error.value = response.error
        return false
      }
      // Optionally update local state with backend response
      if (response.data) {
        goals.value[goalIndex] = { ...goals.value[goalIndex], ...response.data }
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
      authStore.user.coins=profile.value.coins
      goal.current_amount += amount
      await apiService.updateGoalAmount(goalId, goal.current_amount)


      await apiService.updateUserCoins(profile.value.id, profile.value.coins)
      const transaction: Transaction = {
        id: Date.now().toString(),
        type: 'save',
        amount,
        description: `Contributed to ${goal.title}`,
        category: 'goal',
        created_at: new Date().toISOString(),
        relatedGoalId: goalId
      }

      transactions.value.push(transaction)

      if (goal.current_amount >= goal.target_amount) {
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
            created_at: '2024-01-20T10:30:00Z'
          },
          {
            id: '2',
            type: 'spend',
            amount: 15,
            description: 'Bought: Movie Tickets',
            category: 'entertainment',
            created_at: '2024-01-19T18:00:00Z'
          },
          {
            id: '3',
            type: 'save',
            amount: 20,
            description: 'Contributed to College Fund',
            category: 'goal',
            created_at: '2024-01-18T14:00:00Z',
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
          coins: response.data.stats.coins,
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
      transactions.value = await apiService.getTransactions(profile.value.id)
      goals.value = await apiService.getGoals(profile.value.id)

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
  const computedStreak = computed(() => {
    // Use backend only until we have any transactions
    if (!transactions.value.length) {
      return profile.value?.streak || 0
    }

    const sorted = [...transactions.value].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )

    let streak = 0
    let expectedDate = new Date()
    expectedDate.setHours(0, 0, 0, 0)

    for (const tx of sorted) {
      const txDate = new Date(tx.created_at)
      txDate.setHours(0, 0, 0, 0)

      const diffDays = Math.floor(
        (expectedDate.getTime() - txDate.getTime()) / 86400000
      )

      if (diffDays < 0) {
        // another txn on a day we already counted (e.g., multiple today/yesterday)
        continue
      }

      if (diffDays === 0 || diffDays === 1) {
        streak++
        expectedDate.setDate(expectedDate.getDate() - 1)
      } else {
        break
      }
    }

    // IMPORTANT: do NOT fall back to backend here; 0 is a valid result
    return streak
  })

  // ✅ Keep profile.streak always in sync
  watch(computedStreak, (val) => {
    if (profile.value) {
      profile.value.streak = val
    }
  }, { immediate: true })
  watch(profile, (newVal) => {
    localStorage.setItem('user-profile', JSON.stringify(newVal))
  }, { deep: true })
  watch(recentTransactions, (newVal) => {
    localStorage.setItem('recent-transactions', JSON.stringify(newVal))
  }, { deep: true })
  watch(transactions, (newVal) => {
    transactions.value = newVal.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  })

  const getShopItems = async () => {
    try {
      isLoading.value = true
      error.value = null
      const items = await apiService.getShopItems()
      shopItems.value = items
      return items
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load shop items'
      return []
    } finally {
      isLoading.value = false
    }
  }

  const getOwnedItems = async () => {
    try {
      isLoading.value = true
      error.value = null
      const items = await apiService.getOwnedItems()
      // Assume backend returns array of item ids
      ownedItems.value = Array.isArray(items) ? items.map((item: any) => item.item_id || item.id) : []
      return ownedItems.value
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load owned items'
      return []
    } finally {
      isLoading.value = false
    }
  }

  const purchaseShopItem = async (itemId: string) => {
    try {
      isLoading.value = true
      error.value = null
      // Optimistically add to ownedItems before API call
      if (!ownedItems.value.includes(itemId)) {
        ownedItems.value.push(itemId)
      }
      const response = await apiService.purchaseItem(profile.value?.id, itemId)
      if (response && response.success) {
        // Optionally update ownedItems again if backend returns new data
        if (response.item && response.item.id && !ownedItems.value.includes(response.item.id)) {
          ownedItems.value.push(response.item.id)
        }
        return true
      } else {
        // Rollback if purchase failed
        ownedItems.value = ownedItems.value.filter(id => id !== itemId)
        error.value = response?.message || 'Purchase failed'
        return false
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to purchase item'
      ownedItems.value = ownedItems.value.filter(id => id !== itemId)
      return false
    } finally {
      isLoading.value = false
    }
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
    computedStreak,
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
    $reset,
    shopItems,
    getShopItems,
    ownedItems,
    getOwnedItems,
    purchaseShopItem
  }
})