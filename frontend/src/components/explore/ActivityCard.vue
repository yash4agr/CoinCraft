<template>
  <div
    class="activity-card bg-white rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105 hover:shadow-xl cursor-pointer"
    @click="handleCardClick"
    :class="{ 'ring-2 ring-indigo-500': activity.isBookmarked }"
  >
    <!-- Image Container -->
    <div class="relative h-48 overflow-hidden">
      <img
        :src="activity.image"
        :alt="activity.title"
        class="w-full h-full object-cover transition-transform duration-300 hover:scale-110"
        loading="lazy"
      />
      
      <!-- Overlay Gradient -->
      <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
      
      <!-- Top Right Actions -->
      <div class="absolute top-3 right-3 flex gap-2">
        <button
          @click.stop="handleLike"
          class="w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center transition-all hover:bg-white hover:scale-110"
          :class="{ 'text-red-500': activity.isLiked, 'text-gray-600': !activity.isLiked }"
          :aria-label="activity.isLiked ? 'Unlike activity' : 'Like activity'"
        >
          <i :class="activity.isLiked ? 'ri-heart-fill' : 'ri-heart-line'" class="text-sm"></i>
        </button>
        
        <button
          @click.stop="handleBookmark"
          class="w-8 h-8 rounded-full bg-white/90 backdrop-blur-sm flex items-center justify-center transition-all hover:bg-white hover:scale-110"
          :class="{ 'text-indigo-500': activity.isBookmarked, 'text-gray-600': !activity.isBookmarked }"
          :aria-label="activity.isBookmarked ? 'Remove bookmark' : 'Bookmark activity'"
        >
          <i :class="activity.isBookmarked ? 'ri-bookmark-fill' : 'ri-bookmark-line'" class="text-sm"></i>
        </button>
      </div>
      
      <!-- Difficulty Badge -->
      <div class="absolute top-3 left-3">
        <span
          class="px-2 py-1 rounded-full text-xs font-medium backdrop-blur-sm"
          :class="getDifficultyClass(activity.difficulty)"
        >
          {{ activity.difficulty }}
        </span>
      </div>
      
      <!-- Progress Bar (if activity is started) -->
      <div v-if="activity.progress > 0" class="absolute bottom-0 left-0 right-0 h-1 bg-white/30">
        <div
          class="h-full bg-indigo-500 transition-all duration-500"
          :style="{ width: `${activity.progress}%` }"
        ></div>
      </div>
    </div>
    
    <!-- Content -->
    <div class="p-6">
      <!-- Category and Time -->
      <div class="flex items-center justify-between mb-3">
        <span class="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium">
          {{ activity.category }}
        </span>
        <div class="flex items-center text-gray-500 text-xs">
          <i class="ri-time-line mr-1"></i>
          {{ activity.timeCommitment }} min
        </div>
      </div>
      
      <!-- Title -->
      <h3 class="font-bold text-gray-800 text-lg mb-2 line-clamp-2">
        {{ activity.title }}
      </h3>
      
      <!-- Description -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-3">
        {{ activity.description }}
      </p>
      
      <!-- Tags -->
      <div class="flex flex-wrap gap-1 mb-4">
        <span
          v-for="tag in activity.tags.slice(0, 3)"
          :key="tag"
          class="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs"
        >
          #{{ tag }}
        </span>
        <span v-if="activity.tags.length > 3" class="text-gray-400 text-xs">
          +{{ activity.tags.length - 3 }} more
        </span>
      </div>
      
      <!-- Stats Row -->
      <div class="flex items-center justify-between mb-4">
        <!-- Rating -->
        <div class="flex items-center gap-1">
          <div class="flex">
            <i
              v-for="star in 5"
              :key="star"
              :class="star <= Math.round(activity.rating) ? 'ri-star-fill text-yellow-400' : 'ri-star-line text-gray-300'"
              class="text-sm"
            ></i>
          </div>
          <span class="text-sm text-gray-600 ml-1">
            {{ activity.rating }} ({{ activity.totalRatings }})
          </span>
        </div>
        
        <!-- Likes -->
        <div class="flex items-center gap-1 text-gray-600">
          <i class="ri-heart-line text-sm"></i>
          <span class="text-sm">{{ formatNumber(activity.likes) }}</span>
        </div>
      </div>
      
      <!-- Age Recommendation -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center text-gray-500 text-xs">
          <i class="ri-user-line mr-1"></i>
          Ages {{ activity.ageRecommendation }}
        </div>
        
        <!-- Completion Status -->
        <div v-if="activity.isCompleted" class="flex items-center text-green-600 text-xs">
          <i class="ri-check-line mr-1"></i>
          Completed
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="flex gap-2">
        <button
          @click.stop="handleStart"
          class="flex-1 bg-indigo-500 hover:bg-indigo-600 text-white py-2 px-4 rounded-lg transition-colors font-medium text-sm"
          :disabled="activity.isCompleted"
        >
          {{ activity.progress > 0 ? 'Continue' : activity.isCompleted ? 'Completed' : 'Start' }}
        </button>
        
        <button
          @click.stop="handleExpand"
          class="px-3 py-2 border border-gray-300 hover:border-gray-400 text-gray-600 hover:text-gray-700 rounded-lg transition-colors"
          aria-label="View details"
        >
          <i class="ri-eye-line"></i>
        </button>
        
        <button
          @click.stop="handleShare"
          class="px-3 py-2 border border-gray-300 hover:border-gray-400 text-gray-600 hover:text-gray-700 rounded-lg transition-colors"
          aria-label="Share activity"
        >
          <i class="ri-share-line"></i>
        </button>
      </div>
    </div>
    
    <!-- Hover Overlay for Quick Actions -->
    <div class="absolute inset-0 bg-indigo-500/10 opacity-0 hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
      <div class="flex gap-3">
        <button
          @click.stop="handleQuickRate(5)"
          class="w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          title="Quick rate 5 stars"
        >
          <i class="ri-star-fill text-yellow-400"></i>
        </button>
        <button
          @click.stop="handleExpand"
          class="w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          title="View details"
        >
          <i class="ri-eye-line text-gray-600"></i>
        </button>
        <button
          @click.stop="handleShare"
          class="w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
          title="Share"
        >
          <i class="ri-share-line text-gray-600"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  activity: {
    id: string
    title: string
    description: string
    image: string
    category: string
    difficulty: 'easy' | 'medium' | 'hard'
    timeCommitment: number
    rating: number
    totalRatings: number
    likes: number
    tags: string[]
    ageRecommendation: string
    isLiked: boolean
    isBookmarked: boolean
    isCompleted: boolean
    progress: number
  }
}

const props = defineProps<Props>()

const emit = defineEmits<{
  like: [id: string]
  bookmark: [id: string]
  start: [id: string]
  expand: [id: string]
  share: [id: string]
  click: [id: string]
  quickRate: [id: string, rating: number]
}>()

const handleLike = () => {
  emit('like', props.activity.id)
}

const handleBookmark = () => {
  emit('bookmark', props.activity.id)
}

const handleStart = () => {
  emit('start', props.activity.id)
}

const handleExpand = () => {
  emit('expand', props.activity.id)
}

const handleShare = () => {
  emit('share', props.activity.id)
}

const handleCardClick = () => {
  emit('click', props.activity.id)
}

const handleQuickRate = (rating: number) => {
  emit('quickRate', props.activity.id, rating)
}

const getDifficultyClass = (difficulty: string) => {
  const classes = {
    easy: 'bg-green-500/90 text-white',
    medium: 'bg-yellow-500/90 text-white',
    hard: 'bg-red-500/90 text-white'
  }
  return classes[difficulty] || classes.easy
}

const formatNumber = (num: number) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}
</script>

<style scoped>
.activity-card {
  min-height: 400px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 