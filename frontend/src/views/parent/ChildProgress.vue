<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-blue-600">Child Progress</h1>
        <p class="text-gray-600">Track your child's learning journey and achievements</p>
      </div>
      <button
        class="btn-primary flex items-center gap-2"
        :class="{ 'opacity-50 cursor-not-allowed': exporting }"
        :disabled="exporting"
        @click="openExport"
      >
        <i class="mdi mdi-download"></i> Export Report
      </button>
    </div>

    <!-- Child & Time Selector -->
    <div class="bg-white rounded-lg shadow p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="font-medium text-gray-700">Child</label>
        <select v-model="selectedChildId" @change="loadChildProgress" class="input-base">
          <option value="" disabled>Select a child</option>
          <option v-for="c in children" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div>
        <label class="font-medium text-gray-700">Time Period</label>
        <select v-model="timeframe" @change="loadChildProgress" class="input-base">
          <option v-for="tf in timeframes" :key="tf.value" :value="tf.value">{{ tf.title }}</option>
        </select>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="space-y-4">
      <div class="h-20 bg-gray-200 rounded animate-pulse"></div>
      <div class="h-60 bg-gray-200 rounded animate-pulse"></div>
    </div>

    <!-- Main Content -->
    <div v-else-if="selectedChild">
      <!-- Stats -->
      <div class="w-full max-w-4xl mx-auto px-4">
        <StatCard title="Total Rewards" :value="stats.totalRewards" icon="mdi-trophy" bg="bg-green-100"/>
        <StatCard title="Lessons Completed" :value="stats.lessonsCompleted" icon="mdi-book-open" bg="bg-blue-100"/>
        <StatCard title="Coins Earned" :value="stats.coinsEarned" icon="mdi-coin" bg="bg-yellow-100"/>
        <StatCard title="Goals Achieved" :value="stats.goalsAchieved" icon="mdi-target" bg="bg-teal-100"/>
      </div>

      
       <div class="flex flex-col lg:flex-row gap-4">
           <div class="bg-white rounded-lg shadow p-5 grid grid-cols-1 md:grid-cols-2 gap-4">
                   <!-- Charts & Progress -->
               <div  class="create-task" style="width: 560px;">
                    <div style="width: 100%; padding: 10px;">
                        <div>
                            <p class="text-2xl font-bold text-blue-600">Progress Chart</p>
                            <p class="text-sm">Learning progress visualization</p>
                            <div class="mb-4">
                                <Card title="Subject Performance">
                                    <div v-for="s in subjectProgress" :key="s.name">
                                    <div class="flex justify-between text-sm">
                                        <span>{{ s.name }}</span><span>{{ s.progress }}%</span>
                                    </div>
                                    <progress class="w-full h-2" :value="s.progress" max="100"></progress>
                                    </div>
                                </Card>
                                <Card title="Current Streak" icon="mdi-fire">
                                    <div class="text-center">
                                    <p class="text-3xl font-bold text-yellow-600">{{ stats.currentStreak }} Days</p>
                                    </div>
                                </Card>
                            </div>
                        </div>
                    </div>
                </div>
            <div>
                <div class="create-task" style="width: 560px;">
                 <!-- Recent Activities -->
                <div>
                    <h2 class="text-2xl font-bold text-blue-600">Recent Activities</h2>
                    <div v-for="a in recentActivities" :key="a.id" class="border-l-4 pl-4" :class="getActivityColor(a.type)">
                        <div class="text-sm text-gray-500">{{ formatTime(a.timestamp) }}</div>
                        <span>
                        <p class="font-medium">{{ a.title }}</p>
                        <p class="text-sm text-gray-600">{{ a.description }}</p>
                        </span>

                        <span v-if="a.reward" class="text-sm text-yellow-600">+{{ a.reward }} coins</span>
                    </div>
                </div>
                </div>
            </div>
          </div>
      </div>



    </div>
  </div>
       <!-- Goals & Achievements -->
      <div class="bg-white rounded-lg shadow p-5 grid grid-cols-1 md:grid-cols-2 gap-4" style="margin: 20px;">
        <Card title="Active Goals" icon="mdi-target">
          <template v-if="activeGoals.length === 0">
            <p class="text-center text-gray-500 py-6">No active goals</p>
          </template>
          <template v-else>
            <div v-for="g in activeGoals" :key="g.id" class="border rounded p-4 mb-3">
              <div class="flex justify-between">
                <p class="font-medium">{{ g.title }}</p>
                <span class="text-sm" :class="getGoalStatusColor(g.status)">{{ g.status }}</span>
              </div>
              <progress class="w-full h-2 mt-2" :value="(g.currentValue / g.targetValue) * 100" max="100"></progress>
            </div>
          </template>
        </Card>
        <Card title="Recent Achievements" icon="mdi-medal">
          <template v-if="achievements.length === 0">
            <p class="text-center text-gray-500 py-6">No achievements yet</p>
          </template>
          <template v-else>
            <div v-for="a in achievements" :key="a.id" class="flex items-center border rounded p-3 mb-3">
              <i :class="`mdi ${a.icon} text-2xl mr-3 text-${a.rarity}-500`"></i>
              <div class="flex-1">
                <p class="font-medium">{{ a.title }}</p>
                <span class="text-sm text-gray-600">{{ a.description }}</span>
                <span class="text-sm text-gray-500 p-5">{{ formatDate(a.earnedAt) }}</span>
              </div>
            
            </div>
          </template>
        </Card>
        <!-- Export Modal -->
    <Modal v-model="exportDialog">
      <h3 class="text-lg font-semibold mb-4">Export Progress Report</h3>
      <select v-model="exportFormat" class="input-base mb-4">
        <option v-for="f in exportFormats" :key="f">{{ f }}</option>
      </select>
      <label class="flex items-center gap-2 mb-4">
        <input type="checkbox" v-model="includeCharts" />
        Include charts
      </label>
      <div class="flex justify-end gap-2">
        <button @click="exportDialog=false" class="btn-secondary">Cancel</button>
        <button @click="confirmExport" class="btn-primary" :class="{ 'opacity-50': exporting }" :disabled="exporting">
          {{ exporting ? 'Exporting...' : 'Export' }}
        </button>
      </div>
    </Modal>
    

  

    
  </div>
  <!-- Snackbar -->
   <div class="snackbar">
       <Snackbar v-if="snackbar.show" :type="snackbar.color">
  {{ snackbar.message }}
   </Snackbar>
   </div>
    
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import type { User, Goal, Achievement } from '@/types'

