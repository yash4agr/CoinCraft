<template>
  <div>
    <!-- Piggy Bank Adventure Modal -->
    <v-dialog v-model="showModal" max-width="800px" persistent>
      <v-card class="piggy-bank-adventure">
        <!-- Header -->
        <v-card-title class="bg-gradient-to-r from-pink-400 to-pink-500 text-white text-center py-6">
          <div class="text-center">
            <div class="text-6xl mb-2">🐷</div>
            <h2 class="text-2xl font-bold">Piggy Bank Adventure</h2>
            <p class="text-pink-100">Learn how to save money with your digital piggy bank!</p>
          </div>
        </v-card-title>

        <!-- Content -->
        <v-card-text class="pa-6">
          <!-- Learning Content -->
          <div v-if="!showQuiz" class="learning-content">
            <div class="text-center mb-6">
              <div class="text-4xl mb-4">💰</div>
              <h3 class="text-xl font-bold text-gray-800 mb-2">What is a Piggy Bank?</h3>
              <p class="text-gray-600">A piggy bank is a special container where you can save your money safely!</p>
            </div>

            <div class="space-y-6">
              <!-- Section 1: What is Saving -->
              <div class="bg-blue-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-blue-800 mb-2 flex items-center">
                  <i class="ri-safe-line mr-2"></i>
                  What is Saving?
                </h4>
                <p class="text-blue-700">
                  Saving means keeping some of your money instead of spending it all right away. 
                  It's like putting money in a special box for later when you really need it!
                </p>
              </div>

              <!-- Section 2: Why Save Money -->
              <div class="bg-green-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-green-800 mb-2 flex items-center">
                  <i class="ri-question-line mr-2"></i>
                  Why Should You Save Money?
                </h4>
                <ul class="text-green-700 space-y-1">
                  <li>• To buy something special you really want</li>
                  <li>• For emergencies when you need money quickly</li>
                  <li>• To learn how to be responsible with money</li>
                  <li>• To have money for the future</li>
                </ul>
              </div>

              <!-- Section 3: How to Save -->
              <div class="bg-purple-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-purple-800 mb-2 flex items-center">
                  <i class="ri-lightbulb-line mr-2"></i>
                  How to Save Money
                </h4>
                <ul class="text-purple-700 space-y-1">
                  <li>• Put some coins in your piggy bank every day</li>
                  <li>• Save money you get as gifts</li>
                  <li>• Don't spend all your money at once</li>
                  <li>• Set a goal for what you want to save for</li>
                </ul>
              </div>

              <!-- Section 4: Fun Facts -->
              <div class="bg-orange-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-orange-800 mb-2 flex items-center">
                  <i class="ri-star-line mr-2"></i>
                  Fun Facts About Piggy Banks
                </h4>
                <ul class="text-orange-700 space-y-1">
                  <li>• The first piggy banks were made of clay</li>
                  <li>• They're called "piggy" banks because they look like pigs</li>
                  <li>• People have been using them for over 600 years!</li>
                  <li>• Breaking a piggy bank is called "breaking the bank"</li>
                </ul>
              </div>

              <!-- Section 5: Tips -->
              <div class="bg-pink-50 p-4 rounded-lg">
                <h4 class="text-lg font-semibold text-pink-800 mb-2 flex items-center">
                  <i class="ri-heart-line mr-2"></i>
                  Saving Tips for Kids
                </h4>
                <ul class="text-pink-700 space-y-1">
                  <li>• Start with small amounts - every coin counts!</li>
                  <li>• Make saving a fun game</li>
                  <li>• Ask your parents to help you count your savings</li>
                  <li>• Be patient - good things take time to save for</li>
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
                Are You Ready for a Quiz?
              </v-btn>
            </div>
          </div>

          <!-- Quiz Section -->
          <div v-else class="quiz-content">
            <div class="text-center mb-6">
              <h3 class="text-xl font-bold text-gray-800 mb-2">Piggy Bank Quiz</h3>
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
                <p class="text-green-700">Great job learning about piggy banks!</p>
              </div>

              <div v-else class="bg-orange-50 p-4 rounded-lg mb-6">
                <p class="text-orange-700">
                  Don't worry! Review the lesson and try again. You can do it! 💪
                </p>
              </div>

              <div class="space-x-4">
                <v-btn
                  v-if="quizScore < quizQuestions.length"
                  color="primary"
                  @click="retryQuiz"
                >
                  Try Again
                </v-btn>
                <v-btn
                  color="success"
                  @click="closeModal"
                >
                  {{ quizScore === quizQuestions.length ? 'Continue' : 'Close' }}
                </v-btn>
              </div>
            </div>
          </div>
        </v-card-text>

        <!-- Actions -->
        <v-card-actions class="pa-6 pt-0">
          <v-spacer></v-spacer>
          <v-btn
            v-if="!showQuiz || showResults"
            color="secondary"
            variant="outlined"
            @click="closeModal"
          >
            Close
          </v-btn>
        </v-card-actions>
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
    console.log('🐷 [MODAL] Getting modal value:', props.modelValue)
    return props.modelValue
  },
  set: (value) => {
    console.log('🐷 [MODAL] Setting modal value:', value)
    emit('update:modelValue', value)
  }
})

