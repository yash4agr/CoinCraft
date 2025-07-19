<template>
  <section class="task-history-display">
    <h2 class="section-title">📋 Reports</h2>

    <!-- Responsive table wrapper -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Child</th>
            <th>Status</th>
            <th>Coins</th>
            <th>Assigned</th>
            <th>Completed</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in taskHistory" :key="item.id">
            <td>{{ item.child }}</td>
            <td>
              <span class="chip" :class="getStatusClass(item.status)">
                {{ item.status }}
              </span>
            </td>
            <td>⭐ {{ item.coins }}</td>
            <td>{{ formatDate(item.assignedDate) }}</td>
            <td>{{ item.completedDate ? formatDate(item.completedDate) : '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const taskHistory = ref([
  {
    id: '1',
    child: 'Luna',
    status: 'Completed',
    coins: 15,
    assignedDate: new Date(Date.now() - 2 * 86400000),
    completedDate: new Date(Date.now() - 1 * 86400000)
  },
  {
    id: '2',
    child: 'Harry',
    status: 'In Progress',
    coins: 20,
    assignedDate: new Date(Date.now() - 1 * 86400000),
    completedDate: null
  },
  {
    id: '3',
    child: 'Luna',
    status: 'Overdue',
    coins: 10,
    assignedDate: new Date(Date.now() - 3 * 86400000),
    completedDate: null
  }
])

function formatDate(date: Date | string): string {
  return new Date(date).toLocaleDateString('en-IN')
}

function getStatusClass(status: string): string {
  const s = status.toLowerCase()
  if (s === 'completed') return 'green'
  if (s === 'in progress') return 'yellow'
  if (s === 'overdue') return 'red'
  return 'gray'
}
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
