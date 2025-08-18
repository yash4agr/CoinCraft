/**
 * HTTP Client Configuration using Axios
 * Centralized HTTP client with interceptors for authentication and error handling
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://api.iitmquizzes.tech'

// Create axios instance with default configuration
export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for authentication
httpClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
httpClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      // Redirect to login (can be handled by the component)
      window.location.href = '/login'
    }
    
    // Transform error for consistent handling
    const errorData = error.response?.data as any
    const apiError = {
      message: errorData?.detail || error.message || 'An error occurred',
      status: error.response?.status || 0,
      code: error.code || 'UNKNOWN_ERROR'
    }
    
    return Promise.reject(apiError)
  }
)

// Token management utilities
export const tokenManager = {
  getToken(): string | null {
    return localStorage.getItem('auth_token')
  },
  
  setToken(token: string): void {
    localStorage.setItem('auth_token', token)
  },
  
  removeToken(): void {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  },
  
  hasToken(): boolean {
    return !!this.getToken()
  }
}

export default httpClient
