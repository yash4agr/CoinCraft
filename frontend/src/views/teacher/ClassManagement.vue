<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Class Management</h1>
          <p class="text-gray-600">Create, edit, and manage your classes and student rosters</p>
        </div>
        
        <div class="flex gap-2">
          <button 
            @click="showCreateClassModal = true"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-add-line"></i>
            <span>Create Class</span>
          </button>
          <button 
            @click="showImportModal = true"
            class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-upload-line"></i>
            <span>Import Students</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Class Selection -->
    <div v-if="teacherStore.classes.length > 0" class="mb-8">
      <div class="flex flex-wrap gap-3">
        <button 
          @click="selectedClassId = ''"
          class="px-4 py-2 rounded-lg transition-colors"
          :class="selectedClassId === '' 
            ? 'bg-blue-500 text-white' 
            : 'bg-white text-gray-700 hover:bg-gray-100'"
        >
          All Classes
        </button>
        <button 
          v-for="classItem in teacherStore.classes" 
          :key="classItem.id"
          @click="selectedClassId = classItem.id"
          class="px-4 py-2 rounded-lg transition-colors"
          :class="selectedClassId === classItem.id 
            ? 'bg-blue-500 text-white' 
            : 'bg-white text-gray-700 hover:bg-gray-100'"
        >
          {{ classItem.name }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
      <p class="text-gray-600">Loading class data...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="teacherStore.classes.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-group-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Classes Yet</h3>
      <p class="text-gray-600 mb-6">Get started by creating your first class</p>
      <button 
        @click="showCreateClassModal = true"
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Create Your First Class
      </button>
    </div>

    <!-- All Classes View -->
    <div v-else-if="selectedClassId === ''" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div 
        v-for="classItem in teacherStore.classes" 
        :key="classItem.id"
        class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
      >
        <!-- Class Header -->
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xl font-bold text-gray-800">{{ classItem.name }}</h3>
          </div>
          <p class="text-gray-600 text-sm">
            Created {{ formatDate(classItem.created_at as any) }}
          </p>
        </div>

        <!-- Class Stats -->
        <div class="p-6">
          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ classItem.students_count || 0 }}</div>
              <p class="text-sm text-gray-600">Students</p>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold" :class="getPerformanceColorClass(classItem.average_performance || 0)">
                {{ Math.round(classItem.average_performance || 0) }}%
              </div>
              <p class="text-sm text-gray-600">Avg. Performance</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2">
            <button 
              @click="viewClassDetails(classItem.id)"
              class="flex-1 py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
            >
              Manage Class
            </button>
            <button 
              @click="editClass(classItem.id)"
              class="py-2 px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm"
            >
              <i class="ri-edit-line"></i>
            </button>
            <button 
              @click="confirmDeleteClass(classItem.id)"
              class="py-2 px-3 bg-gray-100 hover:bg-red-100 text-gray-700 hover:text-red-700 rounded-lg transition-colors text-sm"
            >
              <i class="ri-delete-bin-line"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Single Class View -->
    <div v-else-if="selectedClassId !== ''" class="mb-8">
      <!-- Class Header -->
      <div class="bg-white rounded-xl shadow-sm p-6 mb-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">{{ selectedClass?.name || 'Class' }}</h2>
            <p class="text-gray-600">{{ students.length }} students</p>
          </div>
          
          <div class="flex gap-2">
            <button 
              @click="editClass(selectedClassId)"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              <i class="ri-edit-line mr-1"></i> Edit Class
            </button>
            <button 
              @click="showAddStudentModal = true"
              class="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors"
            >
              <i class="ri-user-add-line mr-1"></i> Add Student
            </button>
          </div>
        </div>
      </div>

      <!-- Student Management -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden mb-6">
        <div class="p-6 border-b border-gray-100">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <h3 class="text-xl font-bold text-gray-800">Student Roster</h3>
            
            <!-- Search and Filter -->
            <div class="flex gap-2">
              <div class="relative">
                <i class="ri-search-line absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input 
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search students..."
                  class="pl-9 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select 
                v-model="sortBy"
                class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="name">Name</option>
                <option value="performance">Performance</option>
                <option value="lastActivity">Last Activity</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Student List -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Student
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Performance
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Activity
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="student in filteredStudents" :key="(student as any).user_id || (student as any).id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <img 
                      :src="(student as any).avatar_url || (student as any).avatar" 
                      :alt="`${student.name}'s avatar`"
                      class="w-8 h-8 rounded-full mr-3"
                    />
                    <div class="font-medium text-gray-800">{{ student.name }}</div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div 
                    class="font-medium"
                    :class="getPerformanceColorClass(student.performance_score ?? 0)"
                  >
                    {{ Math.round(student.performance_score ?? 0) }}%
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-gray-600">{{ formatLastActivity(student.last_activity_date) }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="student.needs_support ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'"
                  >
                    {{ student.needs_support ? 'Needs Support' : 'On Track' }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <button 
                    @click="editStudent((student as any).user_id || (student as any).id)"
                    class="text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    <i class="ri-edit-line"></i>
                  </button>
                  <button 
                    @click="viewStudentProgress((student as any).user_id || (student as any).id)"
                    class="ml-3 text-green-600 hover:text-green-800 transition-colors"
                  >
                    <i class="ri-line-chart-line"></i>
                  </button>
                  <button 
                    @click="confirmRemoveStudent((student as any).user_id || (student as any).id)"
                    class="ml-3 text-red-600 hover:text-red-800 transition-colors"
                  >
                    <i class="ri-delete-bin-line"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Empty State for Students -->
        <div v-if="students.length === 0" class="p-8 text-center">
          <i class="ri-user-line text-gray-300 text-4xl mb-2"></i>
          <h4 class="text-lg font-semibold text-gray-800 mb-2">No Students Yet</h4>
          <p class="text-gray-600 mb-4">Add students to this class to get started</p>
          <button 
            @click="showAddStudentModal = true"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
          >
            Add First Student
          </button>
        </div>
      </div>

      <!-- Assigned Modules -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden">
        <div class="p-6 border-b border-gray-100">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <h3 class="text-xl font-bold text-gray-800">Assigned Modules</h3>
            
            <button 
              @click="showAssignModuleModal = true"
              class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
            >
              <i class="ri-add-line mr-1"></i> Assign Module
            </button>
          </div>
        </div>
        
        <!-- Module List -->
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Module
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Category
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Difficulty
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Completion
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="module in assignedModules" :key="module.id || module">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="font-medium text-gray-800">
                    {{ module.title || getModuleName(module) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="text-gray-600">{{ module.category || getModuleCategory(module) }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    class="px-2 py-1 text-xs font-medium rounded-full"
                    :class="getModuleDifficultyClass(module.difficulty || getModuleDifficulty(module))"
                  >
                    {{ module.difficulty || getModuleDifficulty(module) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="w-full bg-gray-200 rounded-full h-2.5 mr-2 max-w-32">
                      <div 
                        class="bg-blue-500 h-2.5 rounded-full" 
                        :style="{ width: `${getModuleCompletionRate(module.id || module)}%` }"
                      ></div>
                    </div>
                    <span>{{ getModuleCompletionRate(module.id || module) }}%</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <button 
                    @click="viewModuleDetails(module.id || module)"
                    class="text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    <i class="ri-eye-line"></i>
                  </button>
                  <button 
                    @click="confirmUnassignModule(module.id || module)"
                    class="ml-3 text-red-600 hover:text-red-800 transition-colors"
                  >
                    <i class="ri-close-circle-line"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Empty State for Modules -->
        <div v-if="assignedModules.length === 0" class="p-8 text-center">
          <i class="ri-book-line text-gray-300 text-4xl mb-2"></i>
          <h4 class="text-lg font-semibold text-gray-800 mb-2">No Modules Assigned</h4>
          <p class="text-gray-600 mb-4">Assign modules to this class to get started</p>
          <button 
            @click="showAssignModuleModal = true"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
          >
            Assign First Module
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Class Modal (placeholder) -->
    <div v-if="showClassModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">
            {{ isEditingClass ? 'Edit Class' : 'Create New Class' }}
          </h3>
          <button 
            @click="showClassModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">
          Class {{ isEditingClass ? 'editing' : 'creation' }} form would be implemented here
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="showClassModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="saveClass"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            {{ isEditingClass ? 'Save Changes' : 'Create Class' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add Student Modal (placeholder) -->
    <div v-if="showAddStudentModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Add Student</h3>
          <button 
            @click="showAddStudentModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">
          Student addition form would be implemented here
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="showAddStudentModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="addStudent"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            Add Student
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Student Modal (placeholder) -->
    <div v-if="showEditStudentModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Edit Student</h3>
          <button 
            @click="showEditStudentModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">
          Student editing form would be implemented here
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="showEditStudentModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="updateStudent"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>

    <!-- Assign Module Modal (placeholder) -->
    <div v-if="showAssignModuleModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Assign Module</h3>
          <button 
            @click="showAssignModuleModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">
          Module assignment form would be implemented here
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="showAssignModuleModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="assignModule"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            Assign Module
          </button>
        </div>
      </div>
    </div>

    <!-- Import Students Modal (placeholder) -->
    <div v-if="showImportModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Import Students</h3>
          <button 
            @click="showImportModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Form would go here -->
        <p class="text-center text-gray-600 mb-6">
          Student import form would be implemented here
        </p>
        
        <div class="flex gap-3">
          <button 
            @click="showImportModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="importStudents"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
          >
            Import Students
          </button>
        </div>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showConfirmModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="w-16 h-16 mx-auto bg-red-100 rounded-full flex items-center justify-center mb-4">
            <i class="ri-error-warning-line text-red-600 text-3xl"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">{{ confirmTitle }}</h3>
          <p class="text-gray-600">{{ confirmMessage }}</p>
        </div>
        
        <div class="flex gap-3">
          <button 
            @click="showConfirmModal = false"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="confirmAction"
            class="flex-1 py-3 px-4 bg-red-500 text-white rounded-lg font-medium hover:bg-red-600 transition-colors"
          >
            {{ confirmButtonText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'
import type { Student } from '@/types'

const route = useRoute()
const router = useRouter()
const teacherStore = useTeacherStore()

// State
const selectedClassId = ref('')
const isLoading = ref(false)
const searchQuery = ref('')
const sortBy = ref('name')
const showCreateClassModal = ref(false)
const showClassModal = ref(false)
const showAddStudentModal = ref(false)
const showEditStudentModal = ref(false)
const showAssignModuleModal = ref(false)
const showImportModal = ref(false)
const showConfirmModal = ref(false)
const isEditingClass = ref(false)
const selectedStudentId = ref('')
const confirmTitle = ref('')
const confirmMessage = ref('')
const confirmButtonText = ref('')
const confirmCallback = ref<() => void>(() => {})

// Local data for selected class
const students = ref<Student[]>([])
const assignedModules = ref<any[]>([])

// Computed properties
const selectedClass = computed(() => {
  return teacherStore.getClassById(selectedClassId.value)
})

const filteredStudents = computed(() => {
  let list = [...students.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    list = list.filter(s => (s.name || '').toLowerCase().includes(query))
  }
  
  list.sort((a: any, b: any) => {
    if (sortBy.value === 'name') return (a.name || '').localeCompare(b.name || '')
    if (sortBy.value === 'performance') return (b.performance_score ?? 0) - (a.performance_score ?? 0)
    if (sortBy.value === 'lastActivity') {
      const ad = a.last_activity_date ? new Date(a.last_activity_date).getTime() : 0
      const bd = b.last_activity_date ? new Date(b.last_activity_date).getTime() : 0
      return bd - ad
    }
    return 0
  })
  
  return list
})

// Methods
const viewClassDetails = async (classId: string) => {
  // Keep URL in sync and trigger data load via watchers
  if (route.params.id !== classId) {
    await router.push(`/teacher/class-management/${classId}`)
  }
  selectedClassId.value = classId
}

const createClass = () => {
  isEditingClass.value = false
  showClassModal.value = true
}

const editClass = (classId: string) => {
  selectedClassId.value = classId
  isEditingClass.value = true
  showClassModal.value = true
}

const saveClass = async () => {
  // In a real app, this would save the class
  showClassModal.value = false
  
  // Show success message or notification
  alert(`Class ${isEditingClass.value ? 'updated' : 'created'} successfully!`)
}

const confirmDeleteClass = (classId: string) => {
  selectedClassId.value = classId
  confirmTitle.value = 'Delete Class'
  confirmMessage.value = 'Are you sure you want to delete this class? This action cannot be undone.'
  confirmButtonText.value = 'Delete Class'
  confirmCallback.value = deleteClass
  showConfirmModal.value = true
}

const deleteClass = async () => {
  try {
    isLoading.value = true
    
    await teacherStore.deleteClass(selectedClassId.value)
    
    // Reset selection if the deleted class was selected
    if (selectedClassId.value === selectedClassId.value) {
      selectedClassId.value = ''
    }
    
    showConfirmModal.value = false
    
    // Show success message
    alert('Class deleted successfully!')
    
  } catch (error) {
    console.error('Error deleting class:', error)
    alert('Failed to delete class. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const editStudent = (studentId: string) => {
  selectedStudentId.value = studentId
  showEditStudentModal.value = true
}

const viewStudentProgress = (studentId: string) => {
  if (!selectedClass.value) return
  
  // Navigate to student progress view
  router.push(`/teacher/class-progress/${selectedClass.value.id}?student=${studentId}`)
}

const confirmRemoveStudent = (studentId: string) => {
  selectedStudentId.value = studentId
  confirmTitle.value = 'Remove Student'
  confirmMessage.value = 'Are you sure you want to remove this student from the class? Their progress data will be lost.'
  confirmButtonText.value = 'Remove Student'
  confirmCallback.value = removeStudent
  showConfirmModal.value = true
}

const removeStudent = async () => {
  try {
    isLoading.value = true
    // TODO: hook to real API; for now update local array
    students.value = students.value.filter((s: any) => (s.user_id || s.id) !== selectedStudentId.value)
    showConfirmModal.value = false
    alert('Student removed successfully!')
  } catch (error) {
    console.error('Error removing student:', error)
    alert('Failed to remove student. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const addStudent = async () => {
  if (!selectedClass.value) return
  
  try {
    isLoading.value = true
    
    // In a real app, this would add a new student
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showAddStudentModal.value = false
    
    // Show success message
    alert('Student added successfully!')
    
  } catch (error) {
    console.error('Error adding student:', error)
    alert('Failed to add student. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const updateStudent = async () => {
  if (!selectedClass.value) return
  
  try {
    isLoading.value = true
    
    // In a real app, this would update the student
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showEditStudentModal.value = false
    
    // Show success message
    alert('Student updated successfully!')
    
  } catch (error) {
    console.error('Error updating student:', error)
    alert('Failed to update student. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const viewModuleDetails = (moduleId: string) => {
  // Navigate to module details view
  router.push(`/teacher/module-management?module=${moduleId}`)
}

const confirmUnassignModule = (moduleId: string) => {
  confirmTitle.value = 'Unassign Module'
  confirmMessage.value = 'Are you sure you want to unassign this module from the class? Student progress for this module will be lost.'
  confirmButtonText.value = 'Unassign Module'
  confirmCallback.value = () => unassignModule(moduleId)
  showConfirmModal.value = true
}

const unassignModule = async (moduleId: string) => {
  try {
    isLoading.value = true
    
    // In a real app, this would call an API to unassign the module
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update local assigned modules list
    assignedModules.value = assignedModules.value.filter((m: any) => (m.id || m) !== moduleId)
    
    showConfirmModal.value = false
    
    // Show success message
    alert('Module unassigned successfully!')
    
  } catch (error) {
    console.error('Error unassigning module:', error)
    alert('Failed to unassign module. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const assignModule = async () => {
  if (!selectedClass.value) return
  
  try {
    isLoading.value = true
    
    // In a real app, this would assign a module to the class
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showAssignModuleModal.value = false
    
    // Show success message
    alert('Module assigned successfully!')
    
  } catch (error) {
    console.error('Error assigning module:', error)
    alert('Failed to assign module. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const importStudents = async () => {
  try {
    isLoading.value = true
    
    // In a real app, this would import students from a file
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showImportModal.value = false
    
    // Show success message
    alert('Students imported successfully!')
    
  } catch (error) {
    console.error('Error importing students:', error)
    alert('Failed to import students. Please try again.')
  } finally {
    isLoading.value = false
  }
}

const confirmAction = () => {
  confirmCallback.value()
}

const getPerformanceColorClass = (performance: number) => {
  if (performance >= 90) return 'text-success'
  if (performance >= 75) return 'text-primary'
  if (performance >= 60) return 'text-warning'
  return 'text-error'
}

const formatLastActivity = (date: any) => {
  const now = new Date()
  const activityDate = new Date(date)
  const diffTime = Math.abs(now.getTime() - activityDate.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getModuleName = (moduleId: string) => {
  const module = teacherStore.getModuleById(moduleId)
  return module ? module.title : 'Unknown Module'
}

const getModuleCategory = (moduleId: string) => {
  const module = teacherStore.getModuleById(moduleId)
  return module ? module.category : 'Unknown'
}

const getModuleDifficulty = (moduleId: string) => {
  const module = teacherStore.getModuleById(moduleId)
  return module ? module.difficulty : 'unknown'
}

const getModuleDifficultyClass = (difficultyOrModuleId: string) => {
  const difficulty = ['beginner', 'intermediate', 'advanced'].includes(difficultyOrModuleId as any)
    ? difficultyOrModuleId
    : getModuleDifficulty(difficultyOrModuleId)
  switch (difficulty) {
    case 'beginner': return 'bg-success-100 text-success-700'
    case 'intermediate': return 'bg-warning-100 text-warning-700'
    case 'advanced': return 'bg-error-100 text-error-700'
    default: return 'bg-surface-100 text-surface-700'
  }
}

const getModuleCompletionRate = (moduleId: string) => {
  const totalStudents = students.value.length
  if (totalStudents === 0) return 0
  const completedCount = (students.value as any[]).filter(s => s.progress?.[moduleId]?.completed).length
  return Math.round((completedCount / totalStudents) * 100)
}

// Lifecycle hooks
onMounted(async () => {
  if (!teacherStore.profile) {
    await teacherStore.loadTeacherProfile()
  }
  await teacherStore.loadClasses()
  const classId = route.params.id as string
  if (classId && teacherStore.getClassById(classId)) {
    selectedClassId.value = classId
    await loadSelectedClassData()
  } else {
    selectedClassId.value = ''
  }
})

// Watch for changes in the route
watch(() => route.params.id, async (newId) => {
  if (newId) {
    selectedClassId.value = newId as string
    await loadSelectedClassData()
  }
})

// Load students and modules for the selected class
const loadSelectedClassData = async () => {
  if (!selectedClassId.value) return
  try {
    isLoading.value = true
    const [loadedStudents, loadedModules] = await Promise.all([
      teacherStore.getClassStudents(selectedClassId.value),
      teacherStore.getModulesAssignedToClass(selectedClassId.value)
    ])
    students.value = Array.isArray(loadedStudents) ? loadedStudents as any : []
    assignedModules.value = Array.isArray(loadedModules) ? loadedModules as any : []
  } catch (e) {
    console.error('Failed to load class data', e)
    students.value = []
    assignedModules.value = []
  } finally {
    isLoading.value = false
  }
}
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

.hover\:bg-red-100:hover {
  background-color: #fee2e2;
}

.hover\:text-red-700:hover {
  color: #b91c1c;
}

/* Focus styles for accessibility */
button:focus,
input:focus,
select:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}
</style>