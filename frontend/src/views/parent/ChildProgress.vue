<template>
  <v-container fluid class="pa-6">
    <!-- Header -->
    <div class="d-flex justify-space-between align-center mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-primary mb-2">
          Child Progress
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis">
          Track your child's learning journey and achievements
        </p>
      </div>
      <v-btn
        color="primary"
        prepend-icon="mdi-download"
        variant="tonal"
        @click="exportProgress"
        :loading="exporting"
      >
        Export Report
      </v-btn>
    </div>

    <!-- Child Selector -->
    <v-card class="mb-6" elevation="2">
      <v-card-title class="text-h6">
        <v-icon class="mr-2">mdi-account-child</v-icon>
        Select Child
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedChildId"
              :items="children"
              item-title="name"
              item-value="id"
              label="Child"
              prepend-inner-icon="mdi-account-child"
              variant="outlined"
              @update:model-value="loadChildProgress"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="timeframe"
              :items="timeframes"
              label="Time Period"
              prepend-inner-icon="mdi-calendar"
              variant="outlined"
              @update:model-value="loadChildProgress"
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <v-skeleton-loader
      v-if="loading"
      type="card, card, table"
      class="mb-6"
    />

    <!-- Content -->
    <div v-else-if="selectedChild">
      <!-- Progress Overview -->
      <v-row class="mb-6">
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="success" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-trophy</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.totalRewards }}</div>
            <div class="text-subtitle-2">Total Rewards</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="primary" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-book-open</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.lessonsCompleted }}</div>
            <div class="text-subtitle-2">Lessons Completed</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="warning" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-coin</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.coinsEarned }}</div>
            <div class="text-subtitle-2">Coins Earned</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="info" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-target</v-icon>
            <div class="text-h4 font-weight-bold">{{ stats.goalsAchieved }}</div>
            <div class="text-subtitle-2">Goals Achieved</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Progress Charts -->
      <v-row class="mb-6">
        <v-col cols="12" lg="8">
          <v-card elevation="2">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-chart-line</v-icon>
              Learning Progress Over Time
            </v-card-title>
            <v-card-text>
              <div class="progress-chart-container">
                <!-- Placeholder for chart - would integrate with chart library -->
                <learning-progress-chart/>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" lg="4">
          <v-card elevation="2" class="mb-4">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-chart-donut</v-icon>
              Subject Performance
            </v-card-title>
            <v-card-text>
              <div v-for="subject in subjectProgress" :key="subject.name" class="mb-3">
                <div class="d-flex justify-space-between mb-1">
                  <span class="text-subtitle-2">{{ subject.name }}</span>
                  <span class="text-caption">{{ subject.progress }}%</span>
                </div>
                <v-progress-linear
                  :model-value="subject.progress"
                  :color="getSubjectColor(subject.name)"
                  height="8"
                  rounded
                />
              </div>
            </v-card-text>
          </v-card>

          <v-card elevation="2">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-streak</v-icon>
              Current Streak
            </v-card-title>
            <v-card-text class="text-center">
              <div class="text-h2 font-weight-bold text-warning">{{ stats.currentStreak }}</div>
              <div class="text-subtitle-1 mb-2">Days</div>
              <v-chip color="success" variant="tonal" size="small">
                <v-icon start>mdi-fire</v-icon>
                Active Streak
              </v-chip>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recent Activities -->
      <v-card class="mb-6" elevation="2">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-history</v-icon>
          Recent Activities
        </v-card-title>
        <v-card-text>
          <v-timeline side="end" density="compact">
            <v-timeline-item
              v-for="activity in recentActivities"
              :key="activity.id"
              :icon="getActivityIcon(activity.type)"
              :dot-color="getActivityColor(activity.type)"
              size="small"
            >
              <template #opposite>
                <span class="text-caption text-disabled">
                  {{ formatTime(activity.timestamp) }}
                </span>
              </template>
              <v-card density="compact">
                <v-card-text class="py-2">
                  <div class="text-subtitle-2">{{ activity.title }}</div>
                  <div class="text-caption text-medium-emphasis">
                    {{ activity.description }}
                  </div>
                  <v-chip
                    v-if="activity.reward"
                    size="x-small"
                    color="warning"
                    variant="tonal"
                    class="mt-1"
                  >
                    +{{ activity.reward }} coins
                  </v-chip>
                </v-card-text>
              </v-card>
            </v-timeline-item>
          </v-timeline>
        </v-card-text>
      </v-card>

      <!-- Goals and Achievements -->
      <v-row class="mb-6">
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-target</v-icon>
              Active Goals
            </v-card-title>
            <v-card-text>
              <div v-if="activeGoals.length === 0" class="text-center py-6">
                <v-icon size="48" class="mb-2 text-disabled">mdi-target-variant</v-icon>
                <div class="text-subtitle-1 text-disabled">No active goals</div>
              </div>
              <div v-else>
                <v-card
                  v-for="goal in activeGoals"
                  :key="goal.id"
                  variant="outlined"
                  class="mb-3"
                >
                  <v-card-text class="py-3">
                    <div class="d-flex justify-space-between align-center mb-2">
                      <span class="text-subtitle-2 font-weight-medium">{{ goal.title }}</span>
                      <v-chip size="small" :color="getGoalStatusColor(goal.status)">
                        {{ goal.status }}
                      </v-chip>
                    </div>
                    <v-progress-linear
                      :model-value="(goal.currentAmount / goal.targetAmount) * 100"
                      color="primary"
                      height="6"
                      rounded
                      class="mb-2"
                    />
                    <div class="text-caption text-medium-emphasis">
                      {{ goal.currentAmount }} / {{ goal.targetAmount }} {{ goal.unit }}
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card elevation="2">
            <v-card-title class="d-flex align-center">
              <v-icon class="mr-2">mdi-medal</v-icon>
              Recent Achievements
            </v-card-title>
            <v-card-text>
              <div v-if="achievements.length === 0" class="text-center py-6">
                <v-icon size="48" class="mb-2 text-disabled">mdi-medal-outline</v-icon>
                <div class="text-subtitle-1 text-disabled">No achievements yet</div>
              </div>
              <div v-else>
                <v-card
                  v-for="achievement in achievements"
                  :key="achievement.id"
                  variant="outlined"
                  class="mb-3"
                >
                  <v-card-text class="py-3">
                    <div class="d-flex align-center">
                      <v-avatar :color="achievement.rarity" size="40" class="mr-3">
                        <v-icon>{{ achievement.icon }}</v-icon>
                      </v-avatar>
                      <div class="flex-grow-1">
                        <div class="text-subtitle-2 font-weight-medium">{{ achievement.title }}</div>
                        <div class="text-caption text-medium-emphasis">{{ achievement.description }}</div>
                      </div>
                      <div class="text-caption text-disabled">
                        {{ formatDate(achievement.earnedAt) }}
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Recommendations -->
      <v-card elevation="2">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2">mdi-lightbulb</v-icon>
          Recommendations
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col
              v-for="recommendation in recommendations"
              :key="recommendation.id"
              cols="12"
              md="4"
            >
              <v-card variant="outlined" height="100%">
                <v-card-text>
                  <div class="d-flex align-center mb-2">
                    <v-icon :color="recommendation.priority" class="mr-2">
                      {{ recommendation.icon }}
                    </v-icon>
                    <span class="text-subtitle-2 font-weight-medium">
                      {{ recommendation.title }}
                    </span>
                  </div>
                  <p class="text-body-2 text-medium-emphasis mb-3">
                    {{ recommendation.description }}
                  </p>
                  <v-btn
                    size="small"
                    color="primary"
                    variant="outlined"
                    @click="applyRecommendation(recommendation)"
                  >
                    {{ recommendation.action }}
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </div>

    <!-- No Child Selected -->
    <v-card v-else-if="!loading" class="text-center pa-8" elevation="1">
      <v-icon size="64" class="mb-4 text-disabled">mdi-account-child-outline</v-icon>
      <h3 class="text-h6 mb-2 text-disabled">Select a Child</h3>
      <p class="text-body-2 text-medium-emphasis">
        Choose a child from the dropdown above to view their progress
      </p>
    </v-card>

    <!-- Export Dialog -->
    <v-dialog v-model="exportDialog" max-width="400">
      <v-card>
        <v-card-title>Export Progress Report</v-card-title>
        <v-card-text>
          <v-select
            v-model="exportFormat"
            :items="exportFormats"
            label="Format"
            variant="outlined"
            class="mb-3"
          />
          <v-checkbox
            v-model="includeCharts"
            label="Include charts and visualizations"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="exportDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="confirmExport"
            :loading="exporting"
          >
            Export
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="4000"
      location="bottom right"
    >
      {{ snackbar.message }}
      <template #actions>
        <v-btn icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import type { User, Goal, Achievement } from '@/types'
