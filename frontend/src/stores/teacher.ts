import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '../services/api'
import type { User } from '../types'

// Teacher class interface aligned with backend ClassRead
export interface TeacherClass {
  id: string
  name: string
  description?: string
  teacher_id: string
  class_code: string
  is_active: boolean
  created_at: string
  students_count?: number
  average_performance?: number
  students?: User[]  // Populated when needed
  modules?: string[]  // Module IDs
}

// Teacher statistics interface
export interface TeacherStats {
  total_students: number
  total_classes: number
  average_performance: number
  total_modules: number
}

export const useTeacherStore = defineStore('teacher', () => {
  // State
  const classes = ref<TeacherClass[]>([])
  const stats = ref<TeacherStats>({
    total_students: 0,
    total_classes: 0,
    average_performance: 0,
    total_modules: 0
  })
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const totalStudents = computed(() => 
    classes.value.reduce((total, cls) => total + (cls.students_count || 0), 0)
  )
  const totalClasses = computed(() => classes.value.length)

  // Actions
  const loadDashboard = async (): Promise<void> => {
    console.log('📊 [TEACHER] Loading teacher dashboard...')
    
    isLoading.value = true
    error.value = null

    try {
      const dashboardData = await apiService.getTeacherDashboard()

      if (dashboardData.data) {
        // Update stats from dashboard data
        stats.value = {
          total_students: dashboardData.data.students_count || 0,
          total_classes: dashboardData.data.classes_count || 0,
          average_performance: dashboardData.data.average_performance || 0,
          total_modules: dashboardData.data.modules_count || 0
        }
      } else {
        error.value = dashboardData.error || 'Failed to fetch teacher dashboard'
      }

      console.log('✅ [TEACHER] Dashboard loaded successfully')

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load dashboard:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const createClass = async (classData: {
    name: string
    description?: string
  }): Promise<TeacherClass | null> => {
    console.log('🏫 [TEACHER] Creating new class...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.createClass(classData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        const newClass: TeacherClass = {
          id: response.data.id,
          name: response.data.name,
          description: response.data.description,
          teacher_id: response.data.teacher_id,
          class_code: response.data.class_code,
          is_active: response.data.is_active,
          created_at: response.data.created_at,
          students_count: 0,
          average_performance: 0
        }
        
        classes.value.push(newClass)
        
        console.log('✅ [TEACHER] Class created successfully:', newClass.name)
        return newClass
      }

      return null

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to create class:', err.message)
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  const getClassById = (classId: string): TeacherClass | undefined => {
    return classes.value.find(cls => cls.id === classId)
  }

  const loadClasses = async (): Promise<void> => {
    console.log('🏫 [TEACHER] Loading classes...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getTeacherClasses()
      
      if (response.data) {
        classes.value = response.data.map(cls => ({
          id: cls.id,
          name: cls.name,
          description: cls.description,
          teacher_id: cls.teacher_id,
          class_code: cls.class_code,
          is_active: cls.is_active,
          created_at: cls.created_at,
          students_count: cls.students_count || 0,
          average_performance: cls.average_performance || 0
        }))
        
        console.log(`✅ [TEACHER] Loaded ${classes.value.length} classes`)
      } else {
        error.value = response.error || 'Failed to load classes'
      }

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load classes:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const updateClass = async (classId: string, updates: Partial<TeacherClass>): Promise<boolean> => {
    console.log('🔄 [TEACHER] Updating class:', classId)
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.updateClass(classId, updates)
      
      if (response.data) {
        const classIndex = classes.value.findIndex(cls => cls.id === classId)
        if (classIndex !== -1) {
          classes.value[classIndex] = {
            ...classes.value[classIndex],
            ...response.data
          }
        }
        
        console.log('✅ [TEACHER] Class updated successfully')
        return true
      } else {
        error.value = response.error || 'Failed to update class'
        return false
      }

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to update class:', err.message)
      error.value = err.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  const deleteClass = async (classId: string): Promise<boolean> => {
    console.log('🗑️ [TEACHER] Deleting class:', classId)
    
    isLoading.value = true
    error.value = null

    try {
      // For now, we'll simulate deletion since the API method doesn't exist yet
      // TODO: Implement actual API call when backend endpoint is available
      classes.value = classes.value.filter(cls => cls.id !== classId)
      
      console.log('✅ [TEACHER] Class deleted successfully (simulated)')
      return true

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to delete class:', err.message)
      error.value = err.message
      return false
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    classes,
    stats,
    isLoading,
    error,
    
    // Computed
    totalStudents,
    totalClasses,
    
    // Actions
    loadDashboard,
    loadClasses,
    createClass,
    updateClass,
    deleteClass,
    getClassById,
    clearError
  }
})
