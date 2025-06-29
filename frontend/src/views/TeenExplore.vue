<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Explore Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Explore Financial World 🌍</h1>
      <p class="text-gray-600">Discover financial concepts and expand your knowledge</p>
    </div>

    <!-- Knowledge Cards -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Financial Knowledge Cards</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <KnowledgeCard
          v-for="card in knowledgeCards"
          :key="card.id"
          :title="card.title"
          :description="card.description"
          :emoji="card.emoji"
          :coins="card.coins"
        />
      </div>
    </div>

    <!-- My Favorites Section -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">⭐ My Favorites</h2>
      <div class="bg-white rounded-xl p-6 shadow-sm">
        <div class="text-center py-8">
          <div class="text-4xl mb-4">📚</div>
          <h3 class="font-semibold text-gray-800 mb-2">No favorites yet</h3>
          <p class="text-gray-600 text-sm">Tap the star on any card to add it to your favorites</p>
        </div>
      </div>
    </div>

    <!-- Quick Quiz Section -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Quick Quiz Challenge 🧠</h2>
      <div class="bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-xl font-bold mb-2">Test Your Knowledge!</h3>
            <p class="text-purple-100 mb-4">Answer quick questions about financial concepts</p>
            <button class="bg-white text-purple-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
              Start Quiz
            </button>
          </div>
          <div class="text-right">
            <div class="text-3xl font-bold">+10</div>
            <div class="text-purple-200 text-sm">coins per quiz</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Trending Topics -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Trending Topics 🔥</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <i class="ri-stock-line text-2xl text-red-600"></i>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Stock Market Basics</h3>
              <p class="text-sm text-gray-600">Learn how the stock market works</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <i class="ri-leaf-line text-2xl text-green-600"></i>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Sustainable Finance</h3>
              <p class="text-sm text-gray-600">Money choices that help the planet</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
              <i class="ri-smartphone-line text-2xl text-blue-600"></i>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Digital Banking</h3>
              <p class="text-sm text-gray-600">Banking in the digital age</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm border hover:shadow-md transition-shadow cursor-pointer">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
              <i class="ri-bitcoin-line text-2xl text-yellow-600"></i>
            </div>
            <div>
              <h3 class="font-semibold text-gray-800">Cryptocurrency 101</h3>
              <p class="text-sm text-gray-600">Introduction to digital currencies</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import KnowledgeCard from '@/components/shared/KnowledgeCard.vue'

// Knowledge cards data - following DRY principle
const knowledgeCards = ref([
  {
    id: 1,
    title: 'TAXES',
    description: 'What are taxes and why do we pay them?',
    emoji: '🧾',
    coins: 245
  },
  {
    id: 2,
    title: 'GLOBAL ECONOMY',
    description: 'How does money work around the world?',
    emoji: '🌍',
    coins: 245
  },
  {
    id: 3,
    title: 'BANKING BASICS',
    description: 'Interest, loans, and bank accounts',
    emoji: '🏦',
    coins: 245
  },
  {
    id: 4,
    title: 'CREDIT CARDS',
    description: 'How credit works and building good credit',
    emoji: '💳',
    coins: 245
  },
  {
    id: 5,
    title: 'INVESTING',
    description: 'Stocks, bonds, and growing your money',
    emoji: '📈',
    coins: 245
  },
  {
    id: 6,
    title: 'ENTREPRENEURSHIP',
    description: 'Starting and running your own business',
    emoji: '🚀',
    coins: 245
  }
])
</script> 