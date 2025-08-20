<template>
  <div>
    <!-- Stock Market Simulator Modal -->
    <v-dialog v-model="showModal" max-width="900px" persistent>
      <v-card class="stock-market-simulator">
        <!-- Header -->
        <v-card-title class="bg-gradient-to-r from-green-400 to-green-600 text-white text-center py-6">
          <div class="text-center">
            <div class="text-6xl mb-2">📈</div>
            <h2 class="text-2xl font-bold">Stock Market Simulator</h2>
            <p class="text-green-100">Learn to invest in stocks with virtual money and real market data!</p>
          </div>
        </v-card-title>

        <!-- Content -->
        <v-card-text class="pa-6">
          <!-- Learning Content -->
          <div v-if="!showQuiz" class="learning-content">
            <div class="text-center mb-6">
              <div class="text-4xl mb-4">💼</div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">Stock Market Fundamentals</h3>
              <p class="text-gray-600">Discover how the stock market works and learn investment strategies!</p>
            </div>

            <div class="space-y-6">
              <!-- Section 1: What is the Stock Market -->
              <div class="bg-blue-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-blue-800 mb-2 flex items-center">
                  <i class="ri-building-line mr-2"></i>
                  What is the Stock Market?
                </h4>
                <p class="text-blue-700">
                  The stock market is a marketplace where shares of publicly traded companies are bought and sold. 
                  When you buy a stock, you're purchasing a small piece of ownership in that company.
                </p>
              </div>

              <!-- Section 2: How Stocks Work -->
              <div class="bg-green-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-green-800 mb-2 flex items-center">
                  <i class="ri-line-chart-line mr-2"></i>
                  How Stocks Work
                </h4>
                <p class="text-green-700 mb-2">
                  Stocks represent ownership in a company. When the company does well, stock prices typically rise. 
                  When it struggles, prices may fall.
                </p>
                <ul class="text-green-700 space-y-1 text-sm">
                  <li>• Stock prices change based on supply and demand</li>
                  <li>• Company performance affects stock value</li>
                  <li>• Market sentiment influences prices</li>
                  <li>• Stocks can pay dividends to shareholders</li>
                </ul>
              </div>

              <!-- Section 3: Types of Stocks -->
              <div class="bg-purple-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-purple-800 mb-2 flex items-center">
                  <i class="ri-folder-line mr-2"></i>
                  Types of Stocks
                </h4>
                <p class="text-purple-700 mb-2">
                  Different types of stocks offer various risk and reward profiles.
                </p>
                <ul class="text-purple-700 space-y-1 text-sm">
                  <li>• Growth Stocks: Companies expected to grow rapidly</li>
                  <li>• Value Stocks: Undervalued companies with strong fundamentals</li>
                  <li>• Dividend Stocks: Companies that pay regular dividends</li>
                  <li>• Blue-Chip Stocks: Large, established, reliable companies</li>
                </ul>
              </div>

              <!-- Section 4: Investment Strategies -->
              <div class="bg-orange-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-orange-800 mb-2 flex items-center">
                  <i class="ri-strategy-line mr-2"></i>
                  Investment Strategies
                </h4>
                <p class="text-orange-700 mb-2">
                  Successful investing requires a well-thought-out strategy and risk management.
                </p>
                <ul class="text-orange-700 space-y-1 text-sm">
                  <li>• Diversification: Don't put all eggs in one basket</li>
                  <li>• Long-term thinking: Stocks tend to rise over time</li>
                  <li>• Dollar-cost averaging: Invest regularly regardless of price</li>
                  <li>• Research: Understand what you're investing in</li>
                </ul>
              </div>

              <!-- Section 5: Risk Management -->
              <div class="bg-red-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-red-800 mb-2 flex items-center">
                  <i class="ri-shield-line mr-2"></i>
                  Risk Management
                </h4>
                <p class="text-red-700 mb-2">
                  Understanding and managing risk is crucial for successful investing.
                </p>
                <ul class="text-red-700 space-y-1 text-sm">
                  <li>• Only invest money you can afford to lose</li>
                  <li>• Diversify across different sectors and companies</li>
                  <li>• Set stop-loss orders to limit potential losses</li>
                  <li>• Don't invest based on emotions or rumors</li>
                </ul>
              </div>

              <!-- Section 6: Market Analysis -->
              <div class="bg-teal-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-teal-800 mb-2 flex items-center">
                  <i class="ri-search-line mr-2"></i>
                  Market Analysis
                </h4>
                <p class="text-teal-700 mb-2">
                  Learn to analyze companies and markets to make informed decisions.
                </p>
                <ul class="text-teal-700 space-y-1 text-sm">
                  <li>• Fundamental Analysis: Study company financials</li>
                  <li>• Technical Analysis: Study price charts and patterns</li>
                  <li>• Market Research: Understand industry trends</li>
                  <li>• Economic Indicators: Monitor broader market conditions</li>
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
                Ready for the Stock Market Quiz?
              </v-btn>
            </div>
          </div>

          <!-- Quiz Section -->
          <div v-else class="quiz-content">
            <div class="text-center mb-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Stock Market Quiz</h3>
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
                  You've mastered stock market fundamentals! Use this knowledge to make informed investment decisions.
                </p>
              </div>

              <div v-else class="bg-orange-50 p-4 rounded-lg mb-6">
                <div class="text-lg font-semibold text-orange-700 mb-2">
                  Keep Learning! 📚
                </div>
                <p class="text-orange-600">
                  Review the material and try again. Stock market knowledge builds over time!
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
    console.log('📈 [MODAL] Getting modal value:', props.modelValue)
    return props.modelValue
  },
  set: (value) => {
    console.log('📈 [MODAL] Setting modal value:', value)
    emit('update:modelValue', value)
  }
})

