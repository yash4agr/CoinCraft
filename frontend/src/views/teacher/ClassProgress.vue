<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Class Progress</h1>
          <p class="text-gray-600">Monitor student performance and identify areas for improvement</p>
        </div>
        
        <div class="w-full md:w-64">
          <select
            v-model="selectedClassId"
            @change="loadClassData"
            class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">Select a class</option>
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

    <!-- Class Overview Cards -->
    <div v-if="selectedClass" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Total Students</p>
            <p class="text-2xl font-bold text-gray-800">{{ selectedClass.students.length }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
            <i class="ri-group-line text-blue-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Average Score</p>
            <p class="text-2xl font-bold text-gray-800">{{ averageScore }}%</p>
          </div>
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
            <i class="ri-trophy-line text-green-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Completed Modules</p>
            <p class="text-2xl font-bold text-gray-800">{{ completedModules }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
            <i class="ri-book-line text-purple-600 text-xl"></i>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 mb-1">Need Help</p>
            <p class="text-2xl font-bold text-gray-800">{{ studentsNeedingHelp }}</p>
          </div>
          <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
            <i class="ri-alert-line text-red-600 text-xl"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div v-if="selectedClass" class="bg-white rounded-xl shadow-sm p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="relative flex-1">
          <i class="ri-search-line absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search students by name..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <select 
          v-model="sortBy"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="name">Sort by Name</option>
          <option value="score">Sort by Score</option>
          <option value="progress">Sort by Progress</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
      <p class="text-gray-600">Loading class data...</p>
    </div>

    <!-- No Class Selected -->
    <div v-else-if="!selectedClass" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-group-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">Select a Class</h3>
      <p class="text-gray-600">Choose a class from the dropdown to view student progress</p>
    </div>

    <!-- Students List -->
    <div v-else class="space-y-4">
      <div 
        v-for="student in filteredStudents" 
        :key="student.id"
        class="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow"
      >
        <div class="flex flex-col lg:flex-row lg:items-center gap-4">
          <!-- Student Info -->
          <div class="flex items-center gap-4 flex-1">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-semibold">{{ student.name.charAt(0) }}</span>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">{{ student.name }}</h3>
              <p class="text-sm text-gray-600">{{ student.email }}</p>
            </div>
          </div>

          <!-- Progress Stats -->
          <div class="grid grid-cols-3 gap-4 lg:gap-8">
            <div class="text-center">
              <div class="text-sm text-gray-500 mb-1">Overall Score</div>
              <div class="text-lg font-bold" :class="getScoreColor(student.overallScore)">
                {{ student.overallScore }}%
              </div>
            </div>
            <div class="text-center">
              <div class="text-sm text-gray-500 mb-1">Modules</div>
              <div class="text-lg font-bold text-gray-800">
                {{ student.completedModules }}/{{ student.totalModules }}
              </div>
            </div>
            <div class="text-center">
              <div class="text-sm text-gray-500 mb-1">Status</div>
              <span 
                class="px-3 py-1 rounded-full text-xs font-medium"
                :class="getStatusClass(student.performanceCategory)"
              >
                {{ formatCategoryLabel(student.performanceCategory) }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2">
            <button 
              @click="showStudentDetails(student.id)"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-eye-line mr-1"></i> View Details
            </button>
            <button 
              v-if="student.performanceCategory === 'needsHelp'"
              @click="openInterventionModal(student.id)"
              class="px-4 py-2 bg-orange-500 hover:bg-orange-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-heart-pulse-line mr-1"></i> Intervention
            </button>
          </div>
        </div>

        <!-- Progress Bar -->
        <div class="mt-4">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>Course Progress</span>
            <span>{{ Math.round((student.completedModules / student.totalModules) * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-500 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${(student.completedModules / student.totalModules) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Student Details Modal -->
    <div v-if="showStudentDetailsModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Student Details</h3>
          <button 
            @click="showStudentDetailsModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Modal content would go here -->
        <div class="text-center py-8">
          <p class="text-gray-600">Student details will be displayed here</p>
        </div>
      </div>
    </div>

    <!-- Intervention Modal -->
    <div v-if="showInterventionModalRef" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-2xl w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Plan Intervention</h3>
          <button 
            @click="closeInterventionModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Modal content would go here -->
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Intervention Type</label>
            <select class="w-full p-3 border border-gray-300 rounded-lg">
              <option>One-on-one tutoring</option>
              <option>Additional practice materials</option>
              <option>Peer mentoring</option>
              <option>Parent conference</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Notes</label>
            <textarea 
              class="w-full p-3 border border-gray-300 rounded-lg h-24"
              placeholder="Add notes about the intervention plan..."
            ></textarea>
          </div>
          
          <div class="flex gap-3 pt-4">
            <button 
              @click="saveIntervention"
              class="flex-1 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              Save Intervention
            </button>
            <button 
              @click="closeInterventionModal"
              class="flex-1 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'
import type { Student, Class } from '@/stores/teacher'

const route = useRoute()
const router = useRouter()
const teacherStore = useTeacherStore()

// State
const selectedClassId = ref('')
const isLoading = ref(false)
const searchQuery = ref('')
const sortBy = ref('name')
const showStudentDetailsModal = ref(false)
const showInterventionModalRef = ref(false)
const selectedStudentId = ref('')

const selectedClass = computed(() => {
  return teacherStore.getClassById(selectedClassId.value)
})

const filteredStudents = computed(() => {
  if (!selectedClass.value) return []
  
  let students = [...selectedClass.value.students]
  
  // Apply search filter
  if (searchQuery.value) {
    students = students.filter(student =>
      student.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  // Apply sorting
  students.sort((a, b) => {
    switch (sortBy.value) {
      case 'score':
        return b.overallScore - a.overallScore
      case 'progress':
        return (b.completedModules / b.totalModules) - (a.completedModules / a.totalModules)
      default:
        return a.name.localeCompare(b.name)
    }
  })
  
  return students
})

const averageScore = computed(() => {
  if (!selectedClass.value || selectedClass.value.students.length === 0) return 0
  const total = selectedClass.value.students.reduce((sum, student) => sum + student.overallScore, 0)
  return Math.round(total / selectedClass.value.students.length)
})

const completedModules = computed(() => {
  if (!selectedClass.value) return 0
  return selectedClass.value.students.reduce((sum, student) => sum + student.completedModules, 0)
})

const studentsNeedingHelp = computed(() => {
  if (!selectedClass.value) return 0
  return selectedClass.value.students.filter(student => student.performanceCategory === 'needsHelp').length
})

const loadClassData = async () => {
  if (!selectedClassId.value) return
  
  isLoading.value = true
  try {
    await teacherStore.loadClassProgress(selectedClassId.value)
  } catch (error) {
    console.error('Failed to load class data:', error)
  } finally {
    isLoading.value = false
  }
}

const getScoreColor = (score: number) => {
  if (score >= 90) return 'text-green-600'
  if (score >= 80) return 'text-blue-600'
  if (score >= 70) return 'text-yellow-600'
  return 'text-red-600'
}

const getStatusClass = (category: string) => {
  switch (category) {
    case 'excellent': return 'bg-green-100 text-green-700'
    case 'good': return 'bg-blue-100 text-blue-700'
    case 'average': return 'bg-yellow-100 text-yellow-700'
    case 'needsHelp': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

const formatCategoryLabel = (category: string) => {
  switch (category) {
    case 'excellent': return 'Excellent'
    case 'good': return 'Good'
    case 'average': return 'Average'
    case 'needsHelp': return 'Needs Help'
    default: return ''
  }
}

const showStudentDetails = (studentId: string) => {
  selectedStudentId.value = studentId
  showStudentDetailsModal.value = true
}

const openInterventionModal = (studentId: string) => {
  selectedStudentId.value = studentId
  showInterventionModalRef.value = true
}

const closeInterventionModal = () => {
  showInterventionModalRef.value = false
}

const saveIntervention = () => {
  showInterventionModalRef.value = false
}

// Lifecycle hooks
onMounted(async () => {
  if (!teacherStore.profile) {
    await teacherStore.loadTeacherProfile()
  }
  
  const classId = route.params.id as string
  if (classId) {
    selectedClassId.value = classId
    await loadClassData()
  }
})

watch(() => route.params.id, (newId) => {
  if (newId) {
    selectedClassId.value = newId as string
    loadClassData()
  }
})
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