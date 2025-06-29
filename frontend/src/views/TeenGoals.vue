<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Goals Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Smart Goals 🎯</h1>
      <p class="text-gray-600">Set, track, and achieve your financial objectives</p>
    </div>

    <!-- Active Goals -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Active Goals</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Headphones Goal -->
        <div class="bg-white rounded-xl p-6 shadow-sm border border-blue-200">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <span class="text-2xl">🎧</span>
              <h3 class="font-bold text-gray-800">Headphones</h3>
            </div>
            <span class="text-sm bg-blue-100 text-blue-700 px-2 py-1 rounded-full">Week 3 of 6</span>
          </div>
          
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span class="font-medium">30/60 coins</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-4">
              <div class="bg-blue-500 h-4 rounded-full transition-all duration-500" style="width: 50%"></div>
            </div>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Strategy:</span>
              <span class="font-medium">Save 10 coins/week for 6 weeks</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Linked to:</span>
              <span class="text-blue-600 font-medium">Saving Budget</span>
            </div>
          </div>
        </div>
        
        <!-- Phone Case Goal -->
        <div class="bg-white rounded-xl p-6 shadow-sm border border-green-200">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-3">
              <span class="text-2xl">📱</span>
              <h3 class="font-bold text-gray-800">Phone Case</h3>
            </div>
            <span class="text-sm bg-green-100 text-green-700 px-2 py-1 rounded-full">Almost there!</span>
          </div>
          
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span class="font-medium">20/25 coins</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-4">
              <div class="bg-green-500 h-4 rounded-full transition-all duration-500" style="width: 80%"></div>
            </div>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-600">Strategy:</span>
              <span class="font-medium">Use "Wants" budget</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Linked to:</span>
              <span class="text-yellow-600 font-medium">Wants Budget</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Goal Actions -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Goal Management</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button class="bg-green-500 hover:bg-green-600 text-white p-4 rounded-xl transition-colors">
          <div class="flex items-center justify-center gap-3">
            <i class="ri-add-line text-2xl"></i>
            <span class="font-semibold">Create Smart Goal</span>
          </div>
        </button>
        
        <button class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-xl transition-colors">
          <div class="flex items-center justify-center gap-3">
            <i class="ri-user-settings-line text-2xl"></i>
            <span class="font-semibold">Goal Assistant</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Goal Templates -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Popular Goal Templates</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer border">
          <div class="text-center">
            <div class="text-3xl mb-3">📚</div>
            <h3 class="font-semibold text-gray-800 mb-2">College Fund</h3>
            <p class="text-sm text-gray-600">Start saving for your future education</p>
            <div class="mt-3 text-xs text-blue-600 font-medium">Long-term goal</div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer border">
          <div class="text-center">
            <div class="text-3xl mb-3">🎮</div>
            <h3 class="font-semibold text-gray-800 mb-2">Gaming Console</h3>
            <p class="text-sm text-gray-600">Save up for the latest gaming system</p>
            <div class="mt-3 text-xs text-purple-600 font-medium">6-month goal</div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer border">
          <div class="text-center">
            <div class="text-3xl mb-3">🚲</div>
            <h3 class="font-semibold text-gray-800 mb-2">New Bike</h3>
            <p class="text-sm text-gray-600">Get that bike you've been wanting</p>
            <div class="mt-3 text-xs text-green-600 font-medium">3-month goal</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Goal Tips -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Goal Setting Tips 💡</h2>
      <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-200">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="font-semibold text-gray-800 mb-3">Make SMART Goals</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center gap-2">
                <i class="ri-check-line text-green-500"></i>
                <span><strong>S</strong>pecific: Be clear about what you want</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-check-line text-green-500"></i>
                <span><strong>M</strong>easurable: Set a specific amount</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-check-line text-green-500"></i>
                <span><strong>A</strong>chievable: Make it realistic</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-check-line text-green-500"></i>
                <span><strong>R</strong>elevant: Choose something meaningful</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-check-line text-green-500"></i>
                <span><strong>T</strong>ime-bound: Set a deadline</span>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 class="font-semibold text-gray-800 mb-3">Success Strategies</h3>
            <ul class="space-y-2 text-sm text-gray-700">
              <li class="flex items-center gap-2">
                <i class="ri-lightbulb-line text-yellow-500"></i>
                <span>Break big goals into smaller steps</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-lightbulb-line text-yellow-500"></i>
                <span>Track your progress regularly</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-lightbulb-line text-yellow-500"></i>
                <span>Celebrate small wins along the way</span>
              </li>
              <li class="flex items-center gap-2">
                <i class="ri-lightbulb-line text-yellow-500"></i>
                <span>Link goals to your budget categories</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Teen goal management with SMART goal principles
</script> 