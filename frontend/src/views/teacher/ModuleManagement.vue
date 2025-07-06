<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="mb-8">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Module Management</h1>
          <p class="text-gray-600">Create, edit, and assign learning modules to your classes</p>
        </div>
        
        <div class="flex gap-2">
          <button 
            @click="showCreateModuleModal = true"
            class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-add-line"></i>
            <span>Create Module</span>
          </button>
          <button 
            @click="showAIAssistModal = true"
            class="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <i class="ri-robot-line"></i>
            <span>AI Assist</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Search and Filter Bar -->
    <div class="bg-white rounded-xl shadow-sm p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search Input -->
        <div class="relative flex-1">
          <i class="ri-search-line absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search modules by title, description, or skills..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <!-- Filters -->
        <div class="flex flex-wrap gap-2">
          <select 
            v-model="filterCategory"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
          
          <select 
            v-model="filterDifficulty"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Difficulties</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          
          <select 
            v-model="filterAgeGroup"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Age Groups</option>
            <option value="10-12">10-12 years</option>
            <option value="12-14">12-14 years</option>
            <option value="14-16">14-16 years</option>
          </select>
          
          <button 
            v-if="hasActiveFilters"
            @click="clearFilters"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
      <p class="text-gray-600">Loading modules...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="teacherStore.modules.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-book-line text-blue-500 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Modules Yet</h3>
      <p class="text-gray-600 mb-6">Get started by creating your first learning module</p>
      <button 
        @click="showCreateModuleModal = true"
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Create Your First Module
      </button>
    </div>

    <!-- No Results State -->
    <div v-else-if="filteredModules.length === 0" class="bg-white rounded-xl p-12 text-center">
      <i class="ri-search-line text-gray-400 text-5xl mb-4"></i>
      <h3 class="text-xl font-semibold text-gray-800 mb-2">No Matching Modules</h3>
      <p class="text-gray-600 mb-6">Try adjusting your search or filters</p>
      <button 
        @click="clearFilters"
        class="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors"
      >
        Clear All Filters
      </button>
    </div>

    <!-- Modules Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div 
        v-for="module in filteredModules" 
        :key="module.id"
        class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
      >
        <!-- Module Header -->
        <div class="p-6 border-b border-gray-100">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xl font-bold text-gray-800 line-clamp-1">{{ module.title }}</h3>
            <span 
              class="px-3 py-1 rounded-full text-xs font-medium"
              :class="getDifficultyClass(module.difficulty)"
            >
              {{ module.difficulty }}
            </span>
          </div>
          <p class="text-gray-600 text-sm line-clamp-2 mb-3">{{ module.description }}</p>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="skill in module.skills.slice(0, 2)" 
              :key="skill"
              class="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs"
            >
              {{ skill }}
            </span>
            <span v-if="module.skills.length > 2" class="px-2 py-1 bg-gray-50 text-gray-600 rounded text-xs">
              +{{ module.skills.length - 2 }} more
            </span>
          </div>
        </div>

        <!-- Module Details -->
        <div class="p-6">
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="text-center">
              <div class="text-sm text-gray-500">Duration</div>
              <div class="font-semibold text-gray-800">{{ module.duration }} min</div>
            </div>
            <div class="text-center">
              <div class="text-sm text-gray-500">Age Group</div>
              <div class="font-semibold text-gray-800">{{ module.ageGroup }}</div>
            </div>
          </div>
          
          <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
            <div>Category: <span class="font-medium text-gray-700">{{ module.category }}</span></div>
            <div>
              <span 
                class="px-2 py-1 rounded-full text-xs"
                :class="module.published ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
              >
                {{ module.published ? 'Published' : 'Draft' }}
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-2 mt-4">
            <button 
              @click="previewModule(module.id)"
              class="flex-1 py-2 px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors text-sm"
            >
              <i class="ri-eye-line mr-1"></i> Preview
            </button>
            <button 
              @click="editModule(module.id)"
              class="flex-1 py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-edit-line mr-1"></i> Edit
            </button>
            <button 
              @click="openAssignModal(module.id)"
              class="flex-1 py-2 px-3 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors text-sm"
            >
              <i class="ri-share-line mr-1"></i> Assign
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Module Preview Modal -->
    <div v-if="showPreviewModal && selectedModule" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Module Preview</h3>
          <button 
            @click="showPreviewModal = false"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>
        
        <!-- Module Content Preview -->
        <div class="space-y-6">
          <div class="bg-gray-50 rounded-xl p-6">
            <h4 class="text-2xl font-bold text-gray-800 mb-2">{{ selectedModule.title }}</h4>
            <div class="flex flex-wrap gap-2 mb-4">
              <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                {{ selectedModule.category }}
              </span>
              <span 
                class="px-3 py-1 rounded-full text-sm"
                :class="getDifficultyClass(selectedModule.difficulty)"
              >
                {{ selectedModule.difficulty }}
              </span>
              <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                {{ selectedModule.ageGroup }}
              </span>
            </div>
            <p class="text-gray-700 mb-4">{{ selectedModule.description }}</p>
            <div class="flex flex-wrap gap-4 text-sm text-gray-600">
              <div class="flex items-center">
                <i class="ri-time-line mr-1"></i>
                <span>{{ selectedModule.duration }} minutes</span>
              </div>
              <div class="flex items-center">
                <i class="ri-calendar-line mr-1"></i>
                <span>{{ formatDate(selectedModule.createdAt) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTeacherStore } from '@/stores/teacher'

const router = useRouter()
const teacherStore = useTeacherStore()

// State
const isLoading = ref(false)
const searchQuery = ref('')
const filterCategory = ref('')
const filterDifficulty = ref('')
const filterAgeGroup = ref('')
const showCreateModuleModal = ref(false)
const showAIAssistModal = ref(false)
const showPreviewModal = ref(false)
const selectedModule = ref(null)

// Computed properties
const categories = computed(() => {
  const uniqueCategories = new Set<string>()
  teacherStore.modules.forEach(module => {
    uniqueCategories.add(module.category)
  })
  return Array.from(uniqueCategories)
})

const filteredModules = computed(() => {
  let modules = [...teacherStore.modules]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    modules = modules.filter(module =>
      module.title.toLowerCase().includes(query) ||
      module.description.toLowerCase().includes(query) ||
      module.skills.some(skill => skill.toLowerCase().includes(query))
    )
  }
  
  // Apply category filter
  if (filterCategory.value) {
    modules = modules.filter(module => module.category === filterCategory.value)
  }
  
  // Apply difficulty filter
  if (filterDifficulty.value) {
    modules = modules.filter(module => module.difficulty === filterDifficulty.value)
  }
  
  // Apply age group filter
  if (filterAgeGroup.value) {
    modules = modules.filter(module => module.ageGroup === filterAgeGroup.value)
  }
  
  return modules
})

const hasActiveFilters = computed(() => {
  return searchQuery.value || filterCategory.value || filterDifficulty.value || filterAgeGroup.value
})

// Methods
const clearFilters = () => {
  searchQuery.value = ''
  filterCategory.value = ''
  filterDifficulty.value = ''
  filterAgeGroup.value = ''
}

const getDifficultyClass = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'bg-green-100 text-green-700'
    case 'intermediate': return 'bg-yellow-100 text-yellow-700'
    case 'advanced': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const previewModule = (moduleId: string) => {
  selectedModule.value = teacherStore.getModuleById(moduleId)
  showPreviewModal.value = true
}

const editModule = (moduleId: string) => {
  router.push(`/teacher/modules/${moduleId}/edit`)
}

const openAssignModal = (moduleId: string) => {
  // Implementation for assign modal
  console.log('Assign module:', moduleId)
}

// Lifecycle
onMounted(async () => {
  if (!teacherStore.profile) {
    await teacherStore.loadTeacherProfile()
  }
  await teacherStore.loadModules()
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