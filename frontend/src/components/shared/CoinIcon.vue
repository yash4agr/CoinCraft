<template>
  <span 
    class="coin-icon inline-flex items-center justify-center"
    :class="sizeClass"
  >
    <svg 
      viewBox="0 0 24 24" 
      fill="currentColor" 
      :class="iconClass"
    >
      <circle cx="12" cy="12" r="10" :fill="coinColor" stroke="#f59e0b" stroke-width="1"/>
      <circle cx="12" cy="12" r="7" fill="none" stroke="#f59e0b" stroke-width="0.5" opacity="0.6"/>
      <text x="12" y="16" text-anchor="middle" font-size="8" font-weight="bold" fill="#92400e">₵</text>
    </svg>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'default' | 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'default'
})

const sizeClass = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4', 
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-8 h-8'
  }
  return sizes[props.size]
})

const iconClass = computed(() => {
  return `${sizeClass.value} text-yellow-500`
})

const coinColor = computed(() => {
  const colors = {
    default: '#fbbf24',
    light: '#fde047',
    dark: '#f59e0b'
  }
  return colors[props.variant]
})
</script>

<style scoped>
.coin-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
</style> 