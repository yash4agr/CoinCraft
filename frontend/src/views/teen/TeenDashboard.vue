<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Welcome Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">
        Welcome back, {{ userStore.profile?.fullName?.split(' ')[0] }}! 👋
      </h1>
      <p class="text-gray-600">Here's your financial overview for today</p>
    </div>

    <!-- Budget Overview Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Budget Overview 📊</h2>
      <div 
        class="bg-white rounded-2xl p-6 shadow-sm cursor-pointer hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        @click="handleBudgetOverviewClick"
        role="button"
        aria-label="View detailed budget breakdown and management options"
        tabindex="0"
        @keydown.enter="handleBudgetOverviewClick"
        @keydown.space.prevent="handleBudgetOverviewClick"
      >
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Pie Chart Placeholder -->
          <div class="flex items-center justify-center">
            <div class="relative w-48 h-48">
              <svg class="w-48 h-48 transform -rotate-90" viewBox="0 0 100 100" aria-hidden="true">
                <!-- Saving slice (40%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" stroke-width="20" 
                        stroke-dasharray="100 150" stroke-dashoffset="0" />
                <!-- Spending slice (35%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#3b82f6" stroke-width="20" 
                        stroke-dasharray="87.5 162.5" stroke-dashoffset="-100" />
                <!-- Wants slice (25%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#f59e0b" stroke-width="20" 
                        stroke-dasharray="62.5 187.5" stroke-dashoffset="-187.5" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-2xl font-bold text-gray-800">{{ userStore.totalCoins }}</div>
                  <div class="text-sm text-gray-600">Total Coins</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Budget Breakdown -->
          <div class="space-y-4">
            <div 
              class="flex items-center justify-between p-3 bg-green-50 rounded-lg cursor-pointer hover:bg-green-100 transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
              @click="handleBudgetCategoryClick('saving')"
              role="button"
              aria-label="View saving category details: 40% of budget"
              tabindex="0"
              @keydown.enter="handleBudgetCategoryClick('saving')"
              @keydown.space.prevent="handleBudgetCategoryClick('saving')"
            >
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-green-500 rounded-full" aria-hidden="true"></div>
                <span class="font-medium text-gray-800">Saving</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-green-600">{{ Math.floor(userStore.totalCoins * 0.4) }} coins</div>
                <div class="text-sm text-green-500">40%</div>
              </div>
            </div>
            
            <div 
              class="flex items-center justify-between p-3 bg-blue-50 rounded-lg cursor-pointer hover:bg-blue-100 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              @click="handleBudgetCategoryClick('spending')"
              role="button"
              aria-label="View spending category details: 35% of budget"
              tabindex="0"
              @keydown.enter="handleBudgetCategoryClick('spending')"
              @keydown.space.prevent="handleBudgetCategoryClick('spending')"
            >
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-blue-500 rounded-full" aria-hidden="true"></div>
                <span class="font-medium text-gray-800">Spending</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-blue-600">{{ Math.floor(userStore.totalCoins * 0.35) }} coins</div>
                <div class="text-sm text-blue-500">35%</div>
              </div>
            </div>
            
            <div 
              class="flex items-center justify-between p-3 bg-yellow-50 rounded-lg cursor-pointer hover:bg-yellow-100 transition-colors focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2"
              @click="handleBudgetCategoryClick('wants')"
              role="button"
              aria-label="View wants category details: 25% of budget"
              tabindex="0"
              @keydown.enter="handleBudgetCategoryClick('wants')"
              @keydown.space.prevent="handleBudgetCategoryClick('wants')"
            >
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-yellow-500 rounded-full" aria-hidden="true"></div>
                <span class="font-medium text-gray-800">Wants</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-yellow-600">{{ Math.floor(userStore.totalCoins * 0.25) }} coins</div>
                <div class="text-sm text-yellow-500">25%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Teacher-Assigned Modules Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">📚 Teacher-Assigned Modules</h2>
      <div v-if="assignedModules.length === 0" class="text-center py-8 bg-white rounded-xl shadow-sm">
        <i class="ri-book-line text-4xl text-gray-300 mb-4"></i>
        <p class="text-gray-500">No modules assigned by your teacher yet.</p>
        <p class="text-sm text-gray-400 mt-1">Check back later for new assignments!</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="module in assignedModules"
          :key="module.id"
          class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow cursor-pointer"
          @click="startAssignedModule(module)"
        >
          <!-- Module Header -->
          <div class="p-4 border-b border-gray-100">
            <div class="flex items-center justify-between mb-2">
              <h3 class="font-semibold text-gray-800 line-clamp-1">{{ module.title }}</h3>
              <span 
                class="px-2 py-1 rounded-full text-xs font-medium"
                :class="getModuleDifficultyClass(module.difficulty)"
              >
                {{ module.difficulty }}
              </span>
            </div>
            <p class="text-sm text-gray-600 line-clamp-2">{{ module.description }}</p>
          </div>

          <!-- Module Stats -->
          <div class="p-4">
            <div class="flex items-center justify-between text-sm text-gray-500 mb-3">
              <span class="flex items-center gap-1">
                <i class="ri-time-line"></i>
                {{ module.duration }} min
              </span>
              <span class="flex items-center gap-1">
                <i class="ri-calendar-line"></i>
                {{ formatModuleDate(module.assigned_at) }}
              </span>
            </div>

            <!-- Action Button -->
            <button 
              class="w-full py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm font-medium"
              @click.stop="startAssignedModule(module)"
            >
              <i class="ri-play-circle-line mr-1"></i>
              Start Module
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Module Execution Modal -->
    <ModuleExecutionModal
      :show-modal="showModuleExecutionModal"
      :current-module="currentModule"
      @close="showModuleExecutionModal = false"
      @module-completed="handleModuleCompleted"
    />

    <!-- Quick Actions -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Quick Actions 🚀</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div 
          v-for="action in dashboardStore.quickActions"
          :key="action.id"
          class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-all duration-200 cursor-pointer focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          @click="handleQuickActionClick(action)"
          role="button"
          :aria-label="`Navigate to ${action.title}: ${action.description}`"
          tabindex="0"
          @keydown.enter="handleQuickActionClick(action)"
          @keydown.space.prevent="handleQuickActionClick(action)"
        >
          <div class="text-center">
            <div 
              class="w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3"
              :class="action.iconBg"
              aria-hidden="true"
            >
              <i :class="`${action.icon} text-2xl`" :style="{ color: action.iconColor }"></i>
            </div>
            <h3 class="font-semibold text-gray-800">{{ action.title }}</h3>
            <p class="text-xs text-gray-600 mt-1">{{ action.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Current Goals Progress -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Current Goals 🎯</h2>
        <button
          @click="handleViewAllGoalsClick"
          class="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded px-2 py-1"
          aria-label="View all goals"
        >
          View All Goals
        </button>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="goal in displayedGoals" 
          :key="goal.id"
          class="bg-white rounded-xl p-6 shadow-sm cursor-pointer hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          @click="handleGoalClick(goal)"
          role="button"
          :aria-label="`View ${goal.title} goal details. ${Math.round((goal.currentAmount / goal.targetAmount) * 100)}% complete`"
          tabindex="0"
          @keydown.enter="handleGoalClick(goal)"
          @keydown.space.prevent="handleGoalClick(goal)"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">
              <i :class="goal.icon" class="mr-2" aria-hidden="true"></i>
              {{ goal.title }}
            </h3>
            <span class="text-sm text-blue-600 font-medium">
              {{ Math.round((goal.currentAmount / goal.targetAmount) * 100) }}% complete
            </span>
          </div>
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{{ goal.currentAmount }}/{{ goal.targetAmount }} coins</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div 
                class="bg-blue-500 h-3 rounded-full transition-all duration-500" 
                :style="{ width: Math.min((goal.currentAmount / goal.targetAmount) * 100, 100) + '%' }"
                :aria-label="`${Math.round((goal.currentAmount / goal.targetAmount) * 100)}% progress`"
              ></div>
            </div>
          </div>
          <p class="text-sm text-gray-600">{{ goal.description }}</p>
        </div>
      </div>
      
      <!-- Empty state for goals -->
      <div v-if="displayedGoals.length === 0" class="text-center py-8">
        <div class="text-4xl mb-4">🎯</div>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">No active goals</h3>
        <p class="text-gray-500 mb-4">Create your first goal to start tracking your progress!</p>
        <button
          @click="handleCreateGoalClick"
          class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Create Your First Goal
        </button>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Recent Activities 📈</h2>
        <button
          @click="handleViewAllActivitiesClick"
          class="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded px-2 py-1"
          aria-label="View all activities"
        >
          View All
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm">
        <div 
          v-for="(transaction, index) in displayedTransactions" 
          :key="transaction.id"
          class="p-4 cursor-pointer hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
          :class="{ 'border-b border-gray-100': index < displayedTransactions.length - 1 }"
          @click="handleTransactionClick(_transaction)"
          role="button"
          :aria-label="`View ${transaction.description} transaction details. Amount: ${transaction.type === 'spend' ? '-' : '+'}${transaction.amount} coins`"
          tabindex="0"
          @keydown.enter="handleTransactionClick(_transaction)"
          @keydown.space.prevent="handleTransactionClick(_transaction)"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :class="{
                  'bg-green-100': transaction.type === 'earn',
                  'bg-blue-100': transaction.type === 'save',
                  'bg-red-100': transaction.type === 'spend'
                }"
                aria-hidden="true"
              >
                <i 
                  :class="{
                    'ri-arrow-up-line text-green-600': transaction.type === 'earn',
                    'ri-target-line text-blue-600': transaction.type === 'save',
                    'ri-arrow-down-line text-red-600': transaction.type === 'spend'
                  }"
                ></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                <div class="text-sm text-gray-500">{{ formatDate(transaction.timestamp) }}</div>
              </div>
            </div>
            <div 
              class="font-semibold"
              :class="{
                'text-green-600': transaction.type === 'earn',
                'text-blue-600': transaction.type === 'save',
                'text-red-600': transaction.type === 'spend'
              }"
            >
              {{ transaction.type === 'spend' ? '-' : '+' }}{{ transaction.amount }} coins
            </div>
          </div>
        </div>
        
        <!-- Empty state for transactions -->
        <div v-if="displayedTransactions.length === 0" class="text-center py-8">
          <div class="text-4xl mb-4">📊</div>
          <h3 class="text-lg font-semibold text-gray-700 mb-2">No recent activities</h3>
          <p class="text-gray-500">Your financial activities will appear here.</p>
        </div>
      </div>
    </div>

    <!-- Recent Purchases (Shop Transactions) -->
    <div class="mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-800">All Shop Purchases 🛍️</h2>
        <button
          @click="handleViewAllPurchasesClick"
          class="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded px-2 py-1"
          aria-label="View all purchases"
        >
          View All
        </button>
      </div>
      <div class="bg-white rounded-xl shadow-sm">
        <div v-if="isLoadingShopTransactions" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
          <p class="text-gray-600">Loading recent purchases...</p>
        </div>
        
        <div v-else-if="shopTransactions && shopTransactions.length > 0">
          <div 
            v-for="(transaction, index) in displayedShopTransactions" 
            :key="transaction.id"
            class="p-4 cursor-pointer hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-inset"
            :class="{ 'border-b border-gray-100': index < displayedShopTransactions.length - 1 }"
            @click="handleShopTransactionClick(_transaction)"
            role="button"
            :aria-label="`View ${transaction.description} purchase details. Amount: ${transaction.amount} coins`"
            tabindex="0"
            @keydown.enter="handleShopTransactionClick(_transaction)"
            @keydown.space.prevent="handleShopTransactionClick(_transaction)"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                  <i class="ri-shopping-cart-line text-red-600"></i>
                </div>
                <div>
                  <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                  <div class="text-sm text-gray-500">{{ formatDate(transaction.created_at) }}</div>
                </div>
              </div>
              <div class="font-semibold text-red-600">
                -{{ transaction.amount }} coins
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty state for shop transactions -->
        <div v-else class="text-center py-8">
          <div class="text-4xl mb-4">🛍️</div>
          <h3 class="text-lg font-semibold text-gray-700 mb-2">No shop purchases yet</h3>
          <p class="text-gray-500">Your shop purchases will appear here when you make them.</p>
        </div>
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 flex items-center gap-3">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
        <span class="text-gray-700">{{ loadingMessage }}</span>
      </div>
    </div>

    <!-- Error Toast -->
    <div 
      v-if="showErrorToast" 
      class="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform"
      :class="showErrorToast ? 'translate-x-0' : 'translate-x-full'"
      role="alert"
      aria-live="polite"
    >
      <div class="flex items-center gap-2">
        <i class="ri-error-warning-line" aria-hidden="true"></i>
        <span>{{ errorMessage }}</span>
        <button 
          @click="dismissError" 
          class="ml-2 text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-red-500 rounded"
          aria-label="Dismiss error message"
        >
          <i class="ri-close-line" aria-hidden="true"></i>
        </button>
      </div>
    </div>

    <!-- Success Toast -->
    <div 
      v-if="showSuccessToast" 
      class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform"
      :class="showSuccessToast ? 'translate-x-0' : 'translate-x-full'"
      role="alert"
      aria-live="polite"
    >
      <div class="flex items-center gap-2">
        <i class="ri-check-line" aria-hidden="true"></i>
        <span>{{ successMessage }}</span>
        <button 
          @click="dismissSuccess" 
          class="ml-2 text-white hover:text-gray-200 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-green-500 rounded"
          aria-label="Dismiss success message"
        >
          <i class="ri-close-line" aria-hidden="true"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useDashboardStore } from '@/stores/dashboard'
import apiService from '@/services/api'
import ModuleExecutionModal from '@/components/child/ModuleExecutionModal.vue'
import { formatTransactionDate } from '@/utils/dateUtils'

// Stores and router
const router = useRouter()
const userStore = useUserStore()
const dashboardStore = useDashboardStore()

// State
const isLoading = ref(false)
const loadingMessage = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const showErrorToast = ref(false)
const showSuccessToast = ref(false)
const errorTimer = ref<number | null>(null)
const successTimer = ref<number | null>(null)
const assignedModules = ref<any[]>([])
const isLoadingModules = ref(false)
const showModuleExecutionModal = ref(false)
const currentModule = ref<any>(null)
const isLoadingShopTransactions = ref(false)
const shopTransactions = ref<any[]>([])

// Computed properties
const displayedGoals = computed(() => userStore.activeGoals.slice(0, 2))
const displayedTransactions = computed(() => userStore.recentTransactions.slice(0, 3))
const displayedShopTransactions = computed(() => shopTransactions.value)

// Event handlers with comprehensive error handling
const handleBudgetOverviewClick = async () => {
  try {
    await router.push('/teen/budget')
    showSuccess('Budget page loaded successfully!')
  } catch (error) {
    console.error('Budget navigation failed:', error)
    showError('Unable to load budget page. Please try again.')
  }
}

const handleBudgetCategoryClick = async (category: string) => {
  try {
    await router.push({ 
      path: '/teen/budget', 
      query: { category } 
    })
    
    showSuccess(`${category.charAt(0).toUpperCase() + category.slice(1)} category loaded!`)
  } catch (error) {
    console.error('Budget category navigation failed:', error)
    showError(`Unable to load ${category} details. Please try again.`)
  }
}

const handleQuickActionClick = async (action: any) => {
  try {
    await router.push(action.route)
    showSuccess(`${action.title} loaded successfully!`)
  } catch (error) {
    console.error('Quick action navigation failed:', error)
    showError(`Unable to load ${action.title}. Please try again.`)
  }
}

const handleGoalClick = async (goal: any) => {
  try {
    await router.push({ 
      path: '/teen/goals', 
      query: { goalId: goal.id } 
    })
    
    showSuccess('Goal details loaded successfully!')
  } catch (error) {
    console.error('Goal navigation failed:', error)
    showError('Unable to load goal details. Please try again.')
  }
}

const handleViewAllGoalsClick = async () => {
  try {
    await router.push('/teen/goals')
    showSuccess('Goals page loaded successfully!')
  } catch (error) {
    console.error('Goals navigation failed:', error)
    showError('Unable to load goals page. Please try again.')
  }
}

const handleCreateGoalClick = async () => {
  try {
    await router.push({ 
      path: '/teen/goals', 
      query: { action: 'create' } 
    })
    
    showSuccess('Goal creation opened!')
  } catch (error) {
    console.error('Goal creation navigation failed:', error)
    showError('Unable to open goal creation. Please try again.')
  }
}

const handleTransactionClick = async (_transaction: any) => {
  try {
    // show success - could open modal or navigate to detailed view
    showSuccess('Transaction details loaded!')
    
    // Future: Open transaction detail modal or navigate to transactions page
    // openTransactionModal(transaction.id)
  } catch (error) {
    console.error('Transaction click failed:', error)
    showError('Unable to load transaction details.')
  }
}

const handleViewAllActivitiesClick = async () => {
  try {
    await router.push('/teen/activities')
    showSuccess('Activity history loaded successfully!')
  } catch (error) {
    console.error('Activities navigation failed:', error)
    showError('Unable to load activity history. Please try again.')
  }
}

const handleViewAllPurchasesClick = async () => {
  try {
    await router.push('/teen/shop')
    showSuccess('Shop history loaded successfully!')
  } catch (error) {
    console.error('Shop navigation failed:', error)
    showError('Unable to load shop history. Please try again.')
  }
}

const handleShopTransactionClick = async (_transaction: any) => {
  try {
    // show success - could open modal or navigate to detailed view
    showSuccess('Purchase details loaded!')
    
    // Future: Open purchase detail modal or navigate to shop page
    // openPurchaseModal(transaction.id)
  } catch (error) {
    console.error('Shop transaction click failed:', error)
    showError('Unable to load purchase details.')
  }
}

// Teacher module methods
const startAssignedModule = (module: any) => {
  console.log('🚀 [TEEN] Starting assigned module:', module.title)
  // Open the module execution modal
  showModuleExecutionModal.value = true
  currentModule.value = module
}

const handleModuleCompleted = (module: any, score: number) => {
  console.log('🎉 [TEEN] Module completed!', { module: module.title, score })
  
  // Show success message
  showSuccess(`Congratulations! You completed "${module.title}" with a score of ${score}%`)
  
  // Close the modal
  showModuleExecutionModal.value = false
  currentModule.value = null
  
  // Refresh assigned modules to show updated status
  loadAssignedModules()
  
  // Optionally refresh user data to show updated coins
  if (userStore.profile?.id) {
    userStore.loadUserData(userStore.profile.id)
  }
}

const getModuleDifficultyClass = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'bg-green-100 text-green-700'
    case 'intermediate': return 'bg-yellow-100 text-yellow-700'
    case 'advanced': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

const formatModuleDate = (date: any) => {
  if (!date) return 'Recently'
  
  // Ensure date is a proper Date object
  let dateObj: Date
  if (typeof date === 'string') {
    dateObj = new Date(date)
  } else if (date instanceof Date) {
    dateObj = date
  } else {
    console.warn('Invalid date format:', date)
    return 'Recently'
  }
  
  // Check if date is valid
  if (isNaN(dateObj.getTime())) {
    console.warn('Invalid date object:', date)
    return 'Recently'
  }
  
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - dateObj.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  return dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// Utility functions
// const setLoading = (loading: boolean, message = '') => {
//   isLoading.value = loading
//   loadingMessage.value = message
// }

const showError = (message: string) => {
  errorMessage.value = message
  showErrorToast.value = true
  
  if (errorTimer.value) {
    clearTimeout(errorTimer.value)
  }
  
  errorTimer.value = setTimeout(() => {
    dismissError()
  }, 5000)
}

const showSuccess = (message: string) => {
  successMessage.value = message
  showSuccessToast.value = true
  
  if (successTimer.value) {
    clearTimeout(successTimer.value)
  }
  
  successTimer.value = setTimeout(() => {
    dismissSuccess()
  }, 3000)
}

const dismissError = () => {
  showErrorToast.value = false
  if (errorTimer.value) {
    clearTimeout(errorTimer.value)
    errorTimer.value = null
  }
}

const dismissSuccess = () => {
  showSuccessToast.value = false
  if (successTimer.value) {
    clearTimeout(successTimer.value)
    successTimer.value = null
  }
}

// Use the utility function for date formatting
const formatDate = formatTransactionDate

// Methods
const loadAssignedModules = async () => {
  try {
    isLoadingModules.value = true
    const response = await apiService.getAssignedModules()
    
    if (response.data) {
      assignedModules.value = response.data
      console.log('✅ [TEEN] Loaded assigned modules:', assignedModules.value.length)
    } else {
      console.error('❌ [TEEN] Failed to load assigned modules:', response.error)
      assignedModules.value = []
    }
  } catch (error) {
    console.error('❌ [TEEN] Error loading assigned modules:', error)
    assignedModules.value = []
  } finally {
    isLoadingModules.value = false
  }
}

const loadShopTransactions = async () => {
  try {
    if (!userStore.profile?.id) {
      console.log('⚠️ [TEEN] No user profile ID available for shop transactions')
      return
    }
    
    isLoadingShopTransactions.value = true
    const response = await apiService.getShopTransactions(userStore.profile.id)
    if (response.data) {
      shopTransactions.value = response.data
      console.log('✅ [TEEN] Loaded shop transactions:', shopTransactions.value.length)
    } else {
      console.error('❌ [TEEN] Failed to load shop transactions:', response.error)
      shopTransactions.value = []
    }
  } catch (error) {
    console.error('❌ [TEEN] Error loading shop transactions:', error)
    shopTransactions.value = []
  } finally {
    isLoadingShopTransactions.value = false
  }
}

// Keyboard navigation support
const handleKeyboardNavigation = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    dismissError()
    dismissSuccess()
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('keydown', handleKeyboardNavigation)
  
  // Load initial data if needed
  if (!userStore.activeGoals.length) {
    userStore.loadUserData(userStore.profile?.id || '')
  }
  loadAssignedModules()
  loadShopTransactions()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardNavigation)
  
  // Clean up timers
  if (errorTimer.value) clearTimeout(errorTimer.value)
  if (successTimer.value) clearTimeout(successTimer.value)
})
</script>

<style scoped>
/* Enhanced focus styles for accessibility */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
}

.focus\:ring-offset-2:focus {
  box-shadow: 0 0 0 2px white, 0 0 0 4px rgba(59, 130, 246, 0.5);
}

.focus\:ring-inset:focus {
  box-shadow: inset 0 0 0 2px rgba(59, 130, 246, 0.5);
}

/* Smooth transitions for all interactive elements */
.transition-all {
  transition: all 0.2s ease-in-out;
}

.transition-colors {
  transition: color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.transition-shadow {
  transition: box-shadow 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Toast animations */
.transform {
  transition: transform 0.3s ease-in-out;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .focus\:ring-2:focus {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 1);
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .transition-all,
  .transition-colors,
  .transition-shadow,
  .transform {
    transition: none;
  }
  
  .animate-spin {
    animation: none;
  }
  
  .hover\:shadow-md:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
}

/* Ensure proper contrast for text */
.text-gray-800 {
  color: #1f2937;
}

.text-gray-600 {
  color: #4b5563;
}

.text-gray-500 {
  color: #6b7280;
}
</style>