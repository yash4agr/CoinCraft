<template>
  <section class="task-history-display">
    <h2 class="section-title">📋 Reports</h2>

    <!-- Loading state -->
    <div v-if="parentStore.isLoading" class="loading-container">
      <p>Loading reports...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="parentStore.error" class="error-container">
      <p>Error loading reports: {{ parentStore.error.message }}</p>
      <button @click="loadData" class="retry-btn">Retry</button>
    </div>

    <!-- Reports Content -->
    <div v-else class="reports-content">
      <!-- Goals Completed Section -->
      <div class="report-section">
        <h3 class="section-subtitle d-flex align-center justify-space-between">
          <span>🎯 Goals Completed</span>
          <v-btn
            size="small"
            color="primary"
            variant="outlined"
            @click="refreshGoalsData"
            :loading="refreshingGoals"
          >
            <v-icon start>mdi-refresh</v-icon>
            Refresh Goals
          </v-btn>
        </h3>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
          <div class="summary-card">
            <div class="summary-icon">🎯</div>
            <div class="summary-content">
              <div class="summary-number">{{ allGoals.length }}</div>
              <div class="summary-label">Total Goals</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">✅</div>
            <div class="summary-content">
              <div class="summary-number">{{ completedGoals.length }}</div>
              <div class="summary-label">Goals Completed</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">👥</div>
            <div class="summary-content">
              <div class="summary-number">{{ uniqueChildrenWithGoals }}</div>
              <div class="summary-label">Children with Goals</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">⭐</div>
            <div class="summary-content">
              <div class="summary-number">{{ totalCoinsEarned }}</div>
              <div class="summary-label">Total Coins Earned</div>
            </div>
          </div>
        </div>

        <!-- All Goals Table (Active + Completed) -->
        <div v-if="allGoals.length > 0" class="table-container">
          <h3 class="section-subtitle mb-4">🎯 All Children Goals</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Child</th>
                <th>Goal</th>
                <th>Target Coins</th>
                <th>Current Progress</th>
                <th>Status</th>
                <th>Created Date</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="goal in allGoals" :key="goal.id">
                <td class="child-name">
                  <div class="child-info">
                    <div class="child-avatar">{{ getChildInitials(goal.child_name) }}</div>
                    <span>{{ goal.child_name }}</span>
                  </div>
                </td>
                <td class="goal-title">
                  <div class="goal-info">
                    <span class="goal-icon">{{ getGoalEmoji(goal.icon) }}</span>
                    <span>{{ goal.title }}</span>
                  </div>
                </td>
                <td class="coins-cell">
                  <div class="coins-display">
                    <img src="/coin.svg" class="coin-icon" alt="coin" style="width: 16px; height: 16px;">
                    <span>{{ goal.target_amount }}</span>
                  </div>
                </td>
                <td class="progress-cell">
                  <div class="progress-display">
                    <img src="/coin.svg" class="coin-icon" alt="coin" style="width: 14px; height: 14px;">
                    <span>{{ goal.current_amount }} / {{ goal.target_amount }}</span>
                  </div>
                </td>
                <td>
                  <span :class="getStatusChipClass(goal.is_completed)">
                    {{ goal.is_completed ? 'Completed' : 'Pending' }}
                  </span>
                </td>
                <td>{{ formatDate(goal.created_at) }}</td>
                <td class="goal-description">{{ goal.description || 'No description' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty Goals State -->
        <div v-else class="empty-container">
          <div class="empty-icon">🎯</div>
          <p>No goals set yet. Encourage your children to set and achieve their goals!</p>
        </div>
      </div>

      <!-- Debug Section (Development Only) -->
      <!-- <v-card class="mb-6" elevation="1" color="grey-lighten-4">
        <v-card-title class="text-caption">Debug Info (Development)</v-card-title>
        <v-card-text class="text-caption">
          <div>All Children Goals Count: {{ parentStore.allChildrenGoals?.length || 0 }}</div>
          <div>Completed Goals Count: {{ completedGoals.length }}</div>
          <div>Raw Goals Data: {{ JSON.stringify(parentStore.allChildrenGoals?.slice(0, 3), null, 2) }}</div>
        </v-card-text> -->
      <!-- </v-card> -->

      <!-- Task History Section -->
      <div class="report-section">
        <h3 class="section-subtitle">📋 Task History</h3>
        
        <!-- Empty state -->
        <div v-if="taskHistory.length === 0" class="empty-container">
          <div class="empty-icon">📋</div>
          <p>No tasks assigned yet. Start by creating some tasks for your children!</p>
        </div>

        <!-- Task history table -->
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Task</th>
                <th>Child</th>
                <th>Status</th>
                <th>Coins</th>
                <th>Assigned</th>
                <th>Completed</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in taskHistory" :key="item.id">
                <td class="task-title">{{ item.title || 'Untitled Task' }}</td>
                <td>{{ item.child || 'Unknown Child' }}</td>
                <td>
                  <span class="chip" :class="getStatusClass(item.status)">
                    {{ item.status || 'Unknown' }}
                  </span>
                </td>
                <td>⭐ {{ item.coins || 0 }}</td>
                <td>{{ item.assignedDate ? formatDate(item.assignedDate) : '-' }}</td>
                <td>{{ item.completedDate ? formatDate(item.completedDate) : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useParentStore } from '@/stores/parent'

const parentStore = useParentStore()

// State for refreshing
const refreshingGoals = ref(false)

// Goals completed data
const completedGoals = computed(() => {
  console.log('🔍 [REPORTS] Parent store allChildrenGoals:', parentStore.allChildrenGoals)
  console.log('🔍 [REPORTS] Parent store allChildrenGoals length:', parentStore.allChildrenGoals?.length || 0)
  
  if (!parentStore.allChildrenGoals || parentStore.allChildrenGoals.length === 0) {
    console.log('⚠️ [REPORTS] No goals loaded yet')
    return []
  }
  
  // Log all goals to see their is_completed values
  parentStore.allChildrenGoals.forEach(goal => {
    console.log(`🔍 [REPORTS] Goal: ${goal.title} (${goal.child_name}) - is_completed: ${goal.is_completed} (type: ${typeof goal.is_completed})`)
  })
  
  const completed = parentStore.allChildrenGoals
    .filter(goal => goal.is_completed === true) // Explicit boolean comparison
    .map(goal => ({
      id: goal.id,
      child_name: goal.child_name,
      goal_title: goal.title,
      description: goal.description || '',
      target_amount: goal.target_amount,
      icon: goal.icon || '🎯',
      completed_date: goal.updated_at || new Date().toISOString()
    }))
    .sort((a, b) => new Date(b.completed_date).getTime() - new Date(a.completed_date).getTime())
  
  console.log('🎯 [REPORTS] Completed goals processed:', completed.length, completed)
  return completed
})

// Summary statistics
const uniqueChildrenWithGoals = computed(() => {
  if (!completedGoals.value.length) return 0
  const uniqueChildren = new Set(completedGoals.value.map(goal => goal.child_name))
  return uniqueChildren.size
})

const totalCoinsEarned = computed(() => {
  return completedGoals.value.reduce((total, goal) => total + goal.target_amount, 0)
})

const allGoals = computed(() => {
  if (!parentStore.allChildrenGoals || parentStore.allChildrenGoals.length === 0) {
    return []
  }
  return parentStore.allChildrenGoals.map(goal => ({
    id: goal.id,
    child_name: goal.child_name,
    title: goal.title,
    description: goal.description || '',
    target_amount: goal.target_amount,
    icon: goal.icon || '🎯',
    current_amount: goal.current_amount || 0,
    is_completed: goal.is_completed,
    created_at: goal.created_at || new Date().toISOString()
  })).sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
})

const taskHistory = computed(() => {
  if (!parentStore.tasks || parentStore.tasks.length === 0) {
    return []
  }
  
  return parentStore.tasks.map(task => {
    const status = getStatusDisplay(task.status)
    console.log(task)
    return {
      id: task.id || `task-${Math.random()}`,
      title: task.title || 'Untitled Task',
      child: task.childName || 'Unknown Child',
      status,
      coins: task.coins_reward || 0,
      assignedDate: task.created_at ? new Date(task.created_at) : new Date(),
      completedDate: task.completed_at ? new Date(task.completed_at) : null
    }
  }).sort((a, b) => b.assignedDate.getTime() - a.assignedDate.getTime()) // Sort by newest first
})

const getStatusDisplay = (status: string | undefined): string => {
  if (!status) return 'Unknown'
  
  const statusMap: Record<string, string> = {
    'pending': 'Pending',
    'in_progress': 'In Progress',
    'completed': 'Completed',
    'approved': 'Completed',
    'overdue': 'Overdue'
  }
  return statusMap[status] || status
}

function formatDate(date: Date | string | null | undefined): string {
  if (!date) return '-'
  
  try {
    return new Date(date).toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric'
    })
  } catch (error) {
    console.warn('Invalid date format:', date)
    return '-'
  }
}

function getStatusClass(status: string | undefined): string {
  if (!status) return 'gray'
  
  const s = status.toLowerCase()
  if (s === 'completed') return 'green'
  if (s === 'in progress' || s === 'pending') return 'yellow'
  if (s === 'overdue') return 'red'
  return 'gray'
}

// Goal helper functions
const getGoalEmoji = (icon: string) => {
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
    'ri-car-line': '🚗',
    'ri-star-line': '⭐',
    'ri-computer-line': '💻'
  }
  return iconMap[icon] || '🎯'
}

