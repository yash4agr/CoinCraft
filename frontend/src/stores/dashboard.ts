import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService, type DashboardData as ApiDashboardData } from '../services/api'

export interface Activity {
  id: string
  title: string
  description: string
  type: 'game' | 'quiz' | 'module' | 'challenge'
  difficulty: 'easy' | 'medium' | 'hard'
  coins: number
  duration: number
  completed: boolean
  icon: string
  category: string
  ageGroup: 'younger_child' | 'older_child' | 'both'
}

export interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  badge: string
  coins: number
  date: string
  colorScheme: 'green' | 'orange' | 'blue' | 'purple'
}

export interface ProgressGoal {
  id: string
  title: string
  current: number
  total: number
  icon: string
  colorScheme: 'orange' | 'blue' | 'green' | 'purple'
}

export interface LearningModule {
  id: string
  title: string
  description: string
  emoji: string
  difficulty: 'easy' | 'medium' | 'hard'
  coins: number
  completed: boolean
  colorScheme: 'pink' | 'teal' | 'blue' | 'green' | 'yellow' | 'purple'
  buttonText: string
  estimatedTime: number
  skills: string[]
}

export const useDashboardStore = defineStore('dashboard', () => {
  const activities = ref<Activity[]>([])
  const achievements = ref<Achievement[]>([])
  const todaysGoals = ref<ProgressGoal[]>([])
  const learningModules = ref<LearningModule[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const availableActivities = computed(() => 
    activities.value.filter(activity => !activity.completed)
  )
  
  const completedActivities = computed(() => 
    activities.value.filter(activity => activity.completed)
  )

  const recentAchievements = computed(() => 
    achievements.value.slice(0, 3)
  )

  const completedModulesCount = computed(() => 
    learningModules.value.filter(module => module.completed).length
  )

  const totalCoinsFromModules = computed(() => 
    learningModules.value
      .filter(module => module.completed)
      .reduce((total, module) => total + module.coins, 0)
  )

  const loadDashboardData = async (userRole: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      // Check if user is authenticated (has valid token)
      if (!apiService.isAuthenticated()) {
        // Use mock data for demo/unauthenticated users
        if (userRole === 'younger_child') {
          await loadYoungerChildData()
        } else if (userRole === 'older_child') {
          await loadOlderChildData()
        }
        return
      }
      
      // Use real API data for authenticated users
      const response = await apiService.getDashboardData(userRole)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No dashboard data received')
      }

      // Convert API data to local format
      const apiData = response.data
      
      // Load activities from API
      await loadActivitiesFromAPI(userRole)

      // Update achievements from API
      achievements.value = apiData.achievements.map(achievement => ({
        id: achievement.id,
        title: achievement.title,
        description: achievement.description,
        icon: achievement.icon || 'ri-trophy-line',
        badge: achievement.rarity || 'Common',
        coins: achievement.points_reward || 0,
        date: new Date(achievement.created_at || Date.now()).toLocaleDateString(),
        colorScheme: 'green' as const
      }))

      // Update goals from API
      todaysGoals.value = apiData.active_goals.map(goal => ({
        id: goal.id,
        title: goal.title,
        current: goal.current_amount,
        total: goal.target_amount,
        icon: goal.icon || 'ri-target-line',
        colorScheme: 'blue' as const
      }))

      // Update learning modules from API
      learningModules.value = apiData.recent_transactions
        .filter(t => t.reference_type === 'module')
        .map(transaction => ({
          id: transaction.reference_id || transaction.id,
          title: transaction.description,
          description: `Completed module: ${transaction.description}`,
          emoji: '📚',
          difficulty: 'easy' as const,
          coins: transaction.amount,
          completed: true,
          colorScheme: 'green' as const,
          buttonText: 'Completed',
          estimatedTime: 15,
          skills: ['Learning', 'Progress']
        }))

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load dashboard data'
      console.error('Dashboard data loading error:', err)
      
      // Fallback to mock data if API fails
      if (userRole === 'younger_child') {
        await loadYoungerChildData()
      } else if (userRole === 'older_child') {
        await loadOlderChildData()
      }
    } finally {
      isLoading.value = false
    }
  }

  const loadActivitiesFromAPI = async (userRole: string) => {
    try {
      // Load modules as activities
      const modulesResponse = await apiService.getModules()
      if (modulesResponse.data) {
        activities.value = modulesResponse.data.map(module => ({
          id: module.id,
          title: module.title,
          description: module.description,
          type: 'module' as const,
          difficulty: module.difficulty,
          coins: module.points_reward,
          duration: module.estimated_duration,
          completed: false, // TODO: Check user progress
          icon: '📚',
          category: module.category,
          ageGroup: userRole === 'younger_child' ? 'younger_child' : 'older_child'
        }))
      }
    } catch (error) {
      console.error('Failed to load activities:', error)
      // Fallback to empty array
      activities.value = []
    }
  }

  const loadYoungerChildActivities = async () => {
    todaysGoals.value = [
      {
        id: '1',
        title: 'Read Lessons',
        current: 2,
        total: 3,
        icon: 'ri-book-open-line',
        colorScheme: 'orange'
      },
      {
        id: '2',
        title: 'Earn Coins',
        current: 45,
        total: 50,
        icon: 'ri-coins-line',
        colorScheme: 'blue'
      },
      {
        id: '3',
        title: 'Complete Games',
        current: 1,
        total: 2,
        icon: 'ri-gamepad-line',
        colorScheme: 'green'
      },
      {
        id: '4',
        title: 'Practice Time',
        current: 15,
        total: 20,
        icon: 'ri-time-line',
        colorScheme: 'purple'
      }
    ]

    activities.value = [
      {
        id: '1',
        title: 'Piggy Bank Adventure',
        description: 'Learn how to save money with your digital piggy bank!',
        type: 'game',
        difficulty: 'easy',
        coins: 10,
        duration: 5,
        completed: false,
        icon: 'ri-bank-fill',
        category: 'saving',
        ageGroup: 'younger_child'
      },
      {
        id: '2',
        title: 'Needs vs Wants Game',
        description: 'Discover the difference between things you need and want.',
        type: 'game',
        difficulty: 'easy',
        coins: 15,
        duration: 7,
        completed: true,
        icon: 'ri-question-line',
        category: 'spending',
        ageGroup: 'younger_child'
      },
      {
        id: '3',
        title: 'Coin Counting Challenge',
        description: 'Practice counting coins and making change!',
        type: 'challenge',
        difficulty: 'medium',
        coins: 20,
        duration: 10,
        completed: false,
        icon: 'ri-coins-line',
        category: 'math',
        ageGroup: 'younger_child'
      }
    ]

    achievements.value = [
      {
        id: '1',
        title: 'First Steps',
        description: 'Completed your first lesson!',
        icon: 'ri-foot-print-line',
        badge: 'Beginner',
        coins: 10,
        date: 'Today',
        colorScheme: 'green'
      },
      {
        id: '2',
        title: 'Coin Collector',
        description: 'Earned your first 50 coins.',
        icon: 'ri-coins-line',
        badge: 'Collector',
        coins: 20,
        date: 'Yesterday',
        colorScheme: 'orange'
      },
      {
        id: '3',
        title: 'Smart Saver',
        description: 'Saved money for 3 days straight.',
        icon: 'ri-save-line',
        badge: 'Saver',
        coins: 25,
        date: '2 days ago',
        colorScheme: 'blue'
      }
    ]

    learningModules.value = [
      {
        id: '1',
        title: 'Money Basics',
        description: 'Learn about different types of money and how to count them.',
        emoji: '💰',
        difficulty: 'easy',
        coins: 15,
        completed: true,
        colorScheme: 'green',
        buttonText: 'Completed',
        estimatedTime: 10,
        skills: ['Counting', 'Money Recognition']
      },
      {
        id: '2',
        title: 'Saving Goals',
        description: 'Set and achieve your first savings goal.',
        emoji: '🎯',
        difficulty: 'easy',
        coins: 20,
        completed: false,
        colorScheme: 'blue',
        buttonText: 'Start Learning',
        estimatedTime: 15,
        skills: ['Goal Setting', 'Planning']
      },
      {
        id: '3',
        title: 'Smart Spending',
        description: 'Learn how to make smart choices when spending money.',
        emoji: '🛒',
        difficulty: 'medium',
        coins: 25,
        completed: false,
        colorScheme: 'yellow',
        buttonText: 'Start Learning',
        estimatedTime: 20,
        skills: ['Decision Making', 'Budgeting']
      }
    ]
  }

  const loadOlderChildActivities = async () => {
    todaysGoals.value = [
      {
        id: '1',
        title: 'Complete Modules',
        current: 1,
        total: 2,
        icon: 'ri-book-open-line',
        colorScheme: 'orange'
      },
      {
        id: '2',
        title: 'Earn Coins',
        current: 85,
        total: 100,
        icon: 'ri-coins-line',
        colorScheme: 'blue'
      },
      {
        id: '3',
        title: 'Investment Challenge',
        current: 2,
        total: 3,
        icon: 'ri-line-chart-line',
        colorScheme: 'green'
      },
      {
        id: '4',
        title: 'Budget Planning',
        current: 1,
        total: 1,
        icon: 'ri-calculator-line',
        colorScheme: 'purple'
      }
    ]

    activities.value = [
      {
        id: '1',
        title: 'Investment Simulator',
        description: 'Learn about stocks and bonds through interactive simulations.',
        type: 'module',
        difficulty: 'medium',
        coins: 30,
        duration: 15,
        completed: false,
        icon: 'ri-line-chart-line',
        category: 'investing',
        ageGroup: 'older_child'
      },
      {
        id: '2',
        title: 'Budget Master',
        description: 'Create and manage your personal budget.',
        type: 'game',
        difficulty: 'medium',
        coins: 25,
        duration: 12,
        completed: true,
        icon: 'ri-calculator-line',
        category: 'budgeting',
        ageGroup: 'older_child'
      },
      {
        id: '3',
        title: 'Crypto Basics',
        description: 'Understanding cryptocurrency and digital money.',
        type: 'quiz',
        difficulty: 'hard',
        coins: 40,
        duration: 20,
        completed: false,
        icon: 'ri-bitcoin-line',
        category: 'investing',
        ageGroup: 'older_child'
      }
    ]

    achievements.value = [
      {
        id: '1',
        title: 'Investment Pro',
        description: 'Completed your first investment simulation.',
        icon: 'ri-line-chart-line',
        badge: 'Pro Investor',
        coins: 50,
        date: 'Today',
        colorScheme: 'green'
      },
      {
        id: '2',
        title: 'Budget Planner',
        description: 'Successfully created your first budget.',
        icon: 'ri-calculator-line',
        badge: 'Budget Master',
        coins: 30,
        date: 'Yesterday',
        colorScheme: 'blue'
      },
      {
        id: '3',
        title: 'Crypto Scholar',
        description: 'Learned the basics of cryptocurrency.',
        icon: 'ri-bitcoin-line',
        badge: 'Crypto Expert',
        coins: 45,
        date: '2 days ago',
        colorScheme: 'orange'
      }
    ]

    learningModules.value = [
      {
        id: '1',
        title: 'Investment Fundamentals',
        description: 'Learn the basics of investing and growing your money.',
        emoji: '📈',
        difficulty: 'medium',
        coins: 35,
        completed: true,
        colorScheme: 'teal',
        buttonText: 'Completed',
        estimatedTime: 25,
        skills: ['Investment Basics', 'Risk Management']
      },
      {
        id: '2',
        title: 'Advanced Budgeting',
        description: 'Master advanced budgeting techniques and strategies.',
        emoji: '📊',
        difficulty: 'medium',
        coins: 40,
        completed: false,
        colorScheme: 'purple',
        buttonText: 'Start Learning',
        estimatedTime: 30,
        skills: ['Advanced Budgeting', 'Financial Planning']
      },
      {
        id: '3',
        title: 'Entrepreneurship',
        description: 'Learn how to start and manage your own business.',
        emoji: '🚀',
        difficulty: 'hard',
        coins: 50,
        completed: false,
        colorScheme: 'pink',
        buttonText: 'Start Learning',
        estimatedTime: 40,
        skills: ['Business Planning', 'Leadership']
      }
    ]
  }

  const completeActivity = async (activityId: string) => {
    try {
      const activity = activities.value.find(a => a.id === activityId)
      if (activity) {
        activity.completed = true
        return activity.coins
      }
      return 0
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to complete activity'
      return 0
    }
  }

  const completeModule = async (moduleId: string) => {
    try {
      const module = learningModules.value.find(m => m.id === moduleId)
      if (module) {
        module.completed = true
        return module.coins
      }
      return 0
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to complete module'
      return 0
    }
  }

  const updateTodaysGoalProgress = async (goalId: string, progress: number) => {
    try {
      const goal = todaysGoals.value.find(g => g.id === goalId)
      if (goal) {
        goal.current = Math.min(progress, goal.total)
        return true
      }
      return false
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update goal progress'
      return false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const $reset = () => {
    activities.value = []
    achievements.value = []
    todaysGoals.value = []
    learningModules.value = []
    isLoading.value = false
    error.value = null
  }

  return {
    activities,
    achievements,
    todaysGoals,
    learningModules,
    isLoading,
    error,
    availableActivities,
    completedActivities,
    recentAchievements,
    completedModulesCount,
    totalCoinsFromModules,
    loadDashboardData,
    completeActivity,
    completeModule,
    updateTodaysGoalProgress,
    clearError,
    $reset
  }
}) 