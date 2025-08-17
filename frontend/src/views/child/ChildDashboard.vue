<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Today's Goals Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Today's Goals 🎯</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ProgressCard
          v-for="goal in todaysGoals"
          :key="goal.id"
          :title="goal.title"
          :current="goal.current"
          :total="goal.total"
          :icon="goal.icon"
          :color-scheme="(goal.colorScheme as 'blue' | 'green' | 'purple' | 'orange') || 'blue'"
          @click="handleGoalClick(goal.id)"
          class="cursor-pointer hover:scale-105 transition-transform focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 rounded-lg"
          role="button"
          :aria-label="`View ${goal.title} progress: ${goal.current} of ${goal.total} completed`"
          tabindex="0"
          @keydown.enter="handleGoalClick(goal.id)"
          @keydown.space.prevent="handleGoalClick(goal.id)"
        />
      </div>
    </div>

    <!-- Assigned Tasks Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Assigned Tasks ✅</h2>
      <div v-if="assignedTasks.length === 0" class="text-gray-500">No tasks assigned yet.</div>
      <div v-else class="space-y-3">
        <div
          v-for="task in assignedTasks"
          :key="task.id"
          class="bg-white rounded-lg p-4 shadow flex items-center justify-between"
        >
          <div class="flex items-center gap-3">
            <input
              type="checkbox"
              :checked="task.status === 'completed' || task.status === 'approved'"
              :disabled="task.status === 'completed' || task.status === 'approved'"
              @change="() => markTaskCompleted(task.id)"
              class="h-5 w-5"
              :aria-label="`Mark ${task.title} as completed`"
            />
            <div>
              <div class="font-semibold text-gray-800">{{ task.title }}</div>
              <div class="text-sm text-gray-500">
                {{ task.description || 'No description' }}
              </div>
              <div class="text-xs text-gray-400 mt-1">
                Reward: {{ task.coins_reward }} coins
                <span v-if="task.due_date"> • Due: {{ new Date(task.due_date).toLocaleDateString() }}</span>
              </div>
            </div>
          </div>
          <div>
            <span
              class="px-2 py-1 rounded text-xs"
              :class="{
                'bg-yellow-100 text-yellow-800': task.status === 'pending',
                'bg-blue-100 text-blue-800': task.status === 'in_progress',
                'bg-green-100 text-green-800': task.status === 'completed',
                'bg-emerald-100 text-emerald-800': task.status === 'approved'
              }"
            >
              {{ task.status === 'approved' ? 'Approved' : task.status === 'completed' ? 'Awaiting Approval' : task.status.replace('_', ' ') }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Teacher-Assigned Modules Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">📚 Teacher-Assigned Modules</h2>
      <div v-if="isLoadingModules" class="text-center py-8 bg-white rounded-xl shadow-sm">
        <i class="ri-book-line text-4xl text-gray-300 mb-4"></i>
        <p class="text-gray-500">Loading modules...</p>
      </div>
      <div v-else-if="assignedModules.length === 0" class="text-center py-8 bg-white rounded-xl shadow-sm">
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

            <!-- Progress Bar -->
            <div class="mb-3">
              <div class="flex justify-between text-xs text-gray-500 mb-1">
                <span>Progress</span>
                <span>{{ module.progress || 0 }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${module.progress || 0}%` }"
                ></div>
              </div>
            </div>

            <!-- Action Button -->
            <button 
              class="w-full py-2 px-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors text-sm font-medium"
              @click.stop="startAssignedModule(module)"
            >
              <i class="ri-play-circle-line mr-1"></i>
              {{ module.progress > 0 ? 'Continue' : 'Start' }} Module
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Choose Your Adventure Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Choose Your Adventure! 🚀</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AdventureCard
          v-for="adventure in adventures"
          :key="adventure.id"
          :title="adventure.title"
          :description="adventure.description"
          :emoji="adventure.emoji"
          :difficulty="adventure.difficulty"
          :coins="adventure.coins"
          :completed="adventure.completed"
          :color-scheme="adventure.colorScheme"
          :button-text="getAdventureButtonText(adventure)"
          @click="handleAdventureClick(adventure)"
          :class="getAdventureCardClasses(adventure)"
          role="button"
          :aria-label="`${adventure.completed ? 'Replay' : 'Start'} ${adventure.title} adventure. Difficulty: ${adventure.difficulty}. Reward: ${adventure.coins} coins`"
          :tabindex="adventure.completed && !allowReplay ? -1 : 0"
          @keydown.enter="handleAdventureClick(adventure)"
          @keydown.space.prevent="handleAdventureClick(adventure)"
        />
      </div>
    </div>

    <!-- Recent Achievements Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Recent Achievements 🏆</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AchievementCard
          v-for="achievement in achievements"
          :key="achievement.id"
          :title="achievement.title"
          :description="achievement.description"
          :icon="achievement.icon"
          :badge="achievement.badge"
          :coins="achievement.coins"
          :date="achievement.date"
          :color-scheme="achievement.colorScheme"
          @click="handleAchievementClick(achievement.id)"
          class="cursor-pointer hover:scale-105 transition-transform focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 rounded-lg"
          role="button"
          :aria-label="`View ${achievement.title} achievement details. Earned ${achievement.coins} coins on ${achievement.date}`"
          tabindex="0"
          @keydown.enter="handleAchievementClick(achievement.id)"
          @keydown.space.prevent="handleAchievementClick(achievement.id)"
        />
      </div>
    </div>

    <!-- Your Learning Journey Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Your Learning Journey 📚</h2>
      <div class="space-y-3">
        <JourneyCard
          v-for="journey in learningJourney"
          :key="journey.id"
          :title="journey.title"
          :description="journey.description"
          :status="journey.status"
          :icon="journey.icon"
          @click="handleJourneyClick(journey)"
          :class="getJourneyCardClasses(journey)"
          role="button"
          :aria-label="`${getJourneyActionText(journey.status)} ${journey.title}. Status: ${journey.status}`"
          :tabindex="journey.status === 'locked' ? -1 : 0"
          @keydown.enter="handleJourneyClick(journey)"
          @keydown.space.prevent="handleJourneyClick(journey)"
        />
      </div>
    </div>

    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 flex items-center gap-3">
        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-500"></div>
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
          class="ml-2 text-white hover:text-gray-200"
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
          class="ml-2 text-white hover:text-gray-200"
          aria-label="Dismiss success message"
        >
          <i class="ri-close-line" aria-hidden="true"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- Piggy Bank Adventure Modal -->
  <PiggyBankAdventure
    v-model="showPiggyBankModal"
    :coins="10"
    @completed="handlePiggyBankCompleted"
  />
  
  <!-- Debug Modal State (remove this in production) -->
  <div v-if="showPiggyBankModal" class="fixed top-4 right-4 bg-red-500 text-white p-2 rounded z-50">
    Modal is OPEN! State: {{ showPiggyBankModal }}
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboard'
import { useChildStore } from '@/stores/child'
import { useUserStore } from '@/stores/user'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import PiggyBankAdventure from '@/components/explore/PiggyBankAdventure.vue'
import ProgressCard from '@/components/shared/ProgressCard.vue'
import AchievementCard from '@/components/shared/AchievementCard.vue'
import JourneyCard from '@/components/shared/JourneyCard.vue'
import apiService from '@/services/api'

// Stores and router
const router = useRouter()
const dashboardStore = useDashboardStore()
const childStore = useChildStore()
const userStore = useUserStore()

// State
const showPiggyBankModal = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const showErrorToast = ref(false)
const showSuccessToast = ref(false)
const errorTimer = ref<NodeJS.Timeout | null>(null)
const successTimer = ref<NodeJS.Timeout | null>(null)
const allowReplay = ref(false)

// Teacher modules state
const assignedModules = ref<any[]>([])
const isLoadingModules = ref(false)

// Debug modal state changes
watch(showPiggyBankModal, (newVal) => {
  console.log('🐷 [CHILD] Modal state changed to:', newVal)
})
// Assigned tasks from child store
const assignedTasks = computed(() => childStore.tasks)

const markTaskCompleted = async (taskId: string) => {
  try {
    await childStore.completeTask(taskId)
    showSuccess('Task marked as completed! Awaiting parent approval.')
  } catch (e) {
    showError('Failed to mark task completed')
  }
}


// Use dashboard store data
const todaysGoals = computed(() => {
  // Combine old dashboard store and new child store goals
  const dashboardGoals = dashboardStore.todaysGoals || []
  const childGoals = childStore.goals.filter(goal => !goal.is_completed).slice(0, 4).map(goal => ({
    id: goal.id,
    title: goal.title,
    current: goal.current_amount,
    total: goal.target_amount,
    icon: goal.icon || '🎯',
    colorScheme: goal.color || 'orange'
  })) || []
  
  return childGoals.length > 0 ? childGoals : dashboardGoals
})

const achievements = computed(() => {
  // Use child store achievements if available, otherwise dashboard store
  const childAchievements = childStore.achievements.map(achievement => ({
    ...achievement,
    badge: achievement.rarity,
    coins: achievement.points_reward,
    date: achievement.earned_at?.toLocaleDateString(),
    colorScheme: achievement.rarity === 'legendary' ? 'gold' : 
                 achievement.rarity === 'epic' ? 'purple' : 
                 achievement.rarity === 'rare' ? 'blue' : 'green'
  })) || []
  
  return childAchievements.length > 0 ? childAchievements : dashboardStore.recentAchievements
})

// Adventures Data - converted to use activities from store
const adventures = ref([
  {
    id: '1',
    title: 'Piggy Bank Adventure',
    description: 'Learn how to save money with your digital piggy bank!',
    emoji: '🐷',
    difficulty: 'easy' as const,
    coins: 10,
    completed: false,
    colorScheme: 'pink' as const,
    buttonText: 'Start Saving!'
  },
  {
    id: '2',
    title: 'Needs vs Wants Game',
    description: 'Discover the difference between things you need and want.',
    emoji: '🤔',
    difficulty: 'easy' as const,
    coins: 15,
    completed: true,
    colorScheme: 'teal' as const,
    buttonText: 'Play Again'
  },
  {
    id: '3',
    title: 'Coin Counting Challenge',
    description: 'Practice counting coins and making change!',
    emoji: '🪙',
    difficulty: 'medium' as const,
    coins: 20,
    completed: false,
    colorScheme: 'blue' as const,
    buttonText: 'Start Challenge'
  },
  {
    id: '4',
    title: 'Budget Builder',
    description: 'Create your first budget and learn to plan ahead.',
    emoji: '📊',
    difficulty: 'medium' as const,
    coins: 25,
    completed: false,
    colorScheme: 'green' as const,
    buttonText: 'Build Budget'
  },
  {
    id: '5',
    title: 'Shopping Smart',
    description: 'Learn smart shopping tips and compare prices.',
    emoji: '🛒',
    difficulty: 'hard' as const,
    coins: 30,
    completed: false,
    colorScheme: 'yellow' as const,
    buttonText: 'Shop Smart'
  },
  {
    id: '6',
    title: 'Goal Setting Quest',
    description: 'Set and achieve your financial goals step by step.',
    emoji: '🎯',
    difficulty: 'hard' as const,
    coins: 35,
    completed: false,
    colorScheme: 'purple' as const,
    buttonText: 'Set Goals'
  }
])

// Learning Journey Data
const learningJourney = ref([
  {
    id: '1',
    title: 'Money Basics',
    description: 'Learn what money is and why we use it',
    status: 'completed' as const,
    icon: 'ri-money-dollar-circle-line'
  },
  {
    id: '2',
    title: 'Counting Coins',
    description: 'Practice identifying and counting different coins',
    status: 'completed' as const,
    icon: 'ri-coins-line'
  },
  {
    id: '3',
    title: 'Saving Strategies',
    description: 'Discover fun ways to save your money',
    status: 'current' as const,
    icon: 'ri-safe-line'
  },
  {
    id: '4',
    title: 'Spending Wisely',
    description: 'Learn how to make smart spending choices',
    status: 'locked' as const,
    icon: 'ri-shopping-cart-line'
  },
  {
    id: '5',
    title: 'Setting Goals',
    description: 'Create and work towards your money goals',
    status: 'locked' as const,
    icon: 'ri-flag-line'
  }
])

// Computed properties for button states
const getAdventureButtonText = (adventure: any) => {
  if (adventure.completed) {
    return allowReplay.value ? 'Play Again' : 'Completed'
  }
  return adventure.buttonText || 'Start Adventure'
}

const getAdventureCardClasses = (adventure: any) => {
  const baseClasses = 'cursor-pointer transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 rounded-lg'
  
  if (adventure.completed && !allowReplay.value) {
    return `${baseClasses} opacity-75 cursor-not-allowed`
  }
  
  return `${baseClasses} hover:scale-105 hover:shadow-lg`
}

const getJourneyCardClasses = (journey: any) => {
  const baseClasses = 'transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 rounded-lg'
  
  if (journey.status === 'locked') {
    return `${baseClasses} opacity-50 cursor-not-allowed`
  }
  
  return `${baseClasses} cursor-pointer hover:scale-105 hover:shadow-lg`
}

const getJourneyActionText = (status: string) => {
  switch (status) {
    case 'completed': return 'Review'
    case 'current': return 'Continue'
    case 'locked': return 'Locked'
    default: return 'Start'
  }
}

// Event handlers with comprehensive error handling
const handleGoalClick = async (goalId: string) => {
  try {
    await router.push({
      path: '/child/goals',
      query: { highlight: goalId }
    })
    
    showSuccess('Goal details loaded successfully!')
  } catch (error) {
    console.error('Goal navigation failed:', error)
    showError('Unable to load goal details. Please try again.')
  }
}

const handleAdventureClick = async (adventure: any) => {
  try {
    console.log('🎮 [CHILD] Adventure clicked:', adventure)
    
    if (adventure.completed && !allowReplay.value) {
      showError('This adventure is already completed!')
      return
    }
    
    if (adventure.id === '1') {
      console.log('🐷 [CHILD] Piggy Bank Adventure clicked, showing modal...')
      // Show Piggy Bank Adventure modal
      showPiggyBankModal.value = true
      console.log('🐷 [CHILD] Modal state set to:', showPiggyBankModal.value)
      return
    }
    
    console.log('🎮 [CHILD] Other adventure clicked, navigating to games...')
    // Update adventure progress in store
    await dashboardStore.completeActivity(adventure.id)
    
    await router.push({
      path: `/child/games/${adventure.id}`
    })
    
    showSuccess(`${adventure.title} started successfully!`)
  } catch (error) {
    console.error('❌ [CHILD] Adventure start failed:', error)
    showError(`Unable to start ${adventure.title}. Please try again.`)
  }
}

const handleAchievementClick = async (_achievementId: string) => {
  try {
    // For now, just show success - could open modal or navigate
    showSuccess('Achievement details loaded!')
    
    // Future: Open achievement detail modal
    // openAchievementModal(achievementId)
  } catch (error) {
    console.error('Achievement click failed:', error)
    showError('Unable to load achievement details.')
  }
}

const handleJourneyClick = async (journey: any) => {
  try {
    if (journey.status === 'locked') {
      showError('This lesson is locked. Complete previous lessons first!')
      return
    }
    
    // Navigate to specific lesson or activity
    await router.push({
      path: '/child/games',
      query: { lesson: journey.id, type: 'journey' }
    })
    
    showSuccess(`${journey.title} loaded successfully!`)
  } catch (error) {
    console.error('Journey navigation failed:', error)
    showError(`Unable to load ${journey.title}. Please try again.`)
  }
}

const handlePiggyBankCompleted = async (coins: number) => {
  try {
    console.log('🎉 [CHILD] Piggy Bank Adventure completed! Coins earned:', coins)
    
    // Close the modal
    showPiggyBankModal.value = false
    
    // Refresh user coins to show updated balance
    await userStore.refreshCoins()
    
  } catch (error) {
    console.error('Failed to handle piggy bank completion:', error)
    showError('Failed to complete the adventure. Please try again.')
  }
}

// Teacher module methods
const startAssignedModule = (module: any) => {
  console.log('🚀 [CHILD] Starting assigned module:', module.title)
  // TODO: Implement module execution
  alert(`Starting module: ${module.title}`)
}

const getModuleDifficultyClass = (difficulty: string) => {
  switch (difficulty) {
    case 'beginner': return 'bg-green-100 text-green-700'
    case 'intermediate': return 'bg-yellow-100 text-yellow-700'
    case 'advanced': return 'bg-red-100 text-red-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

const formatModuleDate = (date: Date) => {
  if (!date) return 'Recently'
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// Utility functions
const showError = (message: string) => {
  errorMessage.value = message
  showErrorToast.value = true
  
  // Clear any existing timer
  if (errorTimer) {
    clearTimeout(errorTimer)
  }
  
  // Auto-dismiss after 5 seconds
  errorTimer = setTimeout(() => {
    dismissError()
  }, 5000)
}

const showSuccess = (message: string) => {
  successMessage.value = message
  showSuccessToast.value = true
  
  // Clear any existing timer
  if (successTimer) {
    clearTimeout(successTimer)
  }
  
  // Auto-dismiss after 3 seconds
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

// Keyboard navigation support
const handleKeyboardNavigation = (event: KeyboardEvent) => {
  // Handle global keyboard shortcuts if needed
  if (event.key === 'Escape') {
    dismissError()
    dismissSuccess()
  }
}

// Lifecycle hooks
onMounted(async () => {
  document.addEventListener('keydown', handleKeyboardNavigation)
  
  // Load child dashboard data
  try {
    await Promise.all([
      childStore.loadDashboard(),
      childStore.loadTasks()
    ])
    console.log('✅ [CHILD] Dashboard and tasks loaded successfully')
  } catch (error) {
    console.error('❌ [CHILD] Failed to load dashboard or tasks:', error)
  }
  
  // Also load dashboard store data for backwards compatibility
  if (!dashboardStore.todaysGoals.length) {
    dashboardStore.loadDashboardData('younger_child')
  }

  // Load assigned modules
  loadAssignedModules()
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardNavigation)
  
  // Clean up timers
  if (errorTimer) clearTimeout(errorTimer)
  if (successTimer) clearTimeout(successTimer)
})

// Methods
const loadAssignedModules = async () => {
  try {
    isLoadingModules.value = true
    const response = await apiService.getAssignedModules()
    
    if (response.data) {
      assignedModules.value = response.data
      console.log('✅ [CHILD] Loaded assigned modules:', assignedModules.value.length)
    } else {
      console.error('❌ [CHILD] Failed to load assigned modules:', response.error)
      assignedModules.value = []
    }
  } catch (error) {
    console.error('❌ [CHILD] Error loading assigned modules:', error)
    assignedModules.value = []
  } finally {
    isLoadingModules.value = false
  }
}
</script>

<style scoped>
/* Enhanced focus styles for accessibility */
.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(251, 146, 60, 0.5);
}

.focus\:ring-offset-2:focus {
  box-shadow: 0 0 0 2px white, 0 0 0 4px rgba(251, 146, 60, 0.5);
}

/* Smooth transitions for all interactive elements */
.transition-all {
  transition: all 0.2s ease-in-out;
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
    box-shadow: 0 0 0 3px rgba(251, 146, 60, 1);
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .transition-all,
  .transform,
  .hover\:scale-105:hover {
    transition: none;
    transform: none;
  }
  
  .animate-spin {
    animation: none;
  }
}
</style>