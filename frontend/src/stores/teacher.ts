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
  age_group: string  // Add age_group field
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
  const currentClass = ref<TeacherClass | null>(null)
  const modules = ref<any[]>([])
  const students = ref<User[]>([])
  const stats = ref<TeacherStats>({
    total_students: 0,
    total_classes: 0,
    average_performance: 0,
    total_modules: 0
  })
  const profile = ref<any>(null) // Teacher profile data
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
        const { user, stats: dashboardStats, classes: dashboardClasses } = dashboardData.data
        
        // Update profile information
        if (user) {
          profile.value = {
            avatar: user.avatar_url,
            school: (dashboardStats as any)?.school || '',
            subject: (dashboardStats as any)?.subject || ''
          }
        }
        
        // Update stats from dashboard data
        if (dashboardStats) {
          stats.value = {
            total_students: (dashboardStats as any).total_students || 0,
            total_classes: (dashboardStats as any).total_classes || 0,
            average_performance: (dashboardStats as any).avg_performance || 0,
            total_modules: (dashboardStats as any).total_modules || 0
          }
        }
        
        // Update classes if available
        if (dashboardClasses) {
          classes.value = dashboardClasses.map((cls: any) => ({
            id: cls.id,
            name: cls.name,
            description: cls.description || '',
            teacher_id: cls.teacher_id || user?.id || '',
            age_group: cls.age_group || '',  // Add age_group field
            class_code: cls.class_code || '',
            is_active: cls.is_active !== false,
            created_at: cls.created_at || new Date().toISOString(),
            students_count: cls.student_count || 0,
            average_performance: cls.avg_performance || 0,
            grade: cls.grade || ''
          }))
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
    age_group: string  // Add age_group parameter
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
          age_group: response.data.age_group,  // Add age_group field
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
          age_group: cls.age_group,  // Add age_group field
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

  const addStudentToClass = async (classId: string, studentData: { email: string }) => {
    console.log('👥 [TEACHER] Adding student to class...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.addStudentToClass(classId, studentData)
      
      if (response.error) {
        return { error: response.error }
      }

      // Update the class student count locally
      const classIndex = classes.value.findIndex(cls => cls.id === classId)
      if (classIndex !== -1) {
        const existingClass = classes.value[classIndex]
        if (existingClass) {
          existingClass.students_count = (existingClass.students_count || 0) + 1
        }
      }

      console.log('✅ [TEACHER] Student added successfully')
      return { success: true, data: response.data }

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to add student:', err.message)
      return { error: err.message }
    } finally {
      isLoading.value = false
    }
  }

  const loadClassDetails = async (classId: string) => {
    console.log('📋 [TEACHER] Loading class details...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getClassDetails(classId)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        // Store the current class details
        currentClass.value = response.data as TeacherClass
        
        // Update students if included in response
        if (response.data.students) {
          students.value = response.data.students
        }
        
        // Update the class in our local store with full details including students
        const classIndex = classes.value.findIndex(cls => cls.id === classId)
        if (classIndex !== -1) {
          const existingClass = classes.value[classIndex]
          if (existingClass) {
            classes.value[classIndex] = {
              ...existingClass,
              students: response.data.students || existingClass.students,
              students_count: response.data.students?.length || existingClass.students_count || 0,
              average_performance: response.data.avg_performance || existingClass.average_performance || 0
            }
          }
        }

        console.log('✅ [TEACHER] Class details loaded successfully')
        return response.data
      }

      return null

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load class details:', err.message)
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  const loadTeacherProfile = async () => {
    // For now, just set a basic profile since we don't have a separate profile endpoint
    console.log('📋 [TEACHER] Loading teacher profile...')
    profile.value = {
      avatar: null,
      school: 'Default School',
      subject: 'Financial Literacy'
    }
    return Promise.resolve()
  }

  const loadModules = async () => {
    console.log('📚 [TEACHER] Loading teacher modules...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getTeacherModules()
      
      if (response.error) {
        throw new Error(response.error)
      }

      // For now, we'll just log success since modules aren't fully implemented
      console.log('✅ [TEACHER] Modules loaded successfully')
      return response.data || []

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load modules:', err.message)
      error.value = err.message
      return []
    } finally {
      isLoading.value = false
    }
  }

  // Search for students by name
  const searchStudents = async (query: string): Promise<any[]> => {
    console.log('🔍 [TEACHER] Searching for students:', query)
    
    try {
      const response = await apiService.searchStudents(query)
      
      if (response.data && response.data.students) {
        return response.data.students
      } else {
        console.error('Invalid response format for student search:', response)
        return []
      }
    } catch (error) {
      console.error('Error searching students:', error)
      throw error
    }
  }

  return {
    // State
    classes,
    currentClass,
    modules,
    students,
    profile,
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
    addStudentToClass,
    loadClassDetails,
    loadTeacherProfile,
    loadModules,
    clearError,
    searchStudents
  }
})
