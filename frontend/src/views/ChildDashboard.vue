<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Today's Goals Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Today's Goals 🎯</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <ProgressCard
          v-for="goal in todaysGoals"
          :key="goal.id"
          :title="goal.title"
          :current="goal.current"
          :total="goal.total"
          :icon="goal.icon"
          :color-scheme="goal.colorScheme"
        />
      </div>
    </div>

    <!-- Choose Your Adventure Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Choose Your Adventure! 🚀</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
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
    </div>

    <!-- Recent Achievements Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Recent Achievements 🏆</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AchievementCard
          v-for="achievement in achievements"
          :key="achievement.id"
          :title="achievement.title"
          :description="achievement.description"
          :icon="achievement.icon"
          :badge="achievement.badge"
          :coins="achievement.coins"
          :date="achievement.date"
          :color-scheme="achievement.colorScheme"
        />
      </div>
    </div>

    <!-- Your Learning Journey Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Your Learning Journey 📚</h2>
      <div class="space-y-3">
        <JourneyCard
          v-for="journey in learningJourney"
          :key="journey.id"
          :title="journey.title"
          :description="journey.description"
          :status="journey.status"
          :icon="journey.icon"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import ProgressCard from '@/components/shared/ProgressCard.vue'
import AchievementCard from '@/components/shared/AchievementCard.vue'
import JourneyCard from '@/components/shared/JourneyCard.vue'

// Today's Goals Data
const todaysGoals = ref([
  {
    id: 1,
    title: 'Read Lessons',
    current: 2,
    total: 3,
    icon: 'ri-book-open-line',
    colorScheme: 'orange' as const
  },
  {
    id: 2,
    title: 'Earn Coins',
    current: 45,
    total: 50,
    icon: 'ri-coins-line',
    colorScheme: 'blue' as const
  },
  {
    id: 3,
    title: 'Complete Games',
    current: 1,
    total: 2,
    icon: 'ri-gamepad-line',
    colorScheme: 'green' as const
  },
  {
    id: 4,
    title: 'Practice Time',
    current: 15,
    total: 20,
    icon: 'ri-time-line',
    colorScheme: 'purple' as const
  }
])

// Adventures Data
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

// Achievements Data
const achievements = ref([
  {
    id: 1,
    title: 'First Steps',
    description: 'Completed your first lesson!',
    icon: 'ri-foot-print-line',
    badge: 'Beginner',
    coins: 10,
    date: 'Today',
    colorScheme: 'green' as const
  },
  {
    id: 2,
    title: 'Coin Collector',
    description: 'Earned your first 50 coins.',
    icon: 'ri-treasure-map-line',
    badge: 'Collector',
    coins: 15,
    date: 'Yesterday',
    colorScheme: 'orange' as const
  },
  {
    id: 3,
    title: 'Streak Master',
    description: 'Completed 5 days in a row!',
    icon: 'ri-fire-line',
    badge: 'Dedicated',
    coins: 25,
    date: '2 days ago',
    colorScheme: 'blue' as const
  }
])

// Learning Journey Data
const learningJourney = ref([
  {
    id: 1,
    title: 'Money Basics',
    description: 'Learn what money is and why we use it',
    status: 'completed' as const,
    icon: 'ri-money-dollar-circle-line'
  },
  {
    id: 2,
    title: 'Counting Coins',
    description: 'Practice identifying and counting different coins',
    status: 'completed' as const,
    icon: 'ri-coins-line'
  },
  {
    id: 3,
    title: 'Saving Strategies',
    description: 'Discover fun ways to save your money',
    status: 'current' as const,
    icon: 'ri-safe-line'
  },
  {
    id: 4,
    title: 'Spending Wisely',
    description: 'Learn how to make smart spending choices',
    status: 'locked' as const,
    icon: 'ri-shopping-cart-line'
  },
  {
    id: 5,
    title: 'Setting Goals',
    description: 'Create and work towards your money goals',
    status: 'locked' as const,
    icon: 'ri-flag-line'
  }
])
</script>

