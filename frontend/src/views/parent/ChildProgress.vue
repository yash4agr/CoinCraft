<template>
  <div>
    <!-- Error Boundary -->
    <div v-if="hasError" class="pa-6">
      <v-alert
        type="error"
        variant="tonal"
        class="mb-6"
        closable
        @click:close="clearError"
      >
        <template #title>Component Error</template>
        <template #text>
          {{ errorMessage }}
        </template>
      </v-alert>
      
      <v-btn color="primary" @click="clearError">
        <v-icon start>mdi-refresh</v-icon>
        Try Again
      </v-btn>
    </div>

    <!-- Main Content -->
    <v-container v-else fluid class="pa-6">
    <!-- Header -->
      <v-row class="mb-6">
        <v-col cols="12">
          <v-row align="center" class="flex-column flex-md-row justify-space-between">
            
            <!-- Title & Subtitle -->
            <v-col cols="12" md="auto" class="pa-0 mb-4 mb-md-0">
              <h1 class="text-h5 text-md-h4 font-weight-bold text-primary mb-2">
                Child Progress
              </h1>
              <p class="text-subtitle-2 text-md-subtitle-1 text-medium-emphasis">
                Track your child's learning journey and achievements
              </p>
            </v-col>

            <!-- Button -->
            <v-col cols="12" md="auto" class="pa-0 text-md-right">
              <v-row>
                <v-col cols="12" class="pa-0">
                  <v-btn
                    block
                    color="primary"
                    prepend-icon="mdi-download"
                    variant="tonal"
                    @click="exportProgress"
                    :loading="exporting"
                  >
                    Export Report
                  </v-btn>
                </v-col>
              </v-row>
            </v-col>

          </v-row>
        </v-col>
      </v-row>


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

    <!-- Fallback UI when no child selected or error -->
    <div v-else-if="!selectedChild || hasError" class="text-center py-12">
      <div v-if="hasError" class="mb-6">
        <v-icon size="64" color="error" class="mb-4">mdi-alert-circle</v-icon>
        <h3 class="text-h5 text-error mb-2">Something went wrong</h3>
        <p class="text-body-1 text-medium-emphasis mb-4">{{ errorMessage }}</p>
        <v-btn color="primary" @click="refreshChildProgress" :loading="refreshingGoals">
          <v-icon start>mdi-refresh</v-icon>
          Try Again
        </v-btn>
      </div>
      
      <div v-else class="mb-6">
        <v-icon size="64" color="primary" class="mb-4">mdi-account-child</v-icon>
        <h3 class="text-h5 text-primary mb-2">No Child Selected</h3>
        <p class="text-body-1 text-medium-emphasis">Please select a child from the dropdown above to view their progress.</p>
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="selectedChild">
      <!-- Error State -->
      <v-alert
        v-if="hasError"
        type="error"
        variant="tonal"
        class="mb-6"
        closable
        @click:close="clearError"
      >
        <template #title>Error Loading Child Progress</template>
        <template #text>
          There was an error loading the child progress data. Please try refreshing the page.
        </template>
      </v-alert>

      <!-- Progress Overview -->
      <v-row class="mb-6" v-if="!hasError">
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="success" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-trophy</v-icon>
            <div class="text-h4 font-weight-bold">{{ childStats.totalRewards }}</div>
            <div class="text-subtitle-2">Total Rewards</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="primary" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-book-open</v-icon>
            <div class="text-h4 font-weight-bold">{{ childStats.lessonsCompleted }}</div>
            <div class="text-subtitle-2">Lessons Completed</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="warning" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-coin</v-icon>
            <div class="text-h4 font-weight-bold">{{ childStats.coinsEarned }}</div>
            <div class="text-subtitle-2">Coins Earned</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="3">
          <v-card class="text-center pa-4" color="info" variant="tonal">
            <v-icon size="40" class="mb-2">mdi-target</v-icon>
            <div class="text-h4 font-weight-bold">{{ childStats.goalsAchieved }}</div>
            <div class="text-subtitle-2">Goals Achieved</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Progress Charts -->
      <v-row class="mb-6">
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

      <!-- Alerts: Task Completions Awaiting Approval -->
      <v-card class="mb-6" elevation="2">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2" color="warning">mdi-alert</v-icon>
          Alerts: Task Completions
        </v-card-title>
        <v-card-text>
          <div v-if="pendingCompletions.length === 0" class="text-medium-emphasis">No pending task approvals.</div>
          <v-list v-else>
            <v-list-item
              v-for="task in pendingCompletions"
              :key="task.id"
            >
              <template #prepend>
                <v-icon color="info">mdi-check-circle</v-icon>
              </template>
              <v-list-item-title>{{ task.title }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ parentStore.getChildName(task.assigned_to) }} • {{ task.coins_reward }} coins
              </v-list-item-subtitle>
              <template #append>
                <v-btn size="small" color="success" variant="tonal" class="mr-2" @click="approve(task.id)">Approve</v-btn>
                <v-btn size="small" color="error" variant="tonal" @click="reject(task.id)">Reject</v-btn>
              </template>
            </v-list-item>
          </v-list>
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
                      <v-chip size="small" :color="getGoalStatusColor(goal.is_completed ? 'completed' : 'active')">
                        {{ goal.is_completed ? 'Completed' : 'Active' }}
                      </v-chip>
                    </div>
                    <v-progress-linear
                      :model-value="(goal.current_amount / goal.target_amount) * 100"
                      color="primary"
                      height="6"
                      rounded
                      class="mb-2"
                    />
                    <div class="text-caption text-medium-emphasis">
                      {{ goal.current_amount }} / {{ goal.target_amount }} {{ goal.unit }}
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
                        {{ achievement.earned_at ? new Date(achievement.earned_at).toLocaleDateString() : 'N/A' }}
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Goals Completed Section -->
      <v-card class="mb-6" elevation="2">
        <v-card-title class="d-flex align-center justify-space-between">
          <div class="d-flex align-center">
            <v-icon class="mr-2" color="success">mdi-target-check</v-icon>
            All Children's Completed Goals
          </div>
          <v-btn
            size="small"
            color="primary"
            variant="outlined"
            @click="refreshGoalsData"
            :loading="refreshingGoals"
          >
            <v-icon start>mdi-refresh</v-icon>
            Refresh
          </v-btn>
        </v-card-title>
        <v-card-text>
          <!-- Summary Card -->
          <div class="mb-4">
            <v-alert
              type="info"
              variant="tonal"
              class="mb-4"
            >
              <template #prepend>
                <v-icon>mdi-information</v-icon>
              </template>
              <strong>Completed Goals Summary:</strong> 
              {{ completedGoals.length }} goal{{ completedGoals.length !== 1 ? 's' : '' }} completed across all children
            </v-alert>
            
            <!-- Manual Refresh Button -->
            <v-btn
              color="primary"
              variant="outlined"
              size="small"
              @click="refreshGoalsData"
              :loading="refreshingGoals"
              class="mb-2"
            >
              <v-icon start>mdi-refresh</v-icon>
              Refresh Goals Data
            </v-btn>
          </div>

          <div v-if="completedGoals.length === 0" class="text-center py-6">
            <v-icon size="48" class="mb-2 text-disabled">mdi-target-variant</v-icon>
            <div class="text-subtitle-1 text-disabled">No completed goals yet</div>
            <div class="text-caption text-medium-emphasis">Goals will appear here when any child marks them as completed</div>
          </div>
          <v-data-table
            v-else
            :headers="completedGoalsHeaders"
            :items="completedGoals"
            :items-per-page="5"
            class="elevation-1"
            density="compact"
          >
            <template #item.child_name="{ item }">
              <div class="d-flex align-center">
                <v-avatar size="32" color="primary" class="mr-2">
                  {{ getChildInitials(item.child_name) }}
                </v-avatar>
                <span class="font-weight-medium">{{ item.child_name }}</span>
              </div>
            </template>
            <template #item.goal_title="{ item }">
              <div class="d-flex align-center">
                <span class="text-2xl mr-2">{{ getGoalEmoji(item.icon) }}</span>
                <div>
                  <div class="font-weight-medium">{{ item.goal_title }}</div>
                  <div class="text-caption text-medium-emphasis">{{ item.description }}</div>
                </div>
              </div>
            </template>
            <template #item.target_amount="{ item }">
              <div class="d-flex align-center">
                <img src="/coin.svg" class="coin-icon mr-1" alt="coin" style="width: 16px; height: 16px;">
                <span class="font-weight-medium">{{ item.target_amount }}</span>
              </div>
            </template>
            <template #item.status="{ item }">
              <v-chip size="small" color="success" variant="tonal">
                <v-icon start size="16">mdi-check-circle</v-icon>
                Completed
              </v-chip>
            </template>
            <template #item.completed_date="{ item }">
              <span class="text-caption">{{ formatDate(item.completed_date || item.updated_at) }}</span>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>

      <!-- Selected Child's Active Goals -->
      <v-card class="mb-6" elevation="2">
        <v-card-title class="d-flex align-center">
          <v-icon class="mr-2" color="primary">mdi-target</v-icon>
          {{ selectedChild?.name }}'s Active Goals
        </v-card-title>
        <v-card-text>
          <div v-if="!selectedChild || !childProgress.active_goals || childProgress.active_goals.length === 0" class="text-center py-6">
            <v-icon size="48" class="mb-2 text-disabled">mdi-target-variant</v-icon>
            <div class="text-subtitle-1 text-disabled">No active goals</div>
            <div class="text-caption text-medium-emphasis">This child hasn't set any goals yet</div>
          </div>
          <div v-else class="goals-grid">
            <v-card
              v-for="goal in childProgress.active_goals"
              :key="goal.id"
              variant="outlined"
              class="goal-card"
            >
              <v-card-text class="py-4">
                <div class="d-flex justify-space-between align-center mb-3">
                  <div class="d-flex align-center">
                    <span class="text-2xl mr-2">{{ getGoalEmoji(goal?.icon) }}</span>
                    <span class="text-h6 font-weight-medium">{{ goal?.title || 'Untitled Goal' }}</span>
                  </div>
                  <v-chip 
                    size="small" 
                    :color="goal?.is_completed ? 'success' : 'primary'"
                    variant="tonal"
                  >
                    {{ goal?.is_completed ? 'Completed' : 'Active' }}
                  </v-chip>
                </div>
                
                <p v-if="goal?.description" class="text-body-2 text-medium-emphasis mb-3">
                  {{ goal.description }}
                </p>
                
                <div class="goal-progress mb-3">
                  <div class="d-flex justify-space-between text-caption mb-1">
                    <span>Progress</span>
                    <span>{{ Math.round(((goal?.current_amount || 0) / (goal?.target_amount || 1)) * 100) }}%</span>
                  </div>
                  <v-progress-linear
                    :model-value="((goal?.current_amount || 0) / (goal?.target_amount || 1)) * 100"
                    :color="goal?.is_completed ? 'success' : 'primary'"
                    height="8"
                    rounded
                  />
                  <div class="d-flex justify-space-between text-caption mt-1">
                    <span>{{ goal?.current_amount || 0 }} / {{ goal?.target_amount || 1 }} coins</span>
                    <span v-if="goal?.deadline" class="text-medium-emphasis">
                      Due: {{ formatDate(goal.deadline) }}
                    </span>
                  </div>
                </div>
                
                <div class="goal-meta text-caption text-medium-emphasis">
                  <div v-if="goal?.created_at">Created: {{ formatDate(goal.created_at) }}</div>
                  <div v-if="goal?.updated_at && goal.updated_at !== goal.created_at">
                    Updated: {{ formatDate(goal.updated_at) }}
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-card-text>
      </v-card>

      <!-- Debug Section (Development Only) -->
      <v-card class="mb-6" elevation="1" color="grey-lighten-4">
        <v-card-title class="text-caption">Debug Info (Development)</v-card-title>
        <v-card-text class="text-caption">
          <div>All Children Goals Count: {{ parentStore.allChildrenGoals?.length || 0 }}</div>
          <div>Completed Goals Count: {{ completedGoals.length }}</div>
          <div>Selected Child: {{ selectedChild?.name || 'None' }}</div>
          <div>Raw All Children Goals: {{ JSON.stringify(parentStore.allChildrenGoals?.slice(0, 2), null, 2) }}</div>
          <div>Raw Completed Goals: {{ JSON.stringify(completedGoals.slice(0, 2), null, 2) }}</div>
        </v-card-text>
      </v-card>

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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, onErrorCaptured } from 'vue'
import type { User, Goal, Achievement, ChildProgress } from '@/types'  
import { useParentStore } from '@/stores/parent'

