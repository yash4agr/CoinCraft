<template>
  <div class="min-h-screen bg-gray-50 p-4 pb-20">
    <!-- Main Content Container -->
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">My Profile</h1>
        <p class="text-gray-600">Manage your account and notification preferences</p>
      </div>

      <!-- Profile and Notifications Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile Section -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Profile Picture and Basic Info -->
          <div class="bg-white rounded-2xl shadow-sm p-6">
            <div class="flex flex-col sm:flex-row items-center gap-6">
              <!-- Profile Picture -->
              <div class="relative">
                <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 border-4 border-white shadow-lg">
                  <img 
                    v-if="profileData.avatar"
                    :src="profileData.avatar" 
                    :alt="`${profileData.fullName}'s profile picture`"
                    class="w-full h-full object-cover"
                  />
                  <div v-else class="w-full h-full flex items-center justify-center text-4xl text-gray-400">
                    <i class="ri-user-line"></i>
                  </div>
                </div>
                
                <!-- Upload Button -->
                <button 
                  @click="triggerFileUpload"
                  class="absolute bottom-0 right-0 w-10 h-10 bg-blue-500 hover:bg-blue-600 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
                  :aria-label="profileData.avatar ? 'Change profile picture' : 'Upload profile picture'"
                >
                  <i class="ri-camera-line text-lg"></i>
                </button>
                
                <!-- Hidden File Input -->
                <input 
                  ref="fileInput"
                  type="file" 
                  accept="image/*" 
                  @change="handleFileUpload"
                  class="hidden"
                  aria-hidden="true"
                />
              </div>
              
              <!-- Basic Info -->
              <div class="flex-1 text-center sm:text-left">
                <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ profileData.fullName }}</h2>
                <p class="text-gray-600 mb-1">@{{ profileData.username }}</p>
                <p class="text-gray-600 mb-3">{{ profileData.email }}</p>
                <div class="flex flex-wrap gap-2 justify-center sm:justify-start">
                  <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                    {{ getRoleDisplayName(profileData.role) }}
                  </span>
                  <span class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                    Level {{ profileData.level }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- About Me Section -->
          <div class="bg-white rounded-2xl shadow-sm p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-800">About Me</h3>
              <button 
                @click="toggleEditBio"
                class="text-blue-500 hover:text-blue-600 transition-colors"
                :aria-label="isEditingBio ? 'Cancel editing bio' : 'Edit bio'"
              >
                <i :class="isEditingBio ? 'ri-close-line' : 'ri-edit-line'"></i>
              </button>
            </div>
            
            <div v-if="!isEditingBio">
              <p v-if="profileData.bio" class="text-gray-700 leading-relaxed">{{ profileData.bio }}</p>
              <p v-else class="text-gray-500 italic">No bio added yet. Click edit to add one!</p>
            </div>
            
            <div v-else class="space-y-4">
              <textarea 
                v-model="editedBio"
                placeholder="Tell us about yourself..."
                class="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="4"
                maxlength="500"
                :aria-label="'Edit bio, maximum 500 characters'"
              ></textarea>
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-500">{{ editedBio.length }}/500 characters</span>
                <div class="flex gap-2">
                  <button 
                    @click="cancelEditBio"
                    class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button 
                    @click="saveBio"
                    :disabled="isSavingBio"
                    class="px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white rounded-lg transition-colors"
                  >
                    {{ isSavingBio ? 'Saving...' : 'Save' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="bg-white rounded-2xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Contact Information</h3>
            <div class="space-y-4">
              <div class="flex items-center gap-3">
                <i class="ri-mail-line text-gray-400"></i>
                <span class="text-gray-700">{{ profileData.email }}</span>
              </div>
              <div class="flex items-center gap-3">
                <i class="ri-phone-line text-gray-400"></i>
                <span class="text-gray-700">{{ profileData.phone || 'Not provided' }}</span>
              </div>
              <div class="flex items-center gap-3">
                <i class="ri-map-pin-line text-gray-400"></i>
                <span class="text-gray-700">{{ profileData.location || 'Not provided' }}</span>
              </div>
            </div>
          </div>

          <!-- Account Information -->
          <div class="bg-white rounded-2xl shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Account Information</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Member Since</label>
                <p class="text-gray-800">{{ formatDate(profileData.createdAt) }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Last Login</label>
                <p class="text-gray-800">{{ formatDate(profileData.lastLogin) }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Total Coins Earned</label>
                <p class="text-gray-800 flex items-center gap-1">
                  <img src="/coin.svg" class="logo-icon" alt="coin">
                  {{ profileData.totalCoinsEarned }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Goals Completed</label>
                <p class="text-gray-800">{{ profileData.goalsCompleted }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Notification Center -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-2xl shadow-sm p-6 sticky top-4">
            <!-- Notification Header -->
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-semibold text-gray-800">Notifications</h3>
                <span 
                  v-if="unreadCount > 0"
                  class="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full min-w-[20px] text-center"
                  :aria-label="`${unreadCount} unread notifications`"
                >
                  {{ unreadCount > 99 ? '99+' : unreadCount }}
                </span>
              </div>
              
              <!-- Notification Actions -->
              <div class="flex items-center gap-2">
                <button 
                  @click="toggleNotificationSettings"
                  class="text-gray-400 hover:text-gray-600 transition-colors"
                  :aria-label="'Notification settings'"
                >
                  <i class="ri-settings-3-line"></i>
                </button>
                <button 
                  @click="markAllAsRead"
                  :disabled="unreadCount === 0"
                  class="text-gray-400 hover:text-gray-600 disabled:text-gray-300 transition-colors"
                  :aria-label="'Mark all notifications as read'"
                >
                  <i class="ri-check-double-line"></i>
                </button>
                <button 
                  @click="clearAllNotifications"
                  :disabled="notifications.length === 0"
                  class="text-gray-400 hover:text-red-500 disabled:text-gray-300 transition-colors"
                  :aria-label="'Clear all notifications'"
                >
                  <i class="ri-delete-bin-line"></i>
                </button>
              </div>
            </div>

            <!-- Notification Filters -->
            <div class="mb-4">
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="filter in notificationFilters"
                  :key="filter.value"
                  @click="selectedFilter = filter.value"
                  class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
                  :class="selectedFilter === filter.value 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
                  :aria-pressed="selectedFilter === filter.value"
                >
                  {{ filter.label }}
                </button>
              </div>
            </div>

            <!-- Notification Settings Panel -->
            <div v-if="showNotificationSettings" class="mb-4 p-4 bg-gray-50 rounded-lg">
              <h4 class="font-medium text-gray-800 mb-3">Notification Preferences</h4>
              <div class="space-y-3">
                <label class="flex items-center gap-3 cursor-pointer">
                  <input 
                    v-model="notificationPreferences.system"
                    type="checkbox" 
                    class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">System notifications</span>
                </label>
                <label class="flex items-center gap-3 cursor-pointer">
                  <input 
                    v-model="notificationPreferences.messages"
                    type="checkbox" 
                    class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">Message notifications</span>
                </label>
                <label class="flex items-center gap-3 cursor-pointer">
                  <input 
                    v-model="notificationPreferences.updates"
                    type="checkbox" 
                    class="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                  />
                  <span class="text-sm text-gray-700">Update notifications</span>
                </label>
              </div>
              <button 
                @click="saveNotificationPreferences"
                class="mt-3 w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm transition-colors"
              >
                Save Preferences
              </button>
            </div>

            <!-- Notifications List -->
            <div class="space-y-3 max-h-96 overflow-y-auto">
              <div v-if="isLoadingNotifications" class="text-center py-8">
                <div class="animate-spin w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full mx-auto mb-2"></div>
                <p class="text-sm text-gray-500">Loading notifications...</p>
              </div>
              
              <div v-else-if="filteredNotifications.length === 0" class="text-center py-8">
                <i class="ri-notification-off-line text-4xl text-gray-300 mb-2"></i>
                <p class="text-sm text-gray-500">No notifications found</p>
              </div>
              
              <div 
                v-else
                v-for="notification in paginatedNotifications" 
                :key="notification.id"
                class="p-3 rounded-lg border transition-colors cursor-pointer"
                :class="{
                  'bg-blue-50 border-blue-200': !notification.read,
                  'bg-white border-gray-200 hover:bg-gray-50': notification.read
                }"
                @click="markAsRead(notification.id)"
                :aria-label="`Notification: ${notification.title}`"
                role="button"
                tabindex="0"
                @keydown.enter="markAsRead(notification.id)"
                @keydown.space.prevent="markAsRead(notification.id)"
              >
                <div class="flex items-start gap-3">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                    :class="getNotificationIconClass(notification.type)"
                  >
                    <i :class="getNotificationIcon(notification.type)" class="text-sm"></i>
                  </div>
                  
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                      <h4 class="font-medium text-gray-800 text-sm truncate">{{ notification.title }}</h4>
                      <div class="flex items-center gap-2 flex-shrink-0">
                        <span class="text-xs text-gray-500">{{ formatNotificationTime(notification.timestamp) }}</span>
                        <button 
                          @click.stop="deleteNotification(notification.id)"
                          class="text-gray-400 hover:text-red-500 transition-colors"
                          :aria-label="`Delete notification: ${notification.title}`"
                        >
                          <i class="ri-close-line text-xs"></i>
                        </button>
                      </div>
                    </div>
                    <p class="text-sm text-gray-600 line-clamp-2">{{ notification.message }}</p>
                    <div class="flex items-center justify-between mt-2">
                      <span 
                        class="text-xs px-2 py-1 rounded-full"
                        :class="getNotificationTypeClass(notification.type)"
                      >
                        {{ notification.type }}
                      </span>
                      <div v-if="!notification.read" class="w-2 h-2 bg-blue-500 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="mt-4 flex items-center justify-between">
              <button 
                @click="previousPage"
                :disabled="currentPage === 1"
                class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:text-gray-400 transition-colors"
              >
                Previous
              </button>
              <span class="text-sm text-gray-500">
                Page {{ currentPage }} of {{ totalPages }}
              </span>
              <button 
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:text-gray-400 transition-colors"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div 
      v-if="showSuccessToast" 
      class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform"
      :class="showSuccessToast ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="flex items-center gap-2">
        <i class="ri-check-line"></i>
        <span>{{ successMessage }}</span>
      </div>
    </div>

    <!-- Error Toast -->
    <div 
      v-if="showErrorToast" 
      class="fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform"
      :class="showErrorToast ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="flex items-center gap-2">
        <i class="ri-error-warning-line"></i>
        <span>{{ errorMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'

const userStore = useUserStore()
const authStore = useAuthStore()

const profileData = ref({
  fullName: authStore.user?.fullName || '',
  username: authStore.user?.username || '',
  email: authStore.user?.email || '',
  role: authStore.user?.role || 'younger_child',
  level: userStore.profile?.level || 1,
  avatar: '',
  bio: '',
  phone: '',
  location: '',
  createdAt: authStore.user?.createdAt || new Date().toISOString(),
  lastLogin: new Date().toISOString(),
  totalCoinsEarned: userStore.profile?.totalCoinsEarned || 0,
  goalsCompleted: userStore.profile?.goalsCompleted || 0
})
console.log("This is from UserProfile.vue", profileData.value)
const isEditingBio = ref(false)
const editedBio = ref('')
const isSavingBio = ref(false)
const fileInput = ref<HTMLInputElement>()
const notifications = ref<Notification[]>([])
const isLoadingNotifications = ref(false)
const selectedFilter = ref('all')
const currentPage = ref(1)
const notificationsPerPage = 10
const showNotificationSettings = ref(false)

const notificationPreferences = ref({
  system: true,
  messages: true,
  updates: true
})

const showSuccessToast = ref(false)
const showErrorToast = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

interface Notification {
  id: string
  title: string
  message: string
  type: 'system' | 'message' | 'update'
  read: boolean
  timestamp: string
}

const notificationFilters = [
  { label: 'All', value: 'all' },
  { label: 'System', value: 'system' },
  { label: 'Messages', value: 'message' },
  { label: 'Updates', value: 'update' },
  { label: 'Unread', value: 'unread' }
]

const unreadCount = computed(() => 
  notifications.value.filter(n => !n.read).length
)

const filteredNotifications = computed(() => {
  let filtered = notifications.value

  if (selectedFilter.value === 'unread') {
    filtered = filtered.filter(n => !n.read)
  } else if (selectedFilter.value !== 'all') {
    filtered = filtered.filter(n => n.type === selectedFilter.value)
  }

  return filtered.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
})

const totalPages = computed(() => 
  Math.ceil(filteredNotifications.value.length / notificationsPerPage)
)

const paginatedNotifications = computed(() => {
  const start = (currentPage.value - 1) * notificationsPerPage
  const end = start + notificationsPerPage
  return filteredNotifications.value.slice(start, end)
})

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (!file) return
  
  if (!file.type.startsWith('image/')) {
    showError('Please select a valid image file')
    return
  }
  
  if (file.size > 5 * 1024 * 1024) {
    showError('Image size must be less than 5MB')
    return
  }
  
  try {
    const reader = new FileReader()
    reader.onload = (e) => {
      profileData.value.avatar = e.target?.result as string
      showSuccess('Profile picture updated successfully!')
    }
    reader.readAsDataURL(file)
  } catch (error) {
    showError('Failed to upload image. Please try again.')
  }
}

const toggleEditBio = () => {
  if (!isEditingBio.value) {
    editedBio.value = profileData.value.bio
  }
  isEditingBio.value = !isEditingBio.value
}

const cancelEditBio = () => {
  editedBio.value = profileData.value.bio
  isEditingBio.value = false
}

const saveBio = async () => {
  isSavingBio.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    profileData.value.bio = editedBio.value
    isEditingBio.value = false
    showSuccess('Bio updated successfully!')
  } catch (error) {
    showError('Failed to update bio. Please try again.')
  } finally {
    isSavingBio.value = false
  }
}

const loadNotifications = async () => {
  isLoadingNotifications.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    notifications.value = [
      {
        id: '1',
        title: 'Welcome to CoinCraft!',
        message: 'Start your financial learning journey today.',
        type: 'system',
        read: false,
        timestamp: new Date().toISOString()
      },
      {
        id: '2',
        title: 'Goal Achievement',
        message: 'Congratulations! You completed your savings goal.',
        type: 'update',
        read: false,
        timestamp: new Date(Date.now() - 3600000).toISOString()
      },
      {
        id: '3',
        title: 'New Message',
        message: 'You have a new message from your parent.',
        type: 'message',
        read: true,
        timestamp: new Date(Date.now() - 7200000).toISOString()
      },
      {
        id: '4',
        title: 'Coin Reward',
        message: 'You earned 25 coins for completing a task!',
        type: 'system',
        read: true,
        timestamp: new Date(Date.now() - 86400000).toISOString()
      },
      {
        id: '5',
        title: 'Weekly Report',
        message: 'Your weekly financial progress report is ready.',
        type: 'update',
        read: false,
        timestamp: new Date(Date.now() - 172800000).toISOString()
      }
    ]
  } catch (error) {
    showError('Failed to load notifications')
  } finally {
    isLoadingNotifications.value = false
  }
}

const markAsRead = (notificationId: string) => {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification && !notification.read) {
    notification.read = true
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
  showSuccess('All notifications marked as read')
}

const deleteNotification = (notificationId: string) => {
  const index = notifications.value.findIndex(n => n.id === notificationId)
  if (index > -1) {
    notifications.value.splice(index, 1)
    showSuccess('Notification deleted')
  }
}

const clearAllNotifications = () => {
  if (confirm('Are you sure you want to clear all notifications?')) {
    notifications.value = []
    currentPage.value = 1
    showSuccess('All notifications cleared')
  }
}

const toggleNotificationSettings = () => {
  showNotificationSettings.value = !showNotificationSettings.value
}

const saveNotificationPreferences = () => {
  showSuccess('Notification preferences saved')
  showNotificationSettings.value = false
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const getRoleDisplayName = (role: string) => {
  const roleMap: Record<string, string> = {
    'younger_child': 'Young Learner',
    'older_child': 'Teen Investor',
    'parent': 'Parent',
    'teacher': 'Teacher'
  }
  return roleMap[role] || role
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatNotificationTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
  return `${Math.floor(diffInMinutes / 1440)}d ago`
}

const getNotificationIcon = (type: string) => {
  const iconMap: Record<string, string> = {
    'system': 'ri-settings-line',
    'message': 'ri-message-line',
    'update': 'ri-notification-line'
  }
  return iconMap[type] || 'ri-notification-line'
}

const getNotificationIconClass = (type: string) => {
  const classMap: Record<string, string> = {
    'system': 'bg-blue-100 text-blue-600',
    'message': 'bg-green-100 text-green-600',
    'update': 'bg-purple-100 text-purple-600'
  }
  return classMap[type] || 'bg-gray-100 text-gray-600'
}

const getNotificationTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    'system': 'bg-blue-100 text-blue-700',
    'message': 'bg-green-100 text-green-700',
    'update': 'bg-purple-100 text-purple-700'
  }
  return classMap[type] || 'bg-gray-100 text-gray-700'
}

const showSuccess = (message: string) => {
  successMessage.value = message
  showSuccessToast.value = true
  setTimeout(() => {
    showSuccessToast.value = false
  }, 3000)
}

const showError = (message: string) => {
  errorMessage.value = message
  showErrorToast.value = true
  setTimeout(() => {
    showErrorToast.value = false
  }, 3000)
}

let notificationInterval: number

const simulateRealTimeNotifications = () => {
  notificationInterval = setInterval(() => {
    if (Math.random() < 0.1) {
      const newNotification: Notification = {
        id: Date.now().toString(),
        title: 'New Activity',
        message: 'You have new activity to check out!',
        type: ['system', 'message', 'update'][Math.floor(Math.random() * 3)] as any,
        read: false,
        timestamp: new Date().toISOString()
      }
      notifications.value.unshift(newNotification)
      
      if (notifications.value.length > 50) {
        notifications.value = notifications.value.slice(0, 50)
      }
    }
  }, 30000)
}

onMounted(() => {
  loadNotifications()
  simulateRealTimeNotifications()
})

onUnmounted(() => {
  if (notificationInterval) {
    clearInterval(notificationInterval)
  }
})

watch(selectedFilter, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

* {
  transition: all 0.2s ease;
}

button:focus,
input:focus,
textarea:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.transform {
  transition: transform 0.3s ease-in-out;
}

@media (max-width: 640px) {
  .sticky {
    position: static;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style> 