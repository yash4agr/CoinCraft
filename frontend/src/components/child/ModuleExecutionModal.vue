<template>
  <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-[9999] p-4">
    <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
      <!-- Modal Header -->
      <div class="p-6 border-b border-gray-200 flex items-center justify-between bg-gradient-to-r from-blue-50 to-indigo-50">
        <div>
          <h3 class="text-2xl font-bold text-gray-800">{{ currentModule?.title }}</h3>
          <p class="text-gray-600 mt-1">{{ currentModule?.description }}</p>
        </div>
        <button 
          @click="closeModal"
          class="text-gray-400 hover:text-gray-600 transition-colors p-2 hover:bg-gray-100 rounded-full"
        >
          <i class="ri-close-line text-2xl"></i>
        </button>
      </div>

      <!-- Module Content -->
      <div class="p-6">
        <div v-if="currentModule" class="space-y-6">
          <!-- Module Info -->
          <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div class="flex items-center gap-4 text-sm text-blue-700">
              <span class="flex items-center gap-1">
                <i class="ri-time-line"></i>
                {{ currentModule.duration || 15 }} minutes
              </span>
              <span class="flex items-center gap-1">
                <i class="ri-bar-chart-line"></i>
                {{ currentModule.difficulty || 'beginner' }}
              </span>
              <span class="flex items-center gap-1">
                <i class="ri-folder-line"></i>
                {{ currentModule.category || 'general' }}
              </span>
            </div>
          </div>

          <!-- Mode Toggle -->
          <div class="flex space-x-2 p-1 bg-gray-100 rounded-lg">
            <button
              @click="currentMode = 'content'"
              :class="[
                'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
                currentMode === 'content' 
                  ? 'bg-white text-blue-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              <i class="ri-book-open-line mr-2"></i>
              Module Content
            </button>
            <button
              @click="currentMode = 'quiz'"
              :class="[
                'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
                currentMode === 'quiz' 
                  ? 'bg-white text-blue-600 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              <i class="ri-help-circle-line mr-2"></i>
              Take Quiz
            </button>
          </div>

          <!-- Content Mode -->
          <div v-if="currentMode === 'content'" class="space-y-4">
            <h4 class="text-lg font-semibold text-gray-800">📚 Module Content</h4>
            <p class="text-gray-600">
              This module contains interactive lessons and activities. Read through the content before taking the quiz!
            </p>
            
            <!-- Loading state -->
            <div v-if="isLoadingContent" class="bg-gray-50 p-8 rounded-lg text-center border-2 border-dashed border-gray-300">
              <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
              <p class="text-gray-600 font-medium">Loading module content...</p>
              <p class="text-sm text-gray-500 mt-2">Please wait while we fetch your learning materials</p>
            </div>
            
            <!-- Module Sections -->
            <div v-else-if="moduleSections && moduleSections.length > 0" class="space-y-4">
              <div 
                v-for="(section, index) in moduleSections" 
                :key="index"
                class="bg-gray-50 p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors"
              >
                <div class="flex items-center gap-3 mb-3">
                  <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-blue-600 font-medium text-sm">{{ index + 1 }}</span>
                  </div>
                  <h5 class="font-semibold text-gray-800">{{ section.title }}</h5>
                  <span class="ml-auto px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                    {{ section.type }}
                  </span>
                </div>
                <p class="text-gray-700">{{ section.content }}</p>
              </div>
            </div>
            
            <!-- Default Content if no sections -->
            <div v-else class="bg-gray-50 p-8 rounded-lg text-center border-2 border-dashed border-gray-300">
              <i class="ri-book-line text-6xl text-gray-300 mb-4"></i>
              <h5 class="text-lg font-semibold text-gray-600 mb-2">Module Content</h5>
              <p class="text-gray-500 mb-4">This module contains interactive lessons and activities.</p>
              <p class="text-sm text-gray-400">Switch to Quiz mode to test your knowledge!</p>
            </div>
          </div>

          <!-- Quiz Mode -->
          <div v-else class="space-y-4">
            <h4 class="text-lg font-semibold text-gray-800">🧠 Knowledge Check</h4>
            
            <!-- Loading state -->
            <div v-if="isLoadingContent" class="text-center py-12">
              <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-6"></div>
              <p class="text-gray-600 font-medium text-lg mb-2">Loading Quiz Questions</p>
              <p class="text-sm text-gray-500">Preparing your knowledge test...</p>
            </div>
            
            <div v-else-if="!quizCompleted" class="space-y-4">
              <!-- Quiz Questions -->
              <div 
                v-for="(question, index) in quizQuestions" 
                :key="index"
                class="bg-white p-6 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
              >
                <h5 class="font-semibold text-gray-800 mb-4 text-lg">
                  Q{{ index + 1 }}: {{ question.question }}
                </h5>
                
                <!-- Multiple Choice Options -->
                <div class="space-y-3">
                  <label 
                    v-for="(option, optIndex) in question.options" 
                    :key="optIndex"
                    class="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                    :class="{ 'bg-blue-50 border-blue-300 ring-2 ring-blue-200': quizAnswers[index] === optIndex }"
                  >
                    <input
                      type="radio"
                      :name="`question-${index}`"
                      :value="optIndex"
                      v-model="quizAnswers[index]"
                      class="mr-3 text-blue-600"
                    />
                    <span class="text-gray-700 font-medium">{{ option.text }}</span>
                  </label>
                </div>
                
                <!-- Answer Feedback -->
                <div 
                  v-if="showQuizFeedback && quizAnswers[index] !== undefined"
                  class="mt-4 p-4 rounded-lg"
                  :class="isAnswerCorrect(index) ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'"
                >
                  <div class="flex items-center gap-2">
                    <i :class="isAnswerCorrect(index) ? 'ri-check-line' : 'ri-close-line'"></i>
                    <span class="font-medium">
                      {{ isAnswerCorrect(index) ? 'Correct!' : 'Incorrect.' }}
                    </span>
                  </div>
                  <p class="text-sm mt-2">{{ question.explanation }}</p>
                </div>
              </div>
              
              <!-- Quiz Actions -->
              <div class="flex justify-between items-center pt-6 bg-gray-50 p-4 rounded-lg">
                <div class="text-sm text-gray-600">
                  <span class="font-medium">{{ answeredQuestions }}</span> of <span class="font-medium">{{ quizQuestions.length }}</span> questions answered
                </div>
                <button 
                  @click="checkQuiz"
                  :disabled="answeredQuestions < quizQuestions.length"
                  class="px-8 py-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors shadow-sm"
                >
                  <i class="ri-check-circle-line mr-2"></i>
                  Check Answers
                </button>
              </div>
            </div>
            
            <!-- Quiz Results -->
            <div v-else class="text-center">
              <div class="bg-white p-8 rounded-lg border border-gray-200 shadow-sm">
                <div class="text-6xl mb-4">
                  {{ quizScore >= 70 ? '🎉' : '😔' }}
                </div>
                <h4 class="text-2xl font-bold text-gray-800 mb-2">
                  {{ quizScore >= 70 ? 'Congratulations!' : 'Good Effort!' }}
                </h4>
                <p class="text-4xl font-bold mb-4" :class="quizScore >= 70 ? 'text-green-600' : 'text-blue-600'">
                  {{ quizScore }}%
                </p>
                <p class="text-gray-600 mb-6">
                  You got {{ correctAnswers }} out of {{ quizQuestions.length }} questions correct.
                </p>
                
                <!-- Success Message -->
                <div v-if="quizScore >= 70" class="bg-green-50 p-4 rounded-lg mb-6">
                  <div class="flex items-center gap-2 text-green-700">
                    <i class="ri-trophy-line text-xl"></i>
                    <span class="font-medium">Module Completed Successfully!</span>
                  </div>
                  <p class="text-sm text-green-600 mt-1">
                    You've earned coins and completed this teacher-assigned module.
                  </p>
                </div>
                
                <!-- Retry Option -->
                <div v-if="quizScore < 70" class="bg-yellow-50 p-4 rounded-lg mb-6">
                  <div class="flex items-center gap-2 text-yellow-700">
                    <i class="ri-information-line text-xl"></i>
                    <span class="font-medium">Almost There!</span>
                  </div>
                  <p class="text-sm text-yellow-600 mt-1">
                    You need 70% to pass. Review the content and try again!
                  </p>
                </div>
                
                <!-- Action Buttons -->
                <div class="flex gap-3 justify-center">
                  <button 
                    v-if="quizScore < 70"
                    @click="retryQuiz"
                    class="px-6 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-lg font-medium transition-colors"
                  >
                    <i class="ri-refresh-line mr-2"></i>
                    Try Again
                  </button>
                  <button 
                    @click="completeModule"
                    class="px-6 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors"
                  >
                    <i class="ri-flag-checkered-line mr-2"></i>
                    {{ quizScore >= 70 ? 'Complete Module' : 'Close' }}
                  </button>
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
import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import apiService from '@/services/api'

