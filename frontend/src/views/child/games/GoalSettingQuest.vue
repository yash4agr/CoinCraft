<template>
  <div class="min-h-screen bg-gradient-to-br from-green-100 via-yellow-50 to-blue-100 p-4 pb-20">
    <div class="max-w-3xl mx-auto">
      <h2 class="text-3xl font-bold mb-6 text-center">Goal Setting Quest</h2>
      <!-- Stepper UI -->
      <div class="mb-6 flex justify-center gap-4">
        <div v-for="step in steps" :key="step.id" class="flex flex-col items-center">
          <div :class="['w-8 h-8 rounded-full flex items-center justify-center font-bold', currentStep === step.id ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-500']">
            {{ step.id }}
          </div>
          <span class="text-xs mt-1" :class="currentStep === step.id ? 'text-green-600 font-semibold' : 'text-gray-400'">{{ step.label }}</span>
        </div>
      </div>
      <!-- Step 1: Select Item -->
      <div v-if="currentStep === 1">
        <h3 class="text-lg font-semibold mb-4 text-center">Select an item to save for:</h3>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-6 mb-8">
          <button
            v-for="item in items"
            :key="item.name"
            @click="selectItem(_item)"
            :class="['flex flex-col items-center justify-center p-6 rounded-xl border-2 transition-colors cursor-pointer shadow selection-box', selectedItem?.name === item.name ? 'border-green-500 bg-green-700 text-white' : 'border-gray-300 bg-blue-700 text-white hover:border-green-200']"
          >
            <div class="text-5xl mb-2">{{ item.emoji }}</div>
            <div class="font-semibold text-lg">{{ item.name }}</div>
            <div class="text-sm text-gray-200">{{ item.cost }} coins</div>
          </button>
        </div>
        <div class="flex justify-end">
          <button
            :disabled="!selectedItem"
            @click="goToStep(2)"
            class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-full font-medium transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
      <!-- Step 2: Show Plan -->
      <div v-if="currentStep === 2">
        <div class="flex flex-col items-center mb-8">
          <div class="text-6xl mb-2">{{ selectedItem?.emoji }}</div>
          <div class="font-bold text-2xl mb-1">{{ selectedItem?.name }}</div>
          <div class="text-sm text-gray-500 mb-2">{{ selectedItem?.cost }} coins</div>
        </div>
        <div v-if="selectedItem && selectedItem.cost <= 1000">
          <p class="mb-2 text-center">Here's how you can save up for your goal in 7 days:</p>
          <div class="overflow-x-auto">
            <table class="calendar-table">
              <thead>
                <tr>
                  <th v-for="(day, _idx) in weekDays" :key="day" class="calendar-cell calendar-header">{{ day }}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td v-for="(amt, idx) in dailyPlan" :key="idx" class="calendar-cell">
                    <div class="font-bold">{{ amt }} coins</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="selectedItem">
          <p class="mb-2 text-center">This is a big goal! Let's see how weekly saving can help you reach it:</p>
          <div class="overflow-x-auto">
            <table class="calendar-table">
              <thead>
                <tr>
                  <th v-for="(week, _idx) in weekLabels" :key="week" class="calendar-cell calendar-header">{{ week }}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td v-for="(amt, idx) in weeklyPlan" :key="idx" class="calendar-cell">
                    <div class="font-bold">{{ amt }} coins</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="mt-2 text-sm text-gray-600 text-center">You can reach your goal in {{ weekLabels.length }} weeks if you save this amount each week!</p>
        </div>
        <div class="flex justify-between mt-8">
          <button
            @click="goToStep(1)"
            class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-2 rounded-full font-medium transition-colors"
          >
            Previous
          </button>
          <button
            @click="addGoalFromQuest"
            class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-full font-medium transition-colors"
          >
            <i class="ri-add-line mr-2"></i>Add as Goal
          </button>
        </div>
        <div v-if="showSuccessMessage" class="mt-6 text-green-600 font-semibold text-center">
          <i class="ri-check-line mr-1"></i>{{ successMessage }}
        </div>
        <div v-if="showCoinReward" class="mt-6 text-yellow-600 font-bold text-center text-xl">
          <i class="ri-coin-line mr-2"></i>+35 coins for completing this activity!
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChildStore } from '@/stores/child'
import apiService from '@/services/api'