// Store
const parentStore = useParentStore()

// Data
const loading = ref(false)
const refreshingGoals = ref(false)
const exportDialog = ref(false)
const exporting = ref(false)
const selectedChildId = ref<string>('')
const timeframe = ref('month')

// Error state management
const hasError = ref(false)
const errorMessage = ref('')

const clearError = () => {
  hasError.value = false
  errorMessage.value = ''
}

const setError = (message: string) => {
  hasError.value = true
  errorMessage.value = message
  console.error('❌ [CHILD_PROGRESS] Error:', message)
}

// Error boundary
const onErrorCaptured = (error: Error, instance: any, info: string) => {
  console.error('🚨 [CHILD_PROGRESS] Vue error captured:', error, info)
  setError('A component error occurred. Please refresh the page.')
  return false // Prevent error from propagating
}

// Use real children data from parent store
const children = computed(() => {
  try {
    return parentStore.children || []
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error accessing children:', error)
    return []
  }
})

const timeframes = [
  { title: 'Last Week', value: 'week' },
  { title: 'Last Month', value: 'month' },
  { title: 'Last 3 Months', value: 'quarter' },
  { title: 'Last Year', value: 'year' }
]

const exportFormats = ['PDF', 'Excel', 'CSV']
const exportFormat = ref('PDF')
const includeCharts = ref(true)

