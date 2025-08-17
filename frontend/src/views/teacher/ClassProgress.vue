<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Class Progress</h1>
          <p class="text-gray-600">Monitor student performance and module completion</p>
        </div>
        
        <div class="w-full md:w-64">
          <label class="block text-sm font-medium text-gray-700 mb-2">Select Class</label>
          <select
            v-model="selectedClassId"
            @change="loadClassData"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            :disabled="teacherStore.isLoading || teacherStore.classes.length === 0"
          >
            <option value="" disabled>
              {{ teacherStore.isLoading ? 'Loading classes...' : 'Select a class' }}
            </option>
            <option 
              v-if="!teacherStore.isLoading && teacherStore.classes.length === 0" 
              value="" 
              disabled
            >
              No classes available
            </option>
            <option 
              v-for="classItem in teacherStore.classes" 
              :key="classItem.id" 
              :value="classItem.id"
            >
              {{ classItem.name }} - {{ classItem.students_count || 0 }} student{{ (classItem.students_count || 0) !== 1 ? 's' : '' }}
            </option>
          </select>
          <p v-if="teacherStore.isLoading" class="text-xs text-gray-500 mt-1">Loading classes...</p>
          <p v-else-if="teacherStore.classes.length > 0" class="text-xs text-gray-500 mt-1">
            {{ teacherStore.classes.length }} class{{ teacherStore.classes.length !== 1 ? 'es' : '' }} • 
            {{ teacherStore.classes.reduce((total, cls) => total + (cls.students_count || 0), 0) }} total students
          </p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="teacherStore.isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
      <p class="text-gray-600">Loading class data...</p>
    </div>

    <!-- No Classes State -->
    <div v-else-if="teacherStore.classes.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-book-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Classes Yet</h3>
      <p class="text-gray-600 mb-6">Create your first class to start monitoring student progress</p>
      <router-link 
        to="/teacher/dashboard"
        class="inline-block px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Go to Dashboard
      </router-link>
    </div>

    <!-- No Class Selected State -->
    <div v-else-if="!selectedClassId" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-group-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">Select a Class</h3>
      <p class="text-gray-600 mb-6">Choose a class from the dropdown above to view student progress</p>
    </div>

    <!-- Class Progress Content -->
    <div v-else-if="selectedClass" class="space-y-6">
      <!-- Loading State for Class Data -->
      <div v-if="isLoadingStudents || isLoadingModuleStatus" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
        <p class="text-gray-600">Loading class progress data...</p>
      </div>
      
      <!-- Class Content when loaded -->
      <div v-else class="space-y-6">
        <!-- Debug Info (remove in production) -->
        <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <h4 class="font-medium text-yellow-800 mb-2">Debug Info</h4>
          <div class="text-sm text-yellow-700 space-y-1">
            <p>Selected Class ID: {{ selectedClassId }}</p>
            <p>Class Data: {{ selectedClass ? 'Loaded' : 'Not loaded' }}</p>
            <p>Student Count from Class: {{ selectedClass?.students_count }}</p>
            <p>Actual Students Loaded: {{ classStudents.length }}</p>
            <p>Classes Available: {{ teacherStore.classes.length }}</p>
          </div>
        </div>
        
        <!-- Simple Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Total Students</p>
                <p class="text-2xl font-bold text-gray-800">{{ selectedClass.students_count || classStudents.length || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <i class="ri-group-line text-blue-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
              <p class="text-sm text-gray-600 mb-1">Class Created</p>
              <p class="text-2xl font-bold text-gray-800">{{ formatDate(selectedClass.created_at) }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <i class="ri-calendar-line text-green-600 text-xl"></i>
          </div>
          </div>
        </div>
      </div>

      <!-- Student List -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Students in {{ selectedClass.name }}</h3>
        
        <div v-if="isLoadingStudents" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
          <p class="text-gray-600">Loading students...</p>
        </div>
        
        <div v-else-if="classStudents && classStudents.length > 0" class="space-y-4">
          <div 
            v-for="student in classStudents" 
        :key="student.id"
            class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
          >
            <div class="flex items-center space-x-4">
              <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                <span class="text-gray-600 font-medium">{{ student.name.charAt(0) }}</span>
              </div>
              <div>
                <p class="font-medium text-gray-900">{{ student.name }}</p>
                <p class="text-sm text-gray-500">Student ID: {{ student.id }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-500">Enrolled</p>
              <p class="text-sm text-gray-600">{{ formatDate(selectedClass.created_at) }}</p>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <i class="ri-user-line text-gray-400 text-4xl mb-2"></i>
          <p class="text-gray-500">No students enrolled in this class yet</p>
        </div>
      </div>

      <!-- Module Completion Status Table -->
      <div class="bg-white rounded-xl shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Module Completion Status</h3>
        
        <div v-if="isLoadingModuleStatus" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
          <p class="text-gray-600">Loading module status...</p>
        </div>
        
        <div v-else-if="moduleCompletionStatus && moduleCompletionStatus.length > 0" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Module</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Completed Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="status in moduleCompletionStatus" :key="status.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center mr-3">
                      <span class="text-gray-600 text-sm font-medium">{{ status.student_name.charAt(0) }}</span>
        </div>
                    <div class="text-sm font-medium text-gray-900">{{ status.student_name }}</div>
      </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{{ status.module_title }}</div>
                  <div class="text-xs text-gray-500">{{ status.module_category }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                    :class="getStatusClass(status.status)"
                  >
                    {{ status.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ status.completed_at ? formatDate(status.completed_at) : 'Not completed' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ status.score ? `${status.score}%` : 'N/A' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-else class="text-center py-8">
          <i class="ri-book-open-line text-gray-400 text-4xl mb-2"></i>
          <p class="text-gray-500">No modules assigned to this class yet</p>
          <p class="text-sm text-gray-400 mt-1">Assign modules from the Modules tab to see completion status</p>
        </div>
      </div>
      </div> <!-- Close the class content div -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'

const route = useRoute()
const teacherStore = useTeacherStore()

// State
const selectedClassId = ref<string>('')
const classStudents = ref<any[]>([])
const isLoadingStudents = ref(false)
const isLoadingModuleStatus = ref(false) // New state for module status loading
const moduleCompletionStatus = ref<any[]>([]) // New state for module completion status

// Computed
const selectedClass = computed(() => {
  if (!selectedClassId.value) return null
  const cls = teacherStore.classes.find(cls => cls.id === selectedClassId.value)
  console.log('🔍 [CLASS_PROGRESS] Selected class data:', cls)
  console.log('🔍 [CLASS_PROGRESS] Student count from class:', cls?.students_count)
  console.log('🔍 [CLASS_PROGRESS] Actual students loaded:', classStudents.value.length)
  return cls
})

// Methods
const loadClassData = async () => {
  if (!selectedClassId.value) return
  
  try {
    isLoadingStudents.value = true
    isLoadingModuleStatus.value = true
    
    console.log('🔍 [CLASS_PROGRESS] Loading data for class:', selectedClassId.value)
    
    // Force refresh classes first to get latest data
    await teacherStore.forceRefresh()
    
    // Get the updated class data
    const updatedClass = teacherStore.classes.find(c => c.id === selectedClassId.value)
    console.log('🔍 [CLASS_PROGRESS] Updated class data:', updatedClass)
    
    // Fetch students from API
    const students = await teacherStore.getClassStudents(selectedClassId.value)
    console.log('🔍 [CLASS_PROGRESS] Students from API:', students)
    
    // The teacher store now returns the students array directly
    classStudents.value = students || []
    
    console.log('✅ [CLASS_PROGRESS] Processed students:', classStudents.value.length)
    
    // Load module completion status
    await loadModuleCompletionStatus()
  } catch (error) {
    console.error('Failed to load class data:', error)
    classStudents.value = []
    moduleCompletionStatus.value = []
  } finally {
    isLoadingStudents.value = false
    isLoadingModuleStatus.value = false
  }
}

const loadModuleCompletionStatus = async () => {
  if (!selectedClassId.value) return
  
  try {
    isLoadingModuleStatus.value = true
    console.log('🔍 [CLASS_PROGRESS] Loading module completion status for class:', selectedClassId.value)
    
    // Get modules assigned to this class
    const modules = await teacherStore.getModulesAssignedToClass(selectedClassId.value)
    
    if (modules && modules.length > 0) {
      // Get completion status for each module and student
      const statusData = []
      
      for (const module of modules) {
        // Get students for this class - the teacher store now returns the students array directly
        const students = await teacherStore.getClassStudents(selectedClassId.value)
        
        console.log(`🔍 [CLASS_PROGRESS] Processing ${students.length} students for module:`, module.title)
        
        for (const student of students) {
          const progress = await teacherStore.getStudentModuleProgress(student.id, module.id)
          
          statusData.push({
            id: `${student.id}-${module.id}`,
            student_name: student.name || student.full_name || 'Unknown Student',
            module_title: module.title,
            module_category: module.category || 'General',
            status: progress?.status || 'Not Started',
            completed_at: progress?.completed_at,
            score: progress?.score
          })
        }
      }
      
      moduleCompletionStatus.value = statusData
      console.log('✅ [CLASS_PROGRESS] Loaded module completion status:', statusData.length, 'entries')
    } else {
      moduleCompletionStatus.value = []
      console.log('ℹ️ [CLASS_PROGRESS] No modules assigned to this class')
    }
  } catch (error) {
    console.error('Failed to load module completion status:', error)
    moduleCompletionStatus.value = []
  } finally {
    isLoadingModuleStatus.value = false
  }
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return 'Invalid Date'
  }
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-green-100 text-green-800'
    case 'In Progress':
      return 'bg-yellow-100 text-yellow-800'
    case 'Not Started':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// Lifecycle hooks
onMounted(async () => {
  console.log('🚀 [CLASS_PROGRESS] Component mounted, loading classes...')
  
  // Load classes first
  await teacherStore.loadClasses()
  console.log('✅ [CLASS_PROGRESS] Classes loaded:', teacherStore.classes.length)
  
  // Auto-select first class if available
  if (teacherStore.classes.length > 0 && !selectedClassId.value) {
    selectedClassId.value = teacherStore.classes[0].id
    console.log('🎯 [CLASS_PROGRESS] Auto-selected first class:', teacherStore.classes[0].name)
  }
  
  // Check if route has a specific class ID
  const classId = route.params.id as string
  if (classId) {
    selectedClassId.value = classId
    console.log('🎯 [CLASS_PROGRESS] Route has class ID:', classId)
  }
})

// Watch for changes in classes
watch(() => teacherStore.classes, (newClasses) => {
  if (newClasses.length > 0 && !selectedClassId.value) {
    selectedClassId.value = newClasses[0].id
    console.log('🎯 [CLASS_PROGRESS] Auto-selected first class from watch:', newClasses[0].name)
  }
}, { immediate: true })

// Watch for changes in selectedClassId and auto-load data
watch(() => selectedClassId.value, async (newClassId) => {
  if (newClassId) {
    console.log('🔄 [CLASS_PROGRESS] Class selection changed to:', newClassId)
    // Auto-load class data when a class is selected
    await loadClassData()
  }
}, { immediate: true })
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>