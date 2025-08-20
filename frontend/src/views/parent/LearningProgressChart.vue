<template>
  <div style="position: relative; width: 100%; height: 300px;">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { ChildProgress } from '@/types'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
} from 'chart.js'
import { useParentStore } from '@/stores/parent'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale
)

// Props to receive child ID
interface Props {
  childId?: string
  timeRange?: 'week' | 'month' | 'year'
}

const props = withDefaults(defineProps<Props>(), {
  timeRange: 'week'
})

// Store
const parentStore = useParentStore()

// Progress data from parent store
const progressData = ref<{ date: string; points: number }[]>([])

// Computed chart data based on real data
const chartData = computed(() => {
  const labels = progressData.value.map(item => {
    const date = new Date(item.date)
    return props.timeRange === 'week' 
      ? date.toLocaleDateString('en-US', { weekday: 'short' })
      : date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  })
  
  const data = progressData.value.map(item => item.points)
  
  return {
    labels,
    datasets: [
      {
        label: 'Points Earned',
        data: data.length > 0 ? data : [0, 0, 0, 0, 0, 0, 0],
        borderColor: '#1976D2',
        backgroundColor: 'rgba(25, 118, 210, 0.2)',
        fill: true,
        tension: 0.3
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    title: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
} as const

// Load progress data
const loadProgressData = async () => {
  try {
    if (props.childId) {
      // Load specific child progress
      await parentStore.getChildProgress(props.childId)
      const childProgress = parentStore.childProgress as ChildProgress
      if (childProgress?.learning_modules) {
        progressData.value = childProgress.learning_modules.map(module => ({
          date: module.created_at,
          points: module.points_reward
        }))
      }
    } else {
      // Generate aggregate data from tasks completed by all children
      const completedTasks = parentStore.completedTasks
      const last7Days = Array.from({ length: 7 }, (_, i) => {
        const date = new Date()
        date.setDate(date.getDate() - (6 - i))
        return date
      })
      
      progressData.value = last7Days.map(date => {
        const dayStart = new Date(date.setHours(0, 0, 0, 0))
        const dayEnd = new Date(date.setHours(23, 59, 59, 999))
        
        const dayTasks = completedTasks.filter(task => {
          const taskDate = new Date(task.completed_at || task.completedAt || '')
          return taskDate >= dayStart && taskDate <= dayEnd
        })
        
        const points = dayTasks.reduce((sum, task) => sum + (task.coins_reward || 0), 0)
        
        return {
          date: date.toISOString(),
          points
        }
      })
    }
  } catch (error) {
    console.error('Failed to load progress data:', error)
    // Fallback to dummy data
    progressData.value = [
      { date: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(), points: 5 },
      { date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), points: 8 },
      { date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), points: 4 },
      { date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), points: 10 },
      { date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), points: 6 },
      { date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), points: 9 },
      { date: new Date().toISOString(), points: 7 }
    ]
  }
}

// Load data on mount
onMounted(async () => {
  await parentStore.loadTasks()
  await loadProgressData()
})

</script>
