<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 via-orange-50 to-yellow-100 p-4 pb-20">
    <!-- Main Content Container - Centered on Desktop -->
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
         
          My Piggy Bank
        </h1>
        <p class="text-gray-600 text-lg">Save your coins and watch them grow!</p>
      </div>

      <!-- Savings Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Main Piggy Bank Display -->
        <div class="lg:col-span-2 bg-white rounded-2xl shadow-md p-8 text-center">
          <div class="text-8xl mb-4 animate-bounce">🐷</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Total Saved</h2>
          <div class="text-4xl font-bold text-pink-500 mb-6 flex items-center justify-center gap-2">
            <img src="/coin.svg" class="logo-icon text-6xl" alt="coin">
            <span>{{ userStore.totalCoins }}</span>
          </div>
          
          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              @click="showAddCoinsModal"
              class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-full transition-colors font-medium shadow-md hover:shadow-lg transform hover:-translate-y-1"
            >
              <i class="ri-add-line mr-2"></i>Add Coins
            </button>
            <button 
              @click="showSpendCoinsModal"
              :disabled="userStore.totalCoins === 0"
              class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-6 py-3 rounded-full transition-colors font-medium shadow-md hover:shadow-lg transform hover:-translate-y-1 disabled:transform-none"
            >
              <i class="ri-subtract-line mr-2"></i>Spend Coins
            </button>
          </div>
        </div>

        <!-- Savings Stats -->
        <div class="space-y-6">
          <!-- This Week Stats -->
          <div class="bg-white rounded-2xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <i class="ri-calendar-fill text-blue-500 mr-2"></i>
              This Week
            </h3>
            <div class="text-3xl font-bold text-blue-500 mb-2">+{{ weeklyEarnings }} coins</div>
            <p class="text-sm text-gray-600">Great job saving!</p>
          </div>
          
          <!-- Goal Progress -->
          <div class="bg-white rounded-2xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <i class="ri-target-fill text-yellow-500 mr-2"></i>
              Goal Progress
            </h3>
            <div class="text-3xl font-bold text-yellow-500 mb-2">{{ goalProgress }}%</div>
            <p class="text-sm text-gray-600">{{ activeGoalName || 'Set a goal to track progress!' }}</p>
          </div>

          <!-- Savings Streak -->
          <div class="bg-white rounded-2xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <i class="ri-fire-fill text-red-500 mr-2"></i>
              Savings Streak
            </h3>
            <div class="text-3xl font-bold text-red-500 mb-2">{{ savingsStreak }} days</div>
            <p class="text-sm text-gray-600">Keep it up!</p>
          </div>
        </div>
      </div>

      <!-- Recent Transactions -->
      <div class="bg-white rounded-2xl shadow-md p-6 mb-8">
        <h2 class="text-xl font-bold text-gray-800 mb-6 flex items-center">
          <i class="ri-history-line mr-2"></i>
          Recent Activity
        </h2>
        
        <div v-if="userStore.recentTransactions.length === 0" class="text-center py-8">
          <div class="text-4xl mb-4">📝</div>
          <p class="text-gray-500">No transactions yet. Start saving or spending!</p>
        </div>
        
        <div v-else class="space-y-3">
          <div 
            v-for="transaction in userStore.recentTransactions.slice(0, 5)" 
            :key="transaction.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :class="{
                  'bg-green-100': transaction.type === 'earn',
                  'bg-blue-100': transaction.type === 'save',
                  'bg-orange-100': transaction.type === 'spend'
                }"
              >
                <i 
                  :class="{
                    'ri-add-line text-green-600': transaction.type === 'earn',
                    'ri-target-line text-blue-600': transaction.type === 'save',
                    'ri-subtract-line text-orange-600': transaction.type === 'spend'
                  }"
                ></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                <div class="text-sm text-gray-500">{{ formatDate(transaction.created_at) }}</div>
              </div>
            </div>
            <div 
              class="font-bold flex items-center gap-1"
              :class="{
                'text-green-600': transaction.type === 'earn',
                'text-blue-600': transaction.type === 'save',
                'text-orange-600': transaction.type === 'spend'
              }"
            >
              <span>{{ transaction.type === 'spend' ? '-' : '+' }}{{ transaction.amount }}</span>
              <img src="/coin.svg" class="logo-icon text-sm" alt="coin">
            </div>
          </div>
        </div>
      </div>

      <!-- Savings Tips -->
      <div class="bg-gradient-to-r from-purple-400 to-pink-500 rounded-2xl p-6 text-white">
        <h2 class="text-xl font-bold mb-4">
          <i class="ri-lightbulb-line mr-2"></i>
          Savings Tips for You! 💡
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-white/20 rounded-lg p-4">
            <h3 class="font-semibold mb-2">🎯 Set Small Goals</h3>
            <p class="text-sm opacity-90">Start with small, achievable goals to build your saving habit!</p>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <h3 class="font-semibold mb-2">📅 Save Regularly</h3>
            <p class="text-sm opacity-90">Try to save a little bit every day, even if it's just 1 coin!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Coins Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">💰</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Add Coins to Piggy Bank</h3>
          <p class="text-gray-600">How many coins did you earn?</p>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Number of coins to add:
          </label>
          <input 
            v-model.number="coinsToAdd"
            type="number" 
            min="1" 
            max="1000"
            class="w-full p-3 border border-gray-300 rounded-lg text-center text-lg font-semibold"
            placeholder="0"
          />
          
          <!-- Quick Amount Buttons -->
          <div class="grid grid-cols-4 gap-2 mt-3">
            <button 
              v-for="amount in [1, 5, 10, 20]"
              :key="amount"
              @click="coinsToAdd = amount"
              class="py-2 px-3 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors"
            >
              {{ amount }}
            </button>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            What did you do to earn these coins?
          </label>
          <select 
            v-model="earnReason"
            class="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">Select a reason...</option>
            <option value="Completed chores">Completed chores</option>
            <option value="Good behavior">Good behavior</option>
            <option value="Helped family">Helped family</option>
            <option value="Finished homework">Finished homework</option>
            <option value="Learning activity">Learning activity</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="flex gap-3">
          <button 
            @click="closeAddModal"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="addCoins"
            :disabled="!coinsToAdd || coinsToAdd <= 0 || !earnReason"
            class="flex-1 py-3 px-4 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Add Coins
          </button>
        </div>
      </div>
    </div>

    <!-- Spend Coins Modal -->
    <div v-if="showSpendModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">🛒</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Spend Coins</h3>
          <p class="text-gray-600">What would you like to buy?</p>
        </div>

        <div class="mb-4">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>Your coins:</span>
            <span class="font-medium flex items-center gap-1">
              <img src="/coin.svg" class="logo-icon text-sm" alt="coin">
              {{ userStore.totalCoins }}
            </span>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Number of coins to spend:
          </label>
          <input 
            v-model.number="coinsToSpend"
            type="number" 
            :min="1" 
            :max="userStore.totalCoins"
            class="w-full p-3 border border-gray-300 rounded-lg text-center text-lg font-semibold"
            placeholder="0"
          />
          
          <!-- Quick Amount Buttons -->
          <div class="grid grid-cols-4 gap-2 mt-3">
            <button 
              v-for="amount in getSpendAmounts()"
              :key="amount"
              @click="coinsToSpend = amount"
              class="py-2 px-3 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors"
            >
              {{ amount }}
            </button>
          </div>
        </div>

        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            What are you buying?
          </label>
          <select 
            v-model="spendReason"
            class="w-full p-3 border border-gray-300 rounded-lg"
          >
            <option value="">Select what you're buying...</option>
            <option value="Toy or game">Toy or game</option>
            <option value="Treats or snacks">Treats or snacks</option>
            <option value="Art supplies">Art supplies</option>
            <option value="Book or magazine">Book or magazine</option>
            <option value="Gift for someone">Gift for someone</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div class="flex gap-3">
          <button 
            @click="closeSpendModal"
            class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="spendCoins"
            :disabled="!coinsToSpend || coinsToSpend <= 0 || coinsToSpend > userStore.totalCoins || !spendReason"
            class="flex-1 py-3 px-4 bg-orange-500 text-white rounded-lg font-medium hover:bg-orange-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            Spend Coins
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// Modal states
const showAddModal = ref(false)
const showSpendModal = ref(false)
const showSuccessMessage = ref(false)
const successMessage = ref('')

