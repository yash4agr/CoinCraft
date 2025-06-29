<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Budget Manager Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-2">Budget Manager 💰</h1>
      <p class="text-gray-600">Track and manage your money allocation</p>
    </div>

    <!-- Current Budget Overview -->
    <div class="mb-8">
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <h2 class="text-xl font-bold text-gray-800 mb-6">Current Budget Split</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Pie Chart -->
          <div class="flex items-center justify-center">
            <div class="relative w-56 h-56">
              <svg class="w-56 h-56 transform -rotate-90" viewBox="0 0 100 100">
                <!-- Saving slice (40%) -->
                <circle cx="50" cy="50" r="35" fill="none" stroke="#10b981" stroke-width="30" 
                        stroke-dasharray="87.9 131.95" stroke-dashoffset="0" />
                <!-- Spending slice (35%) -->
                <circle cx="50" cy="50" r="35" fill="none" stroke="#3b82f6" stroke-width="30" 
                        stroke-dasharray="76.93 142.97" stroke-dashoffset="-87.9" />
                <!-- Wants slice (25%) -->
                <circle cx="50" cy="50" r="35" fill="none" stroke="#f59e0b" stroke-width="30" 
                        stroke-dasharray="54.95 164.85" stroke-dashoffset="-164.83" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-3xl font-bold text-gray-800">245</div>
                  <div class="text-sm text-gray-600">Total Budget</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Budget Categories -->
          <div class="space-y-6">
            <div class="p-4 bg-green-50 rounded-xl border border-green-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-green-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Saving</h3>
                </div>
                <span class="text-sm text-green-600 font-medium">40%</span>
              </div>
              <div class="text-2xl font-bold text-green-600 mb-2">98 coins</div>
              <p class="text-sm text-green-700">Building your future fund</p>
            </div>
            
            <div class="p-4 bg-blue-50 rounded-xl border border-blue-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-blue-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Spending</h3>
                </div>
                <span class="text-sm text-blue-600 font-medium">35%</span>
              </div>
              <div class="text-2xl font-bold text-blue-600 mb-2">86 coins</div>
              <p class="text-sm text-blue-700">Essential purchases & needs</p>
            </div>
            
            <div class="p-4 bg-yellow-50 rounded-xl border border-yellow-200">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-5 h-5 bg-yellow-500 rounded-full"></div>
                  <h3 class="font-semibold text-gray-800">Wants</h3>
                </div>
                <span class="text-sm text-yellow-600 font-medium">25%</span>
              </div>
              <div class="text-2xl font-bold text-yellow-600 mb-2">61 coins</div>
              <p class="text-sm text-yellow-700">Fun purchases & entertainment</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Budget Actions -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Budget Actions</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button class="bg-blue-500 hover:bg-blue-600 text-white p-4 rounded-xl transition-colors">
          <div class="flex items-center gap-3">
            <i class="ri-edit-line text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">Update Budget</div>
              <div class="text-sm opacity-90">Adjust your allocations</div>
            </div>
          </div>
        </button>
        
        <button class="bg-green-500 hover:bg-green-600 text-white p-4 rounded-xl transition-colors">
          <div class="flex items-center gap-3">
            <i class="ri-history-line text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">View History</div>
              <div class="text-sm opacity-90">See past transactions</div>
            </div>
          </div>
        </button>
        
        <button class="bg-purple-500 hover:bg-purple-600 text-white p-4 rounded-xl transition-colors">
          <div class="flex items-center gap-3">
            <i class="ri-save-line text-2xl"></i>
            <div class="text-left">
              <div class="font-semibold">Save Budget</div>
              <div class="text-sm opacity-90">Confirm changes</div>
            </div>
          </div>
        </button>
      </div>
    </div>

    <!-- Recent Transactions -->
    <div class="mb-8">
      <h2 class="text-xl font-bold text-gray-800 mb-6">Transaction History</h2>
      <div class="bg-white rounded-xl shadow-sm">
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <i class="ri-add-line text-green-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">Goal contribution</div>
                <div class="text-sm text-gray-500">To: Headphones fund</div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-green-600 font-semibold">+10 coins</div>
              <div class="text-xs text-gray-500">2 hours ago</div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center">
                <i class="ri-subtract-line text-yellow-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">Entertainment</div>
                <div class="text-sm text-gray-500">Movie tickets</div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-yellow-600 font-semibold">-12 coins</div>
              <div class="text-xs text-gray-500">Yesterday</div>
            </div>
          </div>
        </div>
        
        <div class="p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <i class="ri-shopping-bag-line text-blue-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">School supplies</div>
                <div class="text-sm text-gray-500">Notebooks & pens</div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-blue-600 font-semibold">-8 coins</div>
              <div class="text-xs text-gray-500">2 days ago</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Teen budget management features
</script> 