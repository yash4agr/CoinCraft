<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Budget Overview Section -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Budget Overview 📊</h2>
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Pie Chart Placeholder -->
          <div class="flex items-center justify-center">
            <div class="relative w-48 h-48">
              <svg class="w-48 h-48 transform -rotate-90" viewBox="0 0 100 100">
                <!-- Saving slice (40%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#10b981" stroke-width="20" 
                        stroke-dasharray="100 150" stroke-dashoffset="0" />
                <!-- Spending slice (35%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#3b82f6" stroke-width="20" 
                        stroke-dasharray="87.5 162.5" stroke-dashoffset="-100" />
                <!-- Wants slice (25%) -->
                <circle cx="50" cy="50" r="40" fill="none" stroke="#f59e0b" stroke-width="20" 
                        stroke-dasharray="62.5 187.5" stroke-dashoffset="-187.5" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <div class="text-2xl font-bold text-gray-800">245</div>
                  <div class="text-sm text-gray-600">Total Coins</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Budget Breakdown -->
          <div class="space-y-4">
            <div class="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-green-500 rounded-full"></div>
                <span class="font-medium text-gray-800">Saving</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-green-600">98 coins</div>
                <div class="text-sm text-green-500">40%</div>
              </div>
            </div>
            
            <div class="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-blue-500 rounded-full"></div>
                <span class="font-medium text-gray-800">Spending</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-blue-600">86 coins</div>
                <div class="text-sm text-blue-500">35%</div>
              </div>
            </div>
            
            <div class="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
              <div class="flex items-center gap-3">
                <div class="w-4 h-4 bg-yellow-500 rounded-full"></div>
                <span class="font-medium text-gray-800">Wants</span>
              </div>
              <div class="text-right">
                <div class="font-bold text-yellow-600">61 coins</div>
                <div class="text-sm text-yellow-500">25%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Quick Actions 🚀</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-pie-chart-fill text-2xl text-blue-600"></i>
            </div>
            <h3 class="font-semibold text-gray-800">My Budget</h3>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-target-fill text-2xl text-green-600"></i>
            </div>
            <h3 class="font-semibold text-gray-800">My Goals</h3>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-brain-fill text-2xl text-purple-600"></i>
            </div>
            <h3 class="font-semibold text-gray-800">Activity Hub</h3>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer">
          <div class="text-center">
            <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-3">
              <i class="ri-compass-3-fill text-2xl text-orange-600"></i>
            </div>
            <h3 class="font-semibold text-gray-800">Explore</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Current Goals Progress -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Current Goals 🎯</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">🎧 Headphones</h3>
            <span class="text-sm text-blue-600 font-medium">Week 3 of 6</span>
          </div>
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>30/60 coins</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-blue-500 h-3 rounded-full" style="width: 50%"></div>
            </div>
          </div>
          <p class="text-sm text-gray-600">Strategy: Save 10 coins/week for 6 weeks</p>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-semibold text-gray-800">📱 Phone Case</h3>
            <span class="text-sm text-green-600 font-medium">Almost there!</span>
          </div>
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>20/25 coins</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-green-500 h-3 rounded-full" style="width: 80%"></div>
            </div>
          </div>
          <p class="text-sm text-gray-600">Strategy: Use "Wants" budget</p>
        </div>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-6">Recent Activities 📈</h2>
      <div class="bg-white rounded-xl shadow-sm">
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <i class="ri-arrow-up-line text-green-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">Completed "Smart Spending" module</div>
                <div class="text-sm text-gray-500">2 hours ago</div>
              </div>
            </div>
            <div class="text-green-600 font-semibold">+15 coins</div>
          </div>
        </div>
        
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <i class="ri-target-line text-blue-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">Added to Headphones goal</div>
                <div class="text-sm text-gray-500">Yesterday</div>
              </div>
            </div>
            <div class="text-blue-600 font-semibold">+10 coins</div>
          </div>
        </div>
        
        <div class="p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <i class="ri-brain-line text-purple-600"></i>
              </div>
              <div>
                <div class="font-medium text-gray-800">Finished "Job Earning Scenarios"</div>
                <div class="text-sm text-gray-500">3 days ago</div>
              </div>
            </div>
            <div class="text-purple-600 font-semibold">+25 coins</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Teen dashboard - more sophisticated financial concepts
</script> 