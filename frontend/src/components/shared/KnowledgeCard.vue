<template>
  <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow cursor-pointer">
    <div class="p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold text-gray-800">{{ title }}</h3>
        <div class="flex items-center gap-1 text-sm text-yellow-600">
          <img src="/coin.svg" class="coin-icon-sm" alt="coin">
          <span>{{ coins }}</span>
        </div>
      </div>
      <div class="text-center py-8">
        <div class="text-4xl mb-4">{{ emoji }}</div>
        <p class="text-gray-600 text-sm mb-4">[Tap to flip]</p>
        <p class="text-gray-700">{{ description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  description: string
  emoji: string
  coins?: number
}

const props = withDefaults(defineProps<Props>(), {
  coins: 245
})
</script>