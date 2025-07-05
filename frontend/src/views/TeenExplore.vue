<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 p-4 pb-20">
    <!-- Header Section -->
    <div class="max-w-7xl mx-auto mb-8">
      <div class="text-center mb-8">
        <h1 class="text-4xl lg:text-5xl font-bold text-gray-800 mb-4">
          <span class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Explore Financial World
          </span>
          🌍
        </h1>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Discover exciting financial concepts, activities, and expand your knowledge through interactive learning experiences
        </p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex flex-col lg:flex-row gap-4 items-center">
          <!-- Search Input -->
          <div class="relative flex-1 w-full lg:w-auto">
            <i class="ri-search-line absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search activities, topics, or concepts..."
              class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              @input="handleSearch"
            />
            <div v-if="searchQuery" class="absolute right-4 top-1/2 transform -translate-y-1/2">
              <button
                @click="clearSearch"
                class="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <i class="ri-close-line"></i>
              </button>
            </div>
          </div>

          <!-- Filter Buttons -->
          <div class="flex flex-wrap gap-2">
            <!-- Category Filter -->
            <select
              v-model="selectedCategory"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category" :value="category">
                {{ category }}
              </option>
            </select>

            <!-- Difficulty Filter -->
            <select
              v-model="selectedDifficulty"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>

            <!-- Time Filter -->
            <select
              v-model="selectedTimeCommitment"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="">Any Duration</option>
              <option value="short">Short (< 15 min)</option>
              <option value="medium">Medium (15-30 min)</option>
              <option value="long">Long (30+ min)</option>
            </select>

            <!-- Clear Filters -->
            <button
              v-if="hasActiveFilters"
              @click="clearFilters"
              class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
            >
              Clear Filters
            </button>
          </div>
        </div>

        <!-- Active Filters Display -->
        <div v-if="hasActiveFilters" class="mt-4 flex flex-wrap gap-2">
          <span class="text-sm text-gray-600">Active filters:</span>
          <span v-if="selectedCategory" class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">
            {{ selectedCategory }}
          </span>
          <span v-if="selectedDifficulty" class="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">
            {{ selectedDifficulty }}
          </span>
          <span v-if="selectedTimeCommitment" class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
            {{ getTimeLabel(selectedTimeCommitment) }}
          </span>
        </div>
      </div>

      <!-- Results Summary -->
      <div class="mb-6">
        <p class="text-gray-600">
          Showing {{ filteredActivities.length }} of {{ activities.length }} activities
          <span v-if="searchQuery"> for "{{ searchQuery }}"</span>
        </p>
      </div>
    </div>

    <!-- Activities Grid -->
    <div class="max-w-7xl mx-auto">
      <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <!-- Loading Skeletons -->
        <div v-for="i in 8" :key="i" class="bg-white rounded-2xl shadow-lg overflow-hidden">
          <div class="h-48 bg-gray-200 animate-pulse"></div>
          <div class="p-6">
            <div class="h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
            <div class="h-3 bg-gray-200 rounded animate-pulse mb-4"></div>
            <div class="flex gap-2 mb-4">
              <div class="h-6 w-16 bg-gray-200 rounded-full animate-pulse"></div>
              <div class="h-6 w-20 bg-gray-200 rounded-full animate-pulse"></div>
            </div>
            <div class="h-10 bg-gray-200 rounded animate-pulse"></div>
          </div>
        </div>
      </div>

      <div v-else-if="filteredActivities.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-semibold text-gray-700 mb-2">No activities found</h3>
        <p class="text-gray-500 mb-6">Try adjusting your search or filters to find more activities.</p>
        <button
          @click="clearFilters"
          class="px-6 py-3 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg transition-colors"
        >
          Clear All Filters
        </button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ActivityCard
          v-for="activity in paginatedActivities"
          :key="activity.id"
          :activity="activity"
          @like="toggleLike"
          @bookmark="toggleBookmark"
          @share="shareActivity"
          @rate="rateActivity"
          @expand="expandActivity"
          @start="startActivity"
        />
      </div>

      <!-- Load More Button -->
      <div v-if="showLoadMore" class="text-center mt-12">
        <button
          @click="loadMore"
          :disabled="isLoadingMore"
          class="px-8 py-3 bg-indigo-500 hover:bg-indigo-600 disabled:bg-indigo-300 text-white rounded-lg transition-colors font-medium"
        >
          {{ isLoadingMore ? 'Loading...' : 'Load More Activities' }}
        </button>
      </div>
    </div>

    <!-- Favorites Section -->
    <div v-if="favoriteActivities.length > 0" class="max-w-7xl mx-auto mt-16">
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <i class="ri-heart-fill text-red-500 mr-3"></i>
          Your Favorites
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ActivityCard
            v-for="activity in favoriteActivities.slice(0, 6)"
            :key="`fav-${activity.id}`"
            :activity="activity"
            :is-favorite-view="true"
            @like="toggleLike"
            @bookmark="toggleBookmark"
            @share="shareActivity"
            @rate="rateActivity"
            @expand="expandActivity"
            @start="startActivity"
          />
        </div>
        <div v-if="favoriteActivities.length > 6" class="text-center mt-6">
          <button
            @click="showAllFavorites"
            class="text-indigo-600 hover:text-indigo-700 font-medium"
          >
            View All {{ favoriteActivities.length }} Favorites
          </button>
        </div>
      </div>
    </div>

    <!-- Activity Detail Modal -->
    <ActivityDetailModal
      v-if="selectedActivity"
      :activity="selectedActivity"
      :is-open="showDetailModal"
      @close="closeDetailModal"
      @like="toggleLike"
      @bookmark="toggleBookmark"
      @share="shareActivity"
      @rate="rateActivity"
      @start="startActivity"
      @comment="addComment"
    />

    <!-- Success Toast -->
    <div
      v-if="showToast"
      class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform"
      :class="showToast ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="flex items-center gap-2">
        <i class="ri-check-line"></i>
        <span>{{ toastMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import ActivityCard from '@/components/explore/ActivityCard.vue'
import ActivityDetailModal from '@/components/explore/ActivityDetailModal.vue'

// Interfaces
interface Activity {
  id: string
  title: string
  description: string
  detailedDescription: string
  image: string
  category: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  timeCommitment: number // in minutes
  ageRecommendation: string
  tags: string[]
  likes: number
  rating: number
  totalRatings: number
  isLiked: boolean
  isBookmarked: boolean
  isCompleted: boolean
  progress: number
  comments: Comment[]
  relatedActivities: string[]
  learningObjectives: string[]
  prerequisites: string[]
}

interface Comment {
  id: string
  userId: string
  userName: string
  userAvatar: string
  content: string
  timestamp: string
  likes: number
  isLiked: boolean
}

// Reactive data
const activities = ref<Activity[]>([])
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const selectedTimeCommitment = ref('')
const isLoading = ref(true)
const isLoadingMore = ref(false)
const currentPage = ref(1)
const itemsPerPage = 12
const selectedActivity = ref<Activity | null>(null)
const showDetailModal = ref(false)
const showToast = ref(false)
const toastMessage = ref('')

// Categories
const categories = [
  'Investing', 'Budgeting', 'Entrepreneurship', 'Banking', 'Cryptocurrency',
  'Real Estate', 'Insurance', 'Taxes', 'Career Planning', 'Economics'
]

// Computed properties
const hasActiveFilters = computed(() => 
  selectedCategory.value || selectedDifficulty.value || selectedTimeCommitment.value || searchQuery.value
)

const filteredActivities = computed(() => {
  let filtered = activities.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(activity =>
      activity.title.toLowerCase().includes(query) ||
      activity.description.toLowerCase().includes(query) ||
      activity.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(activity => activity.category === selectedCategory.value)
  }

  // Difficulty filter
  if (selectedDifficulty.value) {
    filtered = filtered.filter(activity => activity.difficulty === selectedDifficulty.value)
  }

  // Time commitment filter
  if (selectedTimeCommitment.value) {
    filtered = filtered.filter(activity => {
      const time = activity.timeCommitment
      switch (selectedTimeCommitment.value) {
        case 'short': return time < 15
        case 'medium': return time >= 15 && time <= 30
        case 'long': return time > 30
        default: return true
      }
    })
  }

  return filtered
})

const paginatedActivities = computed(() => {
  const endIndex = currentPage.value * itemsPerPage
  return filteredActivities.value.slice(0, endIndex)
})

const showLoadMore = computed(() => 
  paginatedActivities.value.length < filteredActivities.value.length
)

const favoriteActivities = computed(() => 
  activities.value.filter(activity => activity.isLiked || activity.isBookmarked)
)

// Methods
const loadActivities = async () => {
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Generate demo activities
    activities.value = generateDemoActivities()
  } catch (error) {
    console.error('Failed to load activities:', error)
  } finally {
    isLoading.value = false
  }
}

const generateDemoActivities = (): Activity[] => {
  const demoActivities: Activity[] = [
    {
      id: '1',
      title: 'Stock Market Simulator',
      description: 'Learn to invest in stocks with virtual money and real market data.',
      detailedDescription: 'Experience the thrill of stock trading without the risk! This comprehensive simulator uses real market data to teach you investment strategies, portfolio management, and risk assessment. Perfect for beginners who want to understand how the stock market works.',
      image: 'https://images.pexels.com/photos/6801648/pexels-photo-6801648.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Investing',
      difficulty: 'intermediate',
      timeCommitment: 25,
      ageRecommendation: '14-18',
      tags: ['stocks', 'investing', 'simulation', 'portfolio'],
      likes: 234,
      rating: 4.7,
      totalRatings: 89,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['2', '3'],
      learningObjectives: ['Understand stock market basics', 'Learn portfolio diversification', 'Practice risk management'],
      prerequisites: ['Basic math skills', 'Understanding of percentages']
    },
    {
      id: '2',
      title: 'Budget Challenge Game',
      description: 'Master budgeting skills through real-life scenarios and challenges.',
      detailedDescription: 'Take on the ultimate budgeting challenge! Navigate through various life scenarios from college student to young professional, making financial decisions that impact your virtual life. Learn to balance wants vs needs while building healthy financial habits.',
      image: 'https://images.pexels.com/photos/4386431/pexels-photo-4386431.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Budgeting',
      difficulty: 'beginner',
      timeCommitment: 20,
      ageRecommendation: '13-17',
      tags: ['budgeting', 'planning', 'expenses', 'savings'],
      likes: 189,
      rating: 4.5,
      totalRatings: 67,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['4', '5'],
      learningObjectives: ['Create effective budgets', 'Track expenses', 'Set financial priorities'],
      prerequisites: ['Basic arithmetic']
    },
    {
      id: '3',
      title: 'Crypto Trading Academy',
      description: 'Explore cryptocurrency basics and trading strategies safely.',
      detailedDescription: 'Dive into the world of cryptocurrency with our comprehensive academy. Learn about blockchain technology, different types of cryptocurrencies, and safe trading practices. Use our virtual trading platform to practice without real money at stake.',
      image: 'https://images.pexels.com/photos/8369648/pexels-photo-8369648.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Cryptocurrency',
      difficulty: 'advanced',
      timeCommitment: 35,
      ageRecommendation: '16-18',
      tags: ['cryptocurrency', 'blockchain', 'trading', 'technology'],
      likes: 156,
      rating: 4.3,
      totalRatings: 45,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['1', '6'],
      learningObjectives: ['Understand blockchain technology', 'Learn crypto trading basics', 'Identify investment risks'],
      prerequisites: ['Stock market knowledge', 'Technology interest']
    },
    {
      id: '4',
      title: 'Startup Simulator',
      description: 'Build and manage your own virtual startup company.',
      detailedDescription: 'Ever dreamed of starting your own company? This immersive simulator lets you experience entrepreneurship firsthand. Make crucial business decisions, manage finances, hire employees, and navigate market challenges in a risk-free environment.',
      image: 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Entrepreneurship',
      difficulty: 'intermediate',
      timeCommitment: 40,
      ageRecommendation: '15-18',
      tags: ['entrepreneurship', 'business', 'startup', 'management'],
      likes: 298,
      rating: 4.8,
      totalRatings: 112,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['7', '8'],
      learningObjectives: ['Learn business fundamentals', 'Understand market dynamics', 'Practice decision making'],
      prerequisites: ['Basic business concepts']
    },
    {
      id: '5',
      title: 'Banking Basics Workshop',
      description: 'Learn about different types of bank accounts and financial services.',
      detailedDescription: 'Navigate the world of banking with confidence! This interactive workshop covers everything from opening your first bank account to understanding loans, credit cards, and investment options. Perfect for teens preparing for financial independence.',
      image: 'https://images.pexels.com/photos/4386370/pexels-photo-4386370.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Banking',
      difficulty: 'beginner',
      timeCommitment: 15,
      ageRecommendation: '13-16',
      tags: ['banking', 'accounts', 'loans', 'credit'],
      likes: 167,
      rating: 4.4,
      totalRatings: 78,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['9', '10'],
      learningObjectives: ['Understand banking services', 'Learn about interest rates', 'Compare account types'],
      prerequisites: ['None']
    },
    {
      id: '6',
      title: 'Real Estate Investment Game',
      description: 'Learn property investment through virtual real estate transactions.',
      detailedDescription: 'Enter the exciting world of real estate investment! Buy, sell, and manage virtual properties while learning about market analysis, financing options, and property management. Understand how real estate can build long-term wealth.',
      image: 'https://images.pexels.com/photos/280229/pexels-photo-280229.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Real Estate',
      difficulty: 'advanced',
      timeCommitment: 30,
      ageRecommendation: '16-18',
      tags: ['real estate', 'investment', 'property', 'wealth building'],
      likes: 143,
      rating: 4.6,
      totalRatings: 56,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['1', '4'],
      learningObjectives: ['Understand property valuation', 'Learn financing options', 'Practice investment analysis'],
      prerequisites: ['Investment basics', 'Math skills']
    },
    {
      id: '7',
      title: 'Tax Preparation Tutorial',
      description: 'Learn how to prepare and file taxes with interactive examples.',
      detailedDescription: 'Demystify the tax system with our step-by-step tutorial! Learn about different types of taxes, deductions, and how to file your first tax return. Interactive examples make complex concepts easy to understand.',
      image: 'https://images.pexels.com/photos/6863183/pexels-photo-6863183.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Taxes',
      difficulty: 'intermediate',
      timeCommitment: 25,
      ageRecommendation: '16-18',
      tags: ['taxes', 'filing', 'deductions', 'income'],
      likes: 98,
      rating: 4.2,
      totalRatings: 34,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['5', '8'],
      learningObjectives: ['Understand tax basics', 'Learn about deductions', 'Practice tax calculations'],
      prerequisites: ['Basic income understanding']
    },
    {
      id: '8',
      title: 'Career Planning Roadmap',
      description: 'Explore different career paths and their financial implications.',
      detailedDescription: 'Plan your future career with financial wisdom! Explore various career paths, understand salary expectations, and learn how education investments pay off. Make informed decisions about your professional future.',
      image: 'https://images.pexels.com/photos/3184292/pexels-photo-3184292.jpeg?auto=compress&cs=tinysrgb&w=400',
      category: 'Career Planning',
      difficulty: 'beginner',
      timeCommitment: 20,
      ageRecommendation: '14-18',
      tags: ['career', 'planning', 'salary', 'education'],
      likes: 201,
      rating: 4.5,
      totalRatings: 89,
      isLiked: false,
      isBookmarked: false,
      isCompleted: false,
      progress: 0,
      comments: [],
      relatedActivities: ['4', '7'],
      learningObjectives: ['Explore career options', 'Understand salary ranges', 'Plan education investments'],
      prerequisites: ['None']
    }
  ]

  // Add more activities to reach a good number for pagination
  const additionalActivities = Array.from({ length: 16 }, (_, index) => ({
    ...demoActivities[index % demoActivities.length],
    id: `${demoActivities.length + index + 1}`,
    title: `${demoActivities[index % demoActivities.length].title} ${index + 2}`,
    likes: Math.floor(Math.random() * 300) + 50,
    rating: Math.round((Math.random() * 2 + 3) * 10) / 10,
    totalRatings: Math.floor(Math.random() * 100) + 20
  }))

  return [...demoActivities, ...additionalActivities]
}

const handleSearch = () => {
  currentPage.value = 1
}

const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  selectedTimeCommitment.value = ''
  currentPage.value = 1
}

