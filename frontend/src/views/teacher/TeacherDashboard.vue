<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Teacher Dashboard</h1>
          <p class="text-gray-600">Manage your classes, modules, and student progress</p>
        </div>
        <div class="flex gap-3">
          <!-- Refresh Button -->
          <button 
            @click="refreshDashboard"
            :disabled="teacherStore.isLoading"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors disabled:opacity-50"
          >
            <i class="ri-refresh-line mr-2"></i>
            {{ teacherStore.isLoading ? 'Refreshing...' : 'Refresh' }}
          </button>
          
          <!-- Add New Class Button -->
          <button 
            @click="openCreateClassModal"
            class="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            <i class="ri-add-line mr-2"></i>
            Add New Class
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Stats Section -->
    <div class="mb-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold text-gray-800">Total Classes</h3>
            <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
              <i class="ri-group-line text-blue-600"></i>
            </div>
          </div>
          <div class="text-3xl font-bold text-blue-600">{{ teacherStore.classes.length }}</div>
          <p class="text-sm text-gray-500 mt-1">Active classes</p>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold text-gray-800">Total Students</h3>
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
              <i class="ri-user-line text-green-600"></i>
            </div>
          </div>
          <div class="text-3xl font-bold text-green-600">{{ totalStudents }}</div>
          <p class="text-sm text-gray-500 mt-1">Enrolled students</p>
        </div>
      </div>
    </div>

    <!-- Classes Section -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Your Classes</h2>
        <div class="flex gap-3">
          <button 
            @click="showAIAssist = true"
            class="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-robot-line"></i>
            <span>AI Assist</span>
          </button>
          <button 
            @click="openCreateClassModal"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-add-line"></i>
            <span>Add New Class</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="teacherStore.isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
        <p class="text-gray-600">Loading your classes...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="teacherStore.error" class="bg-red-50 border border-red-200 rounded-xl p-6 text-center">
        <i class="ri-error-warning-line text-red-500 text-4xl mb-4"></i>
        <p class="text-red-600 mb-2">{{ teacherStore.error }}</p>
        <button 
          @click="() => {}"
          class="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors mt-2"
        >
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="teacherStore.classes.length === 0" class="bg-white rounded-xl p-12 text-center">
        <i class="ri-book-line text-blue-500 text-5xl mb-4"></i>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">No Classes Yet</h3>
        <p class="text-gray-600 mb-6">Get started by creating your first class</p>
        <button 
          @click="openCreateClassModal"
          class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
        >
          Create Your First Class
        </button>
      </div>

      <!-- Classes Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="classItem in teacherStore.classes" 
          :key="classItem.id"
          class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
        >
          <!-- Class Header -->
          <div class="p-6 border-b border-gray-100">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-lg font-semibold text-gray-800">{{ classItem.name }}</h3>
              <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                {{ classItem.students_count || 0 }} students
              </span>
            </div>
            <p v-if="classItem.description" class="text-sm text-gray-600 mb-4">
              {{ classItem.description }}
            </p>
            <div class="flex items-center justify-between text-sm text-gray-500">
              <span>Created {{ formatDate(classItem.created_at) }}</span>
              </div>
            </div>

          <!-- Class Actions -->
          <div class="p-4 bg-gray-50">
            <div class="flex gap-2">
              <button 
                @click="navigateToClassProgress(classItem.id)"
                class="flex-1 py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
              >
                <i class="ri-chart-line mr-1"></i> Progress
              </button>
              <button 
                @click="navigateToClassManagement(classItem.id)"
                class="flex-1 py-2 px-3 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-colors text-sm"
              >
                <i class="ri-settings-line mr-1"></i> Manage
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Recent Activity</h2>
      <div class="bg-white rounded-xl shadow-sm overflow-hidden">
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
              <i class="ri-check-line text-green-600"></i>
            </div>
            <div>
              <h4 class="font-semibold text-gray-800">Module Completed</h4>
              <p class="text-sm text-gray-600">
                <span class="font-medium">Olivia Davis</span> completed 
                <span class="font-medium">Introduction to Money</span> with a score of 95%
              </p>
            </div>
            <div class="ml-auto text-sm text-gray-500">2 hours ago</div>
          </div>
        </div>

        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-full bg-yellow-100 flex items-center justify-center">
              <i class="ri-alert-line text-yellow-600"></i>
            </div>
            <div>
              <h4 class="font-semibold text-gray-800">Low Performance Alert</h4>
              <p class="text-sm text-gray-600">
                <span class="font-medium">Liam Smith</span> is struggling with 
                <span class="font-medium">Saving Basics</span>
              </p>
            </div>
            <div class="ml-auto text-sm text-gray-500">1 day ago</div>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
              <i class="ri-add-line text-blue-600"></i>
            </div>
            <div>
              <h4 class="font-semibold text-gray-800">New Module Assigned</h4>
              <p class="text-sm text-gray-600">
                You assigned <span class="font-medium">Needs vs Wants</span> to 
                <span class="font-medium">Financial Literacy 101</span>
              </p>
            </div>
            <div class="ml-auto text-sm text-gray-500">3 days ago</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Class Modal -->
    <div v-if="showCreateClassModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Create New Class</h3>
          <button 
            @click="showCreateClassModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Class Creation Form -->
        <form @submit.prevent="createNewClass" class="space-y-6">
          <!-- Class Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Class Name</label>
            <input 
              v-model="newClassData.name"
              type="text"
              required
              placeholder="e.g., Financial Literacy 101"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <!-- Class Description -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description (Optional)</label>
            <textarea 
              v-model="newClassData.description"
              rows="3"
              placeholder="Brief description of the class..."
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>

          <!-- Student Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Select Students *
            </label>
            <div class="max-h-60 overflow-y-auto border border-gray-300 rounded-lg p-3">
              <div v-if="teacherStore.isLoading" class="text-center py-4">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                <p class="text-gray-500 mt-2">Loading students...</p>
              </div>
              <div v-else-if="teacherStore.availableStudents.length === 0" class="text-center py-4">
                <p class="text-gray-500">No students available</p>
              </div>
              <div v-else class="space-y-2">
                <div
                  v-for="student in teacherStore.availableStudents"
                  :key="student.id"
                  class="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer"
                  :class="{ 'bg-indigo-50 border border-indigo-200': selectedStudentIds.includes(student.id) }"
                  @click="toggleStudentSelection(student.id)"
                >
                  <input
                    type="checkbox"
                    :checked="selectedStudentIds.includes(student.id)"
                    @change="toggleStudentSelection(student.id)"
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <div class="flex-1">
                    <div class="flex items-center justify-between">
                      <span class="font-medium text-gray-900">{{ student.name }}</span>
                      <span class="text-sm text-gray-500">{{ student.age }} years old</span>
                    </div>
                    <div class="flex items-center space-x-2 text-sm text-gray-600">
                      <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                        {{ student.type }}
                      </span>
                      <span class="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                        Level {{ student.level }}
                      </span>
                      <span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">
                        {{ student.coins }} coins
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <p class="text-sm text-gray-500 mt-1">
              Selected {{ selectedStudentIds.length }} student(s)
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-4">
          <button 
              type="button"
            @click="showCreateClassModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
              type="submit"
              :disabled="!newClassData.name || selectedStudentIds.length === 0 || isCreatingClass"
              class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
              <span v-if="isCreatingClass">Creating...</span>
              <span v-else>Create Class</span>
          </button>
        </div>
        </form>
      </div>
    </div>

    <!-- AI Assist Component -->
    <AIAssistComponent 
      :model-value="showAIAssist"
      @update:model-value="showAIAssist = $event"
      @module-saved="handleModuleSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'