// Form data
const coinsToAdd = ref(0)
const coinsToSpend = ref(0)
const earnReason = ref('')
const spendReason = ref('')

// Computed properties for stats
const weeklyEarnings = computed(() => {
  // Calculate earnings from the last 7 days
  const oneWeekAgo = new Date()
  oneWeekAgo.setDate(oneWeekAgo.getDate() - 7)
  return userStore.recentTransactions
    .filter(transaction => {
      const transactionDate = new Date(transaction.created_at)
      return transactionDate >= oneWeekAgo && transaction.type === 'earn'
    })
    .reduce((total, transaction) => total + transaction.amount, 0)
})

const goalProgress = computed(() => {
  const activeGoal = userStore.activeGoals[0]
  if (!activeGoal) return 0
  return Math.round((activeGoal.current_amount / activeGoal.target_amount) * 100)
})

const activeGoalName = computed(() => {
  const activeGoal = userStore.activeGoals[0]
  return activeGoal ? activeGoal.title : null
})

const savingsStreak = computed(() => {
  
  // Simple calculation - could be enhanced with actual streak tracking
  return userStore.profile?.streak || 0
})

// Modal functions
const showAddCoinsModal = () => {
  coinsToAdd.value = 0
  earnReason.value = ''
  showAddModal.value = true
}