const loadMore = async () => {
  isLoadingMore.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 800))
    currentPage.value++
  } finally {
    isLoadingMore.value = false
  }
}

const toggleLike = (activityId: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    activity.isLiked = !activity.isLiked
    activity.likes += activity.isLiked ? 1 : -1
    showToastMessage(activity.isLiked ? 'Added to favorites!' : 'Removed from favorites')
  }
}

const toggleBookmark = (activityId: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    activity.isBookmarked = !activity.isBookmarked
    showToastMessage(activity.isBookmarked ? 'Bookmarked!' : 'Bookmark removed')
  }
}

const shareActivity = (activityId: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    // Simulate sharing functionality
    if (navigator.share) {
      navigator.share({
        title: activity.title,
        text: activity.description,
        url: window.location.href
      })
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(`Check out this activity: ${activity.title} - ${window.location.href}`)
      showToastMessage('Link copied to clipboard!')
    }
  }
}

const rateActivity = (activityId: string, rating: number) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    // Update rating (simplified calculation)
    const totalScore = activity.rating * activity.totalRatings + rating
    activity.totalRatings++
    activity.rating = Math.round((totalScore / activity.totalRatings) * 10) / 10
    showToastMessage('Thank you for your rating!')
  }
}

const expandActivity = (activityId: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    selectedActivity.value = activity
    showDetailModal.value = true
  }
}