import AIAssistComponent from '@/components/teacher/AIAssistComponent.vue'
import type { Class } from '@/types'
import { apiService } from '@/services/api'

const router = useRouter()
const teacherStore = useTeacherStore()

// State
const showCreateClassModal = ref(false)
const showAIAssist = ref(false)
const isCreatingClass = ref(false)
const newClassData = ref({
  name: '',
  description: ''
})
const selectedStudentIds = ref<string[]>([])

// Computed properties
const totalStudents = computed(() => {
  return teacherStore.classes.reduce((total, classItem) => total + (classItem.students_count || 0), 0)
})

// Methods
const calculateOverallProgress = (_classItem: Class) => {
  // Simple progress based on student count - will be replaced with real data later
  return _classItem.students_count ? Math.min(_classItem.students_count * 10, 100) : 0
}

const getStudentsNeedingSupportCount = (_classItem: Class) => {
  // Simple placeholder - will be replaced with real data later
  return 0
}

const getPerformanceColorClass = (performance: number) => {
  if (performance >= 90) return 'text-success'
  if (performance >= 75) return 'text-primary'
  if (performance >= 60) return 'text-warning'
  return 'text-error'
}

const formatDate = (dateString: string | Date) => {
  const date = typeof dateString === 'string' ? new Date(dateString) : dateString
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const navigateToClassProgress = (classId: string) => {
  router.push(`/teacher/class-progress/${classId}`)
}

const navigateToClassManagement = (classId: string) => {
  router.push(`/teacher/class-management/${classId}`)
}

const handleModuleSaved = (module: any) => {
  console.log('🎉 [TEACHER] AI-generated module saved:', module)
  
  // Close the AI Assist modal
  showAIAssist.value = false
  
  // Show success message
  alert(`Module "${module.title || 'AI Generated Module'}" saved successfully!`)
  
  // Refresh modules list
  teacherStore.loadModules()
}

// Toggle student selection
const toggleStudentSelection = (studentId: string) => {
  const index = selectedStudentIds.value.indexOf(studentId)
  if (index > -1) {
    selectedStudentIds.value.splice(index, 1)
  } else {
    selectedStudentIds.value.push(studentId)
  }
}

// Create new class
const createNewClass = async () => {
  if (!newClassData.value.name || selectedStudentIds.value.length === 0) {
    alert('Please provide a class name and select at least one student')
    return
  }

  console.log('🏫 [TEACHER] Creating new class:', {
    name: newClassData.value.name,
    description: newClassData.value.description,
    students: selectedStudentIds.value
  })

  try {
    isCreatingClass.value = true
    
    // Call the real API to create the class
    const response = await teacherStore.createClass({
      name: newClassData.value.name,
      description: newClassData.value.description,
      student_ids: selectedStudentIds.value
    })

    if (response) {
      // Show success message
      alert(`Class "${newClassData.value.name}" created successfully with ${selectedStudentIds.value.length} students!`)
      
      // Reset form and close modal
      resetCreateClassForm()
      showCreateClassModal.value = false
      
      // FORCE REFRESH from API to get real data from database
      console.log('🔄 [TEACHER] Force refreshing all data from API...')
      await teacherStore.forceRefresh()
      
      console.log('✅ [TEACHER] Dashboard refreshed with real data from database')
    } else {
      alert('Failed to create class. Please try again.')
    }
  } catch (error) {
    console.error('❌ [TEACHER] Error creating class:', error)
    alert('Error creating class. Please try again.')
  } finally {
    isCreatingClass.value = false
  }
}

const resetCreateClassForm = () => {
  newClassData.value = {
    name: '',
    description: ''
  }
  selectedStudentIds.value = []
}

// Load available students when modal opens
const openCreateClassModal = () => {
  console.log('🏫 [TEACHER] Opening create class modal...')
  showCreateClassModal.value = true
  // Load real student data from the database
  teacherStore.loadAvailableStudents()
}

// Refresh dashboard data
const refreshDashboard = async () => {
  console.log('🔄 [TEACHER] Refreshing dashboard data...')
  try {
    await teacherStore.forceRefresh()
    console.log('✅ [TEACHER] Dashboard refreshed successfully')
  } catch (error) {
    console.error('❌ [TEACHER] Error refreshing dashboard:', error)
    alert('Failed to refresh dashboard data. Please try again.')
  }
}

// Lifecycle hooks
onMounted(async () => {
  try {
    // Load teacher dashboard data and classes
    await Promise.all([
      teacherStore.loadDashboard(),
      teacherStore.loadClasses()
    ])
    console.log('✅ [TEACHER] Dashboard loaded successfully')
  } catch (error) {
    console.error('❌ [TEACHER] Failed to load dashboard:', error)
  }
})
</script>

<style scoped>
/* Animation for loading spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Smooth transitions */
.transition-colors {
  transition-property: background-color, border-color, color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-shadow {
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Hover effects */
.hover\:shadow-md:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.hover\:bg-blue-600:hover {
  background-color: #2563eb;
}

.hover\:bg-gray-200:hover {
  background-color: #e5e7eb;
}

/* Focus styles for accessibility */
button:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
</style>