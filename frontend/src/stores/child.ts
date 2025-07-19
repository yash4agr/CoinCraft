import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService, type Goal as ApiGoal, type Transaction as ApiTransaction } from '../services/api'

export interface Goal {
  id: string
  name: string
  targetAmount: number
  currentAmount: number
  icon: string
  createdAt: Date
}

export interface Activity {
  id: string
  name: string
  description: string
  coins: number
  duration: number
  difficulty: 'easy' | 'medium' | 'hard'
  completed: boolean
  icon: string
}

export interface Transaction {
  id: string
  type: 'earned' | 'spent' | 'saved'
  amount: number
  description: string
  timestamp: Date
}

export const useChildStore = defineStore('child', () => {
  const goals = ref<Goal[]>([
    {
      id: '1',
      name: 'Magic Hat',
      targetAmount: 50,
      currentAmount: 35,
      icon: 'ri-magic-line',
      createdAt: new Date()
    },
    {
      id: '2',
      name: 'Video Game',
      targetAmount: 100,
      currentAmount: 10,
      icon: 'ri-gamepad-line',
      createdAt: new Date()
    }
  ])

  const activities = ref<Activity[]>([
    {
      id: '1',
      name: 'Sort Needs vs. Wants',
      description: 'Learn the difference between needs and wants',
      coins: 10,
      duration: 5,
      difficulty: 'easy',
      completed: false,
      icon: 'ri-scales-line'
    },
    {
      id: '2',
      name: 'Shopping Challenge',
      description: 'Practice smart shopping decisions',
      coins: 15,
      duration: 7,
      difficulty: 'medium',
      completed: false,
      icon: 'ri-shopping-cart-line'
    },
    {
      id: '3',
      name: 'Quick Quiz',
      description: 'Test your financial knowledge',
      coins: 5,
      duration: 3,
      difficulty: 'easy',
      completed: false,
      icon: 'ri-question-line'
    }
  ])

  const transactions = ref<Transaction[]>([
    {
      id: '1',
      type: 'earned',
      amount: 15,
      description: 'Shopping Challenge',
      timestamp: new Date()
    },
    {
      id: '2',
      type: 'spent',
      amount: 10,
      description: 'Bought: Star Sticker',
      timestamp: new Date(Date.now() - 86400000)
    },
    {
      id: '3',
      type: 'saved',
      amount: 10,
      description: 'Deposited to Goal: Magic Hat',
      timestamp: new Date(Date.now() - 172800000)
    }
  ])

  const budgetAllocation = ref({
    saving: 40,
    spending: 35,
    wants: 25
  })

  const addGoal = async (goal: Omit<Goal, 'id' | 'createdAt'>) => {
    // Check if we're in demo mode
    const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
    
    if (isDemoMode || !apiService.isAuthenticated()) {
      // Use mock data for demo mode
      goals.value.push({
        ...goal,
        id: Date.now().toString(),
        createdAt: new Date()
      })
      return
    }

    try {
      console.log('🎯 [CHILD] Creating new goal:', goal.name)
      
      // For now, use the existing API method until we add child-specific methods
      const apiGoal = {
        user_id: '', // Will be set by backend
        title: goal.name,
        description: goal.name,
        target_amount: goal.targetAmount,
        current_amount: goal.currentAmount || 0,
        icon: goal.icon,
        color: 'blue'
      }

      const response = await apiService.createGoal(apiGoal)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        const newGoal: Goal = {
          id: response.data.goal.id,
          name: response.data.goal.name,
          targetAmount: response.data.goal.targetAmount,
          currentAmount: response.data.goal.currentAmount,
          icon: response.data.goal.icon,
          createdAt: new Date(response.data.goal.createdAt)
        }
        goals.value.push(newGoal)
        console.log('✅ [CHILD] Goal created successfully:', newGoal.name)
      }
    } catch (error) {
      console.error('❌ [CHILD] Failed to add goal:', error)
      throw error
    }
  }

  const updateGoalProgress = async (goalId: string, amount: number) => {
    // Check if we're in demo mode
    const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
    
    if (isDemoMode || !apiService.isAuthenticated()) {
      // Use mock data for demo mode
      const goal = goals.value.find(g => g.id === goalId)
      if (goal) {
        goal.currentAmount = Math.min(goal.currentAmount + amount, goal.targetAmount)
      }
      return
    }

    try {
      console.log('💰 [CHILD] Updating goal progress:', goalId, '+', amount, 'coins')
      
      const response = await apiService.updateGoalProgress(goalId, amount)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        const goal = goals.value.find(g => g.id === goalId)
        if (goal) {
          goal.currentAmount = response.data.current_amount
          console.log('✅ [CHILD] Goal progress updated:', goal.name, '=', goal.currentAmount)
        }
      }
    } catch (error) {
      console.error('❌ [CHILD] Failed to update goal progress:', error)
      throw error
    }
  }

  const completeActivity = (activityId: string) => {
    const activity = activities.value.find(a => a.id === activityId)
    if (activity) {
      activity.completed = true
      addTransaction({
        type: 'earned',
        amount: activity.coins,
        description: activity.name,
        timestamp: new Date()
      })
    }
  }

  const addTransaction = async (transaction: Omit<Transaction, 'id'>) => {
    // Check if we're in demo mode
    const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
    
    if (isDemoMode || !apiService.isAuthenticated()) {
      // Use mock data for demo mode
      transactions.value.unshift({
        ...transaction,
        id: Date.now().toString()
      })
      return
    }

    try {
      const apiTransaction = {
        user_id: '', // Will be set by backend
        type: transaction.type === 'earned' ? 'earn' : transaction.type === 'spent' ? 'spend' : 'save',
        amount: transaction.amount,
        description: transaction.description,
        category: transaction.type,
        source: 'activity'
      }

      const response = await apiService.createTransaction(apiTransaction)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        const newTransaction: Transaction = {
          id: response.data.id,
          type: response.data.type === 'earn' ? 'earned' : response.data.type === 'spend' ? 'spent' : 'saved',
          amount: response.data.amount,
          description: response.data.description,
          timestamp: new Date(response.data.created_at)
        }
        transactions.value.unshift(newTransaction)
      }
    } catch (error) {
      console.error('Failed to add transaction:', error)
      throw error
    }
  }

  const updateBudget = (allocation: typeof budgetAllocation.value) => {
    budgetAllocation.value = allocation
  }

  return {
    goals,
    activities,
    transactions,
    budgetAllocation,
    addGoal,
    updateGoalProgress,
    completeActivity,
    addTransaction,
    updateBudget
  }
})