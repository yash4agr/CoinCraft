<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation Bar -->
    <nav class="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50 h-16">
      <div class="flex items-center justify-between h-full px-4 lg:px-6">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <img src="/coin.svg" class="logo-icon" alt="coin">
          <span class="text-xl font-bold text-gray-800">CoinCraft - Parent Portal</span>
        </div>

        <!-- Hamburger Icon (Mobile Only) -->
        <button 
          @click="toggleProfileMenu"
          class="sm:hidden flex items-center p-2 rounded hover:bg-gray-100"
        >
          <i class="ri-menu-line text-xl text-gray-700"></i>
        </button>

        <!-- Profile Section (Desktop Only) -->
        <div class="hidden sm:flex items-center gap-4">
          <div class="relative profile-dropdown">
            <button 
              @click="toggleProfileMenu"
              class="profile-button flex items-center gap-2 p-1 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <img 
                :src="getAvatarUrl()"
                :alt="`${authStore.user?.fullName}'s Avatar`" 
                class="w-10 h-10 rounded-full border-2 border-green-300"
              />
              <div class="hidden sm:block">
                <div class="text-sm font-medium text-gray-800">{{ authStore.user?.fullName }}</div>
                <div class="text-xs text-gray-500">Parent</div>
              </div>
              <i class="ri-arrow-down-s-line text-gray-500 hidden sm:block"></i>
            </button>

            <!-- Dropdown Menu (Desktop) -->
            <div 
              v-if="showProfileMenu"
              class="absolute right-0 top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
            >
              <div class="px-4 py-2 border-b border-gray-100">
                <div class="font-medium text-gray-800">{{ authStore.user?.fullName }}</div>
                <div class="text-sm text-gray-500">CoinCraft Parent</div>
              </div>
              <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
                <i class="ri-user-3-line text-gray-400"></i> <span>My Profile</span>
              </button>
              <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
                <i class="ri-settings-3-line text-gray-400"></i> <span>Settings</span>
              </button>
              <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
                <i class="ri-question-line text-gray-400"></i> <span>Help</span>
              </button>
              <div class="border-t border-gray-100 mt-2 pt-2">
                <button 
                  @click="handleLogout"
                  class="w-full flex items-center gap-3 px-4 py-2 text-red-600 hover:bg-red-50 transition-colors"
                >
                  <i class="ri-logout-box-line text-red-400"></i> <span>Logout</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile Dropdown Menu -->
      <div 
        v-if="showProfileMenu"
        class="sm:hidden absolute right-4 top-16 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
      >
        <div class="px-4 py-2 border-b">
          <div class="font-medium text-gray-800">{{ authStore.user?.fullName }}</div>
          <div class="text-sm text-gray-500">CoinCraft Parent</div>
        </div>
        <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
          <i class="ri-user-3-line text-gray-400"></i> <span>My Profile</span>
        </button>
        <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
          <i class="ri-settings-3-line text-gray-400"></i> <span>Settings</span>
        </button>
        <button class="w-full flex items-center gap-3 px-4 py-2 text-gray-700 hover:bg-gray-50 transition-colors">
          <i class="ri-question-line text-gray-400"></i> <span>Help</span>
        </button>
        <div class="border-t border-gray-100 mt-2 pt-2">
          <button 
            @click="handleLogout"
            class="w-full flex items-center gap-3 px-4 py-2 text-red-600 hover:bg-red-50 transition-colors"
          >
            <i class="ri-logout-box-line text-red-400"></i> <span>Logout</span>
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="transition-all duration-300 pt-16 pb-4">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const showProfileMenu = ref(false)

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  const dropdowns = document.querySelectorAll('.profile-dropdown, .profile-button')
  const isInside = [...dropdowns].some(el => el.contains(target))
  if (!isInside) showProfileMenu.value = false
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const getAvatarUrl = () => {
  const name = authStore.user?.fullName || 'Parent'
  return `https://avataaars.io/?avatarStyle=Circle&topType=LongHairStraight&accessoriesType=Blank&hairColor=BrownDark&facialHairType=Blank&clotheType=BlazerShirt&eyeType=Default&eyebrowType=Default&mouthType=Default&skinColor=Light&seed=${encodeURIComponent(name)}`
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    // Even if logout fails, redirect to home page
    router.push('/')
  }
}
</script>

<style scoped>
.logo-icon {
  width: 36px;
  height: 36px;
}
.profile-dropdown {
  position: relative;
}
.profile-button {
  cursor: pointer;
}
</style>
