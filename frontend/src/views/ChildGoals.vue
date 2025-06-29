<template>
  <div class="min-h-screen bg-gradient-to-br from-green-100 via-emerald-50 to-teal-100 p-4 lg:pl-64 pt-20">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl lg:text-4xl font-bold text-gray-800 mb-2">
          <i class="ri-target-fill text-green-500 mr-3"></i>
          My Goals
        </h1>
        <p class="text-gray-600 text-lg">Set goals and save up for something special!</p>
      </div>

      <!-- Goals List -->
      <div class="space-y-6">
        <!-- Goal Card -->
        <div class="bg-white rounded-xl shadow-md p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-4">
              <div class="text-4xl">🎮</div>
              <div>
                <h3 class="text-xl font-semibold text-gray-800">New Video Game</h3>
                <p class="text-gray-600">Save up for the latest game!</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold text-green-500">
                <i class="ri-coins-fill mr-1"></i>75 / 100
              </div>
              <div class="text-sm text-gray-500">75% complete</div>
            </div>
          </div>
          
          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div class="bg-green-500 h-3 rounded-full" style="width: 75%"></div>
          </div>
          
          <div class="flex gap-3">
            <button class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-full transition-colors">
              <i class="ri-add-line mr-1"></i>Add Coins
            </button>
            <button class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-full transition-colors">
              <i class="ri-edit-line mr-1"></i>Edit Goal
            </button>
          </div>
        </div>

        <!-- Add New Goal -->
        <div class="bg-white rounded-xl shadow-md p-6 border-2 border-dashed border-gray-300 text-center">
          <div class="text-gray-400 mb-4">
            <i class="ri-add-circle-line text-4xl"></i>
          </div>
          <h3 class="text-lg font-semibold text-gray-600 mb-2">Add New Goal</h3>
          <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-full transition-colors">
            <i class="ri-add-line mr-2"></i>Create Goal
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Goals logic will go here
</script> 