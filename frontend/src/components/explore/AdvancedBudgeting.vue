<template>
  <div>
    <!-- Advanced Budgeting Modal -->
    <v-dialog v-model="showModal" max-width="900px" persistent>
      <v-card class="advanced-budgeting">
        <!-- Header -->
        <v-card-title class="bg-gradient-to-r from-purple-400 to-purple-600 text-white text-center py-6 relative">
          <!-- Close Button -->
          <v-btn
            icon
            variant="text"
            @click="closeModal"
            class="absolute top-4 right-4 text-white hover:bg-white hover:bg-opacity-20"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          
          <div class="text-center">
            <div class="text-6xl mb-2">📊</div>
            <h2 class="text-2xl font-bold">Advanced Budgeting</h2>
            <p class="text-purple-100">Master advanced budgeting techniques and strategies!</p>
          </div>
        </v-card-title>

        <!-- Content -->
        <v-card-text class="pa-6">
          <!-- Learning Content -->
          <div v-if="!showQuiz" class="learning-content">
            <div class="text-center mb-6">
              <div class="text-4xl mb-4">💡</div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Advanced Budgeting Mastery</h3>
              <p class="text-gray-600">Learn sophisticated budgeting techniques to take control of your finances!</p>
            </div>

            <div class="space-y-6">
              <!-- Section 1: What is Advanced Budgeting -->
              <div class="bg-blue-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-blue-800 mb-2 flex items-center">
                  <i class="ri-calculator-line mr-2"></i>
                  What is Advanced Budgeting?
                </h4>
                <p class="text-blue-700">
                  Advanced budgeting goes beyond simple income vs. expenses. It involves strategic planning, 
                  multiple account management, and long-term financial goal setting to build wealth and security.
                </p>
              </div>

              <!-- Section 2: Zero-Based Budgeting -->
              <div class="bg-green-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-green-800 mb-2 flex items-center">
                  <i class="ri-target-line mr-2"></i>
                  Zero-Based Budgeting
                </h4>
                <p class="text-green-700 mb-2">
                  Every dollar has a purpose! Zero-based budgeting means your income minus expenses equals zero.
                </p>
                <ul class="text-green-700 space-y-1 text-sm">
                  <li>• Assign every dollar to a specific category</li>
                  <li>• No money left unaccounted for</li>
                  <li>• Forces intentional spending decisions</li>
                  <li>• Great for tight financial situations</li>
                </ul>
              </div>

              <!-- Section 3: Envelope System -->
              <div class="bg-purple-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-purple-800 mb-2 flex items-center">
                  <i class="ri-wallet-3-line mr-2"></i>
                  Envelope System
                </h4>
                <p class="text-purple-700 mb-2">
                  Physical or digital envelopes for different spending categories to prevent overspending.
                </p>
                <ul class="text-purple-700 space-y-1 text-sm">
                  <li>• Separate envelopes for groceries, entertainment, clothing</li>
                  <li>• When envelope is empty, spending stops</li>
                  <li>• Visual representation of budget limits</li>
                  <li>• Helps develop spending discipline</li>
                </ul>
              </div>

              <!-- Section 4: 50/30/20 Rule -->
              <div class="bg-orange-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-orange-800 mb-2 flex items-center">
                  <i class="ri-pie-chart-line mr-2"></i>
                  50/30/20 Budget Rule
                </h4>
                <p class="text-orange-700 mb-2">
                  A simple yet effective budgeting framework that divides your income into three categories.
                </p>
                <ul class="text-orange-700 space-y-1 text-sm">
                  <li>• 50% for needs (housing, food, utilities, transportation)</li>
                  <li>• 30% for wants (entertainment, dining out, shopping)</li>
                  <li>• 20% for savings and debt repayment</li>
                  <li>• Flexible percentages based on your situation</li>
                </ul>
              </div>

              <!-- Section 5: Emergency Fund Planning -->
              <div class="bg-red-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-red-800 mb-2 flex items-center">
                  <i class="ri-shield-check-line mr-2"></i>
                  Emergency Fund Planning
                </h4>
                <p class="text-red-700 mb-2">
                  Building a financial safety net is crucial for long-term financial stability.
                </p>
                <ul class="text-red-700 space-y-1 text-sm">
                  <li>• Aim for 3-6 months of living expenses</li>
                  <li>• Keep in high-yield savings account</li>
                  <li>• Only use for true emergencies</li>
                  <li>• Replenish after using</li>
                </ul>
              </div>

              <!-- Section 6: Budget Tracking Tools -->
              <div class="bg-teal-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-teal-800 mb-2 flex items-center">
                  <i class="ri-tools-line mr-2"></i>
                  Budget Tracking Tools
                </h4>
                <p class="text-teal-700 mb-2">
                  Modern tools make budgeting easier and more effective than ever.
                </p>
                <ul class="text-teal-700 space-y-1 text-sm">
                  <li>• Apps: Mint, YNAB, Personal Capital</li>
                  <li>• Spreadsheets: Excel, Google Sheets</li>
                  <li>• Traditional: Pen and paper, cash envelopes</li>
                  <li>• Automation: Set up recurring transfers</li>
                </ul>
              </div>
            </div>

            <!-- Quiz Button -->
            <div class="text-center mt-8">
              <v-btn
                color="success"
                size="large"
                @click="startQuiz"
                class="px-8"
              >
                <i class="ri-question-line mr-2"></i>
                Ready for the Advanced Budgeting Quiz?
              </v-btn>
            </div>
          </div>

          <!-- Quiz Section -->
          <div v-else class="quiz-content">
            <div class="text-center mb-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Advanced Budgeting Quiz</h3>
              <p class="text-gray-600">Answer all 5 questions correctly to earn {{ coins }} coins!</p>
              <div class="mt-2">
                <v-progress-linear
                  :model-value="(currentQuestionIndex + 1) / quizQuestions.length * 100"
                  color="success"
                  height="8"
                  rounded
                ></v-progress-linear>
                <span class="text-sm text-gray-500">
                  Question {{ currentQuestionIndex + 1 }} of {{ quizQuestions.length }}
                </span>
              </div>
            </div>

            <!-- Current Question -->
            <div v-if="currentQuestion" class="question-container">
              <div class="bg-gray-50 p-6 rounded-lg mb-6">
                <h4 class="text-lg font-semibold text-gray-800 mb-4">
                  {{ currentQuestion.question }}
                </h4>
                
                <div class="space-y-3">
                  <v-btn
                    v-for="(option, index) in currentQuestion.options"
                    :key="index"
                    :variant="getOptionVariant(_index)"
                    :color="getOptionColor(_index)"
                    block
                    class="justify-start text-left"
                    @click="selectAnswer(_index)"
                    :disabled="answerSelected !== null"
                  >
                    <span class="mr-3">{{ String.fromCharCode(65 + index) }}.</span>
                    {{ option }}
                  </v-btn>
                </div>
              </div>

              <!-- Feedback -->
              <div v-if="answerSelected !== null" class="feedback mb-6">
                <v-alert
                  :type="isAnswerCorrect ? 'success' : 'error'"
                  variant="tonal"
                  class="mb-4"
                >
                  <template #prepend>
                    <v-icon>{{ isAnswerCorrect ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
                  </template>
                  <strong>{{ isAnswerCorrect ? 'Correct!' : 'Incorrect!' }}</strong>
                  {{ currentQuestion.explanation }}
                </v-alert>

                <div class="text-center">
                  <v-btn
                    v-if="currentQuestionIndex < quizQuestions.length - 1"
                    color="primary"
                    @click="nextQuestion"
                  >
                    Next Question
                  </v-btn>
                  <v-btn
                    v-else
                    color="success"
                    @click="finishQuiz"
                  >
                    Finish Quiz
                  </v-btn>
                </div>
              </div>
            </div>

            <!-- Quiz Results -->
            <div v-if="showResults" class="results-container text-center">
              <div class="text-6xl mb-4">
                {{ quizScore === quizQuestions.length ? '🎉' : '😔' }}
              </div>
              
              <h3 class="text-2xl font-bold text-gray-800 mb-2">
                {{ quizScore === quizQuestions.length ? 'Congratulations!' : 'Almost There!' }}
              </h3>
              
              <p class="text-gray-600 mb-4">
                You got {{ quizScore }} out of {{ quizQuestions.length }} questions correct!
              </p>

              <div v-if="quizScore === quizQuestions.length" class="bg-green-50 p-4 rounded-lg mb-6">
                <div class="text-2xl font-bold text-green-600 mb-2">
                  +{{ coins }} Coins Earned! 🪙
                </div>
                <p class="text-green-700">
                  You've mastered advanced budgeting concepts! Use these skills to take control of your finances.
                </p>
              </div>

              <div v-else class="bg-orange-50 p-4 rounded-lg mb-6">
                <div class="text-lg font-semibold text-orange-700 mb-2">
                  Keep Learning! 📚
                </div>
                <p class="text-orange-600">
                  Review the material and try again. Budgeting is a skill that improves with practice!
                </p>
              </div>

              <div class="space-x-4">
                <v-btn
                  v-if="quizScore < quizQuestions.length"
                  color="primary"
                  @click="retryQuiz"
                >
                  <i class="ri-refresh-line mr-2"></i>
                  Try Again
                </v-btn>
                <v-btn
                  color="success"
                  @click="closeModal"
                >
                  <i class="ri-check-line mr-2"></i>
                  {{ quizScore === quizQuestions.length ? 'Complete' : 'Close' }}
                </v-btn>
              </div>
            </div>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useDashboardStore } from '@/stores/dashboard'

interface Props {
  modelValue: boolean
  coins: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'completed': [coins: number]
}>()

const userStore = useUserStore()
const dashboardStore = useDashboardStore()

// Modal state
const showModal = computed({
  get: () => {
    console.log('📊 [MODAL] Getting modal value:', props.modelValue)
    return props.modelValue
  },
  set: (value) => {
    console.log('📊 [MODAL] Setting modal value:', value)
    emit('update:modelValue', value)
  }
})

// Debug when component mounts
onMounted(() => {
  console.log('📊 [MODAL] AdvancedBudgeting component mounted')
  console.log('📊 [MODAL] Props received:', props)
  console.log('📊 [MODAL] Initial modal state:', showModal.value)
})

// Quiz state
const showQuiz = ref(false)
const showResults = ref(false)
const currentQuestionIndex = ref(0)
const answerSelected = ref<number | null>(null)
const quizScore = ref(0)
const userAnswers = ref<number[]>([])

// Quiz questions
const quizQuestions = ref([
  {
    question: "What is zero-based budgeting?",
    options: [
      "Spending all your money each month",
      "Assigning every dollar to a specific purpose",
      "Only spending on essential items",
      "Saving 20% of your income"
    ],
    correctAnswer: 1,
    explanation: "Zero-based budgeting means every dollar has a purpose - income minus expenses equals zero!"
  },
  {
    question: "What does the 50/30/20 rule allocate for needs?",
    options: [
      "30% of your income",
      "50% of your income",
      "20% of your income",
      "All of your income"
    ],
    correctAnswer: 1,
    explanation: "The 50/30/20 rule allocates 50% for needs like housing, food, and utilities!"
  },
  {
    question: "How much should you aim to save in an emergency fund?",
    options: [
      "1-2 months of expenses",
      "3-6 months of expenses",
      "6-12 months of expenses",
      "No emergency fund needed"
    ],
    correctAnswer: 1,
    explanation: "Aim for 3-6 months of living expenses in your emergency fund for financial security!"
  },
  {
    question: "What is the envelope system used for?",
    options: [
      "Sending mail",
      "Organizing receipts",
      "Preventing overspending in categories",
      "Tracking investments"
    ],
    correctAnswer: 2,
    explanation: "The envelope system uses separate envelopes for different spending categories to prevent overspending!"
  },
  {
    question: "Which budgeting tool is best for beginners?",
    options: [
      "Complex spreadsheets",
      "Pen and paper",
      "Advanced financial software",
      "All of the above"
    ],
    correctAnswer: 1,
    explanation: "Pen and paper is often the best starting point for beginners as it's simple and visual!"
  }
])

// Computed properties
const currentQuestion = computed(() => {
  return quizQuestions.value[currentQuestionIndex.value]
})

const isAnswerCorrect = computed(() => {
  if (answerSelected.value === null) return false
  return answerSelected.value === currentQuestion.value?.correctAnswer
})

// Methods
const startQuiz = () => {
  console.log('📊 [QUIZ] Starting Advanced Budgeting quiz...')
  showQuiz.value = true
  currentQuestionIndex.value = 0
  answerSelected.value = null
  quizScore.value = 0
  userAnswers.value = []
}

const selectAnswer = (index: number) => {
  console.log('📊 [QUIZ] Answer selected:', index)
  answerSelected.value = index
  userAnswers.value[currentQuestionIndex.value] = index
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
    currentQuestionIndex.value++
    answerSelected.value = null
  }
}

