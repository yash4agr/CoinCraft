<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Activity Hub Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Activity Hub 🧠</h1>
      <p class="text-gray-600">Interactive learning modules to build financial skills</p>
    </div>

    <!-- Learning Modules -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Learning Modules</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AdventureCard
          v-for="module in learningModules"
          :key="module.id"
          :title="module.title"
          :description="module.description"
          :emoji="module.emoji"
          :difficulty="module.difficulty"
          :coins="module.coins"
          :completed="module.completed"
          :color-scheme="module.colorScheme"
          :button-text="module.buttonText"
        />
      </div>
    </div>

    <!-- Progress Tracker -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Your Learning Progress 📈</h2>
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 bg-green-50 rounded-lg">
            <div class="text-2xl font-bold text-green-600">{{ completedModules }}</div>
            <div class="text-sm text-green-700">Modules Completed</div>
          </div>
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <div class="text-2xl font-bold text-blue-600">{{ totalCoinsEarned }}</div>
            <div class="text-sm text-blue-700">Coins Earned</div>
          </div>
          <div class="text-center p-4 bg-purple-50 rounded-lg">
            <div class="text-2xl font-bold text-purple-600">{{ totalTimeSpent }}</div>
            <div class="text-sm text-purple-700">Minutes Learning</div>
          </div>
          <div class="text-center p-4 bg-orange-50 rounded-lg">
            <div class="text-2xl font-bold text-orange-600">{{ nextModuleReward }}</div>
            <div class="text-sm text-orange-700">Next Reward</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Learning Paths -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Recommended Learning Paths 🛤️</h2>
      <div class="space-y-4">
        <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-200">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <i class="ri-briefcase-line text-2xl text-blue-600"></i>
            </div>
            <div>
              <h3 class="font-bold text-gray-800">Future Entrepreneur</h3>
              <p class="text-sm text-gray-600">Learn business and entrepreneurship fundamentals</p>
            </div>
            <div class="ml-auto text-blue-600 font-semibold">3/5 modules</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-500 h-2 rounded-full" style="width: 60%"></div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-green-200">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <i class="ri-line-chart-line text-2xl text-green-600"></i>
            </div>
            <div>
              <h3 class="font-bold text-gray-800">Smart Investor</h3>
              <p class="text-sm text-gray-600">Understand investments and building wealth</p>
            </div>
            <div class="ml-auto text-green-600 font-semibold">1/4 modules</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-green-500 h-2 rounded-full" style="width: 25%"></div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-purple-200">
          <div class="flex items-center gap-4 mb-4">
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
              <i class="ri-wallet-3-line text-2xl text-purple-600"></i>
            </div>
            <div>
              <h3 class="font-bold text-gray-800">Budget Master</h3>
              <p class="text-sm text-gray-600">Master personal finance and budgeting skills</p>
            </div>
            <div class="ml-auto text-purple-600 font-semibold">2/3 modules</div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-purple-500 h-2 rounded-full" style="width: 67%"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Achievement Showcase -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Recent Achievements 🏆</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <AchievementCard
          v-for="achievement in recentAchievements"
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import AchievementCard from '@/components/shared/AchievementCard.vue'

// Teen learning modules - more sophisticated than child activities
const learningModules = ref([
  {
    id: 1,
    title: 'Start a Business',
    description: 'Interactive story with choices. Earn 25-50 coins based on decisions.',
    emoji: '🚀',
    difficulty: 'medium' as const,
    coins: 35,
    completed: false,
    colorScheme: 'blue' as const,
    buttonText: 'Start Journey'
  },
  {
    id: 2,
    title: 'Job Earning Scenarios',
    description: 'Compare different career paths. Bonus: Salary vs hourly decisions.',
    emoji: '💼',
    difficulty: 'medium' as const,
    coins: 30,
    completed: true,
    colorScheme: 'green' as const,
    buttonText: 'Replay'
  },
  {
    id: 3,
    title: 'Smart Spending',
    description: 'Real-world shopping challenges. Budget constraints & choices.',
    emoji: '🛒',
    difficulty: 'easy' as const,
    coins: 25,
    completed: true,
    colorScheme: 'yellow' as const,
    buttonText: 'Try Again'
  },
  {
    id: 4,
    title: 'Investment Basics',
    description: 'Learn about stocks, bonds, and compound interest.',
    emoji: '📈',
    difficulty: 'hard' as const,
    coins: 45,
    completed: false,
    colorScheme: 'purple' as const,
    buttonText: 'Start Learning'
  },
  {
    id: 5,
    title: 'Banking & Credit',
    description: 'Understand bank accounts, loans, and building credit.',
    emoji: '🏦',
    difficulty: 'hard' as const,
    coins: 40,
    completed: false,
    colorScheme: 'teal' as const,
    buttonText: 'Explore'
  },
  {
    id: 6,
    title: 'Tax Fundamentals',
    description: 'Why we pay taxes and how they work in society.',
    emoji: '📊',
    difficulty: 'medium' as const,
    coins: 35,
    completed: false,
    colorScheme: 'pink' as const,
    buttonText: 'Learn More'
  }
])

// Recent achievements
const recentAchievements = ref([
  {
    id: 1,
    title: 'Career Explorer',
    description: 'Completed Job Earning Scenarios module',
    icon: 'ri-briefcase-line',
    badge: 'Achiever',
    coins: 30,
    date: 'Today',
    colorScheme: 'green' as const
  },
  {
    id: 2,
    title: 'Smart Shopper',
    description: 'Mastered the Smart Spending challenge',
    icon: 'ri-shopping-cart-line',
    badge: 'Expert',
    coins: 25,
    date: 'Yesterday',
    colorScheme: 'yellow' as const
  },
  {
    id: 3,
    title: 'Learning Streak',
    description: 'Completed modules 5 days in a row',
    icon: 'ri-fire-line',
    badge: 'Dedicated',
    coins: 50,
    date: '2 days ago',
    colorScheme: 'orange' as const
  }
])

// Computed stats
const completedModules = computed(() => {
  return learningModules.value.filter(module => module.completed).length
})

const totalCoinsEarned = computed(() => {
  return learningModules.value
    .filter(module => module.completed)
    .reduce((total, module) => total + module.coins, 0)
})

const totalTimeSpent = computed(() => {
  return completedModules.value * 15 // Estimate 15 minutes per module
})

const nextModuleReward = computed(() => {
  const nextModule = learningModules.value.find(module => !module.completed)
  return nextModule ? nextModule.coins : 0
})
</script> 