const userStore = useUserStore()
const childStore = useChildStore()
const ACTIVITY_ID = 6 // Goal Setting Quest activity id

const steps = [
  { id: 1, label: 'Choose Item' },
  { id: 2, label: 'Saving Plan' }
]
const currentStep = ref(1)
const goToStep = async (step: number) => {
  // When going to step 2 for the first time, mark activity complete and show coins
  if (step === 2 && !activityCompleted.value) {
    await apiService.completeActivity(String(ACTIVITY_ID))
    await childStore.loadActivities()
    await userStore.addCoins(35, 'Completed Goal Setting Quest', 'activity')
    showCoinReward.value = true
    setTimeout(() => {
      showCoinReward.value = false
    }, 4000)
    activityCompleted.value = true
  }
  currentStep.value = step
}

const items = [
  { name: 'Book', cost: 150, emoji: '📚' },
  { name: 'Board Game', cost: 400, emoji: '🎲' },
  { name: 'Headphones', cost: 900, emoji: '🎧' },
  { name: 'Game Console', cost: 2500, emoji: '🎮' },
  { name: 'Bicycle', cost: 1800, emoji: '🚲' },
  { name: 'Tablet', cost: 1200, emoji: '💻' }
]

const selectedItem = ref<typeof items[0] | null>(null)
const selectItem = (item: typeof items[0]) => {
  selectedItem.value = item
}

const showSuccessMessage = ref(false)
const successMessage = ref('')
const showCoinReward = ref(false)
const activityCompleted = ref(false)

const weekDays = computed(() => {
  const today = new Date()
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(today)
    d.setDate(today.getDate() + i)
    return d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })
  })
})

const dailyPlan = computed(() => {
  if (!selectedItem.value) return []
  const total = selectedItem.value.cost
  const base = Math.floor(total / 7)
  const remainder = total % 7
  return Array.from({ length: 7 }, (_, i) => base + (i < remainder ? 1 : 0))
})

const weekLabels = computed(() => {
  if (!selectedItem.value) return []
  const total = selectedItem.value.cost
  let weeks = Math.ceil(total / 200)
  if (weeks < 4) weeks = 4
  if (weeks > 12) weeks = 12
  return Array.from({ length: weeks }, (_, i) => `Week ${i + 1}`)
})

const weeklyPlan = computed(() => {
  if (!selectedItem.value) return []
  const total = selectedItem.value.cost
  const weeks = weekLabels.value.length
  const base = Math.floor(total / weeks)
  const remainder = total % weeks
  return Array.from({ length: weeks }, (_, i) => base + (i < remainder ? 1 : 0))
})

// Fixed goal creation code
const addGoalFromQuest = async () => {
  if (!selectedItem.value) return;
  await userStore.createGoal({
    title: selectedItem.value.name,
    description: `Saving for ${selectedItem.value.name} via Goal Setting Quest`,
    target_amount: selectedItem.value.cost,
    current_amount: 0,
    icon: selectedItem.value.emoji === '📚' ? 'ri-book-line' :
          selectedItem.value.emoji === '🎲' ? 'ri-gamepad-line' :
          selectedItem.value.emoji === '🎧' ? 'ri-headphone-line' :
          selectedItem.value.emoji === '🎮' ? 'ri-gamepad-line' :
          selectedItem.value.emoji === '🚲' ? 'ri-bike-line' :
          selectedItem.value.emoji === '💻' ? 'ri-smartphone-line' :
          'ri-gift-line',
    category: 'wants'
  });
  successMessage.value = `Goal "${selectedItem.value.name}" added!`;
  showSuccessMessage.value = true;
  setTimeout(() => {
    showSuccessMessage.value = false;
  }, 3000);
}

onMounted(() => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})
</script>

<style scoped>
.selection-box {
  border: 2px solid #38bdf8;
}
.calendar-table {
  border-collapse: separate;
  border-spacing: 0 8px;
  width: 100%;
}
.calendar-header {
  background: #bae6fd;
  color: #2563eb;
  font-weight: bold;
  border-radius: 8px 8px 0 0;
  padding: 8px 0;
}
.calendar-cell {
  background: #e0f2fe;
  border-radius: 8px;
  text-align: center;
  padding: 16px 0;
  min-width: 100px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  border: 2px solid #38bdf8;
}
select {
  background: #f9fafb;
}
th, td {
  text-align: center;
}
</style>
