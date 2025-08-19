<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 via-purple-50 to-blue-100 p-4 pb-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-store-fill text-pink-500 mr-3"></i>
          Treasure Shop
        </h1>
        <p class="text-gray-600 text-lg">Spend your coins on amazing treasures! ✨</p>
        
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
              ? 'bg-pink-500 text-white' 
              : 'bg-white text-gray-600 hover:bg-pink-100'"
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
              @click="handlePurchase(_item)"
              :disabled="userStore.totalCoins < item.price || item.owned"
              class="w-full py-2 px-3 rounded-lg font-medium transition-colors text-sm"
              :class="item.owned 
                ? 'bg-green-100 text-green-700 cursor-not-allowed' 
                : userStore.totalCoins >= item.price 
                  ? 'bg-pink-500 text-white hover:bg-pink-600' 
                  : 'bg-gray-200 text-gray-500 cursor-not-allowed'"
            >
              {{ item.owned ? 'Got it!' : userStore.totalCoins >= item.price ? 'Buy Now' : 'Need More Coins' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Special Rewards Section -->
      <div class="bg-gradient-to-r from-purple-400 to-pink-500 rounded-2xl p-6 text-white mb-8">
        <h2 class="text-2xl font-bold mb-4">
          <i class="ri-gift-line mr-2"></i>
          Ask Parent for Special Reward
        </h2>
        <p class="mb-4 opacity-90">Save up coins and ask your parent for something special!</p>
        
        <div class="bg-white/20 rounded-xl p-4 mb-4">
          <div class="text-center">
            <div class="text-lg font-semibold mb-2">Coin Value</div>
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
            v-for="amount in specialRewards"
            :key="amount.coins"
            @click="requestSpecialReward(amount)"
            :disabled="userStore.totalCoins < amount.coins"
            class="bg-white/20 hover:bg-white/30 disabled:bg-white/10 disabled:text-white/50 rounded-lg p-3 transition-colors"
          >
            <div class="text-sm font-medium">{{ amount.coins }} coins</div>
            <div class="text-lg font-bold">${{ amount.dollars }}</div>
          </button>
        </div>
      </div>

      <!-- My Treasures -->
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-4">
          <i class="ri-treasure-map-line mr-2"></i>
          My Treasures
        </h2>
        
        <div v-if="myTreasures.length === 0" class="text-center py-8 text-gray-500">
          <i class="ri-treasure-map-line text-4xl mb-2"></i>
          <p>No treasures yet. Start shopping!</p>
        </div>
        
        <div v-else class="grid grid-cols-3 md:grid-cols-6 gap-4">
          <div 
            v-for="treasure in myTreasures"
            :key="treasure.id"
            class="text-center p-3 bg-gray-50 rounded-lg"
          >
            <div class="text-3xl mb-2">{{ treasure.emoji }}</div>
            <div class="text-xs font-medium text-gray-700">{{ treasure.name }}</div>
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
          
          <h3 class="text-xl font-bold text-gray-800 mb-2">Buy This Treasure?</h3>
          <p class="text-gray-600 mb-4">
            Do you want to buy <strong>{{ selectedItem?.name }}</strong>?
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
              No Thanks
            </button>
            <button 
              @click="confirmPurchase"
              class="flex-1 py-2 px-4 bg-pink-500 text-white rounded-lg font-medium hover:bg-pink-600 transition-colors"
            >
              Yes, Buy It!
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Special Reward Request Modal -->
    <div v-if="showRewardModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 bg-purple-100 rounded-full flex items-center justify-center">
            <i class="ri-gift-line text-3xl text-purple-600"></i>
          </div>
          
          <h3 class="text-xl font-bold text-gray-800 mb-2">Ask for Special Reward</h3>
          <p class="text-gray-600 mb-4">
            Trade {{ selectedReward?.coins }} coins for ${{ selectedReward?.dollars }}
          </p>
          
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
            <p class="text-sm text-yellow-800">
              <i class="ri-information-line mr-1"></i>
              Your parent will decide if you can get this reward!
            </p>
          </div>
          
          <div class="mb-4">
            <label class="block text-left text-sm font-medium text-gray-700 mb-2">
              What do you want to buy with this money?
            </label>
            <textarea 
              v-model="rewardReason"
              placeholder="e.g., A new toy, art supplies, save for something special..."
              class="w-full p-3 border border-gray-300 rounded-lg resize-none"
              rows="3"
            ></textarea>
          </div>
          
          <div class="flex gap-3">
            <button 
              @click="showRewardModal = false"
              class="flex-1 py-2 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="submitRewardRequest"
              :disabled="!rewardReason.trim()"
              class="flex-1 py-2 px-4 bg-purple-500 text-white rounded-lg font-medium hover:bg-purple-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Ask Parent
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

const userStore = useUserStore()

// State
const selectedCategory = ref('stickers')
const showPurchaseModal = ref(false)
const showRewardModal = ref(false)
const showSuccessMessage = ref(false)
const selectedItem = ref<ShopItem | null>(null)
const selectedReward = ref<SpecialReward | null>(null)
const rewardReason = ref('')
const successMessage = ref('')
const myTreasures = ref<ShopItem[]>([])

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

interface SpecialReward {
  coins: number
  dollars: number
}

// Categories - Kid-friendly
const categories = [
  { id: 'stickers', name: 'Stickers', icon: 'ri-star-line' },
  { id: 'toys', name: 'Fun Toys', icon: 'ri-gamepad-line' },
  { id: 'art', name: 'Art Stuff', icon: 'ri-brush-line' },
  { id: 'books', name: 'Cool Books', icon: 'ri-book-line' }
]

// Special rewards - smaller amounts for kids
const specialRewards: SpecialReward[] = [
  { coins: 20, dollars: 2 },
  { coins: 50, dollars: 5 },
  { coins: 100, dollars: 10 },
  { coins: 200, dollars: 20 }
]

// Computed
const filteredItems = computed(() => 
  userStore.shopItems.map((item: any) => ({
    ...item,
    owned: userStore.ownedItems.includes(item.id)
  })).filter((item: any) => item.category === selectedCategory.value)
)

// Methods
const handlePurchase = (item: ShopItem) => {
  if (item.owned || userStore.totalCoins < item.price) return
  selectedItem.value = item
  showPurchaseModal.value = true
}

const confirmPurchase = async () => {
  if (!selectedItem.value) return
  const success = await userStore.purchaseShopItem(selectedItem.value.id)
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = `Asked parent to buy ${selectedItem.value.name}! 📨`
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  showPurchaseModal.value = false
  selectedItem.value = null
}

const requestSpecialReward = (reward: SpecialReward) => {
  if (userStore.totalCoins < reward.coins) return
  selectedReward.value = reward
  rewardReason.value = ''
  showRewardModal.value = true
}

const submitRewardRequest = async () => {
  if (!selectedReward.value || !rewardReason.value.trim()) return
  const success = await userStore.requestMoneyConversion(
    selectedReward.value.coins,
    selectedReward.value.dollars,
    rewardReason.value
  )
  if (success) {
    showSuccessMessage.value = true
    successMessage.value = 'Request sent to your parent! 📨'
    setTimeout(() => {
      showSuccessMessage.value = false
    }, 3000)
  }
  showRewardModal.value = false
  selectedReward.value = null
  rewardReason.value = ''
}

// Load owned items and shop items on mount
onMounted(async () => {
  await userStore.getShopItems()
  await userStore.getOwnedItems()
  myTreasures.value = userStore.shopItems
    .filter((item: any) => userStore.ownedItems.includes(item.id))
    .map((item: any) => ({ ...item, owned: true }))
})
</script>