const closeAddModal = () => {
  showAddModal.value = false
  coinsToAdd.value = 0
  earnReason.value = ''
}

const showSpendCoinsModal = () => {
  coinsToSpend.value = 0
  spendReason.value = ''
  showSpendModal.value = true
}

const closeSpendModal = () => {
  showSpendModal.value = false
  coinsToSpend.value = 0
  spendReason.value = ''
}

// Transaction functions
const addCoins = async () => {
  if (!coinsToAdd.value || coinsToAdd.value <= 0 || !earnReason.value) return
  
  await userStore.addCoins(coinsToAdd.value, earnReason.value, 'earning')
  
  showSuccessMessage.value = true
  successMessage.value = `Added ${coinsToAdd.value} coins to your piggy bank! 🎉`
  
  setTimeout(() => {
    showSuccessMessage.value = false
  }, 3000)
  
  closeAddModal()
}

const spendCoins = async () => {
  if (!coinsToSpend.value || coinsToSpend.value <= 0 || coinsToSpend.value > userStore.totalCoins || !spendReason.value) return
  
  const success = await userStore.spendCoins(coinsToSpend.value, spendReason.value, 'purchase')
  
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = `Spent ${coinsToSpend.value} coins on ${spendReason.value}! 💸`
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  
  closeSpendModal()
}

// Helper functions
const getSpendAmounts = () => {
  const maxCoins = userStore.totalCoins
  const amounts = [1, 5, 10, 20].filter(amount => amount <= maxCoins)
  return amounts.slice(0, 4)
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
</script>

<style scoped>
/* Ensure proper spacing and responsive design */
@media (max-width: 768px) {
  .max-w-6xl {
    max-width: 100%;
  }
}

/* Custom scrollbar for modals */
.modal-content {
  max-height: 90vh;
  overflow-y: auto;
}

/* Button hover effects */
button:not(:disabled):hover {
  transform: translateY(-1px);
}

button:disabled {
  transform: none;
}

/* Smooth transitions for all interactive elements */
* {
  transition: all 0.2s ease;
}
</style>