// Props
interface Props {
  showModal: boolean
  currentModule: any
}

// Emits
interface Emits {
  (e: 'close'): void
  (e: 'module-completed', module: any, score: number): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// Stores
const userStore = useUserStore()

// State
const currentMode = ref<'content' | 'quiz'>('content')
const quizAnswers = ref<number[]>([])
const showQuizFeedback = ref(false)
const quizCompleted = ref(false)
const correctAnswers = ref(0)
const quizScore = ref(0)
const isLoading = ref(false)
const moduleSections = ref<any[]>([])
const quizQuestions = ref<any[]>([])
const isLoadingContent = ref(false)

// Computed
const answeredQuestions = computed(() => {
  return quizAnswers.value.filter(answer => answer !== undefined).length
})

// Methods
const closeModal = () => {
  emit('close')
}

const fetchModuleContent = async () => {
  if (!props.currentModule) return
  
  try {
    isLoadingContent.value = true
    
    // Fetch module sections and quiz questions
    const response = await apiService.getModuleContent(props.currentModule.id)
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    if (response.data) {
      moduleSections.value = response.data.sections || []
      quizQuestions.value = response.data.quiz || []
      
      // Initialize quiz answers array
      quizAnswers.value = new Array(quizQuestions.value.length).fill(undefined)
    }
    
  } catch (error) {
    console.error('Failed to fetch module content:', error)
    // Fallback to mock data if API fails
    moduleSections.value = [
      {
        title: "Introduction to Financial Concepts",
        content: "Learn the basics of money management, budgeting, and financial planning.",
        type: "lesson",
        duration: "5 min"
      },
      {
        title: "Interactive Learning Activities",
        content: "Practice what you've learned through hands-on exercises and real-world examples.",
        type: "activity",
        duration: "8 min"
      }
    ]
    
    quizQuestions.value = [
      {
        question: "What is the first step in creating a budget?",
        options: [
          { text: "Spend all your money", isCorrect: false },
          { text: "Track your income and expenses", isCorrect: true },
          { text: "Buy expensive items", isCorrect: false },
          { text: "Ignore your finances", isCorrect: false }
        ],
        explanation: "Tracking your income and expenses is the foundation of budgeting."
      },
      {
        question: "Which of the following is a good saving habit?",
        options: [
          { text: "Spending more than you earn", isCorrect: false },
          { text: "Saving 20% of your income", isCorrect: true },
          { text: "Never saving money", isCorrect: false },
          { text: "Borrowing money frequently", isCorrect: false }
        ],
        explanation: "Saving 20% of your income is a recommended financial practice."
      },
      {
        question: "What is compound interest?",
        options: [
          { text: "Interest only on the principal amount", isCorrect: false },
          { text: "Interest on both principal and accumulated interest", isCorrect: true },
          { text: "A type of loan", isCorrect: false },
          { text: "A bank fee", isCorrect: false }
        ],
        explanation: "Compound interest is interest earned on both the principal and previously accumulated interest."
      }
    ]
    
    // Initialize quiz answers array
    quizAnswers.value = new Array(quizQuestions.value.length).fill(undefined)
  } finally {
    isLoadingContent.value = false
  }
}

const resetQuiz = () => {
  quizAnswers.value = []
  showQuizFeedback.value = false
  quizCompleted.value = false
  correctAnswers.value = 0
  quizScore.value = 0
}

const isAnswerCorrect = (questionIndex: number) => {
  const question = quizQuestions.value[questionIndex]
  const answer = quizAnswers.value[questionIndex]
  return question.options[answer]?.isCorrect
}

const checkQuiz = () => {
  if (answeredQuestions.value < quizQuestions.value.length) {
    alert('Please answer all questions before checking your answers.')
    return
  }
  
  showQuizFeedback.value = true
  
  // Calculate score
  let correct = 0
  quizQuestions.value.forEach((question, index) => {
    if (isAnswerCorrect(index)) {
      correct++
    }
  })
  
  correctAnswers.value = correct
  quizScore.value = Math.round((correct / quizQuestions.value.length) * 100)
  
  // Auto-complete quiz after showing feedback
  setTimeout(() => {
    quizCompleted.value = true
  }, 2000)
}

const retryQuiz = () => {
  resetQuiz()
}

const completeModule = async () => {
  if (!props.currentModule) return
  
  try {
    isLoading.value = true
    
    const progressData = {
      status: quizScore.value >= 70 ? 'completed' : 'in_progress',
      score: quizScore.value,
      completed_at: quizScore.value >= 70 ? new Date().toISOString() : null
    }
    
    console.log('🔍 [MODAL] Completing module:', props.currentModule.title)
    console.log('🔍 [MODAL] Progress data to send:', progressData)
    console.log('🔍 [MODAL] Quiz score:', quizScore.value)
    
    // Update module progress in database
    const response = await apiService.updateModuleProgress(props.currentModule.id, progressData)
    
    console.log('🔍 [MODAL] API response:', response)
    
    if (response.error) {
      throw new Error(response.error)
    }
    
    console.log('✅ [MODAL] Module completed successfully!')
    
    // Emit completion event
    emit('module-completed', props.currentModule, quizScore.value)
    
    // Close modal
    closeModal()
    
  } catch (error) {
    console.error('❌ [MODAL] Failed to complete module:', error)
    alert('Failed to save your progress. Please try again.')
  } finally {
    isLoading.value = false
  }
}

// Watch for module changes
watch(() => props.currentModule, () => {
  if (props.currentModule) {
    console.log('🔍 [MODAL] Module changed:', props.currentModule)
    resetQuiz()
    currentMode.value = 'content'
    fetchModuleContent()
  }
})

// Watch for showModal changes
watch(() => props.showModal, (newVal) => {
  console.log('🔍 [MODAL] Show modal changed:', newVal)
  if (newVal && props.currentModule) {
    console.log('🔍 [MODAL] Opening modal for module:', props.currentModule.title)
    fetchModuleContent()
  }
})
</script>

<style scoped>
.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-6 > * + * {
  margin-top: 1.5rem;
}

.space-y-2 > * + * {
  margin-top: 0.5rem;
}

/* Ensure modal is always visible */
.fixed {
  position: fixed !important;
}

/* Ensure modal content is visible */
.bg-white {
  background-color: white !important;
}

/* Ensure proper z-index */
.z-\[9999\] {
  z-index: 9999 !important;
}

/* Ensure modal backdrop is visible but not too dark */
.bg-black.bg-opacity-60 {
  background-color: rgba(0, 0, 0, 0.6) !important;
}

/* Ensure modal content has proper contrast */
.text-gray-800 {
  color: #1f2937 !important;
}

.text-gray-600 {
  color: #4b5563 !important;
}

/* Ensure buttons are visible */
.bg-blue-500 {
  background-color: #3b82f6 !important;
}

.bg-green-500 {
  background-color: #10b981 !important;
}

/* Ensure proper shadows */
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
}
</style>
