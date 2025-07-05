import { defineStore } from 'pinia'
import { ref } from 'vue'

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

  const addGoal = (goal: Omit<Goal, 'id' | 'createdAt'>) => {
    goals.value.push({
      ...goal,
      id: Date.now().toString(),
      createdAt: new Date()
    })
  }

  const updateGoalProgress = (goalId: string, amount: number) => {
    const goal = goals.value.find(g => g.id === goalId)
    if (goal) {
      goal.currentAmount = Math.min(goal.currentAmount + amount, goal.targetAmount)
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

  const addTransaction = (transaction: Omit<Transaction, 'id'>) => {
    transactions.value.unshift({
      ...transaction,
      id: Date.now().toString()
    })
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