<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-100 via-green-50 to-blue-100 p-4 pb-20">
    <div class="max-w-3xl mx-auto flex flex-col items-center">
      <!-- Back Button -->
      <div class="w-full flex justify-start mb-4">
        <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-full font-medium hover:bg-gray-300 transition-colors flex items-center gap-2" @click="goBackToGames">
          <i class="ri-arrow-left-line"></i> Back to Games
        </button>
      </div>
      <div v-if="!gameOver">
        <!-- Question UI -->
        <div class="mb-8 w-full flex flex-col items-center">
          <div class="text-lg font-semibold mb-2">Your Budget: <span class="font-bold text-blue-600">{{ currentSet.budget }}</span> coins</div>
          <div class="text-lg mb-2">Items you want: <span class="font-bold text-green-600">{{ currentSet.wantedItems.join(' & ') }}</span></div>
        </div>
        <div class="flex flex-row gap-4 mb-8 w-full max-w-xl justify-center">
          <div v-for="option in shopOptions" :key="option.id"
            :class="[
              'bg-white rounded-xl shadow p-4 flex flex-col items-center border-2',
              option.selected && option.id.startsWith('costly') ? 'border-red-500 bg-red-100' :
              option.selected && option.id.startsWith('cheap') ? 'border-green-500 bg-green-100' :
              'border-blue-200',
              answered && option.selected && option.id.startsWith('cheap') ? 'border-green-500 bg-green-100' : '',
              answered && option.selected && option.id.startsWith('costly') ? 'border-red-500 bg-red-100' : ''
            ]">
            <div class="text-3xl mb-1">{{ option.emoji }}</div>
            <div class="font-bold text-base mb-1">{{ option.label }}</div>
            <div class="text-blue-700 font-semibold mb-1">{{ option.price }} coins</div>
            <button
              class="px-3 py-1 bg-green-500 text-white rounded-full font-medium hover:bg-green-600 mt-1 text-sm"
              :disabled="answered || (option.id.startsWith('costly') && answered)"
              @click="purchase(option)"
            >Buy</button>
          </div>
        </div>
        <div v-if="showCongrats" class="mt-2 flex items-center justify-center gap-4 w-full max-w-md">
          <span class="text-3xl">🎉</span>
          <span class="text-lg font-bold text-green-700">Congratulations! Smart choice!</span>
          <button class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="nextSet">
            Next
          </button>
        </div>
        <div v-if="showReset" class="w-full flex justify-center">
          <button
            class="mt-2 px-6 py-2 rounded-full font-medium transition-colors"
            :class="canReset ? 'bg-gray-300 text-gray-800 hover:bg-gray-400' : 'bg-gray-100 text-gray-400 cursor-not-allowed'"
            :disabled="!canReset"
            @click="resetCostly"
          >Reset</button>
        </div>
        <div v-if="resultMessage && !showCongrats" class="mt-4 text-lg font-bold text-center" :class="resultSuccess ? 'text-green-700' : 'text-red-600'">
          <span v-if="resultEmoji">{{ resultEmoji }}</span> {{ resultMessage }}
        </div>
      </div>
      <div v-else class="mt-8 text-center">
        <div class="text-xl font-bold mb-2">Game Over!</div>
        <div class="text-lg mb-2">You answered {{ correctCount }} out of 3 sets correctly.</div>
        <div v-if="!alreadyCompleted && correctCount === 3" class="text-yellow-600 font-bold mb-2">Bonus: +10 coins for all correct!</div>
        <div v-if="!alreadyCompleted" class="text-green-700 font-bold mb-2">+{{ coinsAwarded }} coins for completing the task!</div>
        <div v-else class="text-gray-700 mb-2">(No coins earned for repeat completion)</div>
        <button class="mt-4 px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="restartGame">
          Play Again
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useChildStore } from '@/stores/child'
import { useUserStore } from '@/stores/user'
import apiService from '@/services/api'

const ACTIVITY_ID = 5 // Shopping Smart activity id
const childStore = useChildStore()
const userStore = useUserStore()
const router = useRouter()
const alreadyCompleted = computed(() => {
  const activity = childStore.activities.find(a => a.id == String(ACTIVITY_ID))
  return activity?.completed
})

