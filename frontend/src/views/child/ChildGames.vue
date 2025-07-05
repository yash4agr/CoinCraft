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

      <!-- Adventure Games Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AdventureCard
          v-for="adventure in adventures"
          :key="adventure.id"
          :title="adventure.title"
          :description="adventure.description"
          :emoji="adventure.emoji"
          :difficulty="adventure.difficulty"
          :coins="adventure.coins"
          :completed="adventure.completed"
          :color-scheme="adventure.colorScheme"
          :button-text="adventure.buttonText"
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AdventureCard from '@/components/shared/AdventureCard.vue'

// Adventures Data - Same as dashboard for consistency
const adventures = ref([
  {
    id: 1,
    title: 'Piggy Bank Adventure',
    description: 'Learn how to save money with your digital piggy bank!',
    emoji: '🐷',
    difficulty: 'easy' as const,
    coins: 10,
    completed: false,
    colorScheme: 'pink' as const,
    buttonText: 'Start Saving!'
  },
  {
    id: 2,
    title: 'Needs vs Wants Game',
    description: 'Discover the difference between things you need and want.',
    emoji: '🤔',
    difficulty: 'easy' as const,
    coins: 15,
    completed: true,
    colorScheme: 'teal' as const,
    buttonText: 'Play Again'
  },
  {
    id: 3,
    title: 'Coin Counting Challenge',
    description: 'Practice counting coins and making change!',
    emoji: '🪙',
    difficulty: 'medium' as const,
    coins: 20,
    completed: false,
    colorScheme: 'blue' as const,
    buttonText: 'Start Challenge'
  },
  {
    id: 4,
    title: 'Budget Builder',
    description: 'Create your first budget and learn to plan ahead.',
    emoji: '📊',
    difficulty: 'medium' as const,
    coins: 25,
    completed: false,
    colorScheme: 'green' as const,
    buttonText: 'Build Budget'
  },
  {
    id: 5,
    title: 'Shopping Smart',
    description: 'Learn smart shopping tips and compare prices.',
    emoji: '🛒',
    difficulty: 'hard' as const,
    coins: 30,
    completed: false,
    colorScheme: 'yellow' as const,
    buttonText: 'Shop Smart'
  },
  {
    id: 6,
    title: 'Goal Setting Quest',
    description: 'Set and achieve your financial goals step by step.',
    emoji: '🎯',
    difficulty: 'hard' as const,
    coins: 35,
    completed: false,
    colorScheme: 'purple' as const,
    buttonText: 'Set Goals'
  }
])

// Computed stats for progress section
const completedCount = computed(() => {
  return adventures.value.filter(adventure => adventure.completed).length
})

const totalCoinsEarned = computed(() => {
  return adventures.value
    .filter(adventure => adventure.completed)
    .reduce((total, adventure) => total + adventure.coins, 0)
})

const availableGames = computed(() => {
  return adventures.value.filter(adventure => !adventure.completed).length
})

const nextReward = computed(() => {
  const nextGame = adventures.value.find(adventure => !adventure.completed)
  return nextGame ? nextGame.coins : 0
})
</script> 