const startActivity = (activityId: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    // Simulate starting activity
    activity.progress = 10
    showToastMessage(`Started "${activity.title}"!`)
  }
}

const addComment = (activityId: string, content: string) => {
  const activity = activities.value.find(a => a.id === activityId)
  if (activity) {
    const newComment: Comment = {
      id: Date.now().toString(),
      userId: 'current-user',
      userName: 'You',
      userAvatar: 'https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=Hoodie&clotheColor=Blue01&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light',
      content,
      timestamp: new Date().toISOString(),
      likes: 0,
      isLiked: false
    }
    activity.comments.unshift(newComment)
    showToastMessage('Comment added!')
  }
}

const closeDetailModal = () => {
  showDetailModal.value = false
  selectedActivity.value = null
}

const showAllFavorites = () => {
  // Filter to show only favorites
  selectedCategory.value = ''
  selectedDifficulty.value = ''
  selectedTimeCommitment.value = ''
  searchQuery.value = ''
  // This would typically navigate to a dedicated favorites page
  showToastMessage('Showing all favorites!')
}

const getTimeLabel = (timeCommitment: string) => {
  const labels = {
    short: 'Short (< 15 min)',
    medium: 'Medium (15-30 min)',
    long: 'Long (30+ min)'
  }
  return labels[timeCommitment as keyof typeof labels] || timeCommitment
}

const showToastMessage = (message: string) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Watchers
watch([selectedCategory, selectedDifficulty, selectedTimeCommitment], () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(() => {
  loadActivities()
})
</script>

<style scoped>
/* Custom animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}

/* Loading skeleton animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Smooth transitions */
* {
  transition: all 0.2s ease;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Focus styles for accessibility */
button:focus,
input:focus,
select:focus {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

/* Toast animation */
.transform {
  transition: transform 0.3s ease-in-out;
}
</style>