// Debug when component mounts
onMounted(() => {
  console.log('🐷 [MODAL] PiggyBankAdventure component mounted')
  console.log('🐷 [MODAL] Props received:', props)
  console.log('🐷 [MODAL] Initial modal state:', showModal.value)
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
    question: "What is a piggy bank?",
    options: [
      "A toy pig that makes sounds",
      "A special container to save money",
      "A bank that only accepts coins",
      "A pig that helps you count money"
    ],
    correctAnswer: 1,
    explanation: "A piggy bank is a special container where you can save your money safely!"
  },
  {
    question: "Why should you save money?",
    options: [
      "To spend it all at once",
      "To buy something special later",
      "To give it all away",
      "To hide it from your parents"
    ],
    correctAnswer: 1,
    explanation: "Saving money helps you buy something special you really want later!"
  },
  {
    question: "What is the best way to save money?",
    options: [
      "Spend it all immediately",
      "Put some money in your piggy bank every day",
      "Never save any money",
      "Only save on weekends"
    ],
    correctAnswer: 1,
    explanation: "Putting some money in your piggy bank every day is a great habit!"
  },
  {
    question: "How long have people been using piggy banks?",
    options: [
      "About 10 years",
      "About 100 years",
      "Over 600 years",
      "Since yesterday"
    ],
    correctAnswer: 2,
    explanation: "People have been using piggy banks for over 600 years!"
  },
  {
    question: "What should you do when you want to buy something expensive?",
    options: [
      "Ask your parents to buy it immediately",
      "Save money in your piggy bank until you have enough",
      "Never buy expensive things",
      "Use someone else's money"
    ],
    correctAnswer: 1,
    explanation: "Saving money in your piggy bank until you have enough is the smart way!"
  }
])

// Computed properties
const currentQuestion = computed(() => 
  quizQuestions.value[currentQuestionIndex.value]
)

const isAnswerCorrect = computed(() => 
  answerSelected.value === currentQuestion.value?.correctAnswer
)

// Methods
const startQuiz = () => {
  showQuiz.value = true
  currentQuestionIndex.value = 0
  answerSelected.value = null
  quizScore.value = 0
  userAnswers.value = []
  showResults.value = false
}

const selectAnswer = (optionIndex: number) => {
  answerSelected.value = optionIndex
  userAnswers.value[currentQuestionIndex.value] = optionIndex
  
  if (optionIndex === currentQuestion.value?.correctAnswer) {
    quizScore.value++
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < quizQuestions.value.length - 1) {
    currentQuestionIndex.value++
    answerSelected.value = null
  }
}

const finishQuiz = async () => {
  showResults.value = true
  
  if (quizScore.value === quizQuestions.value.length) {
    // Award coins
    try {
      await userStore.addCoins(props.coins, 'Completed Piggy Bank Adventure', 'activity')
      await dashboardStore.completeActivity('1')
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
.piggy-bank-adventure {
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