const sets = [
  {
    budget: 30,
    wantedItems: ['Book', 'Game'],
    shopOptions: [
      { id: 'costly2', label: 'Costly Game', price: 28, emoji: '🎲', items: ['Game'] },
      { id: 'cheap1', label: 'Cheap Book', price: 12, emoji: '📚', items: ['Book'] },
      { id: 'costly1', label: 'Costly Book', price: 28, emoji: '📚', items: ['Book'] },
      { id: 'cheap2', label: 'Cheap Game', price: 12, emoji: '🎲', items: ['Game'] }
    ]
  },
  {
    budget: 25,
    wantedItems: ['Puzzle', 'Paint'],
    shopOptions: [
      { id: 'cheap2', label: 'Cheap Paint', price: 10, emoji: '🎨', items: ['Paint'] },
      { id: 'costly1', label: 'Costly Puzzle', price: 23, emoji: '🧩', items: ['Puzzle'] },
      { id: 'costly2', label: 'Costly Paint', price: 23, emoji: '🎨', items: ['Paint'] },
      { id: 'cheap1', label: 'Cheap Puzzle', price: 10, emoji: '🧩', items: ['Puzzle'] }
    ]
  },
  {
    budget: 40,
    wantedItems: ['Ball', 'Book'],
    shopOptions: [
      { id: 'costly2', label: 'Costly Book', price: 38, emoji: '📚', items: ['Book'] },
      { id: 'cheap2', label: 'Cheap Book', price: 16, emoji: '📚', items: ['Book'] },
      { id: 'cheap1', label: 'Cheap Ball', price: 16, emoji: '⚽', items: ['Ball'] },
      { id: 'costly1', label: 'Costly Ball', price: 38, emoji: '⚽', items: ['Ball'] }
    ]
  }
]

const currentSetIndex = ref(0)
const currentSet = computed(() => sets[currentSetIndex.value])
const shopOptions = ref(currentSet.value.shopOptions.map(o => ({ ...o, selected: false })))
const answered = ref(false)
const resultMessage = ref('')
const resultSuccess = ref(false)
const resultEmoji = ref('')
const correctCount = ref(0)
const gameOver = ref(false)
const selectedOptions = ref<string[]>([])
const showCongrats = ref(false)
const showReset = ref(true)
const coinsAwarded = ref(0)

function purchase(option: any) {
  if (answered.value) return
  // Costly item logic
  if (option.id.startsWith('costly')) {
    shopOptions.value.forEach(o => o.selected = false)
    option.selected = true
    selectedOptions.value = [option.id]
    answered.value = true
    resultMessage.value = `You bought the ${option.label} ${option.emoji}. You have ${currentSet.value.budget - option.price} coins left, but not enough to buy another item. You don't have any money left.`
    resultSuccess.value = false
    resultEmoji.value = option.emoji
    showCongrats.value = false
    showReset.value = true
    return
  }
  // Cheap item logic
  option.selected = !option.selected
  if (option.selected) {
    selectedOptions.value.push(option.id)
  } else {
    selectedOptions.value = selectedOptions.value.filter(id => id !== option.id)
  }
  // If both cheap items are selected, submit
  const cheapSelected = shopOptions.value.filter(o => o.id.startsWith('cheap') && o.selected)
  if (cheapSelected.length === 2) {
    answered.value = true
    const total = cheapSelected[0].price + cheapSelected[1].price
    resultMessage.value = `Smart choice! You bought both items (${cheapSelected[0].label} ${cheapSelected[0].emoji} and ${cheapSelected[1].label} ${cheapSelected[1].emoji}) and have ${currentSet.value.budget - total} coins left.`
    resultSuccess.value = true
    resultEmoji.value = `${cheapSelected[0].emoji} ${cheapSelected[1].emoji}`
    correctCount.value++
    showCongrats.value = true
    showReset.value = false
  }
}

const canReset = computed(() => shopOptions.value.some(o => o.selected && o.id.startsWith('costly')))

function resetCostly() {
  if (!canReset.value) return
  shopOptions.value.forEach(o => o.selected = false)
  selectedOptions.value = []
  answered.value = false
  resultMessage.value = ''
  resultSuccess.value = false
  resultEmoji.value = ''
  showCongrats.value = false
  showReset.value = true
}

function nextSet() {
  answered.value = false
  resultMessage.value = ''
  resultSuccess.value = false
  resultEmoji.value = ''
  selectedOptions.value = []
  showCongrats.value = false
  showReset.value = true
  currentSetIndex.value++
  if (currentSetIndex.value < sets.length) {
    shopOptions.value = sets[currentSetIndex.value].shopOptions.map(o => ({ ...o, selected: false }))
  } else {
    gameOver.value = true
    awardCoins()
  }
}

async function awardCoins() {
  if (alreadyCompleted.value) {
    coinsAwarded.value = 0
    return
  }
  let coins = 0
  const activity = childStore.activities.find(a => a.id == String(ACTIVITY_ID))
  if (correctCount.value === 3) {
    coins = (activity?.coins || 20) + 10
  } else {
    coins = activity?.coins || 20
  }
  coinsAwarded.value = coins
  await apiService.completeActivity(String(ACTIVITY_ID))
  await childStore.loadActivities()
  await userStore.addCoins(coins, 'Completed Shopping Smart', 'activity')
}

function restartGame() {
  currentSetIndex.value = 0
  shopOptions.value = sets[0].shopOptions.map(o => ({ ...o, selected: false }))
  answered.value = false
  resultMessage.value = ''
  resultSuccess.value = false
  resultEmoji.value = ''
  selectedOptions.value = []
  correctCount.value = 0
  gameOver.value = false
  showCongrats.value = false
  showReset.value = true
}

function goBackToGames() {
  router.push('/child/games')
}
</script>

<style scoped>
.bg-white {
  min-width: 120px;
  max-width: 140px;
}
</style>
