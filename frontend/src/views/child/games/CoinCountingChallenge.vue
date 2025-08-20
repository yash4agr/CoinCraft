<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-yellow-50 to-green-100 p-4 pb-20">
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
        Coin Counting Challenge
      </h1>
      <p class="text-center text-gray-600 mb-8">Count the coins and enter the correct total!</p>

      <div v-if="!gameOver">
        <div class="flex flex-col items-center mb-8">
          <div class="text-lg font-semibold mb-4">Question {{ currentIndex + 1 }} of {{ questions.length }}</div>
          <div class="flex flex-col items-center">
            <div v-if="currentQuestion" class="mb-4">
              <div
                :class="[
                  'grid grid-cols-4 gap-4 justify-center items-center',
                  currentQuestion.coins.slice(0, 8).length > 4 ? 'grid-rows-2' : 'grid-rows-1'
                ]"
              >
                <img
                  v-for="coin in currentQuestion.coins.slice(0, 8)"
                  :key="coin.id"
                  :src="coin.img"
                  :alt="coin.value + ' rupee coin'"
                  :style="coin.value === 1 ? 'width:80px;height:80px;' : coin.value === 2 ? 'width:88px;height:88px;' : 'width:112px;height:112px;'"
                  class="object-contain mx-auto"
                />
              </div>
            </div>
            <input v-model.number="userAnswer" type="number" class="w-48 p-3 border border-gray-300 rounded-lg text-center text-lg font-semibold mb-2" placeholder="Total value" :disabled="answered" />
            <button v-if="!answered" class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600 mt-2" @click="submitAnswer">Submit</button>
          </div>
          <div v-if="feedback" class="mt-4">
            <span :class="feedback === 'correct' ? 'text-green-600 font-bold text-xl' : 'text-red-600 font-bold text-xl'">
              {{ feedback === 'correct' ? '✅ Correct!' : '❌ Wrong!' }}
            </span>
          </div>
          <div v-if="answered" class="mt-6">
            <button class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="nextQuestion">
              Next
            </button>
          </div>
        </div>
      </div>

        <div v-else class="flex flex-col items-center justify-center mt-16">
            <h2 class="text-2xl font-bold text-gray-800 mb-4">Game Over!</h2>
            <div class="text-lg text-gray-700 mb-2">
                You answered <span class="font-bold text-green-600">{{ score }}</span> out of {{ questions.length }} correctly.
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

const ACTIVITY_ID = 3 // Coin Counting Challenge, should match backend id
const childStore = useChildStore()
const userStore = useUserStore()

const baseCoins = 20
const bonusCoins = 10
const coinsEarned = computed(() => score.value === questions.length ? baseCoins + bonusCoins : baseCoins)
const bonusEarned = computed(() => score.value === questions.length)

// Coin image paths
const coinImages: Record<string, string[]> = {
  '1': [
    new URL('@/assets/coins/1/1_001.png', import.meta.url).href,
    new URL('@/assets/coins/1/1_002.png', import.meta.url).href
  ],
  '2': [
    new URL('@/assets/coins/2/2_001.png', import.meta.url).href,
    new URL('@/assets/coins/2/2_002.png', import.meta.url).href,
    new URL('@/assets/coins/2/2_003.png', import.meta.url).href
  ],
  '5': [
    new URL('@/assets/coins/5/5_001.png', import.meta.url).href,
    new URL('@/assets/coins/5/5_002.png', import.meta.url).href
  ],
  '10': [
    new URL('@/assets/coins/10/10_001.png', import.meta.url).href,
    new URL('@/assets/coins/10/10_002.png', import.meta.url).href
  ]
}

function getRandom(arr: any[] | undefined) {
  if (!arr || arr.length === 0) return ''
  return arr[Math.floor(Math.random() * arr.length)]
}

function makeCoins(value: number, count: number) {
  const img = getRandom(coinImages[String(value)])
  return Array.from({ length: count }, (_, i) => ({ id: `${value}_${i}`, value, img }))
}

const questions = [
  {
    id: 1,
    coins: [
      ...makeCoins(1, 2),
      ...makeCoins(2, 1)
    ],
    answer: 4
  },
  {
    id: 2,
    coins: [
      ...makeCoins(2, 2),
      ...makeCoins(5, 1)
    ],
    answer: 9
  },
  {
    id: 3,
    coins: [
      ...makeCoins(1, 3),
      ...makeCoins(10, 1)
    ],
    answer: 13
  },
  {
    id: 4,
    coins: [
      ...makeCoins(5, 2),
      ...makeCoins(2, 1)
    ],
    answer: 12
  },
  {
    id: 5,
    coins: [
      ...makeCoins(1, 1),
      ...makeCoins(2, 2),
      ...makeCoins(10, 1)
    ],
    answer: 15
  }
]

const currentIndex = ref(0)
const score = ref(0)
const gameOver = ref(false)
const userAnswer = ref<number | null>(null)
const answered = ref(false)
const feedback = ref('')

const currentQuestion = computed(() => questions[currentIndex.value])
const alreadyCompleted = computed(() => {
  const activity = childStore.activities.find(a => a.id == String(ACTIVITY_ID))
  return activity?.completed
})

function submitAnswer() {
  if (answered.value || userAnswer.value === null || !currentQuestion.value) return
  if (userAnswer.value === currentQuestion.value.answer) {
    score.value++
    feedback.value = 'correct'
  } else {
    feedback.value = 'wrong'
  }
  answered.value = true
}

function nextQuestion() {
  if (currentIndex.value < questions.length - 1) {
    currentIndex.value++
    userAnswer.value = null
    answered.value = false
    feedback.value = ''
  } else {
    handleGameOver()
    gameOver.value = true
  }
}

function restartGame() {
  currentIndex.value = 0
  score.value = 0
  userAnswer.value = null
  answered.value = false
  feedback.value = ''
  gameOver.value = false
}

async function handleGameOver() {
  if (alreadyCompleted.value) return
  await apiService.completeActivity(String(ACTIVITY_ID))
  await childStore.loadActivities()
  await userStore.addCoins(coinsEarned.value, 'Completed Coin Counting Challenge', 'activity')
}

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>
