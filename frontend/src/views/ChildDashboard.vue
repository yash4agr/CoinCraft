<template>
  <div class="min-h-screen bg-gray-100 p-4 lg:pl-64 pt-20 pb-20 lg:pb-8">
    <div class="max-w-6xl mx-auto space-y-6">
      
      <!-- Today's Goals Section -->
      <div class="bg-white rounded-2xl shadow-sm p-4 md:p-6">
        <div class="flex items-center gap-2 mb-4">
          <i class="ri-target-line text-green-500 text-xl"></i>
          <h2 class="text-lg md:text-xl font-semibold text-gray-800">Today's Goals</h2>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <!-- Read Lessons Goal -->
          <div class="text-center">
            <div class="relative w-16 h-16 md:w-20 md:h-20 mx-auto mb-2">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="rgb(229 231 235)" stroke-width="8" fill="none" />
                <circle cx="50" cy="50" r="40" stroke="rgb(34 197 94)" stroke-width="8" fill="none" 
                        stroke-dasharray="251" stroke-dashoffset="75" stroke-linecap="round" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <i class="ri-book-open-line text-green-500 text-xl md:text-2xl"></i>
              </div>
            </div>
            <h3 class="font-medium text-gray-800 text-sm md:text-base">Read Lessons</h3>
            <p class="text-xs md:text-sm text-gray-500">2/3 lessons</p>
          </div>

          <!-- Earn Coins Goal -->
          <div class="text-center">
            <div class="relative w-16 h-16 md:w-20 md:h-20 mx-auto mb-2">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="rgb(229 231 235)" stroke-width="8" fill="none" />
                <circle cx="50" cy="50" r="40" stroke="rgb(245 158 11)" stroke-width="8" fill="none" 
                        stroke-dasharray="251" stroke-dashoffset="25" stroke-linecap="round" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <i class="ri-coins-line text-yellow-500 text-xl md:text-2xl"></i>
              </div>
            </div>
            <h3 class="font-medium text-gray-800 text-sm md:text-base">Earn Coins</h3>
            <p class="text-xs md:text-sm text-gray-500">45/50 coins</p>
          </div>

          <!-- Complete Games Goal -->
          <div class="text-center">
            <div class="relative w-16 h-16 md:w-20 md:h-20 mx-auto mb-2">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="rgb(229 231 235)" stroke-width="8" fill="none" />
                <circle cx="50" cy="50" r="40" stroke="rgb(34 197 94)" stroke-width="8" fill="none" 
                        stroke-dasharray="251" stroke-dashoffset="126" stroke-linecap="round" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <i class="ri-gamepad-line text-green-500 text-xl md:text-2xl"></i>
              </div>
            </div>
            <h3 class="font-medium text-gray-800 text-sm md:text-base">Complete Games</h3>
            <p class="text-xs md:text-sm text-gray-500">1/2 games</p>
          </div>

          <!-- Practice Time Goal -->
          <div class="text-center">
            <div class="relative w-16 h-16 md:w-20 md:h-20 mx-auto mb-2">
              <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="rgb(229 231 235)" stroke-width="8" fill="none" />
                <circle cx="50" cy="50" r="40" stroke="rgb(59 130 246)" stroke-width="8" fill="none" 
                        stroke-dasharray="251" stroke-dashoffset="63" stroke-linecap="round" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <i class="ri-time-line text-blue-500 text-xl md:text-2xl"></i>
              </div>
            </div>
            <h3 class="font-medium text-gray-800 text-sm md:text-base">Practice Time</h3>
            <p class="text-xs md:text-sm text-gray-500">15/20 minutes</p>
          </div>
        </div>
      </div>

      <!-- Choose Your Adventure Section -->
      <div class="bg-white rounded-2xl shadow-sm p-4 md:p-6">
        <div class="flex items-center gap-2 mb-6">
          <i class="ri-gamepad-line text-gray-700 text-xl"></i>
          <h2 class="text-lg md:text-xl font-semibold text-gray-800">Choose Your Adventure!</h2>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
          <!-- Piggy Bank Adventure -->
          <div class="relative bg-gradient-to-br from-pink-400 to-pink-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="text-6xl mb-4">🐷</div>
            <h3 class="text-xl font-bold mb-2">Piggy Bank Adventure</h3>
            <p class="text-pink-100 text-sm mb-4">Learn about saving money with your virtual piggy bank!</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">easy</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-yellow-300"></i>
                <span>+25</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-pink-500 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Start Adventure
            </button>
          </div>

          <!-- Needs vs Wants Game -->
          <div class="relative bg-gradient-to-br from-teal-400 to-teal-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="absolute top-4 right-4 bg-white/20 rounded-full p-2">
              <i class="ri-check-line text-xl"></i>
            </div>
            <div class="text-6xl mb-4">🛒</div>
            <h3 class="text-xl font-bold mb-2">Needs vs Wants Game</h3>
            <p class="text-teal-100 text-sm mb-4">Sort items into needs and wants categories.</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">medium</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-yellow-300"></i>
                <span>+35</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-teal-500 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Play Again
            </button>
          </div>

          <!-- Coin Counting Challenge -->
          <div class="relative bg-gradient-to-br from-blue-400 to-blue-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="text-6xl mb-4">🪙</div>
            <h3 class="text-xl font-bold mb-2">Coin Counting Challenge</h3>
            <p class="text-blue-100 text-sm mb-4">Practice counting different types of coins.</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">easy</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-yellow-300"></i>
                <span>+30</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-blue-500 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Start Adventure
            </button>
          </div>

          <!-- Budget Builder -->
          <div class="relative bg-gradient-to-br from-green-400 to-green-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="text-6xl mb-4">📊</div>
            <h3 class="text-xl font-bold mb-2">Budget Builder</h3>
            <p class="text-green-100 text-sm mb-4">Create your first budget with fun categories.</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">medium</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-yellow-300"></i>
                <span>+50</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-green-500 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Start Adventure
            </button>
          </div>

          <!-- Shopping Smart -->
          <div class="relative bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="text-6xl mb-4">🛍️</div>
            <h3 class="text-xl font-bold mb-2">Shopping Smart</h3>
            <p class="text-yellow-100 text-sm mb-4">Learn to make smart shopping decisions.</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">medium</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-orange-300"></i>
                <span>+40</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-yellow-600 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Start Adventure
            </button>
          </div>

          <!-- Goal Setting Quest -->
          <div class="relative bg-gradient-to-br from-purple-400 to-purple-500 rounded-2xl p-6 text-white overflow-hidden">
            <div class="text-6xl mb-4">🎯</div>
            <h3 class="text-xl font-bold mb-2">Goal Setting Quest</h3>
            <p class="text-purple-100 text-sm mb-4">Set and track your savings goals.</p>
            <div class="flex items-center justify-between">
              <span class="bg-white/20 px-2 py-1 rounded text-xs">easy</span>
              <div class="flex items-center gap-1 text-sm">
                <i class="ri-coins-fill text-yellow-300"></i>
                <span>+45</span>
              </div>
            </div>
            <button class="w-full mt-4 bg-white text-purple-500 font-medium py-2 rounded-lg hover:bg-gray-50 transition-colors">
              Start Adventure
            </button>
          </div>
        </div>
      </div>

      <!-- Recent Achievements Section -->
      <div class="bg-white rounded-2xl shadow-sm p-4 md:p-6">
        <div class="flex items-center gap-2 mb-4">
          <i class="ri-trophy-line text-yellow-500 text-xl"></i>
          <h2 class="text-lg md:text-xl font-semibold text-gray-800">Recent Achievements</h2>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- First Steps Achievement -->
          <div class="text-center p-4 bg-yellow-50 rounded-xl">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-footprint-line text-yellow-600 text-2xl"></i>
            </div>
            <h3 class="font-medium text-gray-800 mb-1">First Steps</h3>
            <p class="text-sm text-gray-600">Completed your first lesson!</p>
          </div>

          <!-- Coin Collector Achievement -->
          <div class="text-center p-4 bg-yellow-50 rounded-xl">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-coins-line text-yellow-600 text-2xl"></i>
            </div>
            <h3 class="font-medium text-gray-800 mb-1">Coin Collector</h3>
            <p class="text-sm text-gray-600">Earned 100 coins!</p>
          </div>

          <!-- Streak Master Achievement -->
          <div class="text-center p-4 bg-yellow-50 rounded-xl">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-fire-line text-yellow-600 text-2xl"></i>
            </div>
            <h3 class="font-medium text-gray-800 mb-1">Streak Master</h3>
            <p class="text-sm text-gray-600">5 days in a row!</p>
          </div>
        </div>
      </div>

      <!-- Your Learning Journey Section -->
      <div class="bg-white rounded-2xl shadow-sm p-4 md:p-6">
        <div class="flex items-center gap-2 mb-4">
          <i class="ri-map-pin-line text-blue-500 text-xl"></i>
          <h2 class="text-lg md:text-xl font-semibold text-gray-800">Your Learning Journey</h2>
        </div>
        
        <div class="space-y-4">
          <!-- Welcome to Money World -->
          <div class="flex items-center gap-4 p-4 bg-green-50 rounded-xl">
            <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center flex-shrink-0">
              <i class="ri-check-line text-white"></i>
            </div>
            <div class="flex-1">
              <h3 class="font-medium text-gray-800">Welcome to Money World</h3>
              <p class="text-sm text-gray-600">Learn the basics of money</p>
            </div>
          </div>

          <!-- More journey items would be added here -->
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-xl opacity-50">
            <div class="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0">
              <i class="ri-lock-line text-gray-500"></i>
            </div>
            <div class="flex-1">
              <h3 class="font-medium text-gray-600">Saving Strategies</h3>
              <p class="text-sm text-gray-500">Coming soon...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Dashboard content - all navigation handled by ChildLayout
</script>

<!-- All styles handled by Tailwind CSS following DRY principle -->
</style>