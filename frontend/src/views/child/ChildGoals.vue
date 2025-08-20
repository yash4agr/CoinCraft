<template>
  <div class="min-h-screen bg-gradient-to-br from-green-100 via-emerald-50 to-teal-100">
    <!-- Main Content Container - Centered on Desktop -->
    <div class="max-w-4xl mx-auto p-4 pt-20 pb-24 lg:pt-24 lg:pb-8">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-target-fill text-green-500 mr-3"></i>
          My Goals
        </h1>
        <p class="text-gray-600 text-lg">Set goals and save up for something special!</p>
      </div>

      <!-- Current Goals List -->
      <div class="space-y-6 mb-8">
        <!-- Active Goals -->
        <div 
          v-for="goal in userStore.activeGoals" 
          :key="goal.id"
          class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-4">
              <div class="text-4xl">{{ getGoalEmoji(goal.icon) }}</div>
              <div>
                <h3 class="text-xl font-semibold text-gray-800">{{ goal.title }}</h3>
                <p class="text-gray-600">{{ goal.description }}</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-green-500 flex items-center gap-1">
                <img src="/coin.svg" class="coin-icon" alt="coin">
                <span>{{ goal.current_amount }} / {{ goal.target_amount }}</span>
              </div>
              <div class="text-sm text-gray-500">{{ getProgressPercentage(goal) }}% complete</div>
            </div>
          </div>
          
          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div 
              class="bg-green-500 h-3 rounded-full transition-all duration-500" 
              :style="{ width: getProgressPercentage(goal) + '%' }"
            ></div>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex gap-3">
            <button 
              @click="showAddCoinsModal(goal)"
              :disabled="userStore.totalCoins === 0"
              class="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-4 py-2 rounded-full transition-colors font-medium"
            >
              <i class="ri-add-line mr-1"></i>Add Coins
            </button>
            <button 
              @click="showEditGoalModal(goal)"
              class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-full transition-colors font-medium"
            >
              <i class="ri-edit-line mr-1"></i>Edit Goal
            </button>
            <button 
              @click="markCompleted(goal)"
              class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-full transition-colors font-medium"
            >
              <i class="ri-check-double-line mr-1"></i>Mark Completed
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="userStore.activeGoals.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4">🎯</div>
          <h3 class="text-xl font-semibold text-gray-700 mb-2">No goals yet!</h3>
          <p class="text-gray-500 mb-6">Create your first goal to start saving for something special.</p>
          <button 
            @click="showCreateGoalModal"
            class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-full font-medium transition-colors"
          >
            <i class="ri-add-line mr-2"></i>Create My First Goal
          </button>
        </div>
      </div>

      <!-- Add New Goal Button (when goals exist) -->
      <div v-if="userStore.activeGoals.length > 0" class="mb-8">
        <div class="bg-white rounded-xl shadow-md p-6 border-2 border-dashed border-gray-300 text-center hover:border-green-400 transition-colors">
          <div class="text-gray-400 mb-4">
            <i class="ri-add-circle-line text-4xl"></i>
          </div>
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Add New Goal</h3>
          <button 
            @click="showCreateGoalModal"
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-full transition-colors font-medium"
          >
            <i class="ri-add-line mr-2"></i>Create Goal
          </button>
        </div>
      </div>

      <!-- Completed Goals -->
      <div v-if="userStore.completedGoals.length > 0" class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">🏆 Completed Goals</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="goal in userStore.completedGoals" 
            :key="goal.id"
            class="bg-green-50 rounded-xl p-4 border border-green-200"
          >
            <div class="flex items-center gap-3">
              <div class="text-2xl">{{ getGoalEmoji(goal.icon) }}</div>
              <div>
                <h4 class="font-semibold text-green-800">{{ goal.title }}</h4>
                <p class="text-sm text-green-600">Completed! 🎉</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Coins Modal -->
    <div v-if="showAddCoinsModalFlag" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">{{ getGoalEmoji(selectedGoal?.icon) }}</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Add Coins to Goal</h3>
          <p class="text-gray-600">{{ selectedGoal?.title }}</p>
        </div>

        <div class="mb-6">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>Your coins:</span>
            <span class="font-medium flex items-center gap-1">
              <img src="/coin.svg" class="coin-icon-sm" alt="coin">
              {{ userStore.totalCoins }}
            </span>
          </div>
          <div class="flex justify-between text-sm text-gray-600 mb-4">
            <span>Goal progress:</span>
            <span class="font-medium">{{ selectedGoal?.current_amount }}/{{ selectedGoal?.target_amount }}</span>
          </div>

          <label class="block text-sm font-medium text-gray-700 mb-2">
            How many coins to add?
          </label>
          <input 
            v-model.number="coinsToAdd"
            type="number" 
            :min="1" 
            :max="Math.min(userStore.totalCoins, (selectedGoal?.target_amount || 0) - (selectedGoal?.current_amount || 0))"
            class="w-full p-3 border border-gray-300 rounded-lg text-center text-lg font-semibold"
            placeholder="0"
          />
          
          <!-- Quick Amount Buttons -->
          <div class="grid grid-cols-4 gap-2 mt-3">
            <button 
              v-for="amount in getQuickAmounts()"
              :key="amount"
              @click="coinsToAdd = amount"
              :disabled="amount > Math.min(userStore.totalCoins, (selectedGoal?.target_amount || 0) - (selectedGoal?.current_amount || 0))"
              class="py-2 px-3 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 rounded-lg text-sm font-medium transition-colors"
            >
              {{ amount }}
            </button>
          </div>
        </div>

        <div class="flex gap-3">
          <button 
            @click="closeAddCoinsModal"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="addCoinsToGoal"
            :disabled="!coinsToAdd || coinsToAdd > userStore.totalCoins || coinsToAdd <= 0"
            class="flex-1 py-3 px-4 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Add Coins
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Goal Modal -->
    <div v-if="showEditGoalModalFlag" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <h3 class="text-xl font-bold text-gray-800 mb-2">Edit Goal</h3>
        </div>

        <div class="space-y-4 mb-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Goal Name</label>
            <input 
              v-model="editGoalForm.title"
              type="text" 
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="What do you want to save for?"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <input 
              v-model="editGoalForm.description"
              type="text" 
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="Tell us more about it"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Target Amount (coins)</label>
            <input 
              v-model.number="editGoalForm.targetAmount"
              type="number" 
              min="1"
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="How many coins do you need?"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Choose an Icon</label>
            <div class="grid grid-cols-6 gap-2">
              <button 
                v-for="icon in goalIcons"
                :key="icon.value"
                @click="editGoalForm.icon = icon.value"
                class="p-3 rounded-lg border-2 transition-colors text-2xl"
                :class="editGoalForm.icon === icon.value ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
              >
                {{ icon.emoji }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex gap-3">
          <button 
            @click="closeEditGoalModal"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="updateGoal"
            :disabled="!editGoalForm.title || !editGoalForm.targetAmount || editGoalForm.targetAmount <= 0"
            class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>

    <!-- Create Goal Modal -->
    <div v-if="showCreateGoalModalFlag" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">🎯</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Create New Goal</h3>
          <p class="text-gray-600">What do you want to save for?</p>
        </div>

        <div class="space-y-4 mb-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Goal Name</label>
            <input 
              v-model="createGoalForm.title"
              type="text" 
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="e.g., New Toy, Video Game"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <input 
              v-model="createGoalForm.description"
              type="text" 
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="Tell us more about it"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Target Amount (coins)</label>
            <input 
              v-model.number="createGoalForm.targetAmount"
              type="number" 
              min="1"
              class="w-full p-3 border border-gray-300 rounded-lg"
              placeholder="How many coins do you need?"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Choose an Icon</label>
            <div class="grid grid-cols-6 gap-2">
              <button 
                v-for="icon in goalIcons"
                :key="icon.value"
                @click="createGoalForm.icon = icon.value"
                class="p-3 rounded-lg border-2 transition-colors text-2xl"
                :class="createGoalForm.icon === icon.value ? 'border-green-500 bg-green-50' : 'border-gray-200 hover:border-gray-300'"
              >
                {{ icon.emoji }}
              </button>
            </div>
          </div>
        </div>

        <div class="flex gap-3">
          <button 
            @click="closeCreateGoalModal"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="createNewGoal"
            :disabled="!createGoalForm.title || !createGoalForm.targetAmount || createGoalForm.targetAmount <= 0"
            class="flex-1 py-3 px-4 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Create Goal
          </button>
        </div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="showSuccessMessage" class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      <div class="flex items-center gap-2">
        <i class="ri-check-line"></i>
        <span>{{ successMessage }}</span>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="showErrorMessage" class="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      <div class="flex items-center gap-2">
        <i class="ri-close-line"></i>
        <span>{{ errorMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import type { Goal } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'

const userStore = useUserStore()

// Modal states
const showAddCoinsModalFlag = ref(false)
const showEditGoalModalFlag = ref(false)
const showCreateGoalModalFlag = ref(false)
const showSuccessMessage = ref(false)
const successMessage = ref('')
const showErrorMessage = ref(false)
const errorMessage = ref('')

// Selected goal for modals
const selectedGoal = ref<Goal | null>(null)
const coinsToAdd = ref(0)

// Form data
const editGoalForm = ref({
  title: '',
  description: '',
  targetAmount: 0,
  icon: 'ri-gift-line'
})

const createGoalForm = ref({
  title: '',
  description: '',
  targetAmount: 0,
  icon: 'ri-gift-line'
})

// Goal icons for selection
const goalIcons = [
  { value: 'ri-gift-line', emoji: '🎁' },
  { value: 'ri-gamepad-line', emoji: '🎮' },
  { value: 'ri-book-line', emoji: '📚' },
  { value: 'ri-bike-line', emoji: '🚲' },
  { value: 'ri-headphone-line', emoji: '🎧' },
  { value: 'ri-smartphone-line', emoji: '📱' },
  { value: 'ri-palette-line', emoji: '🎨' },
  { value: 'ri-football-line', emoji: '⚽' },
  { value: 'ri-camera-line', emoji: '📷' },
  { value: 'ri-music-line', emoji: '🎵' },
  { value: 'ri-car-line', emoji: '🚗' },
  { value: 'ri-star-line', emoji: '⭐' }
]

// Helper functions
const getGoalEmoji = (iconClass: string) => {
  const icon = goalIcons.find(i => i.value === iconClass)
  return icon ? icon.emoji : '🎯'
}

const getProgressPercentage = (goal: Goal) => {
  return Math.min(Math.round((goal.current_amount / goal.target_amount) * 100), 100)
}

const getQuickAmounts = () => {
  if (!selectedGoal.value) return [1, 5, 10, 20]

  const remaining = selectedGoal.value.target_amount - selectedGoal.value.current_amount
  const maxCoins = userStore.totalCoins
  
  const amounts = [1, 5, 10, 20].filter(amount => amount <= Math.min(maxCoins, remaining))
  
  // Add "All" option if user has coins and it would help complete the goal
  if (maxCoins > 0 && maxCoins <= remaining) {
    amounts.push(maxCoins)
  }
  
  return amounts.slice(0, 4) // Limit to 4 options
}

// Modal functions
const showAddCoinsModal = (goal: Goal) => {
  selectedGoal.value = goal
  coinsToAdd.value = 0
  showAddCoinsModalFlag.value = true
}

const closeAddCoinsModal = () => {
  showAddCoinsModalFlag.value = false
  selectedGoal.value = null
  coinsToAdd.value = 0
}

const showEditGoalModal = (goal: Goal) => {
  selectedGoal.value = goal
  editGoalForm.value = {
    title: goal.title,
    description: goal.description,
    targetAmount: goal.target_amount,
    icon: goal.icon
  }
  showEditGoalModalFlag.value = true
}

const closeEditGoalModal = () => {
  showEditGoalModalFlag.value = false
  selectedGoal.value = null
  editGoalForm.value = {
    title: '',
    description: '',
    targetAmount: 0,
    icon: 'ri-gift-line'
  }
}

const showCreateGoalModal = () => {
  createGoalForm.value = {
    title: '',
    description: '',
    targetAmount: 0,
    icon: 'ri-gift-line'
  }
  showCreateGoalModalFlag.value = true
}

const closeCreateGoalModal = () => {
  showCreateGoalModalFlag.value = false
  createGoalForm.value = {
    title: '',
    description: '',
    targetAmount: 0,
    icon: 'ri-gift-line'
  }
}

// Action functions
const addCoinsToGoal = async () => {
  if (!selectedGoal.value || !coinsToAdd.value) return
  
  const success = await userStore.contributeToGoal(selectedGoal.value.id, coinsToAdd.value)
  
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = `Added ${coinsToAdd.value} coins to ${selectedGoal.value.title}! 🎉`
    
    // Check if goal is completed
    if (selectedGoal.value.current_amount >= selectedGoal.value.target_amount) {
      setTimeout(() => {
        successMessage.value = `🎉 Goal completed! You saved enough for ${selectedGoal.value?.title}!`
      }, 2000)
    }
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 4000)
  }
  
  closeAddCoinsModal()
}

const updateGoal = async () => {
  if (!selectedGoal.value) return
  
  const success = await userStore.updateGoal(selectedGoal.value.id, {
    title: editGoalForm.value.title,
    description: editGoalForm.value.description,
    target_amount: editGoalForm.value.targetAmount,
    icon: editGoalForm.value.icon
  })
  
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = 'Goal updated successfully! ✨'
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  
  closeEditGoalModal()
}

const createNewGoal = async () => {
  const newGoal = await userStore.createGoal({
    title: createGoalForm.value.title,
    description: createGoalForm.value.description,
    target_amount: createGoalForm.value.targetAmount,
    current_amount: 0,
    icon: createGoalForm.value.icon,
    category: 'wants' // Default category for child goals
  })
  
  if (newGoal) {
    showSuccessMessage.value = true
    successMessage.value = `Goal "${createGoalForm.value.title}" created! Start saving! 🎯`
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  
  closeCreateGoalModal()
}

const markCompleted = async (goal: Goal) => {
  try {
    const authStore = useAuthStore()
    const userId = authStore.user?.id
    
    if (!userId) {
      showErrorMessage.value = true
      errorMessage.value = 'User not authenticated'
      return
    }
    
    const ok = await userStore.updateGoal(goal.id, { completed: true })
    if (ok) {
      showSuccessMessage.value = true
      successMessage.value = `Marked goal "${goal.title}" as completed! 🎉`
      setTimeout(() => (showSuccessMessage.value = false), 2500)
      
      // Goal was completed successfully - no need to refresh immediately
      // The UI will update when the user navigates or refreshes
      console.log('✅ [CHILD_GOALS] Goal marked as completed successfully')
    } else {
      showErrorMessage.value = true
      errorMessage.value = 'Failed to mark goal as completed'
    }
  } catch (error) {
    console.error('Error marking goal as completed:', error)
    showErrorMessage.value = true
    errorMessage.value = 'An error occurred while marking goal as completed'
  }
}

watch(coinsToAdd, (newValue) => {
  const compareValue = Math.min(userStore.totalCoins, (selectedGoal.value?.target_amount || 0) - (selectedGoal.value?.current_amount || 0))
  
  if (newValue > compareValue) {
    coinsToAdd.value = compareValue
  }
})
</script>

<style scoped>
/* Ensure proper spacing and responsive design */
@media (max-width: 768px) {
  .max-w-4xl {
    max-width: 100%;
  }
}

/* Custom scrollbar for modals */
.modal-content {
  max-height: 90vh;
  overflow-y: auto;
}

/* Smooth transitions for progress bars */
.bg-green-500 {
  transition: width 0.5s ease-in-out;
}

/* Button hover effects */
button:not(:disabled):hover {
  transform: translateY(-1px);
}

button:disabled {
  transform: none;
}
</style>