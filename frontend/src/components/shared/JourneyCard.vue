<template>
  <div :class="cardClasses" class="rounded-xl p-4 flex items-center gap-4">
    <!-- Status Icon -->
    <div :class="iconContainerClass" class="w-12 h-12 rounded-xl flex items-center justify-center">
      <i :class="iconClass" class="text-xl"></i>
    </div>
    
    <!-- Content -->
    <div class="flex-1">
      <h3 :class="titleClass" class="font-semibold mb-1">{{ title }}</h3>
      <p :class="descriptionClass" class="text-sm">{{ description }}</p>
    </div>
    
    <!-- Action Icon -->
    <div v-if="!locked">
      <i :class="actionIconClass" class="text-xl"></i>
    </div>
    <div v-else class="text-gray-400">
      <i class="ri-lock-line text-xl"></i>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  description: string
  status: 'completed' | 'current' | 'locked'
  icon: string
}

const props = defineProps<Props>()

const locked = computed(() => props.status === 'locked')
const completed = computed(() => props.status === 'completed')
const current = computed(() => props.status === 'current')

const cardClasses = computed(() => {
  if (completed.value) return 'bg-green-50 border border-green-200'
  if (current.value) return 'bg-blue-50 border border-blue-200'
  return 'bg-gray-50 border border-gray-200'
})

const iconContainerClass = computed(() => {
  if (completed.value) return 'bg-green-100'
  if (current.value) return 'bg-blue-100'
  return 'bg-gray-100'
})

const iconClass = computed(() => {
  if (completed.value) return `${props.icon} text-green-600`
  if (current.value) return `${props.icon} text-blue-600`
  return `${props.icon} text-gray-400`
})

const titleClass = computed(() => {
  if (completed.value) return 'text-green-800'
  if (current.value) return 'text-blue-800'
  return 'text-gray-400'
})

const descriptionClass = computed(() => {
  if (completed.value) return 'text-green-600'
  if (current.value) return 'text-blue-600'
  return 'text-gray-400'
})

const actionIconClass = computed(() => {
  if (completed.value) return 'ri-check-line text-green-500'
  if (current.value) return 'ri-play-circle-line text-blue-500'
  return 'ri-lock-line text-gray-400'
})
</script> 