const selectedChild = computed(() => {
  try {
    if (!children.value || !Array.isArray(children.value) || !selectedChildId.value) {
      return null
    }
    return children.value.find(child => child && child.id === selectedChildId.value) || null
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error in selectedChild computed:', error)
    return null
  }
})

const pendingCompletions = computed(() => {
  try {
    return parentStore.tasks?.filter(t => t && t.status === 'completed') || []
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error in pendingCompletions computed:', error)
    return []
  }
})

const approve = async (taskId: string) => {
  const ok = await parentStore.approveTask(taskId)
  if (ok) showSnackbar('Task approved and coins awarded!', 'success')
  else showSnackbar('Failed to approve task', 'error')
}

const reject = async (taskId: string) => {
  const ok = await parentStore.rejectTask(taskId)
  if (ok) showSnackbar('Task rejected', 'success')
  else showSnackbar('Failed to reject task', 'error')
}

const stats = reactive({
  totalRewards: 127,
  lessonsCompleted: 45,
  coinsEarned: 2840,
  goalsAchieved: 8,
  currentStreak: 12
})

// Real-time child stats based on selected child
const childStats = computed(() => {
  if (!selectedChild.value || !childProgress.value) {
    return {
      totalRewards: 0,
      lessonsCompleted: 0,
      coinsEarned: 0,
      goalsAchieved: 0
    }
  }

  // Get child's profile data
  const childProfile = selectedChild.value
  const progress = childProgress.value
  
  // Calculate goals achieved
  const completedGoals = progress.active_goals?.filter(goal => goal.is_completed) || []
  
  return {
    totalRewards: progress.stats?.total_rewards || 0,
    lessonsCompleted: progress.stats?.lessons_completed || 0,
    coinsEarned: childProfile.coins || 0,
    goalsAchieved: completedGoals.length
  }
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

parentStore.getChildProgress(children.value[0]?.id || '')
console.log(parentStore.childProgress, 'childProgress')

const childProgress = computed(() => {
  try {
    return parentStore.childProgress as ChildProgress || null
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error accessing child progress:', error)
    return null
  }
})

const activeGoals = computed(() => {
  try {
    return childProgress.value?.active_goals || []
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error accessing active goals:', error)
    return []
  }
})

const achievements = computed(() => {
  try {
    return childProgress.value?.achievements || []
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error accessing achievements:', error)
    return []
  }
})

// Completed goals data for the table
const completedGoalsHeaders = [
  { title: 'Child', key: 'child_name', sortable: true },
  { title: 'Goal', key: 'goal_title', sortable: true },
  { title: 'Target Coins', key: 'target_amount', sortable: true, align: 'center' },
  { title: 'Status', key: 'status', sortable: false, align: 'center' },
  { title: 'Completed Date', key: 'completed_date', sortable: true, align: 'center' }
]

const completedGoals = computed(() => {
  try {
    const goals: Array<{
      id: string;
      child_name: string;
      goal_title: string;
      description: string;
      target_amount: number;
      icon: string;
      status: string;
      completed_date: string;
    }> = []

    console.log('🔍 [CHILD_PROGRESS] All children goals from parent store:', parentStore.allChildrenGoals)
    console.log('🔍 [CHILD_PROGRESS] Selected child:', selectedChild.value?.name)

    // Get ALL completed goals from ALL children (not just selected child)
    if (parentStore.allChildrenGoals && Array.isArray(parentStore.allChildrenGoals)) {
      const allCompletedGoals = parentStore.allChildrenGoals
        .filter(goal => goal && goal.is_completed === true) // Filter for completed goals
        .map(goal => ({
          id: goal.id || '',
          child_name: goal.child_name || 'Unknown Child',
          goal_title: goal.title || '',
          description: goal.description || '',
          target_amount: goal.target_amount || 0,
          icon: goal.icon || '🎯',
          status: 'completed',
          completed_date: goal.updated_at || goal.created_at || new Date().toISOString()
        }))
      
      goals.push(...allCompletedGoals)
      console.log('🎯 [CHILD_PROGRESS] All completed goals from all children:', allCompletedGoals.length, allCompletedGoals)
    } else {
      console.log('⚠️ [CHILD_PROGRESS] No allChildrenGoals data available')
    }

    console.log('🔍 [CHILD_PROGRESS] Final completed goals:', goals.length, goals)
    return goals.sort((a, b) => {
      try {
        const dateA = new Date(a.completed_date || 0)
        const dateB = new Date(b.completed_date || 0)
        
        if (isNaN(dateA.getTime()) || isNaN(dateB.getTime())) {
          return 0 // If dates are invalid, don't change order
        }
        
        return dateB.getTime() - dateA.getTime()
      } catch (error) {
        console.warn('⚠️ [CHILD_PROGRESS] Error sorting goals by date:', error)
        return 0
      }
    })
  } catch (error) {
    console.error('❌ [CHILD_PROGRESS] Error in completedGoals computed:', error)
    return []
  }
})

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
  hasError.value = false
  
  try {
    console.log('🔄 [CHILD_PROGRESS] Loading progress for child:', selectedChildId.value)
    await parentStore.getChildProgress(selectedChildId.value)
    
    // Also ensure goals are loaded
    await parentStore.loadAllChildrenGoals()
    
    console.log('✅ [CHILD_PROGRESS] Child progress loaded successfully')
  } catch (error) {
    console.error('❌ [CHILD_PROGRESS] Failed to load child progress:', error)
    setError('Failed to load child progress data. Please try again.')
  } finally {
    loading.value = false
  }
}

const refreshGoalsData = async () => {
  refreshingGoals.value = true
  try {
    await parentStore.loadAllChildrenGoals()
    showSnackbar('Goals data refreshed successfully!', 'success')
  } catch (error) {
    showSnackbar('Failed to refresh goals data', 'error')
  } finally {
    refreshingGoals.value = false
  }
}

const refreshChildProgress = async () => {
  if (!selectedChildId.value) return
  
  refreshingGoals.value = true
  hasError.value = false
  
  try {
    console.log('🔄 [CHILD_PROGRESS] Refreshing child progress...')
    
    await Promise.all([
      parentStore.getChildProgress(selectedChildId.value),
      parentStore.loadAllChildrenGoals()
    ])
    
    showSnackbar('Child progress data refreshed!', 'success')
    console.log('✅ [CHILD_PROGRESS] Child progress refreshed successfully')
    
  } catch (error) {
    console.error('❌ [CHILD_PROGRESS] Failed to refresh child progress:', error)
    setError('Failed to refresh child progress data. Please try again.')
  } finally {
    refreshingGoals.value = false
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

const getGoalEmoji = (icon: string | undefined | null) => {
  try {
    if (!icon) {
      return '🎯' // Default emoji for undefined icons
    }
    
    const iconMap: Record<string, string> = {
      'ri-gift-line': '🎁',
      'ri-gamepad-line': '🎮',
      'ri-book-line': '📚',
      'ri-bike-line': '🚲',
      'ri-headphone-line': '🎧',
      'ri-smartphone-line': '📱',
      'ri-palette-line': '🎨',
      'ri-football-line': '⚽',
      'ri-camera-line': '📷',
      'ri-music-line': '🎵',
      'ri-cake-line': '🎂',
      'ri-car-line': '🚗',
      'ri-plane-line': '✈️',
      'ri-heart-line': '❤️',
      'ri-star-line': '⭐',
      'ri-sun-line': '☀️',
      'ri-moon-line': '🌙',
      'ri-tree-line': '🌳',
      'ri-flower-line': '🌸',
      'ri-fish-line': '🐠'
    }
    
    return iconMap[icon] || '🎯'
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error in getGoalEmoji:', error)
    return '🎯'
  }
}

const getChildInitials = (name: string | undefined | null) => {
  try {
    if (!name || typeof name !== 'string') {
      return '??'
    }
    return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().slice(0, 2)
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error in getChildInitials:', error)
    return '??'
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('en-US', { 
    hour: 'numeric', 
    minute: '2-digit',
    hour12: true 
  })
}

const formatDate = (date: Date | string | undefined | null) => {
  try {
    // Debug logging to see what's being passed
    if (date === undefined || date === null) {
      console.log('🔍 [FORMAT_DATE] Received undefined/null date:', date)
      return 'N/A'
    }
    
    // Convert string to Date if needed
    const dateObj = typeof date === 'string' ? new Date(date) : date
    
    // Check if date is valid
    if (isNaN(dateObj.getTime())) {
      console.log('🔍 [FORMAT_DATE] Invalid date value:', date, 'converted to:', dateObj)
      return 'Invalid Date'
    }
    
    const formatted = dateObj.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric' 
    })
    
    console.log('🔍 [FORMAT_DATE] Successfully formatted:', date, '→', formatted)
    return formatted
  } catch (error) {
    console.warn('⚠️ [CHILD_PROGRESS] Error formatting date:', date, error)
    return 'N/A'
  }
}

const showSnackbar = (message: string, color: string = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}

// Lifecycle hooks
onMounted(async () => {
  try {
    // Set up error handling
    window.addEventListener('error', (event) => {
      console.error('🚨 [CHILD_PROGRESS] Global error:', event.error)
      setError('An unexpected error occurred. Please refresh the page.')
    })

    // Load parent data to get real children
    await parentStore.refreshData()
    
    // Load all children's goals for the completed goals table
    await parentStore.loadAllChildrenGoals()

    // Select first child if available
    if (children.value.length > 0 && !selectedChildId.value) {
      selectedChildId.value = children.value[0].id
      await loadChildProgress()
    }
  } catch (error) {
    console.error('❌ [CHILD_PROGRESS] Error in onMounted:', error)
    setError('Failed to initialize component. Please refresh the page.')
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

.goal-description {
  max-width: 200px;
  word-wrap: break-word;
  color: #666;
}

/* Goals Grid Layout */
.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.goal-card {
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.goal-card:hover {
  border-color: #e0e0e0;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.goal-progress {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
}

.goal-meta {
  border-top: 1px solid #e0e0e0;
  padding-top: 0.75rem;
  margin-top: 0.75rem;
}

.goal-meta > div {
  margin-bottom: 0.25rem;
}
</style>