<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation Bar - Always Visible -->
    <nav class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50 h-16">
      <div class="flex items-center justify-between h-full px-4 lg:px-6">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <i class="ri-coins-fill text-2xl text-blue-500"></i>
          <span class="text-xl font-bold text-gray-800">CoinCraft</span>
        </div>
        
        <!-- Profile Section -->
        <div class="flex items-center gap-4">
          <!-- Coin Balance -->
          <div class="flex items-center gap-1 bg-blue-100 px-3 py-1 rounded-full border border-blue-300">
            <i class="ri-coins-fill text-blue-600"></i>
            <span class="font-semibold text-blue-800">245</span>
          </div>
          
          <!-- Profile Dropdown -->
          <div class="relative profile-dropdown">
            <button 
              @click="toggleProfileMenu"
              class="profile-button flex items-center gap-2 p-1 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <img 
                src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=Hoodie&clotheColor=Blue01&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light"
                alt="Harry's Avatar" 
                class="w-10 h-10 rounded-full border-2 border-blue-300"
              />
              <div class="hidden sm:block">
                <div class="text-sm font-medium text-gray-800">Hi Harry!</div>
              </div>
              <i class="ri-arrow-down-s-line text-gray-500 hidden sm:block"></i>
            </button>
            
            <!-- Profile Dropdown Menu -->
            <div 
              v-if="showProfileMenu"
              class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
            >
              <div class="px-4 py-2 border-b border-gray-100">
                <div class="font-medium text-gray-800">Harry</div>
                <div class="text-sm text-gray-500">Level 5 Investor</div>
              </div>
              
              <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
                <i class="ri-user-3-line text-gray-400"></i>
                <span>My Profile</span>
              </button>
              
              <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
                <i class="ri-question-line text-gray-400"></i>
                <span>Help</span>
              </button>
              
              <div class="border-t border-gray-100 mt-2 pt-2">
                <button class="w-full flex items-center gap-3 px-4 py-2 text-red-600 hover:bg-red-50 transition-colors">
                  <i class="ri-logout-box-line text-red-400"></i>
                  <span>Logout</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Sidebar for Desktop -->
    <aside 
      class="fixed left-0 top-16 h-full bg-white border-r border-gray-200 z-40 transition-all duration-300 hidden lg:block"
      :class="sidebarCollapsed ? 'w-16' : 'w-64'"
    >
      <!-- Sidebar Toggle -->
      <div class="flex justify-end p-3 border-b border-gray-100">
        <button 
          @click="toggleSidebar"
          class="p-1 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <i :class="sidebarCollapsed ? 'ri-arrow-right-s-line' : 'ri-arrow-left-s-line'" class="text-gray-500"></i>
        </button>
      </div>

      <!-- Navigation Links -->
      <nav class="p-4 space-y-2">
        <router-link 
          v-for="item in navigationItems" 
          :key="item.name"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-3 rounded-lg transition-colors hover:bg-blue-50"
          :class="$route.name === item.name ? 'bg-blue-100 text-blue-600' : 'text-gray-700 hover:text-blue-600'"
        >
          <i :class="item.icon" class="text-xl min-w-[1.25rem]"></i>
          <span v-if="!sidebarCollapsed" class="font-medium">{{ item.label }}</span>
        </router-link>
      </nav>
    </aside>

    <!-- Main Content Area -->
    <main 
      class="transition-all duration-300 pt-16 lg:pt-16 pb-20 lg:pb-4"
      :class="sidebarCollapsed ? 'lg:pl-16' : 'lg:pl-64'"
    >
      <router-view />
    </main>

    <!-- Bottom Navigation for Mobile/Tablet -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-40 lg:hidden">
      <div class="grid grid-cols-5 h-16">
        <router-link 
          v-for="item in navigationItems" 
          :key="item.name"
          :to="item.path"
          class="flex flex-col items-center justify-center gap-1 transition-colors"
          :class="$route.name === item.name ? 'text-blue-600 bg-blue-50' : 'text-gray-500 hover:text-blue-600'"
        >
          <i :class="item.icon" class="text-xl"></i>
          <span class="text-xs font-medium">{{ item.label }}</span>
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const sidebarCollapsed = ref(false)
const showProfileMenu = ref(false)

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

// Close profile menu when clicking outside
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  const profileDropdown = document.querySelector('.profile-dropdown')
  const profileButton = document.querySelector('.profile-button')
  
  if (profileDropdown && profileButton && 
      !profileDropdown.contains(target) && 
      !profileButton.contains(target)) {
    showProfileMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Teen navigation items - more sophisticated than child version
const navigationItems = [
  {
    name: 'TeenDashboard',
    path: '/teen/dashboard',
    label: 'Dashboard',
    icon: 'ri-dashboard-3-fill'
  },
  {
    name: 'TeenBudget',
    path: '/teen/budget',
    label: 'My Budget',
    icon: 'ri-pie-chart-fill'
  },
  {
    name: 'TeenGoals',
    path: '/teen/goals',
    label: 'My Goals',
    icon: 'ri-target-fill'
  },
  {
    name: 'TeenActivities',
    path: '/teen/activities',
    label: 'Activity Hub',
    icon: 'ri-brain-fill'
  },
  {
    name: 'TeenExplore',
    path: '/teen/explore',
    label: 'Explore',
    icon: 'ri-compass-3-fill'
  }
]
</script> 