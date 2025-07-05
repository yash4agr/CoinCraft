<template>
  <div 
    class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 cursor-pointer hover:shadow-md transition-shadow focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2"
    @click="$emit('click')"
    role="button"
    tabindex="0"
    @keydown.enter="$emit('click')"
    @keydown.space.prevent="$emit('click')"
  >
    <!-- Achievement Icon and Title -->
    <div class="flex items-center gap-3 mb-2">
      <div :class="iconBgClass" class="w-10 h-10 rounded-full flex items-center justify-center">
        <i :class="iconClass" class="text-lg"></i>
      </div>
      <div>
        <h3 class="font-semibold text-gray-800">{{ title }}</h3>
        <p class="text-xs text-gray-500">{{ date }}</p>
      </div>
    </div>
    
    <!-- Achievement Description -->
    <p class="text-sm text-gray-600 mb-3">{{ description }}</p>
    
    <!-- Coins Earned -->
    <div class="flex items-center justify-between">
      <span :class="badgeClass" class="px-2 py-1 rounded text-xs font-medium">
        {{ badge }}
      </span>
      <div class="flex items-center gap-1 text-sm font-medium">
        <img src="/coin.svg" class="coin-icon-sm" alt="coin">
        <span class="text-gray-700">+{{ coins }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Emits
const emit = defineEmits<{
  click: []
}>()

interface Props {
  title: string
  description: string
  icon: string
  badge: string
  coins: number
  date: string
  colorScheme: 'green' | 'orange' | 'blue' | 'purple'
}

const props = defineProps<Props>()

const iconClass = computed(() => {
  const colorMap = {
    green: 'text-green-600',
    orange: 'text-orange-600',
    blue: 'text-blue-600',
    purple: 'text-purple-600'
  }
  return `${props.icon} ${colorMap[props.colorScheme]}`
})

const iconBgClass = computed(() => {
  const colorMap = {
    green: 'bg-green-100',
    orange: 'bg-orange-100', 
    blue: 'bg-blue-100',
    purple: 'bg-purple-100'
  }
  return colorMap[props.colorScheme]
})

const badgeClass = computed(() => {
  const colorMap = {
    green: 'bg-green-100 text-green-700',
    orange: 'bg-orange-100 text-orange-700',
    blue: 'bg-blue-100 text-blue-700', 
    purple: 'bg-purple-100 text-purple-700'
  }
  return colorMap[props.colorScheme]
})
</script> 