// Debug when component mounts
onMounted(() => {
  console.log('📈 [MODAL] StockMarketSimulator component mounted')
  console.log('📈 [MODAL] Props received:', props)
  console.log('📈 [MODAL] Initial modal state:', showModal.value)
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
    question: "What is a stock?",
    options: [
      "A type of bond",
      "A piece of ownership in a company",
      "A savings account",
      "A type of insurance"
    ],
    correctAnswer: 1,
    explanation: "A stock represents ownership in a company. When you buy a stock, you own a small piece of that company!"
  },
  {
    question: "What happens to stock prices when a company performs well?",
    options: [
      "Prices usually fall",
      "Prices usually stay the same",
      "Prices usually rise",
      "Prices become unpredictable"
    ],
    correctAnswer: 2,
    explanation: "When a company performs well, stock prices typically rise because investors want to own shares in successful companies!"
  },
  {
    question: "What is diversification?",
    options: [
      "Putting all your money in one stock",
      "Spreading investments across different companies and sectors",
      "Only investing in technology stocks",
      "Selling all your stocks at once"
    ],
    correctAnswer: 1,
    explanation: "Diversification means spreading your investments across different companies and sectors to reduce risk!"
  },
  {
    question: "What is a dividend?",
    options: [
      "A type of loan",
      "A portion of company profits paid to shareholders",
      "A fee for buying stocks",
      "A tax on investments"
    ],
    correctAnswer: 1,
    explanation: "A dividend is a portion of company profits that some companies pay to their shareholders!"
  },
  {
    question: "What is the best approach for beginner investors?",
    options: [
      "Invest all your money in one hot stock",
      "Invest regularly over time in diversified funds",
      "Try to time the market perfectly",
      "Only invest in companies you've never heard of"
    ],
    correctAnswer: 1,
    explanation: "For beginners, investing regularly over time in diversified funds is the safest and most effective approach!"
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
  console.log('📈 [QUIZ] Starting Stock Market quiz...')
  showQuiz.value = true
  currentQuestionIndex.value = 0
  answerSelected.value = null
  quizScore.value = 0
  userAnswers.value = []
}

const selectAnswer = (index: number) => {
  console.log('📈 [QUIZ] Answer selected:', index)
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
  console.log('📈 [QUIZ] Finishing quiz...')
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
      console.log('📈 [QUIZ] Perfect score! Awarding coins...')
      await userStore.addCoins(props.coins, 'Completed Stock Market Simulator Module', 'activity')
      await dashboardStore.completeActivity('1') // Activity ID for Stock Market Simulator
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
.stock-market-simulator {
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
