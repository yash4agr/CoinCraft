<template>
  <div class="min-h-screen bg-gradient-to-br from-green-100 via-yellow-50 to-blue-100 p-4 pb-20">
    <!-- Back Button -->
    <div class="max-w-3xl mx-auto mb-4 flex justify-start">
      <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-full font-medium hover:bg-gray-300 transition-colors flex items-center gap-2" @click="showBackModal = true">
        <i class="ri-arrow-left-line"></i> Back to Games
      </button>
    </div>
    <!-- Confirmation Modal -->
    <div v-if="showBackModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">❓</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Leave Game?</h3>
          <p class="text-gray-600">Are you sure you want to go back? Your progress in this game will be lost.</p>
        </div>
        <div class="flex gap-3">
          <button @click="showBackModal = false" class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors">Cancel</button>
          <button @click="goBackToGames" class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">Yes, Go Back</button>
        </div>
      </div>
    </div>
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
        Budget Builder
      </h1>
      <p class="text-center text-gray-600 mb-8">Remove items until your basket fits the budget!</p>

      <div v-if="!gameOver">
        <div class="flex flex-col items-center mb-6">
          <div class="text-lg font-semibold mb-2">Budget: <span class="font-bold text-blue-600">{{ budget }}</span> coins</div>
          <div class="text-lg mb-2">Basket Total: <span :class="basketTotal > budget ? 'text-red-600' : 'text-green-600'">{{ basketTotal }}</span> coins</div>
          <div class="text-sm text-gray-500 mb-2">Task {{ currentTaskIndex + 1 }} of {{ budgetTasks.length }}</div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          <div
            v-for="item in allBasketItems"
            :key="item.id"
            class="bg-white rounded-xl shadow p-4 flex flex-col items-center"
            :class="item.included ? 'border-4 border-green-400' : 'border-4 border-gray-300 opacity-60'"
          >
            <div class="text-4xl mb-2">{{ item.emoji }}</div>
            <div class="font-bold text-lg mb-1">{{ item.name }}</div>
            <div class="text-blue-700 font-semibold mb-2">{{ item.cost }} coins</div>
            <button
              v-if="item.included"
              class="px-3 py-1 bg-red-200 text-red-800 rounded-full text-sm font-medium hover:bg-red-300"
              @click="toggleItem(item.id)"
            >Remove</button>
            <button
              v-else
              class="px-3 py-1 bg-green-200 text-green-800 rounded-full text-sm font-medium hover:bg-green-300"
              @click="toggleItem(item.id)"
            >Add</button>
          </div>
        </div>
        <div class="flex justify-center gap-4">
          <button v-if="basketTotal <= budget && currentTaskIndex < budgetTasks.length - 1" class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="nextTask">Next</button>
          <button class="px-6 py-2 bg-gray-300 text-gray-800 rounded-full font-medium hover:bg-gray-400" @click="skipTask">Skip</button>
          <button v-if="basketTotal <= budget && currentTaskIndex === budgetTasks.length - 1" class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="submitBasket">Submit</button>
        </div>
      </div>

        <div v-else class="flex flex-col items-center justify-center mt-16">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Great job!</h2>
            <div class="text-lg text-gray-700 mb-2">
                You completed <span class="font-bold text-green-600">{{ tasksCompleted }}</span> out of {{ budgetTasks.length }} tasks.
            </div>
            <div v-if="!alreadyCompleted" class="text-lg text-gray-700 mb-2">
                Coins earned: <span class="font-bold text-yellow-600">{{ coinsEarned }}</span>
                <span v-if="bonusEarned" class="ml-2 text-green-700 font-bold">(+10 bonus for all correct!)</span>
                </div>
                <div v-else class="text-lg text-gray-700 mb-2">
                (No coins earned for repeat completion)
            </div>
            <button class="mt-6 px-6 py-3 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="restartGame">
                Play Again
            </button>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChildStore } from '@/stores/child'
import { useUserStore } from '@/stores/user'
import apiService from '@/services/api'

const showBackModal = ref(false)
const router = useRouter()
function goBackToGames() {
  showBackModal.value = false
  router.push('/child/games')
}

const ACTIVITY_ID = 4 // Budget Builder activity id
const childStore = useChildStore()
const userStore = useUserStore()

