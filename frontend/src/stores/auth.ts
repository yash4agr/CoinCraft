import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService, type User as ApiUser, type LoginRequest, type RegisterRequest } from '../services/api'

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
    console.log('🎬 [AUTH] ===== LOGIN PROCESS STARTED =====');
    console.log('🎬 [AUTH] Input credentials:', { username: credentials.username, password: '***' });
    console.log('🎬 [AUTH] Auth store state before login:', { 
      isLoading: isLoading.value, 
      isAuthenticated: isAuthenticated.value,
      hasUser: !!user.value,
      hasError: !!error.value
    });
    
    isLoading.value = true
    error.value = null

    try {
      console.log('🔐 [AUTH] Starting login process...');
      console.log('🔐 [AUTH] Converting credentials to API format...');
      
      // Convert to API format (username -> email)
      const apiCredentials: LoginRequest = {
        email: credentials.username, // Using username as email for demo
        password: credentials.password
      }

      console.log('🔐 [AUTH] API credentials prepared:', { email: apiCredentials.email, password: '***' });
      console.log('📡 [AUTH] Calling apiService.login()...');
      
      const response = await apiService.login(apiCredentials)
      
      console.log('🔍 [AUTH] API Service response received');
      console.log('🔍 [AUTH] Response type:', typeof response);
      console.log('🔍 [AUTH] Response structure:', {
        hasError: !!response.error,
        hasData: !!response.data,
        errorMessage: response.error,
        dataKeys: response.data ? Object.keys(response.data) : 'N/A'
      });
      console.log('🔍 [AUTH] Full response:', response);
      
      if (response.error) {
        console.error('❌ Login error:', response.error)
        throw new Error(response.error)
      }

      if (!response.data) {
        console.error('❌ No data received from login')
        throw new Error('Login failed - no data received')
      }

      console.log('✅ Login successful, processing user data...')
      
      // Convert API user to local user format
      const apiUser = response.data.user
      const localUser: User = {
        id: apiUser.id,
        fullName: apiUser.name,
        email: apiUser.email,
        username: apiUser.email, // Using email as username
        role: apiUser.role as User['role'],
        avatar: apiUser.avatar_url || '👤',
        createdAt: apiUser.created_at
      }

      console.log('👤 User data processed:', localUser)

      user.value = localUser
      isAuthenticated.value = true
      
      // Store session
      localStorage.setItem('coincraft_user', JSON.stringify(localUser))
      
      console.log('🎉 Login completed successfully!')

    } catch (err) {
      console.error('💥 Login failed:', err)
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const register = async (data: RegisterData): Promise<void> => {
    console.log('📝 [AUTH] ===== REGISTRATION PROCESS STARTED =====');
    console.log('📝 [AUTH] Registration data:', { 
      fullName: data.fullName, 
      email: data.email, 
      username: data.username, 
      role: data.role,
      password: '***' 
    });

    isLoading.value = true
    error.value = null

    try {
      // Convert to API format
      const apiData: RegisterRequest = {
        email: data.email,
        password: data.password,
        name: data.fullName,
        role: data.role,
        avatar_url: data.role === 'parent' ? '👨‍👩‍👧‍👦' : '👩‍🏫'
      }

      console.log('📝 [AUTH] Calling API registration...');
      
      // Disable demo mode to ensure real API calls
      localStorage.removeItem('coincraft_demo_mode')
      
      const response = await apiService.register(apiData)
      
      console.log('📝 [AUTH] Registration response:', response);

      if (response.error) {
        console.error('❌ Registration error:', response.error);
        throw new Error(response.error)
      }

      if (!response.data) {
        console.error('❌ No data received from registration');
        throw new Error('Registration failed - no data received')
      }

      console.log('✅ Registration successful, processing user data...');

      // Convert API user to local user format
      const apiUser = response.data.user
      const localUser: User = {
        id: apiUser.id,
        fullName: apiUser.name,
        email: apiUser.email,
        username: apiUser.email, // Using email as username
        role: apiUser.role as User['role'],
        avatar: apiUser.avatar_url || '👤',
        createdAt: apiUser.created_at
      }

      console.log('👤 User data processed:', localUser);

      user.value = localUser
      isAuthenticated.value = true
      
      // Store session
      localStorage.setItem('coincraft_user', JSON.stringify(localUser))
      
      // Ensure we're not in demo mode
      localStorage.removeItem('coincraft_demo_mode')

      console.log('🎉 Registration and login completed successfully!');

    } catch (err) {
      console.error('💥 Registration failed:', err);
      
      // Provide more helpful error messages
      let errorMessage = 'Registration failed. Please try again.';
      
      if (err instanceof Error) {
        errorMessage = err.message;
        
        // Enhance common error messages
        if (errorMessage.includes('already exists')) {
          errorMessage = 'A user with this email already exists. Please try another email address.';
        } else if (errorMessage.includes('server error') || errorMessage.includes('500')) {
          errorMessage = 'Server error. Please try again later or contact support.';
        } else if (errorMessage.includes('network') || errorMessage.includes('fetch')) {
          errorMessage = 'Network error. Please check your internet connection and try again.';
        }
      }
      
      error.value = errorMessage;
      throw new Error(errorMessage);
    } finally {
      isLoading.value = false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      isLoading.value = true
      
      // Call API logout
      await apiService.logout()
      
      // Clear all user-related stores
      const { useUserStore } = await import('./user')
      const { useDashboardStore } = await import('./dashboard')
      const userStore = useUserStore()
      const dashboardStore = useDashboardStore()
      
      // Reset all store states
      userStore.$reset()
      dashboardStore.$reset()
      
      // Clear authentication state
      user.value = null
      isAuthenticated.value = false
      
      // Clear session
      localStorage.removeItem('coincraft_user')
      
      // Clear any cached data
      sessionStorage.clear()
      
    } catch (err) {
      console.error('Logout error:', err)
      // Even if API logout fails, clear local state
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('coincraft_user')
      sessionStorage.clear()
    } finally {
      isLoading.value = false
    }
  }

  const checkAuth = async (): Promise<void> => {
    try {
      // Check if we have a token and it's valid
      if (!apiService.isAuthenticated()) {
        return
      }

      const response = await apiService.getCurrentUser()
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (!response.data) {
        throw new Error('No user data received')
      }

      // Convert API user to local user format
      const apiUser = response.data
      const localUser: User = {
        id: apiUser.id,
        fullName: apiUser.name,
        email: apiUser.email,
        username: apiUser.email, // Using email as username
        role: apiUser.role as User['role'],
        avatar: apiUser.avatar_url || '👤',
        createdAt: apiUser.created_at
      }

      user.value = localUser
      isAuthenticated.value = true
      
      // Update stored user
      localStorage.setItem('coincraft_user', JSON.stringify(localUser))
      
    } catch (err) {
      console.error('Auth check error:', err)
      await logout()
    }
  }

  const clearError = (): void => {
    error.value = null
  }

  const demoLogin = async (role: User['role']): Promise<void> => {
    // For demo purposes, we can either:
    // 1. Use real API login with demo credentials
    // 2. Use mock login for demo pages
    
    // Option 1: Real API login (recommended for full demo)
    const demoCredentials = {
      parent: { username: 'parent@demo.com', password: 'demo123' },
      teacher: { username: 'teacher@demo.com', password: 'demo123' },
      younger_child: { username: 'luna@demo.com', password: 'demo123' },
      older_child: { username: 'harry@demo.com', password: 'demo123' }
    }

    const credentials = demoCredentials[role]
    if (credentials) {
      await login(credentials)
    }
  }

  // Mock login for demo pages (when API is not available)
  const mockDemoLogin = async (role: User['role']): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Use mock user data for demo
      const demoUser = demoUsers.find(u => u.role === role)
      if (demoUser) {
        user.value = demoUser
        isAuthenticated.value = true
        localStorage.setItem('coincraft_user', JSON.stringify(demoUser))
        localStorage.setItem('coincraft_demo_mode', 'true')
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Demo login failed'
      throw err
    } finally {
      isLoading.value = false
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
    mockDemoLogin,
    
    // Demo data
    demoUsers
  }
})