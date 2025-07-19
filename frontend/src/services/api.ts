/**
 * API Service Layer for CoinCraft Frontend
 * Handles all HTTP requests to the FastAPI backend
 */

// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Types for API responses
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
  role: 'parent' | 'teacher' | 'younger_child' | 'older_child';
  avatar_url?: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
}

export interface Goal {
  id: string;
  user_id: string;
  title: string;
  description: string;
  target_amount: number;
  current_amount: number;
  icon: string;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface Transaction {
  id: string;
  user_id: string;
  type: 'earn' | 'spend' | 'save';
  amount: number;
  description: string;
  category?: string;
  source?: string;
  reference_id?: string;
  reference_type?: string;
  created_at: string;
}

export interface Task {
  id: string;
  user_id: string;
  assigned_by: string;
  title: string;
  description: string;
  coins_reward: number;
  due_date?: string;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
}

export interface Module {
  id: string;
  title: string;
  description: string;
  category: string;
  difficulty: 'easy' | 'medium' | 'hard';
  estimated_duration: number;
  points_reward: number;
  created_by: string;
  is_published: boolean;
  created_at: string;
}

export interface RedemptionRequest {
  id: string;
  user_id: string;
  item_name: string;
  coins_cost: number;
  status: 'pending' | 'approved' | 'rejected';
  approved_by?: string;
  created_at: string;
}

export interface DashboardData {
  user: User;
  stats: {
    total_coins: number;
    level: number;
    streak_days: number;
    goals_count: number;
    completed_tasks: number;
  };
  recent_transactions: Transaction[];
  active_goals: Goal[];
  pending_tasks: Task[];
  achievements: any[];
}

// API Service Class
class ApiService {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string) {
    console.log('🏗️ [API] Initializing API Service...');
    console.log('🏗️ [API] Base URL:', baseURL);
    console.log('🏗️ [API] Environment variables:', {
      VITE_API_URL: import.meta.env.VITE_API_URL,
      NODE_ENV: import.meta.env.NODE_ENV,
      DEV: import.meta.env.DEV
    });
    
    this.baseURL = baseURL;
    this.loadToken();
    
    console.log('🏗️ [API] Token loaded:', this.token ? 'Present' : 'None');
    console.log('🏗️ [API] API Service initialized successfully');
  }

  // Token management
  private loadToken(): void {
    this.token = localStorage.getItem('auth_token');
  }

  private saveToken(token: string): void {
    this.token = token;
    localStorage.setItem('auth_token', token);
  }

  private clearToken(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // HTTP request helper
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    console.log(`🌐 [API] Starting request to ${endpoint}`);
    console.log(`🔗 [API] Full URL: ${url}`);
    console.log(`📋 [API] Options:`, {
      method: options.method || 'GET',
      bodyType: options.body ? options.body.constructor.name : 'none',
      bodyContent: options.body instanceof FormData ? 'FormData (hidden)' : options.body
    });
    
    const headers: HeadersInit = {
      ...options.headers,
    };

    // Only add Content-Type for JSON requests (not for FormData)
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      console.log(`📝 [API] Added JSON Content-Type`);
    } else {
      console.log(`📝 [API] FormData detected, skipping Content-Type`);
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
      console.log(`🔑 [API] Added Authorization header with token`);
    } else {
      console.log(`🔑 [API] No token available`);
    }

    console.log(`📤 [API] Final headers:`, Object.keys(headers));

