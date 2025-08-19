<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 via-yellow-50 to-blue-100 p-4 pb-20">
    <div class="max-w-3xl mx-auto flex flex-col items-center">
      <!-- Back Button -->
      <div class="w-full flex justify-start mb-4">
        <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-full font-medium hover:bg-gray-300 transition-colors flex items-center gap-2" @click="goBackToGames">
          <i class="ri-arrow-left-line"></i> Back to Games
        </button>
      </div>
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
        Piggy Bank Adventure
      </h1>
      <p class="text-center text-gray-600 mb-8">Click the coins to collect them!</p>
      <div class="relative w-full h-96 mb-8">
        <!-- Piggy Bank -->
        <img ref="piggyBankRef" src="/src/assets/piggybank.png" alt="Piggy Bank" class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-40 h-40 z-10" @load="onPiggyBankLoad" />
        <!-- Floating Coins -->
        <div v-if="piggyBankLoaded" v-for="coin in coins" :key="coin.id">
          <img
            src="/coin.svg"
            alt="coin"
            class="absolute w-12 h-12 cursor-pointer coin"
            :style="coinStyle(coin)"
            @click="collectCoin(coin)"
          />
        </div>
      </div>
      <div v-if="showSuccess" class="mt-2 text-green-700 font-bold text-xl text-center">
        <i class="ri-check-line mr-2"></i>Task complete! +10 coins added to your piggy bank!
      </div>
      <div v-if="showMotivation" class="mt-2 text-blue-700 font-bold text-xl text-center">
        Yay, you collected all the coins! Saving coins helps you buy things you want to.
      </div>
      <button v-if="showSuccess || showMotivation" class="mt-4 px-6 py-3 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="restartGame">
        Play Again
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeUnmount, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChildStore } from '@/stores/child'
import apiService from '@/services/api'

const userStore = useUserStore()
const childStore = useChildStore()
const router = useRouter()
const ACTIVITY_ID = 1 // Piggy Bank Adventure activity id

const coinCount = 7
const coins = ref<{ id: number; x: number; y: number; collected: boolean; animating: boolean }[]>([])
const showSuccess = ref(false)
const showMotivation = ref(false)
const piggyBankRef = ref<HTMLImageElement | null>(null)
const piggyBankCenter = ref({ x: 240, y: 192 }) // Default center
const coinCircleRadius = 120
const piggyBankLoaded = ref(false)

const activityCompleted = computed(() => {
  const activity = childStore.activities.find(a => a.id == String(ACTIVITY_ID))
  return activity?.completed
})

function isMobile() {
  return window.innerWidth <= 768 || /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

function updatePiggyBankCenter() {
  if (piggyBankRef.value) {
    const rect = piggyBankRef.value.getBoundingClientRect()
    const parentRect = piggyBankRef.value.parentElement?.getBoundingClientRect()
    if (parentRect) {
      if (isMobile()) {
        // On mobile, adjust for possible nav overlays or layout shifts
        // Use viewport width/height for centering
        piggyBankCenter.value.x = window.innerWidth / 2
        piggyBankCenter.value.y = rect.top - parentRect.top + rect.height / 2
      } else {
        // Desktop logic (unchanged)
        piggyBankCenter.value.x = rect.left - parentRect.left + rect.width / 2
        piggyBankCenter.value.y = rect.top - parentRect.top + rect.height / 2
      }
    }
  }
}

function randomCirclePosition(i: number) {
  // Space coins evenly around the piggy bank in a circle
  const angle = (2 * Math.PI * i) / coinCount
  const x = piggyBankCenter.value.x + coinCircleRadius * Math.cos(angle) - 24 // 24 = half coin width
  const y = piggyBankCenter.value.y + coinCircleRadius * Math.sin(angle) - 24 // 24 = half coin height
  return { x, y }
}

function setupCoins() {
  coins.value = Array.from({ length: coinCount }, (_, i) => {
    const pos = randomCirclePosition(i)
    return { id: i, x: pos.x, y: pos.y, collected: false, animating: false }
  })
  showSuccess.value = false
}

function coinStyle(coin: { x: number; y: number; collected: boolean; animating: boolean }) {
  let style = {
    left: coin.x + 'px',
    top: coin.y + 'px',
    opacity: coin.collected ? 0 : 1,
    transition: 'all 0.7s cubic-bezier(.68,-0.55,.27,1.55)',
    zIndex: 5
  }
  if (coin.animating) {
    style.left = piggyBankCenter.value.x - 24 + 'px'
    style.top = piggyBankCenter.value.y - 24 + 'px'
  }
  return style
}

function collectCoin(coin: { id: number; x: number; y: number; collected: boolean; animating: boolean }) {
  if (coin.collected || coin.animating) return
  coin.animating = true
  setTimeout(() => {
    coin.collected = true
    coin.animating = false
    if (coins.value.every(c => c.collected)) {
      setTimeout(() => {
        completeActivity()
      }, 400)
    }
  }, 500)
}

async function completeActivity() {
  if (activityCompleted.value) {
    showSuccess.value = false
    showMotivation.value = true
    return
  }
  await apiService.completeActivity(String(ACTIVITY_ID))
  await childStore.loadActivities()
  await userStore.addCoins(10, 'Completed Piggy Bank Adventure', 'activity')
  showSuccess.value = true
  showMotivation.value = false
}

function restartGame() {
  updatePiggyBankCenter()
  setupCoins()
  showSuccess.value = false
  showMotivation.value = false
}

function onPiggyBankLoad() {
  piggyBankLoaded.value = true
  updatePiggyBankCenterAndCoins()
}

function updatePiggyBankCenterAndCoins() {
  updatePiggyBankCenter()
  setupCoins()
}

function goBackToGames() {
  router.push('/child/games')
}

onMounted(async () => {
  await nextTick()
  await childStore.loadActivities()
  window.scrollTo({ top: 0, behavior: 'smooth' })
  window.addEventListener('resize', updatePiggyBankCenterAndCoins)
  window.addEventListener('orientationchange', updatePiggyBankCenterAndCoins)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updatePiggyBankCenterAndCoins)
  window.removeEventListener('orientationchange', updatePiggyBankCenterAndCoins)
})
</script>

<style scoped>
.coin {
  z-index: 5;
}
</style>
