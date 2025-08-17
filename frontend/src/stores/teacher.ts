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
  const modules = ref<any[]>([])
  const profile = ref<any>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const availableStudents = ref<User[]>([])
  
  // Cache management
  const lastFetched = ref<{
    classes: number | null
    dashboard: number | null
    students: Record<string, { data: any[], timestamp: number }>
  }>({
    classes: null,
    dashboard: null,
    students: {}
  })
  
  const CACHE_DURATION = 5 * 60 * 1000 // 5 minutes
  
  // Cache validation methods
  const isCacheValid = (type: 'classes' | 'dashboard' | 'students', classId?: string): boolean => {
    const now = Date.now()
    
    if (type === 'students' && classId) {
      const studentCache = lastFetched.value.students[classId]
      return studentCache ? (now - studentCache.timestamp) < CACHE_DURATION : false
    }
    
    if (type === 'classes' || type === 'dashboard') {
      const timestamp = lastFetched.value[type]
      return timestamp !== null ? (now - timestamp) < CACHE_DURATION : false
    }
    
    return false
  }
  
  const updateCacheTimestamp = (type: 'classes' | 'dashboard' | 'students', classId?: string) => {
    const now = Date.now()
    
    if (type === 'students' && classId) {
      if (!lastFetched.value.students[classId]) {
        lastFetched.value.students[classId] = { data: [], timestamp: now }
      } else {
        lastFetched.value.students[classId].timestamp = now
      }
    } else if (type === 'classes') {
      lastFetched.value.classes = now
    } else if (type === 'dashboard') {
      lastFetched.value.dashboard = now
    }
  }

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
    student_ids?: string[]
  }): Promise<TeacherClass | null> => {
    console.log('🏫 [TEACHER] Creating new class...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.createClass(classData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data && response.data.class) {
        console.log('✅ [TEACHER] Class created successfully:', response.data.class.name)
        
        // Don't add to local state - let the component refresh from API
        // This ensures we always have the latest data from database
        
        return {
          id: response.data.class.id,
          name: response.data.class.name,
          description: response.data.class.description,
          teacher_id: '', // Will be set by backend
          is_active: true,
          created_at: response.data.class.created_at,
          students_count: response.data.class.student_count || 0,
          average_performance: 0
        }
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

  const loadClasses = async (forceRefresh: boolean = false): Promise<void> => {
    console.log('🏫 [TEACHER] Loading classes...')
    
    // Check cache first (unless force refresh is requested)
    if (!forceRefresh && isCacheValid('classes') && classes.value.length > 0) {
      console.log('✅ [TEACHER] Using cached classes data')
      return
    }
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getTeacherClasses()
      
      if (response.data) {
        console.log('🔍 [TEACHER] Raw API response:', response.data)
        
        classes.value = response.data.map(cls => {
          const mappedClass = {
            id: cls.id,
            name: cls.name,
            description: cls.description,
            teacher_id: cls.teacher_id || '',
            is_active: cls.is_active,
            created_at: cls.created_at,
            students_count: cls.student_count || 0,  // Fixed: use student_count from API
            average_performance: cls.avg_performance || 0
          }
          console.log(`🔍 [TEACHER] Mapped class "${cls.name}":`, mappedClass)
          return mappedClass
        })
        
        // Update cache timestamp
        updateCacheTimestamp('classes')
        
        console.log(`✅ [TEACHER] Loaded ${classes.value.length} classes with student counts:`, 
          classes.value.map(c => `${c.name}: ${c.students_count} students`))
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

  const addModule = async (moduleData: any): Promise<any> => {
    console.log('📚 [TEACHER] Adding new module...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.createModule(moduleData)
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        console.log('✅ [TEACHER] Module added successfully:', response.data.title)
        return response.data
      }

      return null

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to add module:', err.message)
      error.value = err.message
      return null
    } finally {
      isLoading.value = false
    }
  }

  const loadModules = async (): Promise<void> => {
    console.log('📚 [TEACHER] Loading modules...')
    
    isLoading.value = true
    error.value = null

    try {
      const response = await apiService.getTeacherModules()
      
      if (response.data) {
        modules.value = response.data
        console.log(`✅ [TEACHER] Loaded ${modules.value.length} modules`)
      } else {
        error.value = response.error || 'Failed to load modules'
      }

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load modules:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const getModuleById = (moduleId: string): any | undefined => {
    return modules.value.find(module => module.id === moduleId)
  }

  const assignModuleToClass = async (moduleId: string, classId: string, dueDate?: string): Promise<boolean> => {
    console.log(`📚 [TEACHER] Assigning module ${moduleId} to class ${classId}...`)
    
    try {
      const response = await apiService.assignModuleToClass(moduleId, {
        class_id: classId,
        due_date: dueDate
      })
      
      if (response.error) {
        throw new Error(response.error)
      }

      if (response.data) {
        console.log(`✅ [TEACHER] Module assigned successfully: ${response.data.message}`)
        return true
      }

      return false

    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to assign module to class:', err.message)
      error.value = err.message
      return false
    }
  }

  const loadTeacherProfile = async (): Promise<void> => {
    console.log('👤 [TEACHER] Loading teacher profile...')
    
    isLoading.value = true
    error.value = null

    try {
      // For now, create a default profile since the endpoint doesn't exist
      // In a real implementation, this would come from an API endpoint
      profile.value = {
        id: 'default-teacher-profile',
        school_name: 'Financial Literacy Academy',
        grade_level: 'K-12',
        subject: 'Financial Education',
        avatar: null
      }
      console.log('✅ [TEACHER] Default profile created')
    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load profile:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const loadAvailableStudents = async (): Promise<void> => {
    console.log('👥 [TEACHER] Loading available students...')
    isLoading.value = true
    error.value = null
    try {
      const response = await apiService.getAvailableStudents()
      if (response.data) {
        availableStudents.value = response.data
        console.log(`✅ [TEACHER] Loaded ${availableStudents.value.length} available students`)
      } else {
        error.value = response.error || 'Failed to load available students'
        console.error('❌ [TEACHER] Failed to load students:', response.error)
      }
    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to load students:', err.message)
      error.value = err.message
    } finally {
      isLoading.value = false
    }
  }

  const getClassStudents = async (classId: string): Promise<any[]> => {
    console.log(`🔍 [TEACHER] Getting students for class: ${classId}`)
    
    // Check cache first
    if (isCacheValid('students', classId)) {
      console.log(`✅ [TEACHER] Using cached students for class: ${classId}`)
      return lastFetched.value.students[classId]?.data || []
    }
    
    try {
      const response = await apiService.getClassStudents(classId)
      if (response.error) {
        throw new Error(response.error)
      }
      
      // The backend returns { class_id, class_name, total_students, students: [...] }
      // We need to extract the students array
      const responseData = response.data || {}
      const students = responseData.students || []
      
      console.log(`✅ [TEACHER] Loaded ${students.length} students for class: ${classId}`)
      console.log(`🔍 [TEACHER] Response structure:`, responseData)
      
      // Update cache with the students array
      lastFetched.value.students[classId] = {
        data: students,
        timestamp: Date.now()
      }
      
      return students
    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to get class students:', err.message)
      error.value = err.message
      return []
    }
  }

  const getModulesAssignedToClass = async (classId: string): Promise<any[]> => {
    console.log(`🔍 [TEACHER] Getting modules assigned to class: ${classId}`)
    
    try {
      // Get modules assigned to this specific class
      const response = await apiService.getModulesAssignedToClass(classId)
      if (response.error) {
        throw new Error(response.error)
      }
      
      const assignedModules = response.data || []
      console.log(`✅ [TEACHER] Found ${assignedModules.length} modules assigned to class: ${classId}`)
      return assignedModules
    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to get modules assigned to class:', err.message)
      error.value = err.message
      return []
    }
  }

  const getStudentModuleProgress = async (studentId: string, moduleId: string): Promise<any> => {
    console.log(`🔍 [TEACHER] Getting progress for student ${studentId} in module ${moduleId}`)
    
    try {
      const response = await apiService.getStudentModuleProgress(studentId, moduleId)
      if (response.error) {
        throw new Error(response.error)
      }
      
      console.log(`✅ [TEACHER] Loaded progress for student ${studentId} in module ${moduleId}`)
      return response.data
    } catch (err: any) {
      console.error('❌ [TEACHER] Failed to get student module progress:', err.message)
      error.value = err.message
      return null
    }
  }

  const forceRefresh = async (): Promise<void> => {
    console.log('🔄 [TEACHER] Force refreshing all data from API...')
    
    // Clear cache to force fresh data
    lastFetched.value = {
      classes: null,
      dashboard: null,
      students: {}
    }
    
    // Clear local state to force fresh data
    classes.value = []
    stats.value = {
      total_students: 0,
      total_classes: 0,
      average_performance: 0,
      total_modules: 0
    }
    
    // Reload everything from API
    await Promise.all([
      loadDashboard(),
      loadClasses(true) // Force refresh
    ])
    
    console.log('✅ [TEACHER] Force refresh completed')
  }

  const forceRefreshClass = async (classId: string): Promise<void> => {
    console.log(`🔄 [TEACHER] Force refreshing class ${classId}...`)
    
    // Clear cache for this specific class
    if (lastFetched.value.students[classId]) {
      delete lastFetched.value.students[classId]
    }
    
    // Force refresh classes list
    await loadClasses(true)
    
    // Force refresh students for this class
    await getClassStudents(classId)
    
    console.log(`✅ [TEACHER] Class ${classId} force refresh completed`)
  }

  return {
    // State
    classes,
    stats,
    modules,
    profile,
    isLoading,
    error,
    availableStudents,
    
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
    clearError,
    addModule,
    loadModules,
    getModuleById,
    assignModuleToClass,
    loadTeacherProfile,
    loadAvailableStudents,
    getClassStudents,
    getModulesAssignedToClass,
    getStudentModuleProgress,
    forceRefresh,
    forceRefreshClass
  }
})
