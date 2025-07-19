import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService } from '../services/api'

export interface Child {
  id: string
  name: string
  age: number
  coins: number
  goalsActive: number
  lastActivity: Date
  avatar: string
  email?: string
  username?: string
  password?: string
  completedTasks?: number
  recentActivity?: any[]
  currentGoals?: any[]
  initials?: string
  avatarColor?: string
}

export interface Task {
  id: string
  childId: string
  description: string
  coins: number
  dueDate?: Date
  completed: boolean
  requiresApproval: boolean
  createdAt: Date
}

export interface RedemptionRequest {
  id: string
  childId: string
  childName: string
  amount: number
  coins: number
  status: 'pending' | 'approved' | 'rejected'
  createdAt: Date
}

export const useParentStore = defineStore('parent', () => {
  const children = ref<Child[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const familyStats = ref({
    totalChildren: 0,
    totalCoinsEarned: 0,
    completedTasks: 0,
    activeGoals: 0
  })

  const tasks = ref<Task[]>([
    {
      id: '1',
      childId: '1',
      description: 'Clean your room',
      coins: 15,
      completed: false,
      requiresApproval: true,
      createdAt: new Date(Date.now() - 86400000)
    }
  ])

  const redemptionRequests = ref<RedemptionRequest[]>([
    {
      id: '1',
      childId: '1',
      childName: 'Luna',
      amount: 2.50,
      coins: 25,
      status: 'approved',
      createdAt: new Date(Date.now() - 172800000)
    },
    {
      id: '2',
      childId: '2',
      childName: 'Harry',
      amount: 5.00,
      coins: 50,
      status: 'pending',
      createdAt: new Date(Date.now() - 86400000)
    }
  ])

  const exchangeRate = ref(0.10)
  const autoApproveLimit = ref(5)

  const addChild = (child: Omit<Child, 'id'>) => {
    children.value.push({
      ...child,
      id: Date.now().toString()
    })
  }

  const assignTask = (task: Omit<Task, 'id' | 'createdAt'>) => {
    tasks.value.push({
      ...task,
      id: Date.now().toString(),
      createdAt: new Date()
    })
  }

  const approveRedemption = (requestId: string) => {
    const request = redemptionRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'approved'
    }
  }

  const rejectRedemption = (requestId: string) => {
    const request = redemptionRequests.value.find(r => r.id === requestId)
    if (request) {
      request.status = 'rejected'
    }
  }

  // API Actions
  const loadDashboard = async () => {
    isLoading.value = true
    error.value = null

    try {
      console.log('🏠 [PARENT] Loading parent dashboard...')
      
      // Check if we're in demo mode
      const isDemoMode = localStorage.getItem('coincraft_demo_mode') === 'true'
      console.log('🏠 [PARENT] Demo mode:', isDemoMode ? 'ON' : 'OFF')
      
      if (isDemoMode) {
        console.log('🏠 [PARENT] Using demo data in demo mode')
        // Use demo data in demo mode
        return
      }
      
      const response = await apiService.request('/api/parent/dashboard', {
        method: 'GET'
      })

      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        console.log('📊 [PARENT] Dashboard response:', response.data)
        console.log('👶 [PARENT] Children data:', response.data.children)
        console.log('🔍 [PARENT] Raw children count:', response.data.children.length)
        console.log('👤 [PARENT] Parent info:', response.data.parent)
        
        // Store parent info in localStorage for reference
        localStorage.setItem('coincraft_parent_id', response.data.parent.id)
        localStorage.setItem('coincraft_parent_email', response.data.parent.email)
        
        // Clear children array first
        children.value = []
        
        // Map children data
        children.value = response.data.children.map((child: any) => {
          console.log('👤 [PARENT] Mapping child:', child.name, 'with username:', child.username)
          return {
          id: child.id,
          name: child.name,
          age: child.age,
          coins: child.coins,
          goalsActive: child.active_goals,
          lastActivity: new Date(),
          avatar: child.avatar_url || '👤',
          email: child.email || 'Not set',
          username: child.username || `${child.name.toLowerCase().replace(/\s+/g, '')}${child.age}`,
          password: '******',  // Placeholder for security
          completedTasks: child.completed_tasks || 0,
          recentActivity: child.recent_activity || [],
          currentGoals: [],  // Default empty goals
          initials: child.name.charAt(0).toUpperCase(),
          avatarColor: 'blue'  // Default color
        }
        })

        console.log('✅ [PARENT] Mapped children array:', children.value.length, 'items')
        console.log('👶 [PARENT] Final children data:', children.value)

        familyStats.value = response.data.family_stats
        console.log('✅ [PARENT] Dashboard loaded successfully, children count:', children.value.length)
      }
    } catch (err) {
      console.error('❌ [PARENT] Failed to load dashboard:', err)
      error.value = err instanceof Error ? err.message : 'Failed to load dashboard'
    } finally {
      isLoading.value = false
    }
  }

  const addChildAPI = async (childData: { name: string; age: number; email?: string; avatarColor?: string }) => {
    isLoading.value = true
    error.value = null

    try {
      console.log('👶 [PARENT] Adding new child:', childData.name)
      
      const response = await apiService.request('/api/parent/children', {
        method: 'POST',
        body: JSON.stringify(childData)
      })

      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        // Reload dashboard to get updated data
        await loadDashboard()
        console.log('✅ [PARENT] Child added successfully')
        return response.data.child
      }
    } catch (err) {
      console.error('❌ [PARENT] Failed to add child:', err)
      error.value = err instanceof Error ? err.message : 'Failed to add child'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    children,
    tasks,
    redemptionRequests,
    familyStats,
    isLoading,
    error,
    exchangeRate,
    autoApproveLimit,
    
    // Actions
    addChild,
    assignTask,
    approveRedemption,
    rejectRedemption,
    loadDashboard,
    addChildAPI,
    clearError
  }
})