    try {
      console.log(`🚀 [API] Executing fetch...`);
      const response = await fetch(url, {
        ...options,
        headers,
        // Remove credentials since CORS doesn't allow it with allow_origins=["*"]
        // credentials: 'include',
      });

      console.log(`📬 [API] Response received:`, {
        status: response.status,
        statusText: response.statusText,
        ok: response.ok,
        type: response.type,
        url: response.url
      });

      if (!response.ok) {
        console.log(`❌ [API] Response not OK, status: ${response.status}`);
        
        if (response.status === 401) {
          console.log(`🔒 [API] 401 Unauthorized - clearing token`);
          this.clearToken();
          throw new Error('Authentication failed - please login again');
        }
        
        if (response.status === 404) {
          console.log(`🔍 [API] 404 Not Found`);
          throw new Error('Resource not found');
        }
        
        if (response.status >= 500) {
          console.log(`🔥 [API] Server error ${response.status}`);
          
          // For registration endpoint, provide more specific error
          if (url.includes('/register')) {
            console.log(`🔥 [API] Registration server error`);
            throw new Error('Registration failed - server error. Please try again with a different email or username.');
          }
          
          throw new Error('Server error - please try again later');
        }
        
        console.log(`📄 [API] Attempting to parse error response...`);
        const errorData = await response.json().catch((parseError) => {
          console.log(`💥 [API] Failed to parse error response:`, parseError);
          return {};
        });
        console.log(`📄 [API] Error data:`, errorData);
        
        // Enhanced error messages for registration
        if (url.includes('/register') && errorData.detail) {
          if (errorData.detail.includes('already exists')) {
            throw new Error('A user with this email already exists. Please try another email address.');
          }
        }
        
        throw new Error(errorData.detail || errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      console.log(`📄 [API] Attempting to parse success response...`);
      const data = await response.json();
      console.log(`✅ [API] Success response parsed:`, {
        dataType: typeof data,
        hasData: !!data,
        keys: data && typeof data === 'object' ? Object.keys(data) : 'N/A'
      });
      console.log(`📄 [API] Full response data:`, data);
      
      return { data };
    } catch (error) {
      console.error(`💥 [API] Request failed for ${endpoint}:`, error);
      
      // Handle network errors
      if (error instanceof TypeError) {
        console.error(`🌐 [API] Network/Type error details:`, {
          endpoint,
          url,
          error: error.message,
          stack: error.stack,
          name: error.name,
          cause: error.cause,
          options: {
            method: options.method,
            headers: Object.keys(headers),
            bodyType: options.body ? options.body.constructor.name : 'none'
          }
        });
        return { 
          error: `Network error on ${endpoint} - please check your connection` 
        };
      }
      
      console.error(`⚠️ [API] Non-network error:`, {
        errorType: error.constructor.name,
        message: error instanceof Error ? error.message : String(error),
        stack: error instanceof Error ? error.stack : 'N/A'
      });
      
      return { 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      };
    }
  }

  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<ApiResponse<{ access_token: string; user: User }>> {
    console.log('🔐 [LOGIN] Starting login API call...');
    console.log('🔐 [LOGIN] Credentials:', { email: credentials.email, password: '***' });
    console.log('🔐 [LOGIN] API Service base URL:', this.baseURL);
    console.log('🔐 [LOGIN] Current token:', this.token ? 'Present' : 'None');
    
    // FastAPI Users uses form data for login
    const formData = new FormData();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);

    console.log('📤 [LOGIN] FormData created with fields:', Array.from(formData.keys()));
    console.log('📤 [LOGIN] Sending login request to /api/auth/jwt/login');
    
    const response = await this.request<{ access_token: string; token_type: string }>('/api/auth/jwt/login', {
      method: 'POST',
      headers: {
        // Remove Content-Type to let browser set multipart/form-data
      },
      body: formData,
    });

    console.log('📥 [LOGIN] Login response received:', response);
    console.log('📥 [LOGIN] Response has error:', !!response.error);
    console.log('📥 [LOGIN] Response has data:', !!response.data);

    if (response.error) {
      console.error('❌ Login request failed:', response.error);
      return { error: response.error };
    }

    if (!response.data?.access_token) {
      console.error('❌ No access token in response:', response);
      return { error: 'No access token received' };
    }

    console.log('🔑 Access token received, saving...');
    this.saveToken(response.data.access_token);
    
    // Get user data after successful login
    console.log('👤 Fetching user data...');
    try {
      const userResponse = await this.getCurrentUser();
      console.log('👤 User data response:', userResponse);
      
      if (userResponse.data) {
        console.log('✅ Login successful with user data');
        return {
          data: {
            access_token: response.data.access_token,
            user: userResponse.data
          }
        };
      } else if (userResponse.error) {
        console.error('⚠️ Failed to get user data after login:', userResponse.error);
        // Return token with minimal user data if user fetch fails
        return {
          data: {
            access_token: response.data.access_token,
            user: {
              id: 'unknown',
              email: credentials.email,
              name: 'User',
              role: 'younger_child',
              avatar_url: '👤',
              is_active: true,
              created_at: new Date().toISOString()
            }
          }
        };
      }
    } catch (userError) {
      console.error('💥 Error fetching user data after login:', userError);
      // Return minimal user data if fetch fails
      return {
        data: {
          access_token: response.data.access_token,
          user: {
            id: 'unknown',
            email: credentials.email,
            name: 'User',
            role: 'younger_child',
            avatar_url: '👤',
            is_active: true,
            created_at: new Date().toISOString()
          }
        }
      };
    }

    console.error('❌ Unexpected login flow end');
    return { error: 'Unexpected login flow error' };
  }

