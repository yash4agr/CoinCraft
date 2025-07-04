import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: string
  fullName: string
  email: string
  username: string
  role: 'parent' | 'teacher' | 'younger_child' | 'older_child'
  coins?: number
  avatar?: string
  createdAt: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  fullName: string
  email: string
  username: string
  role: 'parent' | 'teacher'
  password: string
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const isAuthenticated = ref(false)

  // Demo users for development
  const demoUsers: User[] = [
    {
      id: '1',
      fullName: 'Luna Smith',
      email: 'luna@demo.com',
      username: 'luna_demo',
      role: 'younger_child',
      coins: 135,
      avatar: '🦸‍♀️',
      createdAt: '2024-01-15'
    },
    {
      id: '2',
      fullName: 'Harry Johnson',
      email: 'harry@demo.com',
      username: 'harry_demo',
      role: 'older_child',
      coins: 245,
      avatar: '🧙‍♂️',
      createdAt: '2024-01-10'
    },
    {
      id: '3',
      fullName: 'Sarah Parent',
      email: 'sarah@demo.com',
      username: 'parent_demo',
      role: 'parent',
      avatar: '👩‍💼',
      createdAt: '2024-01-05'
    },
    {
      id: '4',
      fullName: 'Mrs. Johnson',
      email: 'teacher@demo.com',
      username: 'teacher_demo',
      role: 'teacher',
      avatar: '👩‍🏫',
      createdAt: '2024-01-01'
    }
  ]

  // Getters
  const userRole = computed(() => user.value?.role)
  const isParent = computed(() => user.value?.role === 'parent')
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isChild = computed(() => 
    user.value?.role === 'younger_child' || user.value?.role === 'older_child'
  )

  // Actions
  const login = async (credentials: LoginCredentials): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      // TODO: add backend api endpoint for login
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Demo login logic
      const foundUser = demoUsers.find(u => u.username === credentials.username)
      
      if (!foundUser) {
        throw new Error('Invalid username or password')
      }

      user.value = foundUser
      isAuthenticated.value = true
      
      // Store session
      localStorage.setItem('coincraft_user', JSON.stringify(foundUser))
      localStorage.setItem('coincraft_token', 'demo_token_' + foundUser.id)

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: RegisterData): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      // TODO: add backend api endpoint for registration
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500))

      // Check if username/email already exists
      const existingUser = demoUsers.find(u => 
        u.username === data.username || u.email === data.email
      )
      
      if (existingUser) {
        throw new Error('Username or email already exists')
      }

      // Create new user
      const newUser: User = {
        id: Date.now().toString(),
        fullName: data.fullName,
        email: data.email,
        username: data.username,
        role: data.role,
        avatar: data.role === 'parent' ? '👨‍👩‍👧‍👦' : '👩‍🏫',
        createdAt: new Date().toISOString().split('T')[0]
      }

      user.value = newUser
      isAuthenticated.value = true
      
      // Store session
      localStorage.setItem('coincraft_user', JSON.stringify(newUser))
      localStorage.setItem('coincraft_token', 'demo_token_' + newUser.id)

    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      // TODO: add backend api endpoint for logout
      user.value = null
      isAuthenticated.value = false
      
      // Clear session
      localStorage.removeItem('coincraft_user')
      localStorage.removeItem('coincraft_token')
      
    } catch (err) {
      console.error('Logout error:', err)
    }
  }

  const checkAuth = async (): Promise<void> => {
    try {
      // TODO: add backend api endpoint for session validation
      const storedUser = localStorage.getItem('coincraft_user')
      const storedToken = localStorage.getItem('coincraft_token')
      
      if (storedUser && storedToken) {
        user.value = JSON.parse(storedUser)
        isAuthenticated.value = true
      }
    } catch (err) {
      console.error('Auth check error:', err)
      await logout()
    }
  }

  const clearError = (): void => {
    error.value = null
  }

  const demoLogin = async (role: User['role']): Promise<void> => {
    const demoUser = demoUsers.find(u => u.role === role)
    if (demoUser) {
      await login({ username: demoUser.username, password: 'demo123' })
    }
  }

  return {
    // State
    user,
    isLoading,
    error,
    isAuthenticated,
    
    // Getters
    userRole,
    isParent,
    isTeacher,
    isChild,
    
    // Actions
    login,
    register,
    logout,
    checkAuth,
    clearError,
    demoLogin,
    
    // Demo data
    demoUsers
  }
})