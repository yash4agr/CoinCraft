<template>
  <section class="task-history-display">
    <h2 class="section-title">📋 Reports</h2>

    <!-- Loading state -->
    <div v-if="parentStore.isLoading" class="loading-container">
      <p>Loading task history...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="parentStore.error" class="error-container">
      <p>Error loading task history: {{ parentStore.error.message }}</p>
      <button @click="loadData" class="retry-btn">Retry</button>
    </div>

    <!-- Empty state -->
    <div v-else-if="taskHistory.length === 0" class="empty-container">
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
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useParentStore } from '@/stores/parent'

const parentStore = useParentStore()

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

// Load data function
const loadData = async () => {
  try {
    await Promise.all([
      parentStore.loadDashboard(),
      parentStore.loadTasks()
    ])
  } catch (error) {
    console.error('Failed to load task history:', error)
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

/* Loading, error, and empty states */
.loading-container,
.error-container,
.empty-container {
  text-align: center;
  padding: 2rem;
  color: #666;
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
  display: inline-block;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}

.green {
  background: #d4edda;
  color: #155724;
}

.yellow {
  background: #fff3cd;
  color: #856404;
}

.red {
  background: #f8d7da;
  color: #721c24;
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
