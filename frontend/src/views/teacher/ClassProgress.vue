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
          <select
            v-model="selectedClassId"
            @change="loadClassData"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option 
              v-for="classItem in teacherStore.classes" 
              :key="classItem.id" 
              :value="classItem.id"
            >
              {{ classItem.name }}
            </option>
          </select>
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

    <!-- Class Progress Content -->
    <div v-else-if="selectedClass" class="space-y-6">
      <!-- Simple Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600 mb-1">Total Students</p>
              <p class="text-2xl font-bold text-gray-800">{{ selectedClass.student_count || 0 }}</p>
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

// Computed
const selectedClass = computed(() => {
  if (!selectedClassId.value) return null
  return teacherStore.classes.find(cls => cls.id === selectedClassId.value)
})

// Methods
const loadClassData = async () => {
  if (!selectedClassId.value) return
  
  try {
    isLoadingStudents.value = true
    
    console.log('🔍 [CLASS_PROGRESS] Loading data for class:', selectedClassId.value)
    
    // Force refresh classes first to get latest data
    await teacherStore.forceRefresh()
    
    // Get the updated class data
    const updatedClass = teacherStore.classes.find(c => c.id === selectedClassId.value)
    console.log('🔍 [CLASS_PROGRESS] Updated class data:', updatedClass)
    
    // Fetch students from API
    const students = await teacherStore.getClassStudents(selectedClassId.value)
    console.log('🔍 [CLASS_PROGRESS] Students from API:', students)
    
    classStudents.value = students
  } catch (error) {
    console.error('Failed to load class students:', error)
    classStudents.value = []
  } finally {
    isLoadingStudents.value = false
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

// Lifecycle hooks
onMounted(async () => {
  // Load classes first
  await teacherStore.loadClasses()
  
  // Auto-select first class if available
  if (teacherStore.classes.length > 0 && !selectedClassId.value) {
    selectedClassId.value = teacherStore.classes[0].id
  }
  
  // Check if route has a specific class ID
  const classId = route.params.id as string
  if (classId) {
    selectedClassId.value = classId
  }
})

// Watch for changes in classes
watch(() => teacherStore.classes, (newClasses) => {
  if (newClasses.length > 0 && !selectedClassId.value) {
    selectedClassId.value = newClasses[0].id
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