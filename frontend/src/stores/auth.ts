import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { apiService } from '../services/api'
import { validateUser } from '../utils/typeMappers'
import type { User, UserRole } from '../types'
import { resetAllStores } from '@/plugins/storeReset'

// Updated interface to match FastAPI OAuth2 requirements (email as username)
interface LoginCredentials {
  username: string  // Will be email for FastAPI compatibility
  password: string
}

// Updated interface to match backend UserCreate schema
interface RegisterData {
  name: string
  email: string
  password: string
  role: UserRole  // Use proper UserRole type
  avatar_url?: string
  age?: number  // For child profiles
}

// Error interface for better error handling
interface AuthError {
  message: string
  code?: string
  details?: any
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<AuthError | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userRole = computed(() => user.value?.role)
  const isParent = computed(() => user.value?.role === 'parent')
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isChild = computed(() => user.value?.role === 'younger_child')
  const isTeen = computed(() => user.value?.role === 'older_child')

  // Actions
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    console.log('🔐 [AUTH] Attempting login for:', credentials.username)
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.login(credentials)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data?.access_token && response.data?.user) {
        // Validate user data from backend
        if (!validateUser(response.data.user)) {
          throw new Error('Invalid user data received from server')
        }

        token.value = response.data.access_token
        user.value = response.data.user
        if (user.value.role === 'younger_child' || user.value.role === 'older_child') {
          // Ensure age is set for child profiles
          const coinsresponse = await apiService.getCoins(user.value.id)
          if (coinsresponse.error) {
            throw new Error(coinsresponse.error)
          }
          else{
            user.value.coins = coinsresponse.data || 0
            console.log('✅ [AUTH] Coins loaded for child:', user.value.name, 'Coins:', user.value.coins)
          }
        }
        // Persist to localStorage
        localStorage.setItem('auth_token', response.data.access_token)
        localStorage.setItem('auth_user', JSON.stringify(user.value))
        
        console.log('✅ [AUTH] Login successful for:', user.value.name)
        return true
      }

      throw new Error('Invalid response from server')

    } catch (err: any) {
      console.error('❌ [AUTH] Login failed:', err.message)
      error.value = { message: err.message, code: 'LOGIN_FAILED' }
      return false
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData: RegisterData): Promise<boolean> => {
    console.log('📝 [AUTH] Attempting registration for:', userData.email)
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.register(userData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data?.access_token && response.data?.user) {
        // Validate user data from backend
        if (!validateUser(response.data.user)) {
          throw new Error('Invalid user data received from server')
        }

        token.value = response.data.access_token
        user.value = response.data.user
        
        // Persist to localStorage
        localStorage.setItem('auth_token', response.data.access_token)
        localStorage.setItem('auth_user', JSON.stringify(response.data.user))
        
        console.log('✅ [AUTH] Registration successful for:', user.value.name)
        return true
      }

      throw new Error('Invalid response from server')

    } catch (err: any) {
      console.error('❌ [AUTH] Registration failed:', err.message)
      error.value = { message: err.message, code: 'REGISTRATION_FAILED' }
      return false
    } finally {
      isLoading.value = false
    }
  }

    const checkAuth = async (): Promise<boolean> => {
    console.log('🔍 [AUTH] Checking authentication status...')
    
    if (!token.value) {
      console.log('❌ [AUTH] No token found')
      return false
    }

    try {
      // Verify token is still valid by fetching current user
      const response = await apiService.getCurrentUser()
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        user.value = response.data
        if (user.value.role === 'younger_child' || user.value.role === 'older_child') {
          // Ensure age is set for child profiles
          const coinsresponse = await apiService.getCoins(user.value.id)
          if (coinsresponse.error) {
            throw new Error(coinsresponse.error)
          }
          else{
            user.value.coins = coinsresponse.data || 0
            console.log('✅ [AUTH] Coins loaded for child:', user.value.name, 'Coins:', user.value.coins)
          }
        }
        console.log('✅ [AUTH] Token valid, user verified:', user.value.name)
        return true
      }

      throw new Error('Invalid user data received')

    } catch (err: any) {
      console.error('❌ [AUTH] Token validation failed:', err.message)
      // Clear invalid token
      await logout()
      return false
    }
  }

  const logout = async (): Promise<void> => {
    console.log('🚪 [AUTH] Logging out user:', user.value?.name)
    
    try {
      await apiService.logout()
    } catch (err) {
      console.warn('⚠️ [AUTH] Logout API call failed:', err)
    }

    // Clear state
    user.value = null
    token.value = null
    error.value = null

    // Clear localStorage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_user')
    localStorage.removeItem('user-profile')
    localStorage.removeItem('coincraft_user')
    localStorage.removeItem('recent-transactions')
    resetAllStores()
    console.log('✅ [AUTH] Logout complete')
  }

  const initializeAuth = (): void => {
    console.log('🔄 [AUTH] Initializing authentication from storage...')
    
    try {
      const storedToken = localStorage.getItem('auth_token')
      const storedUser = localStorage.getItem('auth_user')

      if (storedToken && storedUser) {
        token.value = storedToken
        user.value = JSON.parse(storedUser)
        
        console.log('✅ [AUTH] Authentication restored for:', user.value?.name)
        
        // Optionally verify token is still valid
        checkAuth().catch(() => {
          console.warn('⚠️ [AUTH] Stored token validation failed')
        })
      } else {
        console.log('ℹ️ [AUTH] No stored authentication found')
      }
    } catch (err) {
      console.error('❌ [AUTH] Failed to initialize auth from storage:', err)
      // Clear corrupted data
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
    }
  }

  const clearError = (): void => {
    error.value = null
  }

  const refreshUser = async (): Promise<void> => {
    if (!token.value) return

    try {
      const response = await apiService.getCurrentUser()
      if (response.data) {
        // Validate user data from backend
        if (!validateUser(response.data)) {
          console.error('❌ [AUTH] Invalid user data received during refresh')
          return
        }
        
        user.value = response.data
        if (user.value.role === 'younger_child' || user.value.role === 'older_child') {
          // Ensure age is set for child profiles
          const coinsresponse = await apiService.getCoins(user.value.id)
          if (coinsresponse.error) {
            throw new Error(coinsresponse.error)
          }
          else{
            user.value.coins = coinsresponse.data || 0
            console.log('✅ [AUTH] Coins loaded for child:', user.value.name, 'Coins:', user.value.coins)
          }
        }
        localStorage.setItem('auth_user', JSON.stringify(user.value))
      }
    } catch (err) {
      console.error('❌ [AUTH] Failed to refresh user data:', err)
    }
  }

  const $reset = () => {
    user.value = null
    token.value = null
    error.value = null
  }

  watch(user, (newVal) => {
    console.log('User state changed:', newVal)
    localStorage.setItem('auth_user', JSON.stringify(newVal))
  }, { deep: true })


  return {
    // State
    user,
    token,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    userRole,
    isParent,
    isTeacher,
    isChild,
    isTeen,
    
    // Actions
    login,
    register,
    logout,
    checkAuth,
    initializeAuth,
    clearError,
    refreshUser
  }
})