const getChildInitials = (name: string) => {
  if (!name) return '?'
  return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().slice(0, 2)
}

const getStatusChipClass = (isCompleted: boolean) => {
  return isCompleted ? 'green' : 'yellow'
}

// Load data function
const loadData = async () => {
  try {
    console.log('🔄 [REPORTS] Loading reports data...')
    
    // Load all data in parallel
    await Promise.all([
      parentStore.loadDashboard(),
      parentStore.loadTasks(),
      parentStore.loadAllChildrenGoals()
    ])
    
    console.log('✅ [REPORTS] All data loaded successfully')
    console.log('📊 [REPORTS] Dashboard loaded:', !!parentStore.familyStats)
    console.log('📋 [REPORTS] Tasks loaded:', parentStore.tasks?.length || 0)
    console.log('🎯 [REPORTS] Goals loaded:', parentStore.allChildrenGoals?.length || 0)
    
  } catch (error) {
    console.error('❌ [REPORTS] Failed to load reports data:', error)
  }
}

// Refresh goals data function
const refreshGoalsData = async () => {
  refreshingGoals.value = true
  try {
    console.log('🔄 [REPORTS] Refreshing goals data...')
    await parentStore.loadAllChildrenGoals()
    console.log('✅ [REPORTS] Goals data refreshed successfully')
  } catch (error) {
    console.error('❌ [REPORTS] Failed to refresh goals data:', error)
  } finally {
    refreshingGoals.value = false
  }
}

