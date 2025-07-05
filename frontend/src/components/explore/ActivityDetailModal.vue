<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    @click="handleBackdropClick"
  >
    <div
      class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden"
      @click.stop
    >
      <!-- Header -->
      <div class="relative">
        <img
          :src="activity.image"
          :alt="activity.title"
          class="w-full h-64 object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
        
        <!-- Close Button -->
        <button
          @click="$emit('close')"
          class="absolute top-4 right-4 w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center hover:bg-white transition-colors"
        >
          <i class="ri-close-line text-gray-600"></i>
        </button>
        
        <!-- Title and Quick Actions -->
        <div class="absolute bottom-4 left-4 right-4">
          <h2 class="text-2xl font-bold text-white mb-2">{{ activity.title }}</h2>
          <div class="flex items-center gap-3">
            <span
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="getDifficultyClass(activity.difficulty)"
            >
              {{ activity.difficulty }}
            </span>
            <span class="px-3 py-1 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm">
              {{ activity.category }}
            </span>
            <span class="px-3 py-1 bg-white/20 backdrop-blur-sm text-white rounded-full text-sm">
              {{ activity.timeCommitment }} min
            </span>
          </div>
        </div>
      </div>
      
      <!-- Content -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-16rem)]">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Description -->
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-3">About This Activity</h3>
              <p class="text-gray-700 leading-relaxed">{{ activity.detailedDescription }}</p>
            </div>
            
            <!-- Learning Objectives -->
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-3">What You'll Learn</h3>
              <ul class="space-y-2">
                <li
                  v-for="objective in activity.learningObjectives"
                  :key="objective"
                  class="flex items-start gap-2"
                >
                  <i class="ri-check-line text-green-500 mt-0.5"></i>
                  <span class="text-gray-700">{{ objective }}</span>
                </li>
              </ul>
            </div>
            
            <!-- Prerequisites -->
            <div v-if="activity.prerequisites.length > 0">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Prerequisites</h3>
              <ul class="space-y-2">
                <li
                  v-for="prerequisite in activity.prerequisites"
                  :key="prerequisite"
                  class="flex items-start gap-2"
                >
                  <i class="ri-information-line text-blue-500 mt-0.5"></i>
                  <span class="text-gray-700">{{ prerequisite }}</span>
                </li>
              </ul>
            </div>
            
            <!-- Tags -->
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-3">Topics Covered</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="tag in activity.tags"
                  :key="tag"
                  class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm"
                >
                  #{{ tag }}
                </span>
              </div>
            </div>
            
            <!-- Comments Section -->
            <div>
              <h3 class="text-lg font-semibold text-gray-800 mb-4">
                Comments ({{ activity.comments.length }})
              </h3>
              
              <!-- Add Comment -->
              <div class="mb-6">
                <div class="flex gap-3">
                  <img
                    src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairShortFlat&accessoriesType=Blank&hairColor=Brown&facialHairType=Blank&clotheType=Hoodie&clotheColor=Blue01&eyeType=Default&eyebrowType=Default&mouthType=Smile&skinColor=Light"
                    alt="Your avatar"
                    class="w-10 h-10 rounded-full"
                  />
                  <div class="flex-1">
                    <textarea
                      v-model="newComment"
                      placeholder="Share your thoughts about this activity..."
                      class="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                      rows="3"
                    ></textarea>
                    <div class="flex justify-end mt-2">
                      <button
                        @click="handleAddComment"
                        :disabled="!newComment.trim()"
                        class="px-4 py-2 bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-300 text-white rounded-lg transition-colors"
                      >
                        Post Comment
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Comments List -->
              <div class="space-y-4">
                <div
                  v-for="comment in activity.comments.slice(0, 5)"
                  :key="comment.id"
                  class="flex gap-3"
                >
                  <img
                    :src="comment.userAvatar"
                    :alt="`${comment.userName}'s avatar`"
                    class="w-10 h-10 rounded-full"
                  />
                  <div class="flex-1">
                    <div class="bg-gray-50 rounded-lg p-3">
                      <div class="flex items-center justify-between mb-1">
                        <span class="font-medium text-gray-800">{{ comment.userName }}</span>
                        <span class="text-xs text-gray-500">{{ formatCommentTime(comment.timestamp) }}</span>
                      </div>
                      <p class="text-gray-700 text-sm">{{ comment.content }}</p>
                    </div>
                    <div class="flex items-center gap-4 mt-2">
                      <button
                        @click="toggleCommentLike(comment.id)"
                        class="flex items-center gap-1 text-gray-500 hover:text-red-500 transition-colors"
                      >
                        <i :class="comment.isLiked ? 'ri-heart-fill text-red-500' : 'ri-heart-line'"></i>
                        <span class="text-xs">{{ comment.likes }}</span>
                      </button>
                      <button class="text-xs text-gray-500 hover:text-gray-700 transition-colors">
                        Reply
                      </button>
                    </div>
                  </div>
                </div>
                
                <div v-if="activity.comments.length > 5" class="text-center">
                  <button class="text-indigo-600 hover:text-indigo-700 text-sm font-medium">
                    View all {{ activity.comments.length }} comments
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Stats Card -->
            <div class="bg-gray-50 rounded-xl p-6">
              <h3 class="font-semibold text-gray-800 mb-4">Activity Stats</h3>
              <div class="space-y-4">
                <!-- Rating -->
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Rating</span>
                  <div class="flex items-center gap-1">
                    <div class="flex">
                      <i
                        v-for="star in 5"
                        :key="star"
                        :class="star <= Math.round(activity.rating) ? 'ri-star-fill text-yellow-400' : 'ri-star-line text-gray-300'"
                        class="text-sm"
                      ></i>
                    </div>
                    <span class="text-sm text-gray-600 ml-1">{{ activity.rating }}</span>
                  </div>
                </div>
                
                <!-- Likes -->
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Likes</span>
                  <span class="font-medium">{{ formatNumber(activity.likes) }}</span>
                </div>
                
                <!-- Age Range -->
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Age Range</span>
                  <span class="font-medium">{{ activity.ageRecommendation }}</span>
                </div>
                
                <!-- Duration -->
                <div class="flex items-center justify-between">
                  <span class="text-gray-600">Duration</span>
                  <span class="font-medium">{{ activity.timeCommitment }} min</span>
                </div>
              </div>
            </div>
            
            <!-- Rate This Activity -->
            <div class="bg-gray-50 rounded-xl p-6">
              <h3 class="font-semibold text-gray-800 mb-4">Rate This Activity</h3>
              <div class="flex justify-center gap-1 mb-4">
                <button
                  v-for="star in 5"
                  :key="star"
                  @click="handleRate(star)"
                  class="text-2xl transition-colors hover:scale-110"
                  :class="star <= userRating ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-300'"
                >
                  <i :class="star <= userRating ? 'ri-star-fill' : 'ri-star-line'"></i>
                </button>
              </div>
              <p class="text-center text-sm text-gray-600">
                {{ userRating > 0 ? `You rated this ${userRating} star${userRating > 1 ? 's' : ''}` : 'Click to rate' }}
              </p>
            </div>
            
            <!-- Action Buttons -->
            <div class="space-y-3">
              <button
                @click="handleStart"
                class="w-full bg-indigo-500 hover:bg-indigo-600 text-white py-3 px-4 rounded-lg transition-colors font-medium"
                :disabled="activity.isCompleted"
              >
                {{ activity.progress > 0 ? 'Continue Activity' : activity.isCompleted ? 'Completed' : 'Start Activity' }}
              </button>
              
              <div class="grid grid-cols-3 gap-2">
                <button
                  @click="handleLike"
                  class="flex items-center justify-center gap-1 py-2 px-3 border border-gray-300 hover:border-red-300 rounded-lg transition-colors"
                  :class="{ 'text-red-500 border-red-300': activity.isLiked }"
                >
                  <i :class="activity.isLiked ? 'ri-heart-fill' : 'ri-heart-line'"></i>
                  <span class="text-xs">{{ activity.isLiked ? 'Liked' : 'Like' }}</span>
                </button>
                
                <button
                  @click="handleBookmark"
                  class="flex items-center justify-center gap-1 py-2 px-3 border border-gray-300 hover:border-indigo-300 rounded-lg transition-colors"
                  :class="{ 'text-indigo-500 border-indigo-300': activity.isBookmarked }"
                >
                  <i :class="activity.isBookmarked ? 'ri-bookmark-fill' : 'ri-bookmark-line'"></i>
                  <span class="text-xs">Save</span>
                </button>
                
                <button
                  @click="handleShare"
                  class="flex items-center justify-center gap-1 py-2 px-3 border border-gray-300 hover:border-gray-400 rounded-lg transition-colors"
                >
                  <i class="ri-share-line"></i>
                  <span class="text-xs">Share</span>
                </button>
              </div>
            </div>
            
            <!-- Related Activities -->
            <div v-if="activity.relatedActivities.length > 0" class="bg-gray-50 rounded-xl p-6">
              <h3 class="font-semibold text-gray-800 mb-4">Related Activities</h3>
              <div class="space-y-3">
                <div
                  v-for="relatedId in activity.relatedActivities.slice(0, 3)"
                  :key="relatedId"
                  class="flex items-center gap-3 p-3 bg-white rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                >
                  <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center">
                    <i class="ri-book-line text-indigo-600"></i>
                  </div>
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-800 text-sm">Related Activity {{ relatedId }}</h4>
                    <p class="text-xs text-gray-500">15 min • Beginner</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  activity: {
    id: string
    title: string
    description: string
    detailedDescription: string
    image: string
    category: string
    difficulty: 'beginner' | 'intermediate' | 'advanced'
    timeCommitment: number
    ageRecommendation: string
    tags: string[]
    likes: number
    rating: number
    totalRatings: number
    isLiked: boolean
    isBookmarked: boolean
    isCompleted: boolean
    progress: number
    comments: Array<{
      id: string
      userId: string
      userName: string
      userAvatar: string
      content: string
      timestamp: string
      likes: number
      isLiked: boolean
    }>
    relatedActivities: string[]
    learningObjectives: string[]
    prerequisites: string[]
  }
  isOpen: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  like: [activityId: string]
  bookmark: [activityId: string]
  share: [activityId: string]
  rate: [activityId: string, rating: number]
  start: [activityId: string]
  comment: [activityId: string, content: string]
}>()