const budgetTasks = [
  {
    budget: 20,
    items: [
      { id: 'toy', name: 'Toy Car', cost: 8, emoji: '🚗' },
      { id: 'book', name: 'Story Book', cost: 6, emoji: '📚' },
      { id: 'ball', name: 'Football', cost: 10, emoji: '⚽' },
      { id: 'snack', name: 'Snack Pack', cost: 4, emoji: '🍪' },
      { id: 'crayons', name: 'Crayons', cost: 3, emoji: '🖍️' },
      { id: 'game', name: 'Board Game', cost: 12, emoji: '🎲' }
    ]
  },
  {
    budget: 15,
    items: [
      { id: 'water', name: 'Water Bottle', cost: 7, emoji: '🧃' },
      { id: 'pencil', name: 'Pencil Box', cost: 5, emoji: '🖍️' },
      { id: 'book', name: 'Story Book', cost: 6, emoji: '📚' },
      { id: 'game', name: 'Board Game', cost: 12, emoji: '🎲' },
      { id: 'snack', name: 'Snack Pack', cost: 4, emoji: '🍪' },
      { id: 'ball', name: 'Football', cost: 10, emoji: '⚽' }
    ]
  },
  {
    budget: 25,
    items: [
      { id: 'teddy', name: 'Teddy Bear', cost: 15, emoji: '🧸' },
      { id: 'paint', name: 'Paint Set', cost: 8, emoji: '🎨' },
      { id: 'book', name: 'Story Book', cost: 6, emoji: '📚' },
      { id: 'crayons', name: 'Crayons', cost: 3, emoji: '🖍️' },
      { id: 'game', name: 'Board Game', cost: 12, emoji: '🎲' },
      { id: 'snack', name: 'Snack Pack', cost: 4, emoji: '🍪' }
    ]
  },
  {
    budget: 18,
    items: [
      { id: 'puzzle', name: 'Puzzle Book', cost: 9, emoji: '🧩' },
      { id: 'water', name: 'Water Bottle', cost: 7, emoji: '🧃' },
      { id: 'crayons', name: 'Crayons', cost: 3, emoji: '🖍️' },
      { id: 'toy', name: 'Toy Car', cost: 8, emoji: '🚗' },
      { id: 'snack', name: 'Snack Pack', cost: 4, emoji: '🍪' },
      { id: 'book', name: 'Story Book', cost: 6, emoji: '📚' }
    ]
  }
]

const currentTaskIndex = ref(0)
const currentTask = computed(() => budgetTasks[currentTaskIndex.value])
const allBasketItems = ref(currentTask.value.items.map(item => ({ ...item, included: true })))
const budget = computed(() => currentTask.value.budget)
const basketTotal = computed(() =>
  allBasketItems.value.filter(i => i.included).reduce((sum, item) => sum + item.cost, 0)
)

const baseCoins = 20
const bonusCoins = 10
const taskResults = ref<boolean[]>(Array(budgetTasks.length).fill(false)) // Track per-task success

const tasksCompleted = computed(() => taskResults.value.filter(Boolean).length)
const coinsEarned = computed(() => tasksCompleted.value === budgetTasks.length ? baseCoins + bonusCoins : baseCoins)
const bonusEarned = computed(() => tasksCompleted.value === budgetTasks.length)

const gameOver = ref(false)
const alreadyCompleted = computed(() => {
  const activity = childStore.activities.find(a => a.id == String(ACTIVITY_ID))
  return activity?.completed
})

function toggleItem(id: string) {
  const item = allBasketItems.value.find(i => i.id === id)
  if (item) item.included = !item.included
}

function nextTask() {
  taskResults.value[currentTaskIndex.value] = basketTotal.value <= budget.value
  if (currentTaskIndex.value < budgetTasks.length - 1) {
    currentTaskIndex.value++
    allBasketItems.value = currentTask.value.items.map(item => ({ ...item, included: true }))
  } else {
    gameOver.value = true
    handleGameOver()
  }
}

function skipTask() {
  // Record whether the current task was completed successfully (basket within budget)
  taskResults.value[currentTaskIndex.value] = basketTotal.value <= budget.value
  if (currentTaskIndex.value < budgetTasks.length - 1) {
    currentTaskIndex.value++
    allBasketItems.value = currentTask.value.items.map(item => ({ ...item, included: true }))
  } else {
    gameOver.value = true
    handleGameOver()
  }
}

function submitBasket() {
  // Record whether the last task was completed successfully
  taskResults.value[currentTaskIndex.value] = basketTotal.value <= budget.value
  gameOver.value = true
  handleGameOver()
}

function restartGame() {
  currentTaskIndex.value = 0
  allBasketItems.value = budgetTasks[0].items.map(item => ({ ...item, included: true }))
  gameOver.value = false
}

async function handleGameOver() {
  if (alreadyCompleted.value) return
  await apiService.completeActivity(String(ACTIVITY_ID))
  await childStore.loadActivities()
  await userStore.addCoins(coinsEarned.value, 'Completed Budget Builder', 'activity')
}

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>