  async register(userData: RegisterRequest): Promise<ApiResponse<{ access_token: string; user: User }>> {
    console.log('📝 [REGISTER] Starting registration API call...');
    console.log('📝 [REGISTER] User data:', { 
      email: userData.email, 
      name: userData.name, 
      role: userData.role,
      password: '***' 
    });

    try {
      const response = await this.request<{ access_token: string; token_type: string; user: User }>('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });

      console.log('📝 [REGISTER] Registration response received:', response);

      if (response.error) {
        console.error('❌ Registration failed:', response.error);
        
        // Enhance error message for common issues
        let errorMessage = response.error;
        if (errorMessage.includes('already exists')) {
          errorMessage = 'A user with this email already exists. Please try another email address.';
        } else if (errorMessage.includes('500')) {
          errorMessage = 'Server error. Please try again later or contact support.';
        }
        
        return { error: errorMessage };
      }

      if (!response.data?.access_token) {
        console.error('❌ No access token in registration response:', response);
        return { error: 'Registration failed - no access token received' };
      }

      console.log('🔑 Registration successful, saving token...');
      this.saveToken(response.data.access_token);

      return {
        data: {
          access_token: response.data.access_token,
          user: response.data.user
        }
      };
    } catch (error) {
      console.error('💥 [REGISTER] Unexpected error during registration:', error);
      
      // Provide more helpful error messages
      let errorMessage = 'Registration failed. Please try again.';
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
          errorMessage = 'Network error. Please check your internet connection and try again.';
        } else if (error.message.includes('500')) {
          errorMessage = 'Server error. Please try again later or contact support.';
        }
      }
      
      return { error: errorMessage };
    }
  }

  async logout(): Promise<ApiResponse<void>> {
    const response = await this.request<void>('/api/auth/jwt/logout', {
      method: 'POST',
    });
    
    this.clearToken();
    return response;
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    console.log('👤 [USER] Getting current user...');
    console.log('👤 [USER] Current token available:', !!this.token);
    console.log('👤 [USER] Token preview:', this.token ? this.token.substring(0, 20) + '...' : 'None');
    
    const response = await this.request<User>('/api/users/me');
    
    console.log('👤 [USER] getCurrentUser response received');
    console.log('👤 [USER] Response has error:', !!response.error);
    console.log('👤 [USER] Response has data:', !!response.data);
    console.log('👤 [USER] Full response:', response);
    
    return response;
  }

  // User management
  async getUserProfile(userId: string): Promise<ApiResponse<User>> {
    return this.request<User>(`/api/users/${userId}`);
  }

  async updateUserProfile(userId: string, updates: Partial<User>): Promise<ApiResponse<User>> {
    return this.request<User>(`/api/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  // Goals
  async getGoals(): Promise<ApiResponse<Goal[]>> {
    return this.request<Goal[]>('/api/goals/');
  }

  async createGoal(goalData: Omit<Goal, 'id' | 'created_at' | 'updated_at'>): Promise<ApiResponse<Goal>> {
    return this.request<Goal>('/api/goals/', {
      method: 'POST',
      body: JSON.stringify(goalData),
    });
  }

  async updateGoal(goalId: string, updates: Partial<Goal>): Promise<ApiResponse<Goal>> {
    return this.request<Goal>(`/api/goals/${goalId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async deleteGoal(goalId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/goals/${goalId}`, {
      method: 'DELETE',
    });
  }

  async updateGoalProgress(goalId: string, amount: number): Promise<ApiResponse<Goal>> {
    return this.request<Goal>(`/api/goals/${goalId}/progress`, {
      method: 'POST',
      body: JSON.stringify({ amount }),
    });
  }

  // Transactions
  async getTransactions(
    type?: 'earn' | 'spend' | 'save',
    limit?: number
  ): Promise<ApiResponse<Transaction[]>> {
    const params = new URLSearchParams();
    if (type) params.append('type', type);
    if (limit) params.append('limit', limit.toString());
    
    return this.request<Transaction[]>(`/api/transactions/?${params.toString()}`);
  }

  async createTransaction(transactionData: Omit<Transaction, 'id' | 'created_at'>): Promise<ApiResponse<Transaction>> {
    return this.request<Transaction>('/api/transactions/', {
      method: 'POST',
      body: JSON.stringify(transactionData),
    });
  }

  // Tasks
  async getTasks(): Promise<ApiResponse<Task[]>> {
    return this.request<Task[]>('/api/tasks/');
  }

  async createTask(taskData: Omit<Task, 'id' | 'created_at'>): Promise<ApiResponse<Task>> {
    return this.request<Task>('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async completeTask(taskId: string): Promise<ApiResponse<Task>> {
    return this.request<Task>(`/api/tasks/${taskId}/complete`, {
      method: 'POST',
    });
  }

  async deleteTask(taskId: string): Promise<ApiResponse<void>> {
    return this.request<void>(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  // Learning Modules
  async getModules(
    difficulty?: 'easy' | 'medium' | 'hard',
    category?: string
  ): Promise<ApiResponse<Module[]>> {
    const params = new URLSearchParams();
    if (difficulty) params.append('difficulty', difficulty);
    if (category) params.append('category', category);
    
    return this.request<Module[]>(`/api/modules/?${params.toString()}`);
  }

  async getModule(moduleId: string): Promise<ApiResponse<Module>> {
    return this.request<Module>(`/api/modules/${moduleId}`);
  }

  async updateModuleProgress(moduleId: string, progress: number): Promise<ApiResponse<any>> {
    return this.request<any>(`/api/modules/${moduleId}/progress`, {
      method: 'POST',
      body: JSON.stringify({ progress }),
    });
  }

  // Redemption Requests
  async getRedemptionRequests(): Promise<ApiResponse<RedemptionRequest[]>> {
    return this.request<RedemptionRequest[]>('/api/redemptions/');
  }

  async createRedemptionRequest(requestData: Omit<RedemptionRequest, 'id' | 'created_at'>): Promise<ApiResponse<RedemptionRequest>> {
    return this.request<RedemptionRequest>('/api/redemptions/', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  }

  async approveRedemptionRequest(requestId: string): Promise<ApiResponse<RedemptionRequest>> {
    return this.request<RedemptionRequest>(`/api/redemptions/${requestId}/approve`, {
      method: 'POST',
    });
  }

  async rejectRedemptionRequest(requestId: string): Promise<ApiResponse<RedemptionRequest>> {
    return this.request<RedemptionRequest>(`/api/redemptions/${requestId}/reject`, {
      method: 'POST',
    });
  }

  // Dashboard
  async getDashboardData(role: string): Promise<ApiResponse<DashboardData>> {
    return this.request<DashboardData>(`/api/dashboard/${role}`);
  }

  // Classes (for teachers)
  async getClasses(): Promise<ApiResponse<any[]>> {
    return this.request<any[]>('/api/classes/');
  }

  async createClass(classData: any): Promise<ApiResponse<any>> {
    return this.request<any>('/api/classes/', {
      method: 'POST',
      body: JSON.stringify(classData),
    });
  }

  async getClassStudents(classId: string): Promise<ApiResponse<any[]>> {
    return this.request<any[]>(`/api/classes/${classId}/students`);
  }

  // Utility methods
  isAuthenticated(): boolean {
    return !!this.token;
  }

  getToken(): string | null {
    return this.token;
  }

  // Test method for debugging
  async testConnection(): Promise<ApiResponse<any>> {
    return this.request<any>('/api/test');
  }
}

// Export singleton instance
export const apiService = new ApiService(API_BASE_URL);

// Export types for use in components
export type {
  LoginRequest,
  RegisterRequest,
  User,
  Goal,
  Transaction,
  Task,
  Module,
  RedemptionRequest,
  DashboardData,
}; 