const newComment = ref('')
const userRating = ref(0)

const handleBackdropClick = () => {
  emit('close')
}

const handleLike = () => {
  emit('like', props.activity.id)
}

const handleBookmark = () => {
  emit('bookmark', props.activity.id)
}

const handleShare = () => {
  emit('share', props.activity.id)
}

const handleStart = () => {
  emit('start', props.activity.id)
}

const handleRate = (rating: number) => {
  userRating.value = rating
  emit('rate', props.activity.id, rating)
}

const handleAddComment = () => {
  if (newComment.value.trim()) {
    emit('comment', props.activity.id, newComment.value.trim())
    newComment.value = ''
  }
}

const toggleCommentLike = (commentId: string) => {
  const comment = props.activity.comments.find(c => c.id === commentId)
  if (comment) {
    comment.isLiked = !comment.isLiked
    comment.likes += comment.isLiked ? 1 : -1
  }
}

const getDifficultyClass = (difficulty: string) => {
  const classes = {
    beginner: 'bg-green-500 text-white',
    intermediate: 'bg-yellow-500 text-white',
    advanced: 'bg-red-500 text-white'
  }
  return classes[difficulty as keyof typeof classes] || 'bg-gray-500 text-white'
}

const formatNumber = (num: number) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const formatCommentTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
  return `${Math.floor(diffInMinutes / 1440)}d ago`
}
</script>

<style scoped>
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

* {
  transition: all 0.2s ease;
}

button:focus,
textarea:focus {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.bg-white {
  animation: modalSlideIn 0.3s ease-out;
}
</style> 