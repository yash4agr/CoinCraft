<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Welcome Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        Welcome back, {{ teacherStore.profile?.name || 'Teacher' }}! 👋
      </h1>
      <p class="text-gray-600">Here's an overview of your classes and student progress</p>
    </div>

    <!-- Quick Stats Section -->
    <div class="mb-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
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

        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold text-gray-800">Avg. Performance</h3>
            <div class="w-10 h-10 rounded-full bg-yellow-100 flex items-center justify-center">
              <i class="ri-line-chart-line text-yellow-600"></i>
            </div>
          </div>
          <div class="text-3xl font-bold text-yellow-600">{{ averagePerformance }}%</div>
          <p class="text-sm text-gray-500 mt-1">Across all classes</p>
        </div>

        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-lg font-semibold text-gray-800">Need Support</h3>
            <div class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">
              <i class="ri-error-warning-line text-red-600"></i>
            </div>
          </div>
          <div class="text-3xl font-bold text-red-600">{{ studentsNeedingSupport }}</div>
          <p class="text-sm text-gray-500 mt-1">Students requiring attention</p>
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
            @click="showCreateClassModal = true"
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
          @click="teacherStore.loadTeacherProfile"
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
          @click="showCreateClassModal = true"
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
              <h3 class="text-xl font-bold text-gray-800">{{ classItem.name }}</h3>
              <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                Grade {{ classItem.grade }}
              </span>
            </div>
            <p class="text-gray-600 text-sm">
              Created {{ formatDate(classItem.createdAt) }}
            </p>
          </div>

          <!-- Class Stats -->
          <div class="p-6">
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{{ classItem.students.length }}</div>
                <p class="text-sm text-gray-600">Students</p>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold" :class="getPerformanceColorClass(classItem.averagePerformance)">
                  {{ Math.round(classItem.averagePerformance) }}%
                </div>
                <p class="text-sm text-gray-600">Avg. Performance</p>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="mb-4">
              <div class="flex justify-between text-sm text-gray-600 mb-1">
                <span>Overall Progress</span>
                <span>{{ calculateOverallProgress(classItem) }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div 
                  class="bg-blue-500 h-2.5 rounded-full" 
                  :style="{ width: `${calculateOverallProgress(classItem)}%` }"
                ></div>
              </div>
            </div>

            <!-- Students Needing Support -->
            <div v-if="getStudentsNeedingSupportCount(classItem) > 0" class="mb-4">
              <div class="flex items-center text-red-500 text-sm">
                <i class="ri-error-warning-line mr-1"></i>
                <span>{{ getStudentsNeedingSupportCount(classItem) }} students need support</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-2 mt-4">
              <button 
                @click="navigateToClassProgress(classItem.id)"
                class="flex-1 py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
              >
                View Progress
              </button>
              <button 
                @click="navigateToClassManagement(classItem.id)"
                class="flex-1 py-2 px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm"
              >
                Manage Class
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

    <!-- Create Class Modal (placeholder) -->
    <div v-if="showCreateClassModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Create New Class</h3>
          <button 
            @click="showCreateClassModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">Class creation form would be implemented here</p>
        
        <div class="flex gap-3">
          <button 
            @click="showCreateClassModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="showCreateClassModal = false"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            Create Class
          </button>
        </div>
      </div>
    </div>

    <!-- AI Assist Component -->
    <AIAssistComponent 
      v-model="showAIAssist"
      @module-saved="handleModuleSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'
import AIAssistComponent from '@/components/teacher/AIAssistComponent.vue'
import type { Class } from '@/stores/teacher'

const router = useRouter()
const teacherStore = useTeacherStore()

// State
const showCreateClassModal = ref(false)
const showAIAssist = ref(false)

// Computed properties
const totalStudents = computed(() => {
  return teacherStore.classes.reduce((total, classItem) => total + classItem.students.length, 0)
})

const averagePerformance = computed(() => {
  if (teacherStore.classes.length === 0) return 0
  
  const totalPerformance = teacherStore.classes.reduce(
    (sum, classItem) => sum + classItem.averagePerformance, 0
  )
  
  return Math.round(totalPerformance / teacherStore.classes.length)
})

const studentsNeedingSupport = computed(() => {
  return teacherStore.classes.reduce((total, classItem) => {
    return total + classItem.students.filter(student => student.needsSupport).length
  }, 0)
})

// Methods
const calculateOverallProgress = (classItem: Class) => {
  if (classItem.modules.length === 0 || classItem.students.length === 0) return 0
  
  let totalCompleted = 0
  let totalModules = classItem.modules.length * classItem.students.length
  
  classItem.students.forEach(student => {
    classItem.modules.forEach(moduleId => {
      if (student.progress[moduleId]?.completed) {
        totalCompleted++
      }
    })
  })
  
  return Math.round((totalCompleted / totalModules) * 100)
}

const getStudentsNeedingSupportCount = (classItem: Class) => {
  return classItem.students.filter(student => student.needsSupport).length
}

const getPerformanceColorClass = (performance: number) => {
  if (performance >= 90) return 'text-success'
  if (performance >= 75) return 'text-primary'
  if (performance >= 60) return 'text-warning'
  return 'text-error'
}

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
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
  // Optionally refresh modules list or show success message
}

// Lifecycle hooks
onMounted(async () => {
  if (!teacherStore.profile) {
    await teacherStore.loadTeacherProfile()
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