// Load data on mount
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.task-history-display {
  width: 100%;
  margin: 2rem auto;
  padding: 1.5rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.08);
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.25rem;
  margin: 1.5rem 0 1rem 0;
  color: #333;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 0.5rem;
}

.reports-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.report-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Summary Cards */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.summary-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.summary-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.summary-number {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.summary-label {
  font-size: 0.875rem;
  opacity: 0.9;
}

/* Goal-specific styling */
.child-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.child-avatar {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.875rem;
}

.goal-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.goal-icon {
  font-size: 1.5rem;
}

.coins-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 500;
}

.progress-display {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 500;
}

.goal-description {
  max-width: 200px;
  word-wrap: break-word;
  color: #666;
}

/* Loading, error, and empty states */
.loading-container,
.error-container,
.empty-container {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.error-container {
  color: #721c24;
  background-color: #f8d7da;
  border-radius: 4px;
  border: 1px solid #f5c6cb;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-btn:hover {
  background-color: #0056b3;
}

.task-title {
  font-weight: 500;
  max-width: 200px;
  word-wrap: break-word;
}

/* Responsive table container */
.table-container {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

.data-table th,
.data-table td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

.chip {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.chip.green {
  background-color: #dcfce7;
  color: #166534;
}

.chip.yellow {
  background-color: #fef3c7;
  color: #92400e;
}

.chip.red {
  background-color: #fee2e2;
  color: #991b1b;
}

.gray {
  background: #e2e3e5;
  color: #383d41;
}

/* Mobile Styles */
@media (max-width: 768px) {
  .section-title {
    font-size: 1.25rem;
    text-align: center;
  }

  .data-table th,
  .data-table td {
    padding: 0.5rem;
    font-size: 0.85rem;
    white-space: nowrap;
  }

  .chip {
    font-size: 0.75rem;
    padding: 2px 6px;
  }
}
</style>
