<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-indigo-100 p-4 pb-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-store-fill text-blue-500 mr-3"></i>
          Rewards Store
        </h1>
        <p class="text-gray-600 text-lg">Redeem your coins for valuable rewards!</p>
        
        <!-- Current Balance -->
        <div class="mt-4 bg-white rounded-xl p-4 shadow-sm inline-block">
          <div class="flex items-center gap-2">
            <img src="/coin.svg" class="coin-icon text-xl" alt="coin">
            <span class="text-xl font-bold text-gray-800">{{ userStore.totalCoins }} coins</span>
          </div>
        </div>
      </div>

      <!-- Shop Categories -->
      <div class="mb-8">
        <div class="flex gap-4 overflow-x-auto pb-2">
          <button 
            v-for="category in categories"
            :key="category.id"
            @click="selectedCategory = category.id"
            class="flex-shrink-0 px-4 py-2 rounded-full font-medium transition-colors"
            :class="selectedCategory === category.id 
              ? 'bg-blue-500 text-white' 
              : 'bg-white text-gray-600 hover:bg-blue-100'"
          >
            <i :class="category.icon" class="mr-2"></i>
            {{ category.name }}
          </button>
        </div>
      </div>

      <!-- Shop Items Grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
        <div 
          v-for="item in filteredItems"
          :key="item.id"
          class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow"
        >
          <div class="text-center">
            <!-- Item Image/Icon -->
            <div class="w-16 h-16 mx-auto mb-3 bg-gradient-to-br rounded-xl flex items-center justify-center text-3xl"
                 :class="item.bgColor">
              {{ item.emoji }}
            </div>
            
            <!-- Item Info -->
            <h3 class="font-semibold text-gray-800 mb-1">{{ item.name }}</h3>
            <p class="text-xs text-gray-600 mb-3">{{ item.description }}</p>
            
            <!-- Price -->
            <div class="flex items-center justify-center gap-1 mb-3">
              <img src="/coin.svg" class="coin-icon" alt="coin">
              <span class="font-bold text-gray-800">{{ item.price }}</span>
            </div>
            
            <!-- Buy Button -->
            <button 
              @click="handlePurchase(item)"
              :disabled="userStore.totalCoins < item.price || item.owned"
              class="w-full py-2 px-3 rounded-lg font-medium transition-colors text-sm"
              :class="item.owned 
                ? 'bg-green-100 text-green-700 cursor-not-allowed' 
                : userStore.totalCoins >= item.price 
                  ? 'bg-blue-500 text-white hover:bg-blue-600' 
                  : 'bg-gray-200 text-gray-500 cursor-not-allowed'"
            >
              {{ item.owned ? 'Owned' : userStore.totalCoins >= item.price ? 'Buy Now' : 'Not Enough Coins' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Money Conversion Section -->
      <div class="bg-gradient-to-r from-green-400 to-blue-500 rounded-2xl p-6 text-white mb-8">
        <h2 class="text-2xl font-bold mb-4">
          <i class="ri-exchange-dollar-line mr-2"></i>
          Convert Coins to Real Money
        </h2>
        <p class="mb-4 opacity-90">Turn your hard-earned coins into real money with parent approval!</p>
        
        <div class="bg-white/20 rounded-xl p-4 mb-4">
          <div class="text-center">
            <div class="text-lg font-semibold mb-2">Exchange Rate</div>
            <div class="flex items-center justify-center gap-2 text-2xl font-bold">
              <span>10</span>
              <img src="/coin.svg" class="coin-icon" alt="coin">
              <span>=</span>
              <span>$1.00</span>
            </div>
          </div>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <button 
            v-for="amount in conversionAmounts"
            :key="amount.coins"
            @click="requestMoneyConversion(amount)"
            :disabled="userStore.totalCoins < amount.coins"
            class="bg-white/20 hover:bg-white/30 disabled:bg-white/10 disabled:text-white/50 rounded-lg p-3 transition-colors"
          >
            <div class="text-sm font-medium">{{ amount.coins }} coins</div>
            <div class="text-lg font-bold">${{ amount.dollars }}</div>
          </button>
        </div>
      </div>

      <!-- Purchase History -->
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-4">
          <i class="ri-history-line mr-2"></i>
          All Shop Purchases
        </h2>
        
        <div v-if="isLoadingPurchases" class="text-center py-8 text-gray-500">
          <i class="ri-loader-4-line animate-spin text-4xl mb-2"></i>
          <p>Loading purchases...</p>
        </div>
        <div v-else-if="shopTransactions.length === 0" class="text-center py-8 text-gray-500">
          <i class="ri-shopping-bag-line text-4xl mb-2"></i>
          <p>No purchases yet. Start shopping!</p>
        </div>
        
        <div v-else class="space-y-3">
          <div 
            v-for="transaction in shopTransactions"
            :key="transaction.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center">
                <i class="ri-shopping-cart-line text-red-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">{{ transaction.description }}</div>
                <div class="text-sm text-gray-500">{{ formatDate(transaction.created_at) }}</div>
              </div>
            </div>
            <div class="flex items-center gap-1 text-sm font-medium text-red-600">
              <img src="/coin.svg" class="coin-icon" alt="coin">
              <span>{{ transaction.amount }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Purchase Confirmation Modal -->
    <div v-if="showPurchaseModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center">
          <div class="w-20 h-20 mx-auto mb-4 bg-gradient-to-br rounded-xl flex items-center justify-center text-4xl"
               :class="selectedItem?.bgColor">
            {{ selectedItem?.emoji }}
          </div>
          
          <h3 class="text-xl font-bold text-gray-800 mb-2">Confirm Purchase</h3>
          <p class="text-gray-600 mb-4">
            Are you sure you want to buy <strong>{{ selectedItem?.name }}</strong>?
          </p>
          
          <div class="flex items-center justify-center gap-2 mb-6 text-lg">
            <span>Cost:</span>
            <img src="/coin.svg" class="coin-icon" alt="coin">
            <span class="font-bold">{{ selectedItem?.price }} coins</span>
          </div>
          
          <div class="flex gap-3">
            <button 
              @click="showPurchaseModal = false"
              class="flex-1 py-2 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="confirmPurchase"
              class="flex-1 py-2 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
            >
              Buy Now
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Money Conversion Request Modal -->
    <div v-if="showConversionModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
            <i class="ri-exchange-dollar-line text-3xl text-green-600"></i>
          </div>
          
          <h3 class="text-xl font-bold text-gray-800 mb-2">Request Money Conversion</h3>
          <p class="text-gray-600 mb-4">
            Convert {{ selectedConversion?.coins }} coins to ${{ selectedConversion?.dollars }}
          </p>
          
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-yellow-800">
              <i class="ri-information-line mr-1"></i>
              This request will be sent to your parent for approval.
            </p>
          </div>
          
          <div class="mb-4">
            <label class="block text-left text-sm font-medium text-gray-700 mb-2">
              What do you want to use this money for?
            </label>
            <textarea 
              v-model="conversionReason"
              placeholder="e.g., Save for a new toy, buy school supplies..."
              class="w-full p-3 border border-gray-300 rounded-lg resize-none"
              rows="3"
            ></textarea>
          </div>
          
          <div class="flex gap-3">
            <button 
              @click="showConversionModal = false"
              class="flex-1 py-2 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="submitConversionRequest"
              :disabled="!conversionReason.trim()"
              class="flex-1 py-2 px-4 bg-green-500 text-white rounded-lg font-medium hover:bg-green-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Send Request
            </button>
          </div>
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
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { apiService } from '@/services/api'
import { formatTransactionDate } from '@/utils/dateUtils'

const userStore = useUserStore()

// State
const selectedCategory = ref('digital')
const showPurchaseModal = ref(false)
const showConversionModal = ref(false)
const showSuccessMessage = ref(false)
const selectedItem = ref<ShopItem | null>(null)
const selectedConversion = ref<ConversionAmount | null>(null)
const conversionReason = ref('')
const successMessage = ref('')
const recentPurchases = ref<PurchaseHistory[]>([])
const isLoadingPurchases = ref(false)
const shopTransactions = ref<any[]>([])

// Interfaces
interface ShopItem {
  id: string
  name: string
  description: string
  price: number
  emoji: string
  category: string
  bgColor: string
  owned: boolean
}

interface ConversionAmount {
  coins: number
  dollars: number
}

interface PurchaseHistory {
  id: string
  name: string
  emoji: string
  price: number
  purchaseDate: string
}

// Categories for teens
const categories = [
  { id: 'digital', name: 'Digital Rewards', icon: 'ri-smartphone-line' },
  { id: 'education', name: 'Learning Tools', icon: 'ri-book-line' },
  { id: 'experiences', name: 'Experiences', icon: 'ri-map-pin-line' },
  { id: 'tech', name: 'Tech Accessories', icon: 'ri-computer-line' }
]

// Shop Items for teens
const shopItems = ref<ShopItem[]>([
  // Digital Rewards
  { id: '1', name: 'Spotify Premium', description: '1 month subscription', price: 100, emoji: '🎵', category: 'digital', bgColor: 'from-green-400 to-green-500', owned: false },
  { id: '2', name: 'Netflix Credit', description: '$10 streaming credit', price: 100, emoji: '📺', category: 'digital', bgColor: 'from-red-400 to-red-500', owned: false },
  { id: '3', name: 'Gaming Credit', description: '$5 game store credit', price: 50, emoji: '🎮', category: 'digital', bgColor: 'from-blue-400 to-blue-500', owned: false },
  { id: '4', name: 'App Store Credit', description: '$10 app store credit', price: 100, emoji: '📱', category: 'digital', bgColor: 'from-purple-400 to-purple-500', owned: false },
  
  // Learning Tools
  { id: '5', name: 'Online Course', description: 'Udemy course of choice', price: 200, emoji: '🎓', category: 'education', bgColor: 'from-indigo-400 to-indigo-500', owned: false },
  { id: '6', name: 'E-Book Credit', description: '$15 book store credit', price: 150, emoji: '📚', category: 'education', bgColor: 'from-orange-400 to-orange-500', owned: false },
  { id: '7', name: 'Language App', description: '3 months premium access', price: 180, emoji: '🗣️', category: 'education', bgColor: 'from-teal-400 to-teal-500', owned: false },
  
  // Experiences
  { id: '8', name: 'Movie Tickets', description: '2 movie theater tickets', price: 250, emoji: '🎬', category: 'experiences', bgColor: 'from-yellow-400 to-yellow-500', owned: false },
  { id: '9', name: 'Restaurant Voucher', description: '$20 dining credit', price: 200, emoji: '🍕', category: 'experiences', bgColor: 'from-red-400 to-orange-500', owned: false },
  { id: '10', name: 'Activity Pass', description: 'Local activity center pass', price: 300, emoji: '🎯', category: 'experiences', bgColor: 'from-pink-400 to-pink-500', owned: false },
  
  // Tech Accessories
  { id: '11', name: 'Phone Case', description: 'Premium protective case', price: 150, emoji: '📱', category: 'tech', bgColor: 'from-gray-400 to-gray-600', owned: false },
  { id: '12', name: 'Wireless Earbuds', description: 'Bluetooth earbuds', price: 500, emoji: '🎧', category: 'tech', bgColor: 'from-blue-500 to-purple-600', owned: false },
  { id: '13', name: 'Power Bank', description: 'Portable phone charger', price: 200, emoji: '🔋', category: 'tech', bgColor: 'from-green-400 to-blue-500', owned: false }
])

// Money conversion amounts for teens
const conversionAmounts: ConversionAmount[] = [
  { coins: 50, dollars: 5 },
  { coins: 100, dollars: 10 },
  { coins: 200, dollars: 20 },
  { coins: 500, dollars: 50 }
]

// Computed
const filteredItems = computed(() => 
  shopItems.value.filter(item => item.category === selectedCategory.value)
)

// Methods
const handlePurchase = (item: ShopItem) => {
  if (item.owned || userStore.totalCoins < item.price) return
  
  selectedItem.value = item
  showPurchaseModal.value = true
}

const confirmPurchase = async () => {
  if (!selectedItem.value) return
  
  const success = await userStore.spendCoins(
    selectedItem.value.price, 
    `Purchased: ${selectedItem.value.name}`,
    'shop'
  )
  
  if (success) {
    selectedItem.value.owned = true
    
    // Refresh shop transactions to show the new purchase
    await loadShopTransactions()
    
    showSuccessMessage.value = true
    successMessage.value = `You bought ${selectedItem.value.name}!`
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  
  showPurchaseModal.value = false
  selectedItem.value = null
}

const requestMoneyConversion = (amount: ConversionAmount) => {
  if (userStore.totalCoins < amount.coins) return
  
  selectedConversion.value = amount
  conversionReason.value = ''
  showConversionModal.value = true
}

const submitConversionRequest = async () => {
  if (!selectedConversion.value || !conversionReason.value.trim()) return
  
  const success = await userStore.requestMoneyConversion(
    selectedConversion.value.coins,
    selectedConversion.value.dollars,
    conversionReason.value
  )
  
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = 'Request sent to parent for approval!'
    
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  
  showConversionModal.value = false
  selectedConversion.value = null
  conversionReason.value = ''
}

// Load purchase history on mount
onMounted(async () => {
  await loadShopTransactions()
})

// Use the utility function for date formatting
const formatDate = formatTransactionDate

// Load shop transactions from API
const loadShopTransactions = async () => {
  try {
    if (!userStore.profile?.id) {
      console.log('⚠️ [TEEN SHOP] No user profile ID available for shop transactions')
      return
    }
    
    isLoadingPurchases.value = true
    const response = await apiService.getShopTransactions(userStore.profile.id)
    if (response.data) {
      shopTransactions.value = response.data
      console.log('✅ [TEEN SHOP] Loaded shop transactions:', shopTransactions.value.length)
    } else {
      console.error('❌ [TEEN SHOP] Failed to load shop transactions:', response.error)
      shopTransactions.value = []
    }
  } catch (error) {
    console.error('❌ [TEEN SHOP] Error loading shop transactions:', error)
    shopTransactions.value = []
  } finally {
    isLoadingPurchases.value = false
  }
}
</script>