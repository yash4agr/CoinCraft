<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Activity Hub Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Activity Hub 🧠</h1>
      <p class="text-gray-600">Interactive learning modules to build financial skills</p>
    </div>

    <!-- Featured Advanced Budgeting Card -->
    <div class="bg-gradient-to-r from-purple-500 to-purple-700 rounded-2xl shadow-2xl p-8 mb-8 text-white">
      <div class="flex flex-col lg:flex-row items-center gap-8">
        <!-- Left Side: Content -->
        <div class="flex-1 text-center lg:text-left">
          <div class="text-6xl mb-4">📊</div>
          <h2 class="text-3xl font-bold mb-3">Advanced Budgeting</h2>
          <p class="text-purple-100 text-lg mb-4">
            Master advanced budgeting techniques and strategies. 
            Learn zero-based budgeting, envelope systems, and financial planning!
          </p>
          
          <!-- Features -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="flex items-center justify-center lg:justify-start gap-2">
              <i class="ri-time-line text-purple-200"></i>
              <span class="text-purple-100">30 min</span>
            </div>
            <div class="flex items-center justify-center lg:justify-start gap-2">
              <i class="ri-star-line text-purple-200"></i>
              <span class="text-purple-100">Intermediate</span>
            </div>
            <div class="flex items-center justify-center lg:justify-start gap-2">
              <i class="ri-coins-line text-purple-200"></i>
              <span class="text-purple-100">+40 coins</span>
            </div>
          </div>

          <!-- Start Button -->
          <button
            @click="openAdvancedBudgeting"
            class="bg-white text-purple-600 hover:bg-purple-50 px-8 py-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg"
          >
            🚀 Start Learning Now
          </button>
        </div>

        <!-- Right Side: Visual -->
        <div class="flex-1 flex justify-center">
          <div class="relative">
            <!-- Calculator Icon -->
            <div class="w-32 h-32 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <i class="ri-calculator-line text-6xl text-white"></i>
            </div>
            
            <!-- Floating Elements -->
            <div class="absolute -top-4 -right-4 w-16 h-16 bg-yellow-400 rounded-full flex items-center justify-center text-2xl">
              💰
            </div>
            <div class="absolute -bottom-4 -left-4 w-12 h-12 bg-blue-400 rounded-full flex items-center justify-center text-xl">
              📈
            </div>
          </div>
        </div>
      </div>
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
          @click="handleModuleClick(module)"
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

    <!-- Advanced Budgeting Modal -->
    <AdvancedBudgeting
      v-model="showAdvancedBudgetingModal"
      :coins="40"
      @completed="handleAdvancedBudgetingCompleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import AdventureCard from '@/components/shared/AdventureCard.vue'
import AchievementCard from '@/components/shared/AchievementCard.vue'
import AdvancedBudgeting from '@/components/explore/AdvancedBudgeting.vue'

const dashboardStore = useDashboardStore()

// Use learning modules from dashboard store
const learningModules = dashboardStore.learningModules

// Recent achievements
const recentAchievements = dashboardStore.recentAchievements

// Computed stats
const completedModules = computed(() => {
  return dashboardStore.completedModulesCount
})

const totalCoinsEarned = computed(() => {
  return dashboardStore.totalCoinsFromModules
})

const totalTimeSpent = computed(() => {
  return completedModules.value * 15 // Estimate 15 minutes per module
})

const nextModuleReward = computed(() => {
  const nextModule = learningModules.find(module => !module.completed)
  return nextModule ? nextModule.coins : 0
})

// Advanced Budgeting Modal
const showAdvancedBudgetingModal = ref(false)

const handleModuleClick = (module: any) => {
  console.log('📚 [TEEN_ACTIVITIES] Module clicked:', module.title)
  
  if (module.title === 'Advanced Budgeting') {
    console.log('📊 [TEEN_ACTIVITIES] Opening Advanced Budgeting modal...')
    showAdvancedBudgetingModal.value = true
  } else {
    // Handle other modules or show coming soon message
    alert(`🚧 ${module.title} is coming soon! Stay tuned for more learning modules.`)
  }
}

const handleAdvancedBudgetingCompleted = async (coinsEarned: number) => {
  console.log('🎉 [TEEN_ACTIVITIES] Advanced Budgeting completed! Coins earned:', coinsEarned)
  
  // Update the module status to completed
  const advancedBudgetingModule = learningModules.find(m => m.title === 'Advanced Budgeting')
  if (advancedBudgetingModule) {
    advancedBudgetingModule.completed = true
  }
  
  // Close the modal
  showAdvancedBudgetingModal.value = false
  
  // Show success message
  alert(`🎉 Congratulations! You completed the Advanced Budgeting module and earned ${coinsEarned} coins!`)
}

const openAdvancedBudgeting = () => {
  showAdvancedBudgetingModal.value = true
  console.log('📊 [TEEN_ACTIVITIES] Opening Advanced Budgeting modal...')
}
</script> 