const finishQuiz = async () => {
  console.log('📊 [QUIZ] Finishing quiz...')
  showResults.value = true
  
  // Calculate score
  let correct = 0
  userAnswers.value.forEach((answer, index) => {
    if (answer === quizQuestions.value[index]?.correctAnswer) {
      correct++
    }
  })
  quizScore.value = correct
  
  if (quizScore.value === quizQuestions.value.length) {
    try {
      console.log('📊 [QUIZ] Perfect score! Awarding coins...')
      await userStore.addCoins(props.coins, 'Completed Advanced Budgeting Module', 'activity')
      await dashboardStore.completeModule('2') // Module ID for Advanced Budgeting
      emit('completed', props.coins)
    } catch (error) {
      console.error('Failed to award coins:', error)
    }
  }
}

const retryQuiz = () => {
  showQuiz.value = false
  showResults.value = false
  startQuiz()
}

const closeModal = () => {
  showModal.value = false
  showQuiz.value = false
  showResults.value = false
  currentQuestionIndex.value = 0
  answerSelected.value = null
  quizScore.value = 0
  userAnswers.value = []
}

// Helper methods for quiz UI
const getOptionVariant = (index: number) => {
  if (answerSelected.value === null) return 'outlined'
  
  if (index === currentQuestion.value?.correctAnswer) {
    return 'elevated'
  }
  
  if (answerSelected.value === index && index !== currentQuestion.value?.correctAnswer) {
    return 'elevated'
  }
  
  return 'outlined'
}

const getOptionColor = (index: number) => {
  if (answerSelected.value === null) return 'primary'
  
  if (index === currentQuestion.value?.correctAnswer) {
    return 'success'
  }
  
  if (answerSelected.value === index && index !== currentQuestion.value?.correctAnswer) {
    return 'error'
  }
  
  return 'primary'
}
</script>

<style scoped>
.advanced-budgeting {
  max-height: 90vh;
  overflow-y: auto;
}

.learning-content {
  max-height: 60vh;
  overflow-y: auto;
}

.quiz-content {
  max-height: 60vh;
  overflow-y: auto;
}

.question-container {
  min-height: 300px;
}

.results-container {
  min-height: 300px;
}

/* Custom scrollbar */
.learning-content::-webkit-scrollbar,
.quiz-content::-webkit-scrollbar {
  width: 8px;
}

.learning-content::-webkit-scrollbar-track,
.quiz-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.learning-content::-webkit-scrollbar-thumb,
.quiz-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.learning-content::-webkit-scrollbar-thumb:hover,
.quiz-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
