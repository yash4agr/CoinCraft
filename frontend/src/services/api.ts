/**
 * API Service Layer for CoinCraft Frontend
 * Handles all HTTP requests to the FastAPI backend using Axios
 */
import { httpClient, tokenManager } from './http'
import { 
  mapBackendUser, mapBackendGoal, mapBackendGoals, mapBackendTask
} from '../utils/typeMappers'
import type { 
  User, UserRole,
  Goal, Transaction, Task, Module,
  RedemptionRequest,
  DashboardData, Activity, AuthResponse
} from '../types'

// Wrapper types for backward compatibility with stores
export interface ApiResponse<T> {
  data?: T
  error?: string
}

// API Request/Response Types
export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  name: string
  role: UserRole
  username?: string
  avatar_url?: string
}

export interface GoalCreateRequest {
  title: string
  description?: string
  target_amount: number
  icon?: string
  color?: string
  deadline?: string
}

export interface TaskCreateRequest {
  title: string
  description?: string
  coins_reward: number
  assigned_to: string
  due_date?: string
  requires_approval?: boolean
}

/**
 * Main API Service Class
 */
class ApiService {
  // ===================
  // AUTHENTICATION METHODS
  // ===================

  /**
   * Login user with email/password
   * Backend expects FormData for OAuth2 compatibility
   */
  async login(credentials: LoginRequest): Promise<ApiResponse<AuthResponse>> {
    try {
      console.log('🔐 [API] Logging in user:', credentials.username)
      
      // Create FormData for OAuth2 login endpoint
    const params = new URLSearchParams()
    params.append('username', credentials.username)
    params.append('password', credentials.password)
    
    console.log('Sending params:', params.toString())
    console.log('Raw credentials:', credentials)
    
    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    }
    
    console.log('Request config:', config)
    
    const response = await httpClient.post('/api/auth/jwt/login', params, config)
      
      const { access_token } = response.data
      tokenManager.setToken(access_token)
      
      // Get user data
      const userResponse = await this.getCurrentUser()
      
      if (userResponse.error || !userResponse.data) {
        return { error: userResponse.error || 'Failed to get user data' }
      }
      
      const authResponse: AuthResponse = {
        access_token,
        token_type: 'bearer',
        user: mapBackendUser(userResponse.data) // Use type mapper
      }
      
      console.log('✅ [API] Login successful for user:', userResponse.data.email)
      return { data: authResponse }
      
    } catch (error: any) {
      console.error('❌ [API] Login failed:', error.message)
      return { error: error.message || 'Login failed' }
    }
  }

  /**
   * Register new user and auto-login
   */
  async register(userData: RegisterRequest): Promise<ApiResponse<AuthResponse>> {
    try {
      console.log('📝 [API] Registering new user:', userData.email)
      
      const response = await httpClient.post('/api/auth/register', userData)
      const { access_token, user } = response.data
      
      tokenManager.setToken(access_token)
      
      const authResponse: AuthResponse = {
        access_token,
        token_type: 'bearer',
        user: mapBackendUser(user) // Use type mapper
      }
      
      console.log('✅ [API] Registration successful for user:', user.email)
      return { data: authResponse }
      
    } catch (error: any) {
      console.error('❌ [API] Registration failed:', error.message)
      return { error: error.message || 'Registration failed' }
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      // Call backend logout endpoint if available
      await httpClient.post('/api/auth/jwt/logout')
    } catch (error) {
      console.log('ℹ️ [API] Backend logout failed (may not be implemented)')
    } finally {
      tokenManager.removeToken()
      console.log('👋 [API] User logged out')
    }
  }

  // ===================
  // USER MANAGEMENT METHODS
  // ===================

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<ApiResponse<User>> {
    try {
      const response = await httpClient.get('/api/users/me')
      return { data: response.data }
    } catch (error: any) {
      return { error: error.message || 'Failed to get user data' }
    }
  }

  /**
   * Get user profile by ID
   */
  async getUserProfile(id: string): Promise<User> {
    const response = await httpClient.get(`/api/users/${id}`)
    return mapBackendUser(response.data)
  }

  /**
   * Update user profile
   */
  async updateUserProfile(id: string, data: Partial<User>): Promise<User> {
    const response = await httpClient.put(`/api/users/${id}`, data)
    return mapBackendUser(response.data)
  }

  // ===================
  // GOALS MANAGEMENT
  // ===================

  /**
   * Get goals for a user
   */
  async getGoals(userId: string): Promise<Goal[]> {
    const response = await httpClient.get(`/api/users/${userId}/goals`)
    return mapBackendGoals(response.data)
  }

  /**
   * Create a new goal
   */
  async createGoal(userId: string, goalData: GoalCreateRequest): Promise<ApiResponse<Goal>> {
    console.log(goalData, userId)
    try {
      const response = await httpClient.post(`/api/users/${userId}/goals`, goalData)
      return { data: mapBackendGoal(response.data) }
    } catch (error: any) {
      return { error: error.message || 'Failed to create goal' }
    }
  }

  /**
   * Update a goal
   */
  async updateGoal(goalId: string, updates: Partial<Goal>): Promise<ApiResponse<Goal>> {
    try {
      const response = await httpClient.post(`/api/goals/${goalId}`, updates)
      return { data: mapBackendGoal(response.data) }
    } catch (error: any) {
      return { error: error.message || 'Failed to update goal' }
    }
  }

  async updateGoalAmount(goalId: string, amount: number): Promise<ApiResponse<Goal>> {
    try {
      const response = await httpClient.post(`/api/goals/${goalId}/amount`, { amount })
      return { data: mapBackendGoal(response.data) }
    } catch (error: any) {
      return { error: error.message || 'Failed to update goal amount' }
    }
  }

  /**
   * Delete a goal
   */
  async deleteGoal(goalId: string): Promise<ApiResponse<void>> {
    try {
      await httpClient.delete(`/api/goals/${goalId}`)
      return { data: undefined }
    } catch (error: any) {
      return { error: error.message || 'Failed to delete goal' }
    }
  }

  /**
   * Add progress to a goal
   */
  async addGoalProgress(goalId: string, amount: number): Promise<ApiResponse<Goal>> {
    try {
      const response = await httpClient.put(`/api/goals/${goalId}/progress`, { amount })
      return { data: response.data }
    } catch (error: any) {
      return { error: error.message || 'Failed to add goal progress' }
    }
  }

  /**
   * Contribute to a goal
   */
  async contributeToGoal(userId: string, goalId: string, amount: number): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.post(`/api/users/${userId}/goals/${goalId}/contribute`, { amount })
      return { data: response.data }
    } catch (error: any) {
      return { error: error.message || 'Failed to contribute to goal' }
    }
  }

  // ===================
  // TRANSACTIONS
  // ===================

  /**
   * Get user transactions
   */
  async getTransactions(userId: string): Promise<Transaction[]> {
    const response = await httpClient.get(`/api/users/${userId}/transactions`)
    return response.data
  }

  /**
   * Create a transaction
   */
  async createTransaction(userId: string, transactionData: Transaction): Promise<ApiResponse<Transaction>> {
    try {
      const response = await httpClient.post(`/api/users/${userId}/transactions`, transactionData)
      return { data: response.data }
    } catch (error: any) {
      return { error: error.message || 'Failed to create transaction' }
    }
  }

  // ===================
  // REDEMPTIONS
  // ===================

  /**
   * Get user conversion requests
   */
  async getUserConversionRequests(userId: string): Promise<RedemptionRequest[]> {
    const response = await httpClient.get(`/api/users/${userId}/conversion-requests`)
    return response.data
  }

  // ===================
  // TASKS MANAGEMENT
  // ===================

  /**
   * Get tasks for current user (works for all roles)
   */
  async getTasks(): Promise<Task[]> {
    const response = await httpClient.get('/api/tasks')
    return response.data
  }

  /**
   * Create a task
   */
  async createTask(taskData: TaskCreateRequest): Promise<Task> {
    const response = await httpClient.post('/api/tasks', taskData)
    return response.data
  }

  /**
   * Update task status
   */
  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task> {
    const response = await httpClient.put(`/api/tasks/${taskId}`, updates)
    return response.data
  }

  /**
   * Complete a task
   */
  async completeTask(taskId: string): Promise<Task> {
    const response = await httpClient.put(`/api/tasks/${taskId}`, { status: 'completed' })
    return response.data
  }

  /**
   * Delete a task
   */
  async deleteTask(taskId: string): Promise<void> {
    await httpClient.delete(`/api/tasks/${taskId}`)
  }

  // ===================
  // ROLE-SPECIFIC DASHBOARDS
  // ===================

  /**
   * Get Parent Dashboard
   */
  async getParentDashboard(): Promise<ApiResponse<DashboardData>> {
    try {
      const response = await httpClient.get('/api/parent/dashboard')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get parent dashboard:', error)
      return { error: error.response?.data?.detail || 'Failed to load parent dashboard' }
    }
  }

  /**
   * Get Teacher Dashboard
   */
  async getTeacherDashboard(): Promise<ApiResponse<DashboardData>> {
    try {
      const response = await httpClient.get('/api/teacher/dashboard')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get teacher dashboard:', error)
      return { error: error.response?.data?.detail || 'Failed to load teacher dashboard' }
    }
  }

  /**
   * Get Child Dashboard
   */
  async getChildDashboard(): Promise<DashboardData> {
    const response = await httpClient.get('/api/child/dashboard')
    return response.data
  }

  /**
   * Get Teen Dashboard
   */
  async getTeenDashboard(): Promise<DashboardData> {
    const response = await httpClient.get('/api/teen/dashboard')
    return response.data
  }

  /**
   * Get dashboard data based on user role
   */
  async getDashboardData(userRole: UserRole): Promise<DashboardData> {
    const roleMap = {
      'parent': '/api/parent/dashboard',
      'teacher': '/api/teacher/dashboard',
      'younger_child': '/api/child/dashboard',
      'older_child': '/api/teen/dashboard'
    }
    
    const endpoint = roleMap[userRole] || '/api/child/dashboard'
    const response = await httpClient.get(endpoint)
    return response.data
  }

  // ===================
  // SHOP SYSTEM
  // ===================

  /**
   * Get shop items
   */
  async getShopItems(): Promise<any[]> {
    const response = await httpClient.get('/api/shop/items')
    return response.data
  }

  async getOwnedItems(): Promise<any[]> {
    const response = await httpClient.get('/api/shop/owned_items')
    return response.data
  }
  /**
   * Purchase an item from shop
   */
  async purchaseItem(userId: string, item_id: string): Promise<any> {
    console.log("BIG CHECK", item_id)
    const response = await httpClient.post(`/api/shop/${userId}/purchase`, { item_id } )
    return response.data
  }

  // ===================
  // PARENT-SPECIFIC METHODS
  // ===================

  /**
   * Create a child account
   */
  async createChild(childData: {
    name: string
    email: string
    password: string
    age: number
    role: UserRole
  }): Promise<ApiResponse<User>> {
    try {
      const response = await httpClient.post('/api/parent/children', childData)
      // Backend now returns ChildCreateResponse: { success, message, child: UserRead }
      const childCreateResponse = response.data
      if (childCreateResponse.success && childCreateResponse.child) {
        const user = mapBackendUser(childCreateResponse.child)
        return { data: user }
      } else {
        return { error: childCreateResponse.message || 'Failed to create child account' }
      }
    } catch (error: any) {
      console.error('❌ [API] Failed to create child:', error)
      return { error: error.response?.data?.detail || 'Failed to create child account' }
    }
  }

  /**
   * Get child progress
   */
  async getChildProgress(childId: string): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.get(`/api/parent/children/${childId}/progress`)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get child progress:', error)
      return { error: error.response?.data?.detail || 'Failed to load child progress' }
    }
  }

  /**
   * Get parent tasks (created by parent)
   */
  async getParentTasks(): Promise<ApiResponse<Task[]>> {
    try {
      const response = await httpClient.get('/api/parent/tasks')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get parent tasks:', error)
      return { error: error.response?.data?.detail || 'Failed to load parent tasks' }
    }
  }

  /**
   * Create a task as parent
   */
  async createParentTask(taskData: {
    title: string
    description?: string
    coins_reward: number
    assigned_to: string
    due_date?: string
    requires_approval?: boolean
  }): Promise<ApiResponse<Task>> {
    try {
      const response = await httpClient.post('/api/parent/tasks', taskData)
      // Backend now returns TaskCreateResponse: { success, task: TaskRead, message }
      const taskCreateResponse = response.data
      if (taskCreateResponse.success && taskCreateResponse.task) {
        const task = mapBackendTask(taskCreateResponse.task)
        return { data: task }
      } else {
        return { error: taskCreateResponse.message || 'Failed to create task' }
      }
    } catch (error: any) {
      console.error('❌ [API] Failed to create parent task:', error)
      return { error: error.response?.data?.detail || 'Failed to create task' }
    }
  }

  /**
   * Approve a task
   */
  async approveTask(taskId: string): Promise<ApiResponse<Task>> {
    try {
      const response = await httpClient.put(`/api/parent/tasks/${taskId}/approve`)
      // Backend now returns TaskApprovalResponse: { success, task: TaskRead, coins_awarded, message }
      const taskApprovalResponse = response.data
      if (taskApprovalResponse.success && taskApprovalResponse.task) {
        const task = mapBackendTask(taskApprovalResponse.task)
        return { data: task }
      } else {
        return { error: taskApprovalResponse.message || 'Failed to approve task' }
      }
    } catch (error: any) {
      console.error('❌ [API] Failed to approve task:', error)
      return { error: error.response?.data?.detail || 'Failed to approve task' }
    }
  }

  /**
   * Get redemption requests for parent
   */
  async getRedemptionRequests(): Promise<ApiResponse<RedemptionRequest[]>> {
    try {
      const response = await httpClient.get('/api/parent/redemptions')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get redemption requests:', error)
      return { error: error.response?.data?.detail || 'Failed to load redemption requests' }
    }
  }

  /**
   * Approve a redemption request
   */
  async approveRedemption(requestId: string): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.put(`/api/redemption-requests/${requestId}/approve`)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to approve redemption:', error)
      return { error: error.response?.data?.detail || 'Failed to approve redemption' }
    }
  }

  /**
   * Reject a redemption request
   */
  async rejectRedemption(requestId: string): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.put(`/api/redemption-requests/${requestId}/reject`)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to reject redemption:', error)
      return { error: error.response?.data?.detail || 'Failed to reject redemption' }
    }
  }

  // ===================
  // TEACHER-SPECIFIC METHODS
  // ===================

  /**
   * Get teacher classes
   */
  async getTeacherClasses(): Promise<ApiResponse<any[]>> {
    try {
      const response = await httpClient.get('/api/teacher/classes')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get teacher classes:', error)
      return { error: error.response?.data?.detail || 'Failed to load teacher classes' }
    }
  }

  /**
   * Create a class
   */
  async createClass(classData: {
    name: string
    description?: string
  }): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.post('/api/teacher/classes', classData)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to create class:', error)
      return { error: error.response?.data?.detail || 'Failed to create class' }
    }
  }

  /**
   * Get class details
   */
  async getClassDetails(classId: string): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.get(`/api/teacher/classes/${classId}`)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get class details:', error)
      return { error: error.response?.data?.detail || 'Failed to load class details' }
    }
  }

  /**
   * Add student to class
   */
  async addStudentToClass(classId: string, studentData: { email: string }): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.post(`/api/teacher/classes/${classId}/students`, studentData)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to add student to class:', error)
      return { error: error.response?.data?.detail || 'Failed to add student to class' }
    }
  }

  /**
   * Remove student from class
   */
  async removeStudentFromClass(classId: string, studentId: string): Promise<ApiResponse<void>> {
    try {
      await httpClient.delete(`/api/classes/${classId}/students/${studentId}`)
      return { data: undefined }
    } catch (error: any) {
      console.error('❌ [API] Failed to remove student from class:', error)
      return { error: error.response?.data?.detail || 'Failed to remove student from class' }
    }
  }

  /**
   * Update class
   */
  async updateClass(classId: string, classData: { name?: string, description?: string }): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.put(`/api/classes/${classId}`, classData)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to update class:', error)
      return { error: error.response?.data?.detail || 'Failed to update class' }
    }
  }

  /**
   * Get teacher modules
   */
  async getTeacherModules(): Promise<ApiResponse<Module[]>> {
    try {
      const response = await httpClient.get('/api/teacher/modules')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get teacher modules:', error)
      return { error: error.response?.data?.detail || 'Failed to load teacher modules' }
    }
  }

  /**
   * Create a module
   */
  async createModule(moduleData: {
    title: string
    description: string
    category?: string
    difficulty?: 'easy' | 'medium' | 'hard'
    estimated_duration?: number
    points_reward?: number
  }): Promise<ApiResponse<Module>> {
    try {
      const response = await httpClient.post('/api/teacher/modules', moduleData)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to create module:', error)
      return { error: error.response?.data?.detail || 'Failed to create module' }
    }
  }

  /**
   * Get all modules (alias for getTeacherModules for compatibility)
   */
  async getModules(): Promise<Module[]> {
    const response = await this.getTeacherModules()
    if (response.error) {
      throw new Error(response.error)
    }
    return response.data || []
  }

  /**
   * Get performance analytics
   */
  async getPerformanceAnalytics(): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.get('/api/teacher/analytics/performance')
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get performance analytics:', error)
      return { error: error.response?.data?.detail || 'Failed to load performance analytics' }
    }
  }

  /**
   * Search for students by name
   */
  async searchStudents(query: string, age_group?: string): Promise<ApiResponse<any>> {
    try {
      let url = `/api/teacher/search-students?query=${encodeURIComponent(query)}`
      if (age_group) {
        url += `&age_group=${encodeURIComponent(age_group)}`
      }
      const response = await httpClient.get(url)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to search students:', error)
      return { error: error.response?.data?.detail || 'Failed to search students' }
    }
  }

  // ===================
  // TEEN-SPECIFIC METHODS
  // ===================

  /**
   * Get teen goals
   */
  async getTeenGoals(): Promise<Goal[]> {
    const response = await httpClient.get('/api/teen/goals')
    return response.data
  }

  /**
   * Create teen goal
   */
  async createTeenGoal(goalData: GoalCreateRequest): Promise<Goal> {
    const response = await httpClient.post('/api/teen/goals', goalData)
    return response.data
  }

  /**
   * Get teen budget
   */
  async getTeenBudget(): Promise<any> {
    const response = await httpClient.get('/api/teen/budget')
    return response.data
  }

  /**
   * Update teen budget
   */
  async updateTeenBudget(budgetData: any): Promise<any> {
    const response = await httpClient.put('/api/teen/budget', budgetData)
    return response.data
  }

  /**
   * Create conversion request (teen)
   */
  async createConversionRequest(requestData: any): Promise<any> {
    const response = await httpClient.post('/api/teen/conversion-requests', requestData)
    return response.data
  }

  /**
   * Get conversion requests (teen)
   */
  async getConversionRequests(): Promise<any[]> {
    const response = await httpClient.get('/api/teen/conversion-requests')
    return response.data
  }

  /**
   * Get teen analytics
   */
  async getTeenAnalytics(): Promise<any> {
    const response = await httpClient.get('/api/teen/analytics')
    return response.data
  }

  // ===================
  // ACTIVITIES & MODULES
  // ===================

  /**
   * Get learning modules
   */
  async getLearningModules(): Promise<Module[]> {
    const response = await httpClient.get('/api/learning-modules')
    return response.data
  }

  /**
   * Complete a learning module
   */
  async completeLearningModule(moduleId: string): Promise<any> {
    const response = await httpClient.post(`/api/learning-modules/${moduleId}/complete`)
    return response.data
  }

  /**
   * Get available activities
   */
  async getActivities(): Promise<Activity[]> {
    const response = await httpClient.get('/api/activities')
    return response.data
  }

  /**
   * Get activity details
   */
  async getActivityDetails(activityId: string): Promise<Activity> {
    const response = await httpClient.get(`/api/activities/${activityId}`)
    return response.data
  }

  async getCoins(userId: string): Promise<ApiResponse<number>> {
    try {
      const response = await httpClient.get(`/api/users/${userId}/coins`)
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to get coins:', error)
      return { error: error.response?.data?.detail || 'Failed to load coins' }
    }
  }

  async updateUserCoins(userId: string, coins: number): Promise<ApiResponse<any>> {
    try {
      const response = await httpClient.post(`/api/users/${userId}/coins`, { coins })
      console.log(response.data, "message was sent successfully")
      return { data: response.data }
    } catch (error: any) {
      console.error('❌ [API] Failed to update coins:', error)
      return { error: error.response?.data?.detail || 'Failed to update coins' }
    }
  }

  /**
   * Complete an activity
   */
  async completeActivity(activityId: string): Promise<any> {
    const response = await httpClient.post(`/api/activities/${activityId}/complete`)
    return response.data
  }

  // ===================
  // MISSING API METHODS
  // ===================

  /**
   * Generic request method (for backward compatibility)
   */
  async request(url: string, options: any = {}): Promise<any> {
    const method = options.method || 'GET'
    const config = {
      method: method.toLowerCase(),
      ...options
    }
    
    const response = await httpClient.request({
      url,
      ...config
    })
    
    return response.data
  }

  // ===================
  // UTILITY METHODS
  // ===================

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return tokenManager.hasToken()
  }

  /**
   * Get stored authentication token
   */
  getToken(): string | null {
    return tokenManager.getToken()
  }
}

// Export singleton instance
export const apiService = new ApiService()
export default apiService

// Re-export types from types file for convenience
export type { User, UserRole, Goal, Transaction, Task, Module, RedemptionRequest, DashboardData, Activity, AuthResponse } from '../types'