// Data
const loading = ref(false)
const exporting = ref(false)
const selectedChildId = ref<string>('')
const timeframe = ref('month')
const exportDialog = ref(false)

const exportFormats = ['PDF', 'Excel', 'CSV']
const exportFormat = ref('PDF')
const includeCharts = ref(true)


const exportProgress = () => {
  if (!selectedChild.value) {
    showSnackbar('Please select a child first', 'warning')
    return
  }
  exportDialog.value = true
}

const confirmExport = async () => {
  exporting.value = true
  try {
    // Simulate export process
    await new Promise(resolve => setTimeout(resolve, 2000))
    showSnackbar(`Progress report exported as ${exportFormat.value}`, 'success')
    exportDialog.value = false
  } catch (error) {
    showSnackbar('Failed to export report', 'error')
  } finally {
    exporting.value = false
  }
}

function openExport() {
  exporting.value = true
}

const children = ref<User[]>([
  { id: '1', name: 'Luna', email: 'emma@example.com', role: 'child', avatar: '' },
  { id: '2', name: 'Harry', email: 'liam@example.com', role: 'child', avatar: '' }
])

const timeframes = [
  { title: 'Last Week', value: 'week' },
  { title: 'Last Month', value: 'month' },
  { title: 'Last 3 Months', value: 'quarter' },
  { title: 'Last Year', value: 'year' }
]

const selectedChild = computed(() => 
  children.value.find(child => child.id === selectedChildId.value)
)

const stats = reactive({
  totalRewards: 127,
  lessonsCompleted: 45,
  coinsEarned: 2840,
  goalsAchieved: 8,
  currentStreak: 12
})

const subjectProgress = ref([
  { name: 'Math', progress: 85 },
  { name: 'Reading', progress: 92 },
  { name: 'Science', progress: 78 },
  { name: 'Art', progress: 95 }
])

const recentActivities = ref([
  {
    id: '1',
    type: 'lesson',
    title: 'Completed Math Lesson',
    description: 'Addition and Subtraction Basics',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    reward: 50
  },
  {
    id: '2',
    type: 'achievement',
    title: 'Achievement Unlocked',
    description: 'Reading Champion - Read 5 books this week',
    timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000),
    reward: 100
  },
  {
    id: '3',
    type: 'goal',
    title: 'Goal Progress',
    description: 'Daily Reading Goal - 30 minutes completed',
    timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000),
    reward: 25
  }
])

const activeGoals = ref<Goal[]>([
  {
    id: '1',
    title: 'Daily Reading',
    description: 'Read for 30 minutes every day',
    targetValue: 30,
    currentValue: 22,
    unit: 'minutes',
    deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
    status: 'active',
    reward: 100
  },
  {
    id: '2',
    title: 'Math Mastery',
    description: 'Complete 20 math exercises',
    targetValue: 20,
    currentValue: 15,
    unit: 'exercises',
    deadline: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000),
    status: 'active',
    reward: 200
  }
])

