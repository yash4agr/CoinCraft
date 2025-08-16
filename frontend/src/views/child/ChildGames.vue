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
          @click="handleAdventureClick(adventure)"
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
import { ref, computed } from 'vue'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import PiggyBankAdventure from '@/components/explore/PiggyBankAdventure.vue'

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
    title: 'Investment Explorer',
    description: 'Learn about different ways to grow your money!',
    emoji: '📈',
    difficulty: 'hard' as const,
    coins: 30,
    completed: false,
    colorScheme: 'yellow' as const,
    buttonText: 'Explore'
  },
  {
    id: 6,
    title: 'Entrepreneur Quest',
    description: 'Start your own business and earn money!',
    emoji: '💼',
    difficulty: 'hard' as const,
    coins: 40,
    completed: false,
    colorScheme: 'purple' as const,
    buttonText: 'Start Quest'
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

// Handle adventure button clicks
const handleAdventureClick = (adventure: any) => {
  console.log('🎮 [CHILD_GAMES] Adventure clicked:', adventure.title)
  console.log('🎮 [CHILD_GAMES] Adventure data:', adventure)
  console.log('🎮 [CHILD_GAMES] Event received at:', new Date().toISOString())
  
  if (adventure.title === 'Piggy Bank Adventure') {
    // Open Piggy Bank Adventure modal/game
    console.log('🐷 [CHILD_GAMES] Opening Piggy Bank Adventure...')
    openPiggyBankAdventure()
  } else if (adventure.title === 'Needs vs Wants Game') {
    // Handle other games
    console.log('🎮 [CHILD_GAMES] Game not implemented yet:', adventure.title)
  } else {
    // Handle other games
    console.log('🎮 [CHILD_GAMES] Game not implemented yet:', adventure.title)
  }
}

// Piggy Bank Adventure functionality
const showPiggyBankModal = ref(false)

const openPiggyBankAdventure = () => {
  console.log('🐷 [CHILD_GAMES] Opening Piggy Bank Adventure...')
  showPiggyBankModal.value = true
}

// Handle Piggy Bank Adventure completion
const handlePiggyBankCompleted = async (coinsEarned: number) => {
  console.log('🎉 [CHILD_GAMES] Piggy Bank Adventure completed! Coins earned:', coinsEarned)
  
  // Update the adventure status to completed
  const piggyBankAdventure = adventures.value.find(a => a.id === 1)
  if (piggyBankAdventure) {
    piggyBankAdventure.completed = true
  }
  
  // Close the modal
  showPiggyBankModal.value = false
  
  // Show success message
  alert(`🎉 Congratulations! You completed the Piggy Bank Adventure and earned ${coinsEarned} coins!`)
}
</script> 