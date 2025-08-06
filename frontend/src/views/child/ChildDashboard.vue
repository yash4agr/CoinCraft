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
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '@/stores/dashboard'
import { useChildStore } from '@/stores/child'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import ProgressCard from '@/components/shared/ProgressCard.vue'
import AchievementCard from '@/components/shared/AchievementCard.vue'
import JourneyCard from '@/components/shared/JourneyCard.vue'

// Stores and router
const router = useRouter()
const dashboardStore = useDashboardStore()
const childStore = useChildStore()

// Reactive state
const isLoading = ref(false)
const loadingMessage = ref('')
const showErrorToast = ref(false)
const showSuccessToast = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const allowReplay = ref(true)

// Auto-dismiss timers
// Timer type for cleanup
let errorTimer: ReturnType<typeof setTimeout> | null = null
let successTimer: ReturnType<typeof setTimeout> | null = null

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
    if (adventure.completed && !allowReplay.value) {
      showError('This adventure is already completed!')
      return
    }
    
    // Update adventure progress in store
    await dashboardStore.completeActivity(adventure.id)
    
    await router.push({
      path: `/child/games/${adventure.id}`
    })
    
    showSuccess(`${adventure.title} started successfully!`)
  } catch (error) {
    console.error('Adventure start failed:', error)
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
    await childStore.loadDashboard()
    console.log('✅ [CHILD] Dashboard loaded successfully')
  } catch (error) {
    console.error('❌ [CHILD] Failed to load dashboard:', error)
  }
  
  // Also load dashboard store data for backwards compatibility
  if (!dashboardStore.todaysGoals.length) {
    dashboardStore.loadDashboardData('younger_child')
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