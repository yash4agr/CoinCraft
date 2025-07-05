<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Budget Manager Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Budget Manager 💰</h1>
      <p class="text-gray-600">Track and manage your money allocation</p>
    </div>

    <!-- Current Budget Overview -->
    <div class="mb-8">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Current Budget Split</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Dynamic Pie Chart -->
          <div class="flex items-center justify-center">
            <div class="relative w-56 h-56">
              <svg class="w-56 h-56 transform -rotate-90" viewBox="0 0 100 100">
                <!-- Saving slice -->
                <circle 
                  cx="50" 
                  cy="50" 
                  r="35" 
                  fill="none" 
                  stroke="#10b981" 
                  stroke-width="30" 
                  :stroke-dasharray="`${savingCircumference} ${totalCircumference - savingCircumference}`"
                  stroke-dashoffset="0" 
                />
                <!-- Spending slice -->
                <circle 
                  cx="50" 
                  cy="50" 
                  r="35" 
                  fill="none" 
                  stroke="#3b82f6" 
                  stroke-width="30" 
                  :stroke-dasharray="`${spendingCircumference} ${totalCircumference - spendingCircumference}`"
                  :stroke-dashoffset="`-${savingCircumference}`"
                />
                <!-- Wants slice -->
                <circle 
                  cx="50" 
                  cy="50" 
                  r="35" 
                  fill="none" 
                  stroke="#f59e0b" 
                  stroke-width="30" 
                  :stroke-dasharray="`${wantsCircumference} ${totalCircumference - wantsCircumference}`"
                  :stroke-dashoffset="`-${savingCircumference + spendingCircumference}`"
                />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-3xl font-bold text-gray-800">{{ userStore.totalCoins }}</div>
                  <div class="text-sm text-gray-600">Total Budget</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Budget Categories -->
          <div class="space-y-6">
            <div class="p-4 bg-green-50 rounded-xl border border-green-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-green-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Saving</h3>
                </div>
                <span class="text-sm text-green-600 font-medium">{{ budgetAllocations.saving }}%</span>
              </div>
              <div class="text-2xl font-bold text-green-600 mb-2">{{ savingAmount }} coins</div>
              <p class="text-sm text-green-700">Building your future fund</p>
            </div>
            
            <div class="p-4 bg-blue-50 rounded-xl border border-blue-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-blue-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Spending</h3>
                </div>
                <span class="text-sm text-blue-600 font-medium">{{ budgetAllocations.spending }}%</span>
              </div>
              <div class="text-2xl font-bold text-blue-600 mb-2">{{ spendingAmount }} coins</div>
              <p class="text-sm text-blue-700">Essential purchases & needs</p>
            </div>
            
            <div class="p-4 bg-yellow-50 rounded-xl border border-yellow-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-yellow-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Wants</h3>
                </div>
                <span class="text-sm text-yellow-600 font-medium">{{ budgetAllocations.wants }}%</span>
              </div>
              <div class="text-2xl font-bold text-yellow-600 mb-2">{{ wantsAmount }} coins</div>
              <p class="text-sm text-yellow-700">Fun purchases & entertainment</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Budget Actions -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Budget Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button 
          @click="showUpdateBudgetModal"
          class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-xl transition-colors"
          :class="{ 'opacity-75': isLoading }"
          :disabled="isLoading"
        >
          <div class="flex items-center gap-3">
            <i class="ri-edit-line text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">Update Budget</div>
              <div class="text-sm opacity-90">Adjust your allocations</div>
            </div>
          </div>
        </button>
        
        <button 
          @click="showViewHistoryModal"
          class="bg-green-500 hover:bg-green-600 text-white p-4 rounded-xl transition-colors"
          :class="{ 'opacity-75': isLoading }"
          :disabled="isLoading"
        >
          <div class="flex items-center gap-3">
            <i class="ri-history-line text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">View History</div>
              <div class="text-sm opacity-90">See past transactions</div>
            </div>
          </div>
        </button>
        
        <button 
          @click="saveBudget"
          class="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-400 text-white p-4 rounded-xl transition-colors"
          :disabled="!hasUnsavedChanges || isSaving"
          :class="{ 'opacity-75': isSaving }"
        >
          <div class="flex items-center gap-3">
            <i :class="isSaving ? 'ri-loader-4-line animate-spin' : 'ri-save-line'" class="text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">{{ isSaving ? 'Saving...' : 'Save Budget' }}</div>
              <div class="text-sm opacity-90">{{ hasUnsavedChanges ? 'Confirm changes' : 'No changes to save' }}</div>
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Transaction History</h2>
      <div class="bg-white rounded-xl shadow-sm">
        <div 
          v-for="(transaction, index) in userStore.recentTransactions.slice(0, 3)" 
          :key="transaction.id"
          class="p-4"
          :class="{ 'border-b border-gray-100': index < 2 }"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center"
                :class="{
                  'bg-green-100': transaction.type === 'earn',
                  'bg-blue-100': transaction.type === 'save',
                  'bg-yellow-100': transaction.type === 'spend'
                }"
              >
                <i 
                  :class="{
                    'ri-add-line text-green-600': transaction.type === 'earn',
                    'ri-target-line text-blue-600': transaction.type === 'save',
                    'ri-subtract-line text-yellow-600': transaction.type === 'spend'
                  }"
                ></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                <div class="text-sm text-gray-500">{{ transaction.category }}</div>
              </div>
            </div>
            <div class="text-right">
              <div 
                class="font-semibold"
                :class="{
                  'text-green-600': transaction.type === 'earn',
                  'text-blue-600': transaction.type === 'save',
                  'text-yellow-600': transaction.type === 'spend'
                }"
              >
                {{ transaction.type === 'spend' ? '-' : '+' }}{{ transaction.amount }} coins
              </div>
              <div class="text-xs text-gray-500">{{ formatDate(transaction.timestamp) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Budget Modal -->
    <div v-if="showUpdateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Update Budget Allocation</h3>
          <button 
            @click="closeUpdateModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>

        <div class="space-y-6">
          <!-- Budget Allocation Form -->
          <div class="space-y-4">
            <!-- Saving Allocation -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Saving Allocation: {{ tempBudgetAllocations.saving }}%
              </label>
              <div class="flex items-center gap-4">
                <input 
                  v-model.number="tempBudgetAllocations.saving"
                  type="range" 
                  min="0" 
                  max="100" 
                  class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-green"
                  @input="validateBudgetAllocations"
                />
                <input 
                  v-model.number="tempBudgetAllocations.saving"
                  type="number" 
                  min="0" 
                  max="100" 
                  class="w-20 p-2 border border-gray-300 rounded-lg text-center"
                  @input="validateBudgetAllocations"
                />
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ Math.floor(userStore.totalCoins * tempBudgetAllocations.saving / 100) }} coins</p>
            </div>

            <!-- Spending Allocation -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Spending Allocation: {{ tempBudgetAllocations.spending }}%
              </label>
              <div class="flex items-center gap-4">
                <input 
                  v-model.number="tempBudgetAllocations.spending"
                  type="range" 
                  min="0" 
                  max="100" 
                  class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-blue"
                  @input="validateBudgetAllocations"
                />
                <input 
                  v-model.number="tempBudgetAllocations.spending"
                  type="number" 
                  min="0" 
                  max="100" 
                  class="w-20 p-2 border border-gray-300 rounded-lg text-center"
                  @input="validateBudgetAllocations"
                />
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ Math.floor(userStore.totalCoins * tempBudgetAllocations.spending / 100) }} coins</p>
            </div>

            <!-- Wants Allocation -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Wants Allocation: {{ tempBudgetAllocations.wants }}%
              </label>
              <div class="flex items-center gap-4">
                <input 
                  v-model.number="tempBudgetAllocations.wants"
                  type="range" 
                  min="0" 
                  max="100" 
                  class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider-yellow"
                  @input="validateBudgetAllocations"
                />
                <input 
                  v-model.number="tempBudgetAllocations.wants"
                  type="number" 
                  min="0" 
                  max="100" 
                  class="w-20 p-2 border border-gray-300 rounded-lg text-center"
                  @input="validateBudgetAllocations"
                />
              </div>
              <p class="text-sm text-gray-600 mt-1">{{ Math.floor(userStore.totalCoins * tempBudgetAllocations.wants / 100) }} coins</p>
            </div>
          </div>

          <!-- Total Validation -->
          <div class="p-4 rounded-lg" :class="totalPercentage === 100 ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'">
            <div class="flex items-center gap-2">
              <i :class="totalPercentage === 100 ? 'ri-check-line text-green-600' : 'ri-error-warning-line text-red-600'"></i>
              <span class="font-medium" :class="totalPercentage === 100 ? 'text-green-800' : 'text-red-800'">
                Total: {{ totalPercentage }}%
              </span>
            </div>
            <p class="text-sm mt-1" :class="totalPercentage === 100 ? 'text-green-700' : 'text-red-700'">
              {{ totalPercentage === 100 ? 'Perfect! Your budget adds up to 100%.' : 'Your budget must total exactly 100%.' }}
            </p>
          </div>

          <!-- Error Messages -->
          <div v-if="budgetError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-center gap-2">
              <i class="ri-error-warning-line text-red-600"></i>
              <span class="font-medium text-red-800">{{ budgetError }}</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-4">
            <button 
              @click="closeUpdateModal"
              class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="applyBudgetChanges"
              :disabled="totalPercentage !== 100 || isUpdatingBudget"
              class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {{ isUpdatingBudget ? 'Updating...' : 'Apply Changes' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- View History Modal -->
    <div v-if="showHistoryModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-800">Transaction History</h3>
          <button 
            @click="closeHistoryModal"
            class="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <i class="ri-close-line text-2xl"></i>
          </button>
        </div>

        <!-- Filters -->
        <div class="mb-6 flex flex-wrap gap-4">
          <select 
            v-model="historyFilter.type"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Types</option>
            <option value="earn">Earnings</option>
            <option value="spend">Spending</option>
            <option value="save">Savings</option>
          </select>

          <select 
            v-model="historyFilter.timeframe"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Time</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
            <option value="quarter">This Quarter</option>
          </select>

          <button 
            @click="clearHistoryFilters"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
          >
            Clear Filters
          </button>
        </div>

        <!-- Transaction List -->
        <div v-if="isLoadingHistory" class="text-center py-8">
          <div class="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p class="text-gray-600">Loading transaction history...</p>
        </div>

        <div v-else-if="filteredTransactions.length === 0" class="text-center py-8">
          <i class="ri-file-list-line text-4xl text-gray-300 mb-4"></i>
          <p class="text-gray-600">No transactions found for the selected filters.</p>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="transaction in paginatedTransactions" 
            :key="transaction.id"
            class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div 
                  class="w-10 h-10 rounded-full flex items-center justify-center"
                  :class="{
                    'bg-green-100': transaction.type === 'earn',
                    'bg-blue-100': transaction.type === 'save',
                    'bg-yellow-100': transaction.type === 'spend'
                  }"
                >
                  <i 
                    :class="{
                      'ri-add-line text-green-600': transaction.type === 'earn',
                      'ri-target-line text-blue-600': transaction.type === 'save',
                      'ri-subtract-line text-yellow-600': transaction.type === 'spend'
                    }"
                  ></i>
                </div>
                <div>
                  <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                  <div class="text-sm text-gray-500">{{ transaction.category }} • {{ formatDate(transaction.timestamp) }}</div>
                </div>
              </div>
              <div class="text-right">
                <div 
                  class="font-semibold text-lg"
                  :class="{
                    'text-green-600': transaction.type === 'earn',
                    'text-blue-600': transaction.type === 'save',
                    'text-yellow-600': transaction.type === 'spend'
                  }"
                >
                  {{ transaction.type === 'spend' ? '-' : '+' }}{{ transaction.amount }} coins
                </div>
                <div class="text-xs text-gray-500">{{ getTransactionTypeLabel(transaction.type) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="totalHistoryPages > 1" class="mt-6 flex items-center justify-between">
          <button 
            @click="previousHistoryPage"
            :disabled="currentHistoryPage === 1"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 text-gray-700 rounded-lg transition-colors"
          >
            Previous
          </button>
          <span class="text-sm text-gray-600">
            Page {{ currentHistoryPage }} of {{ totalHistoryPages }}
          </span>
          <button 
            @click="nextHistoryPage"
            :disabled="currentHistoryPage === totalHistoryPages"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 text-gray-700 rounded-lg transition-colors"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div v-if="showSuccessToast" class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      <div class="flex items-center gap-2">
        <i class="ri-check-line"></i>
        <span>{{ successMessage }}</span>
      </div>
    </div>

    <!-- Error Toast -->
    <div v-if="showErrorToast" class="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50">
      <div class="flex items-center gap-2">
        <i class="ri-error-warning-line"></i>
        <span>{{ errorMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'

// Store
const userStore = useUserStore()

// State
const isLoading = ref(false)
const isSaving = ref(false)
const isUpdatingBudget = ref(false)
const isLoadingHistory = ref(false)
const showUpdateModal = ref(false)
const showHistoryModal = ref(false)
const showSuccessToast = ref(false)
const showErrorToast = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const budgetError = ref('')

// Budget allocations (default percentages)
const budgetAllocations = ref({
  saving: 40,
  spending: 35,
  wants: 25
})

// Temporary allocations for editing
const tempBudgetAllocations = ref({
  saving: 40,
  spending: 35,
  wants: 25
})

// Original allocations to track changes
const originalBudgetAllocations = ref({
  saving: 40,
  spending: 35,
  wants: 25
})

// History filters
const historyFilter = ref({
  type: '',
  timeframe: 'all'
})

const currentHistoryPage = ref(1)
const historyItemsPerPage = 10

// Computed properties
const savingAmount = computed(() => Math.floor(userStore.totalCoins * budgetAllocations.value.saving / 100))
const spendingAmount = computed(() => Math.floor(userStore.totalCoins * budgetAllocations.value.spending / 100))
const wantsAmount = computed(() => Math.floor(userStore.totalCoins * budgetAllocations.value.wants / 100))

// Pie chart calculations
const totalCircumference = 2 * Math.PI * 35 // radius = 35
const savingCircumference = computed(() => (budgetAllocations.value.saving / 100) * totalCircumference)
const spendingCircumference = computed(() => (budgetAllocations.value.spending / 100) * totalCircumference)
const wantsCircumference = computed(() => (budgetAllocations.value.wants / 100) * totalCircumference)

// Budget validation
const totalPercentage = computed(() => 
  tempBudgetAllocations.value.saving + tempBudgetAllocations.value.spending + tempBudgetAllocations.value.wants
)

const hasUnsavedChanges = computed(() => 
  budgetAllocations.value.saving !== originalBudgetAllocations.value.saving ||
  budgetAllocations.value.spending !== originalBudgetAllocations.value.spending ||
  budgetAllocations.value.wants !== originalBudgetAllocations.value.wants
)

// Transaction filtering
const filteredTransactions = computed(() => {
  let transactions = [...userStore.recentTransactions]

  // Filter by type
  if (historyFilter.value.type) {
    transactions = transactions.filter(t => t.type === historyFilter.value.type)
  }

  // Filter by timeframe
  if (historyFilter.value.timeframe !== 'all') {
    const now = new Date()
    const filterDate = new Date()

    switch (historyFilter.value.timeframe) {
      case 'week':
        filterDate.setDate(now.getDate() - 7)
        break
      case 'month':
        filterDate.setMonth(now.getMonth() - 1)
        break
      case 'quarter':
        filterDate.setMonth(now.getMonth() - 3)
        break
    }

    transactions = transactions.filter(t => new Date(t.timestamp) >= filterDate)
  }

  return transactions.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
})

const totalHistoryPages = computed(() => 
  Math.ceil(filteredTransactions.value.length / historyItemsPerPage)
)

const paginatedTransactions = computed(() => {
  const start = (currentHistoryPage.value - 1) * historyItemsPerPage
  const end = start + historyItemsPerPage
  return filteredTransactions.value.slice(start, end)
})

// Methods
const showUpdateBudgetModal = () => {
  tempBudgetAllocations.value = { ...budgetAllocations.value }
  budgetError.value = ''
  showUpdateModal.value = true
}

const closeUpdateModal = () => {
  showUpdateModal.value = false
  tempBudgetAllocations.value = { ...budgetAllocations.value }
  budgetError.value = ''
}

const validateBudgetAllocations = () => {
  budgetError.value = ''
  
  // Ensure all values are valid numbers
  Object.keys(tempBudgetAllocations.value).forEach(key => {
    const value = tempBudgetAllocations.value[key as keyof typeof tempBudgetAllocations.value]
    if (isNaN(value) || value < 0) {
      tempBudgetAllocations.value[key as keyof typeof tempBudgetAllocations.value] = 0
    }
    if (value > 100) {
      tempBudgetAllocations.value[key as keyof typeof tempBudgetAllocations.value] = 100
    }
  })
}

const applyBudgetChanges = async () => {
  if (totalPercentage.value !== 100) {
    budgetError.value = 'Budget allocations must total exactly 100%'
    return
  }

  isUpdatingBudget.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))

    budgetAllocations.value = { ...tempBudgetAllocations.value }
    showUpdateModal.value = false
    showSuccess('Budget allocations updated successfully!')
  } catch (error) {
    showError('Failed to update budget allocations. Please try again.')
  } finally {
    isUpdatingBudget.value = false
  }
}

const showViewHistoryModal = async () => {
  showHistoryModal.value = true
  isLoadingHistory.value = true

  try {
    // Simulate API call to load full transaction history
    await new Promise(resolve => setTimeout(resolve, 1000))
  } catch (error) {
    showError('Failed to load transaction history')
  } finally {
    isLoadingHistory.value = false
  }
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
  historyFilter.value = { type: '', timeframe: 'all' }
  currentHistoryPage.value = 1
}

const clearHistoryFilters = () => {
  historyFilter.value = { type: '', timeframe: 'all' }
  currentHistoryPage.value = 1
}

const previousHistoryPage = () => {
  if (currentHistoryPage.value > 1) {
    currentHistoryPage.value--
  }
}

const nextHistoryPage = () => {
  if (currentHistoryPage.value < totalHistoryPages.value) {
    currentHistoryPage.value++
  }
}

const saveBudget = async () => {
  if (!hasUnsavedChanges.value) return

  isSaving.value = true

  try {
    // Simulate API call to save budget preferences
    await new Promise(resolve => setTimeout(resolve, 1500))

    // Update original allocations to match current
    originalBudgetAllocations.value = { ...budgetAllocations.value }
    
    showSuccess('Budget preferences saved successfully!')
  } catch (error) {
    showError('Failed to save budget preferences. Please try again.')
  } finally {
    isSaving.value = false
  }
}

// Helper functions
const formatDate = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'Just now'
  if (diffInHours < 24) return `${diffInHours} hours ago`
  if (diffInHours < 48) return 'Yesterday'
  return `${Math.floor(diffInHours / 24)} days ago`
}

const getTransactionTypeLabel = (type: string) => {
  const labels = {
    earn: 'Income',
    spend: 'Expense',
    save: 'Savings'
  }
  return labels[type as keyof typeof labels] || type
}

const showSuccess = (message: string) => {
  successMessage.value = message
  showSuccessToast.value = true
  setTimeout(() => {
    showSuccessToast.value = false
  }, 3000)
}

const showError = (message: string) => {
  errorMessage.value = message
  showErrorToast.value = true
  setTimeout(() => {
    showErrorToast.value = false
  }, 3000)
}

// Watchers
watch([() => historyFilter.value.type, () => historyFilter.value.timeframe], () => {
  currentHistoryPage.value = 1
})

// Lifecycle
onMounted(() => {
  // Initialize original allocations
  originalBudgetAllocations.value = { ...budgetAllocations.value }
})
</script>

<style scoped>
/* Custom slider styles */
.slider-green::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #10b981;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-blue::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-yellow::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #f59e0b;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-green::-moz-range-thumb,
.slider-blue::-moz-range-thumb,
.slider-yellow::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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

/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Focus styles for accessibility */
button:focus,
input:focus,
select:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>