<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-indigo-100 p-4 pb-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-gamepad-fill text-purple-500 mr-3"></i>
          Choose Your Adventure!
        </h1>
        <p class="text-gray-600 text-lg">Learn about money while having fun! 🚀</p>
      </div>
      <div v-if="isLoading" class="text-center py-8 text-lg text-gray-500">Loading activities...</div>
      <!-- Adventure Games Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AdventureCard
          v-for="adventure in adventures"
          :key="adventure.id"
          :title="adventure.title"
          :description="adventure.description"
          :emoji="adventure.emoji"
          :difficulty="adventure.difficulty"
          :coins="adventure.coins"
          :completed="adventure.completed"
          :color-scheme="adventure.color_scheme"
          :button-text="adventure.completed ? 'Play Again' : adventure.button_text"
          :path="adventure.path || `/child/games/${adventure.id}`"
        />
      </div>
      <!-- Quick Stats -->
      <div class="mt-12 bg-white rounded-2xl shadow-sm p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          <i class="ri-trophy-line text-yellow-500"></i>
          Your Gaming Progress
        </h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <div class="text-2xl font-bold text-green-600">{{ completedCount }}</div>
            <div class="text-sm text-green-700">Games Completed</div>
          </div>
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <div class="text-2xl font-bold text-blue-600">{{ totalCoinsEarned }}</div>
            <div class="text-sm text-blue-700">Coins Earned</div>
          </div>
          <div class="text-center p-4 bg-purple-50 rounded-lg">
            <div class="text-2xl font-bold text-purple-600">{{ availableGames }}</div>
            <div class="text-sm text-purple-700">Available Games</div>
          </div>
          <div class="text-center p-4 bg-orange-50 rounded-lg">
            <div class="text-2xl font-bold text-orange-600">{{ nextReward }}</div>
            <div class="text-sm text-orange-700">Next Reward</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Piggy Bank Adventure Modal -->
    <PiggyBankAdventure
      v-model="showPiggyBankModal"
      :coins="10"
      @completed="handlePiggyBankCompleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import { useChildStore } from '@/stores/child'

const childStore = useChildStore()
const isLoading = ref(false)

onMounted(async () => {
  isLoading.value = true
  await childStore.loadActivities()
  isLoading.value = false
})

const adventures = computed(() => childStore.activities)

const completedCount = computed(() => adventures.value.filter(adventure => adventure.completed).length)
const totalCoinsEarned = computed(() => adventures.value.filter(adventure => adventure.completed).reduce((total, adventure) => total + adventure.coins, 0))
const availableGames = computed(() => adventures.value.filter(adventure => !adventure.completed).length)
const nextReward = computed(() => {
  const nextGame = adventures.value.find(adventure => !adventure.completed)
  return nextGame ? nextGame.coins : 0
})
</script>