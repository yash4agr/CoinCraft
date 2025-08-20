<template>
  <div 
    class="bg-white rounded-2xl p-6 shadow-sm cursor-pointer hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
    @click="$emit('click')"
    role="button"
    tabindex="0"
    @keydown.enter="$emit('click')"
    @keydown.space.prevent="$emit('click')"
  >
    <!-- Progress Circle -->
    <div class="relative w-16 h-16 mx-auto mb-4">
      <svg class="w-16 h-16 transform -rotate-90" viewBox="0 0 64 64">
        <!-- Background circle -->
        <circle 
          cx="32" 
          cy="32" 
          r="28" 
          fill="none" 
          :stroke="backgroundStrokeColor" 
          stroke-width="4"
        />
        <!-- Progress circle -->
        <circle 
          cx="32" 
          cy="32" 
          r="28" 
          fill="none" 
          :stroke="progressStrokeColor" 
          stroke-width="4"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="progressOffset"
          stroke-linecap="round"
          class="transition-all duration-500"
        />
      </svg>
      <!-- Icon in center -->
      <div class="absolute inset-0 flex items-center justify-center">
        <i :class="iconClass" class="text-2xl"></i>
      </div>
    </div>
    
    <!-- Goal Text -->
    <h3 class="font-semibold text-gray-800 text-center mb-2">{{ title }}</h3>
    <p class="text-center text-sm text-gray-600">
      {{ current }} / {{ total }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Emits
// const _emit = defineEmits<{
//   click: []
// }>()

interface Props {
  title: string
  current: number
  total: number
  icon: string
  colorScheme: 'orange' | 'blue' | 'green' | 'purple'
}

const props = defineProps<Props>()

const percentage = computed(() => {
  return Math.min((props.current / props.total) * 100, 100)
})

const circumference = 2 * Math.PI * 28 // radius = 28

const progressOffset = computed(() => {
  return circumference - (percentage.value / 100) * circumference
})

const iconClass = computed(() => {
  const colorMap = {
    orange: 'text-orange-500',
    blue: 'text-blue-500', 
    green: 'text-green-500',
    purple: 'text-purple-500'
  }
  return `${props.icon} ${colorMap[props.colorScheme]}`
})

const progressStrokeColor = computed(() => {
  const colorMap = {
    orange: '#f97316', // orange-500
    blue: '#3b82f6',   // blue-500
    green: '#10b981',  // green-500  
    purple: '#8b5cf6'  // purple-500
  }
  return colorMap[props.colorScheme]
})

const backgroundStrokeColor = computed(() => {
  const colorMap = {
    orange: '#fed7aa', // orange-200
    blue: '#bfdbfe',   // blue-200
    green: '#a7f3d0',  // green-200
    purple: '#c4b5fd'  // purple-200
  }
  return colorMap[props.colorScheme]
})
</script> 