const achievements = ref<Achievement[]>([
  {
    id: '1',
    title: 'Reading Champion',
    description: 'Read 5 books in one week',
    icon: 'mdi-book-open',
    rarity: 'gold',
    earnedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
  },
  {
    id: '2',
    title: 'Math Wizard',
    description: 'Solved 100 math problems',
    icon: 'mdi-calculator',
    rarity: 'silver',
    earnedAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
  }
])



const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Methods
const loadChildProgress = async () => {
  if (!selectedChildId.value) return
  
  loading.value = true
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Update stats, activities, etc. based on selected child and timeframe
  } catch (error) {
    showSnackbar('Failed to load child progress', 'error')
  } finally {
    loading.value = false
  }
}

const getActivityColor = (type: string) => {
  const colors = {
    lesson: 'primary',
    achievement: 'success',
    goal: 'warning',
    task: 'info'
  }
  return colors[type as keyof typeof colors] || 'grey'
}



const getGoalStatusColor = (status: string) => {
  const colors = {
    active: 'primary',
    completed: 'success',
    paused: 'warning',
    expired: 'error'
  }
  return colors[status as keyof typeof colors] || 'grey'
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit',
    hour12: true 
  })
}

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric' 
  })
}

const showSnackbar = (message: string, color: string = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

// Lifecycle
onMounted(() => {
  if (children.value.length > 0) {
    selectedChildId.value = children.value[0].id
    loadChildProgress()
  }
})
</script>

<style scoped>
/* Container and spacing */
.p-6 {
  padding: 1.5rem;
}
.space-y-6 > * + * {
  margin-top: 1.5rem;
}

/* Header */
.flex {
  display: flex;
}
.justify-between {
  justify-content: space-between;
}
.items-center {
  align-items: center;
}

/* Typography */
.text-2xl {
  font-size: 1.5rem;
  font-weight: bold;
}
.text-blue-600 {
  color: #2563eb;
}
.text-gray-600 {
  color: #4b5563;
}
.text-gray-500 {
  color: #6b7280;
}
.text-yellow-600 {
  color: #ca8a04;
}

.card {
  background: white;
  border: none;
  padding: 20px;
  width: 600px;
  margin-left: 2px;
  margin-right: 2px;
  font-family: sans-serif;
}
/* Buttons */
.btn-primary {
  background: linear-gradient(to right, #f43f5e, #ec4899);
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:disabled,
.btn-primary.opacity-50 {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #e5e7eb;
  color: #374151;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  border: none;
  cursor: pointer;
}

/* Cards and layout */
.bg-white {
  background-color: white;
}
.rounded-lg {
  border-radius: 0.5rem;
}
.shadow {
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.p-5 {
  padding: 1.25rem;
}
.grid {
  display: grid;
}
.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}
.md\:grid-cols-2 {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.lg\:grid-cols-3 {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.gap-4 {
  gap: 1rem;
}
.mt-6 {
  margin-top: 1.5rem;
}

.snackbar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #198754; /* Bootstrap success color */
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slide-up 0.3s ease;
}
/* Form elements */
.input-base {
  width: 100%;
  padding: 0.5rem;
  border-radius: 0.375rem;
  border: 1px solid #ccc;
  font-size: 1rem;
}

/* Progress bar */
progress {
  width: 100%;
  height: 8px;
  appearance: none;
}
progress::-webkit-progress-bar {
  background-color: #eee;
  border-radius: 0.25rem;
}
progress::-webkit-progress-value {
  background-color: #3b82f6;
  border-radius: 0.25rem;
}
progress::-moz-progress-bar {
  background-color: #3b82f6;
}

/* Text sizes */
.text-sm {
  font-size: 0.875rem;
}
.text-3xl {
  font-size: 1.875rem;
  font-weight: bold;
}

/* Utility classes */
.text-center {
  text-align: center;
}
.border {
  border: 1px solid #e5e7eb;
}
.border-l-4 {
  border-left: 4px solid #e5e7eb;
}
.pl-4 {
  padding-left: 1rem;
}
.mb-3 {
  margin-bottom: 0.75rem;
}
.mb-4 {
  margin-bottom: 1rem;
}
.py-6 {
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
}

/* Icon sizes */
.text-6xl {
  font-size: 3.75rem;
}
.text-2xl {
  font-size: 1.5rem;
}
.mr-3 {
  margin-right: 0.75rem;
}

/* Gap utility */
.gap-2 {
  gap: 0.5rem;
}

/* Responsive */
@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
@media (min-width: 1024px) {
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
.create-task {
    background-color: white;
    border-radius: 20px;
    height: auto;
    margin-top: 10px;
    margin-bottom: 20px;
    margin-left: 20px;
    margin-right: 5px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

  }

.row {
  display:flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
  
}
</style>
