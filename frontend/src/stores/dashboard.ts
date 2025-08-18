import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'
import { 
  mapBackendGoals, mapBackendTransactions, mapBackendModules
} from '../utils/typeMappers'
import type { 
  DashboardData, 
  Activity, Achievement, Transaction, Module, UserRole
} from '../types'

// Legacy interfaces kept for backward compatibility during transition
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

// Dashboard Error interface
interface DashboardError {
  message: string
  code?: string
  timestamp: Date
}

export const useDashboardStore = defineStore('dashboard', () => {
  const activities = ref<Activity[]>([])
  const achievements = ref<Achievement[]>([])
  const todaysGoals = ref<ProgressGoal[]>([])
  const learningModules = ref<LearningModule[]>([])
  const quickActions = ref([
    {
      id: 'budget',
      title: 'Budget',
      description: 'Track spending',
      icon: 'ri-pie-chart-line',
      iconBg: 'bg-blue-100',
      iconColor: '#3B82F6',
      route: '/teen/budget'
    },
    {
      id: 'goals',
      title: 'Goals',
      description: 'Set targets',
      icon: 'ri-target-line',
      iconBg: 'bg-green-100',
      iconColor: '#10B981',
      route: '/teen/goals'
    },
    {
      id: 'activities',
      title: 'Activities',
      description: 'Learn & earn',
      icon: 'ri-book-open-line',
      iconBg: 'bg-purple-100',
      iconColor: '#8B5CF6',
      route: '/teen/activities'
    },
    {
      id: 'shop',
      title: 'Shop',
      description: 'Spend coins',
      icon: 'ri-shopping-bag-line',
      iconBg: 'bg-orange-100',
      iconColor: '#F59E0B',
      route: '/teen/shop'
    }
  ])
  const isLoading = ref(false)
  const error = ref<DashboardError | null>(null)

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

  const loadDashboardData = async (userRole: UserRole) => {
    try {
      isLoading.value = true
      error.value = null
      
      // Check if user is authenticated (has valid token)
      if (!apiService.isAuthenticated()) {
        console.log('🔐 [DASHBOARD] User not authenticated, loading mock data...')
        // Use mock data for demo/unauthenticated users
        if (userRole === 'younger_child' || userRole === 'older_child') {
          await loadChildMockData(userRole)
          return // Add this return statement
        }
        return
      }
      
      console.log('🔐 [DASHBOARD] User authenticated, loading from API...')
      // Use real API data for authenticated users
      const response = await apiService.getDashboardData(userRole)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No dashboard data received')
      }

      // Map API response to frontend types using type mappers
      await mapDashboardResponse(response.data, userRole)

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load dashboard data'
      error.value = {
        message: errorMessage,
        code: 'DASHBOARD_LOAD_ERROR',
        timestamp: new Date()
      }
      console.error('Dashboard data loading error:', err)
      
      // Fallback to mock data if API fails
      if (userRole === 'younger_child' || userRole === 'older_child') {
        console.log('🔄 [DASHBOARD] API failed, falling back to mock data...')
        await loadChildMockData(userRole)
      }
    } finally {
      isLoading.value = false
    }
  }

  const mapDashboardResponse = async (data: DashboardData, userRole: UserRole) => {
    try {
      // Map achievements - keep as proper Achievement type
      if (data.achievements) {
        achievements.value = data.achievements
      }

      // Map goals using type mapper  
      if (data.active_goals) {
        todaysGoals.value = mapBackendGoals(data.active_goals).map(goal => ({
          id: goal.id,
          title: goal.title,
          current: goal.current_amount,
          total: goal.target_amount,
          icon: goal.icon || 'ri-target-line',
          colorScheme: 'blue' as const
        }))
      }

      // Map transactions to learning modules (check for activity type instead of module)
      if (data.recent_transactions) {
        const moduleTransactions = mapBackendTransactions(data.recent_transactions)
          .filter((t: Transaction) => t.reference_type === 'activity')
        
        learningModules.value = moduleTransactions.map((transaction: Transaction) => ({
          id: transaction.reference_id || transaction.id,
          title: transaction.description,
          description: `Completed activity: ${transaction.description}`,
          emoji: '📚',
          difficulty: 'easy' as const,
          coins: transaction.amount,
          completed: true,
          colorScheme: 'green' as const,
          buttonText: 'Completed',
          estimatedTime: 15,
          skills: ['Learning', 'Progress']
        }))
      }

      // Load activities from modules
      await loadActivitiesFromAPI(userRole)

    } catch (err) {
      console.error('Error mapping dashboard response:', err)
      throw err
    }
  }

  const loadActivitiesFromAPI = async (userRole: UserRole) => {
    try {
      // Load modules as activities
      const modulesResponse = await apiService.getModules()
      if (modulesResponse) {
        const mappedModules = mapBackendModules(modulesResponse)
        activities.value = mappedModules.map((module: Module) => ({
          id: module.id,
          title: module.title,
          description: module.description,
          type: 'module' as const,
          difficulty: module.difficulty,
          coins: module.points_reward,
          duration: module.estimated_duration || 15,
          completed: false, // TODO: Check user progress
          icon: '📚',
          category: module.category || 'learning',
          age_group: userRole === 'younger_child' ? 'younger_child' : 'older_child'
        }))
      }
    } catch (error) {
      console.error('Failed to load activities:', error)
      // Fallback to empty array
      activities.value = []
    }
  }

  const loadChildMockData = async (userRole: UserRole) => {
    if (userRole === 'younger_child') {
      await loadYoungerChildActivities()
    } else if (userRole === 'older_child') {
      await loadOlderChildActivities()
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
        age_group: 'younger_child'
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
        age_group: 'younger_child'
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
        age_group: 'younger_child'
      }
    ]

    achievements.value = [
      {
        id: '1',
        title: 'First Steps',
        description: 'Completed your first lesson!',
        icon: 'ri-foot-print-line',
        rarity: 'Beginner',
        points_reward: 10,
        earned_at: new Date()
      },
      {
        id: '2',
        title: 'Coin Collector',
        description: 'Earned your first 50 coins.',
        icon: 'ri-coins-line',
        rarity: 'Collector',
        points_reward: 20,
        earned_at: new Date(Date.now() - 86400000) // Yesterday
      },
      {
        id: '3',
        title: 'Smart Saver',
        description: 'Saved money for 3 days straight.',
        icon: 'ri-save-line',
        rarity: 'Saver',
        points_reward: 25,
        earned_at: new Date(Date.now() - 172800000) // 2 days ago
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
        age_group: 'older_child'
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
        age_group: 'older_child'
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
        age_group: 'older_child'
      }
    ]

    achievements.value = [
      {
        id: '1',
        title: 'Investment Pro',
        description: 'Completed your first investment simulation.',
        icon: 'ri-line-chart-line',
        rarity: 'Pro Investor',
        points_reward: 50,
        earned_at: new Date()
      },
      {
        id: '2',
        title: 'Budget Planner',
        description: 'Successfully created your first budget.',
        icon: 'ri-calculator-line',
        rarity: 'Budget Master',
        points_reward: 30,
        earned_at: new Date(Date.now() - 86400000) // Yesterday
      },
      {
        id: '3',
        title: 'Crypto Scholar',
        description: 'Learned the basics of cryptocurrency.',
        icon: 'ri-bitcoin-line',
        rarity: 'Crypto Expert',
        points_reward: 45,
        earned_at: new Date(Date.now() - 172800000) // 2 days ago
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
      const errorMessage = err instanceof Error ? err.message : 'Failed to complete activity'
      error.value = {
        message: errorMessage,
        code: 'ACTIVITY_COMPLETE_ERROR',
        timestamp: new Date()
      }
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
      const errorMessage = err instanceof Error ? err.message : 'Failed to complete module'
      error.value = {
        message: errorMessage,
        code: 'MODULE_COMPLETE_ERROR',
        timestamp: new Date()
      }
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
      const errorMessage = err instanceof Error ? err.message : 'Failed to update goal progress'
      error.value = {
        message: errorMessage,
        code: 'GOAL_UPDATE_ERROR',
        timestamp: new Date()
      }
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
    quickActions,
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