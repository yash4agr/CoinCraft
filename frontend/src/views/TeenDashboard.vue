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

    <!-- Quick Actions -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Quick Actions 🚀</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div 
          v-for="action in quickActions"
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
          @click="handleTransactionClick(transaction)"
          role="button"
          :aria-label="`View ${transaction.description} transaction details. Amount: ${transaction.type === 'spend' ? '-' : '+'}${transaction.amount} coins`"
          tabindex="0"
          @keydown.enter="handleTransactionClick(transaction)"
          @keydown.space.prevent="handleTransactionClick(transaction)"
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

// Stores and router
const router = useRouter()
const userStore = useUserStore()
const dashboardStore = useDashboardStore()

// Reactive state
const isLoading = ref(false)
const loadingMessage = ref('')
const showErrorToast = ref(false)
const showSuccessToast = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// Auto-dismiss timers
let errorTimer: NodeJS.Timeout | null = null
let successTimer: NodeJS.Timeout | null = null

// Quick actions configuration
const quickActions = ref([
  {
    id: 'budget',
    title: 'My Budget',
    description: 'Manage your money allocation',
    icon: 'ri-pie-chart-fill',
    iconColor: '#3b82f6',
    iconBg: 'bg-blue-100',
    route: '/teen/budget'
  },
  {
    id: 'goals',
    title: 'My Goals',
    description: 'Track your savings goals',
    icon: 'ri-flag-fill',
    iconColor: '#10b981',
    iconBg: 'bg-green-100',
    route: '/teen/goals'
  },
  {
    id: 'activities',
    title: 'Activity Hub',
    description: 'Learn through activities',
    icon: 'ri-brain-fill',
    iconColor: '#8b5cf6',
    iconBg: 'bg-purple-100',
    route: '/teen/activities'
  },
  {
    id: 'explore',
    title: 'Explore',
    description: 'Discover new content',
    icon: 'ri-compass-3-fill',
    iconColor: '#f59e0b',
    iconBg: 'bg-orange-100',
    route: '/teen/explore'
  }
])

// Computed properties
const displayedGoals = computed(() => userStore.activeGoals.slice(0, 2))
const displayedTransactions = computed(() => userStore.recentTransactions.slice(0, 3))

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

const handleTransactionClick = async (transaction: any) => {
  try {
    // For now, just show success - could open modal or navigate to detailed view
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

// Utility functions
const setLoading = (loading: boolean, message = '') => {
  isLoading.value = loading
  loadingMessage.value = message
}

const showError = (message: string) => {
  errorMessage.value = message
  showErrorToast.value = true
  
  if (errorTimer) {
    clearTimeout(errorTimer)
  }
  
  errorTimer = setTimeout(() => {
    dismissError()
  }, 5000)
}

const showSuccess = (message: string) => {
  successMessage.value = message
  showSuccessToast.value = true
  
  if (successTimer) {
    clearTimeout(successTimer)
  }
  
  successTimer = setTimeout(() => {
    dismissSuccess()
  }, 3000)
}

const dismissError = () => {
  showErrorToast.value = false
  if (errorTimer) {
    clearTimeout(errorTimer)
    errorTimer = null
  }
}

const dismissSuccess = () => {
  showSuccessToast.value = false
  if (successTimer) {
    clearTimeout(successTimer)
    successTimer = null
  }
}

const formatDate = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'Just now'
  if (diffInHours < 24) return `${diffInHours} hours ago`
  if (diffInHours < 48) return 'Yesterday'
  return `${Math.floor(diffInHours / 24)} days ago`
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
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardNavigation)
  
  // Clean up timers
  if (errorTimer) clearTimeout(errorTimer)
  if (successTimer) clearTimeout(successTimer)
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