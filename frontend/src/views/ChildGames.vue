<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-indigo-100 p-4 lg:pl-64 pt-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-gamepad-fill text-purple-500 mr-3"></i>
          Fun Games
        </h1>
        <p class="text-gray-600 text-lg">Learn about money while having fun!</p>
      </div>

      <!-- Games Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Game Card Example -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6 border border-purple-100">
          <div class="text-center">
            <div class="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="ri-trophy-fill text-3xl text-purple-500"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Coin Collector</h3>
            <p class="text-gray-600 mb-4">Collect coins and learn counting!</p>
            <button class="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-full transition-colors">
              <i class="ri-play-fill mr-2"></i>Play Now
            </button>
          </div>
        </div>

        <!-- More game cards would go here -->
        <div class="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow p-6 border border-blue-100">
          <div class="text-center">
            <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <i class="ri-coins-fill text-3xl text-blue-500"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">Money Math</h3>
            <p class="text-gray-600 mb-4">Practice adding and subtracting money!</p>
            <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-full transition-colors">
              <i class="ri-play-fill mr-2"></i>Play Now
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Games logic will go here
</script> 