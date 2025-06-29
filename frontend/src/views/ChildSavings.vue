<template>
  <div class="min-h-screen bg-gradient-to-br from-pink-100 via-orange-50 to-yellow-100 p-4 lg:pl-64 pt-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-money-dollar-circle-fill text-pink-500 mr-3"></i>
          My Piggy Bank
        </h1>
        <p class="text-gray-600 text-lg">Save your coins and watch them grow!</p>
      </div>

      <!-- Savings Overview -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Piggy Bank -->
        <div class="lg:col-span-2 bg-white rounded-xl shadow-md p-8 text-center">
          <div class="text-8xl mb-4">🐷</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Total Saved</h2>
          <div class="text-4xl font-bold text-pink-500 mb-4">
            <i class="ri-coins-fill mr-2"></i>125
          </div>
          <div class="flex gap-4 justify-center">
            <button class="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-full transition-colors">
              <i class="ri-add-line mr-2"></i>Add Coins
            </button>
            <button class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-full transition-colors">
              <i class="ri-subtract-line mr-2"></i>Spend Coins
            </button>
          </div>
        </div>

        <!-- Savings Stats -->
        <div class="space-y-6">
          <div class="bg-white rounded-xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              <i class="ri-calendar-fill text-blue-500 mr-2"></i>
              This Week
            </h3>
            <div class="text-2xl font-bold text-blue-500">+25 coins</div>
          </div>
          
          <div class="bg-white rounded-xl shadow-md p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">
              <i class="ri-star-fill text-yellow-500 mr-2"></i>
              Goal Progress
            </h3>
            <div class="text-2xl font-bold text-yellow-500">83%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Savings logic will go here
</script> 