import LearningProgressChart from './LearningProgressChart.vue'

// Data
const loading = ref(false)
const exporting = ref(false)
const exportDialog = ref(false)
const selectedChildId = ref<string>('')
const timeframe = ref('month')

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

const exportFormats = ['PDF', 'Excel', 'CSV']
const exportFormat = ref('PDF')
const includeCharts = ref(true)

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

const recommendations = ref([
  {
    id: '1',
    title: 'Focus on Science',
    description: 'Science progress is below average. Consider adding more science activities.',
    icon: 'mdi-flask',
    priority: 'warning',
    action: 'Add Activities'
  },
  {
    id: '2',
    title: 'Increase Challenge',
    description: 'Child is excelling in reading. Consider more advanced materials.',
    icon: 'mdi-trending-up',
    priority: 'success',
    action: 'Level Up'
  },
  {
    id: '3',
    title: 'Maintain Streak',
    description: 'Great job maintaining the daily streak! Keep it up.',
    icon: 'mdi-fire',
    priority: 'info',
    action: 'Encourage'
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

const applyRecommendation = (recommendation: any) => {
  showSnackbar(`Applied recommendation: ${recommendation.title}`, 'success')
}

const getActivityIcon = (type: string) => {
  const icons = {
    lesson: 'mdi-book-open',
    achievement: 'mdi-trophy',
    goal: 'mdi-target',
    task: 'mdi-check-circle'
  }
  return icons[type as keyof typeof icons] || 'mdi-circle'
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

const getSubjectColor = (subject: string) => {
  const colors = {
    Math: 'blue',
    Reading: 'green',
    Science: 'purple',
    Art: 'orange'
  }
  return colors[subject as keyof typeof colors] || 'grey'
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
.chart-placeholder {
  border: 2px dashed #e0e0e0;
}

.v-timeline-item {
  padding-bottom: 16px;
}

.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
}
</style>