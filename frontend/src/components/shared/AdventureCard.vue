<template>
  <div 
    :class="cardClasses" 
    class="relative rounded-2xl p-6 text-white overflow-hidden transition-all duration-200 hover:scale-105 hover:shadow-lg"
    role="button"
    tabindex="0"
  >
    <!-- Completed Badge -->
    <div v-if="completed" class="absolute top-4 right-4 bg-white/20 rounded-full p-2">
      <i class="ri-check-line text-xl"></i>
    </div>
    
    <!-- Emoji Icon -->
    <div class="text-6xl mb-4">{{ emoji }}</div>
    
    <!-- Title and Description -->
    <h3 class="text-xl font-bold mb-2">{{ title }}</h3>
    <p :class="descriptionClasses" class="text-sm mb-4">{{ description }}</p>
    
    <!-- Difficulty and Coins -->
    <div class="flex items-center justify-between">
      <span class="bg-white/20 px-2 py-1 rounded text-xs">{{ difficulty }}</span>
      <div class="flex items-center gap-1 text-sm">
        <img src="/coin.svg" class="coin-icon-sm" alt="coin">
        <span>+{{ coins }}</span>
      </div>
    </div>
    
    <!-- Action Button -->
    <button 
      :class="buttonClasses" 
      class="w-full mt-4 bg-white font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors"
      @click.stop="handleButtonClick"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  description: string
  emoji: string
  difficulty: 'easy' | 'medium' | 'hard'
  coins: number
  completed?: boolean
  buttonText?: string
  colorScheme: 'pink' | 'teal' | 'blue' | 'green' | 'yellow' | 'purple'
}

const props = withDefaults(defineProps<Props>(), {
  completed: false,
  buttonText: 'Start Adventure'
})

const emit = defineEmits<{
  click: []
}>()

const cardClasses = computed(() => {
  const baseClasses = 'bg-gradient-to-br'
  const colorMap = {
    pink: 'from-pink-400 to-pink-500',
    teal: 'from-teal-400 to-teal-500', 
    blue: 'from-blue-400 to-blue-500',
    green: 'from-green-400 to-green-500',
    yellow: 'from-yellow-400 to-yellow-500',
    purple: 'from-purple-400 to-purple-500'
  }
  return `${baseClasses} ${colorMap[props.colorScheme]}`
})

const descriptionClasses = computed(() => {
  const colorMap = {
    pink: 'text-pink-100',
    teal: 'text-teal-100',
    blue: 'text-blue-100', 
    green: 'text-green-100',
    yellow: 'text-yellow-100',
    purple: 'text-purple-100'
  }
  return colorMap[props.colorScheme]
})

const buttonClasses = computed(() => {
  const colorMap = {
    pink: 'text-pink-500',
    teal: 'text-teal-500',
    blue: 'text-blue-500',
    green: 'text-green-500', 
    yellow: 'text-yellow-600',
    purple: 'text-purple-500'
  }
  return colorMap[props.colorScheme]
})

// Handle button click with debugging
const handleButtonClick = (event: Event) => {
  console.log('🎮 [ADVENTURE_CARD] Button clicked for:', props.title)
  console.log('🎮 [ADVENTURE_CARD] Event:', event)
  console.log('🎮 [ADVENTURE_CARD] Emitting click event...')
  event.stopPropagation()
  emit('click')
}

</script> 