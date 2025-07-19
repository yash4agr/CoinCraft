<template>
  <v-dialog v-model="showDialog" max-width="1000px" persistent>
    <v-card>
      <!-- Header -->
      <v-card-title class="bg-primary text-white">
        <v-icon start>mdi-play-circle</v-icon>
        Try Mode: {{ module?.title }}
        <v-spacer></v-spacer>
        <v-btn icon @click="closeDialog" variant="text">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-text class="pa-6">
        <!-- Module Header Info -->
        <div class="mb-6">
          <h2 class="text-h4 font-weight-bold mb-2">{{ module?.title }}</h2>
          <div class="d-flex align-center mb-3">
            <v-chip
              :color="getDifficultyColor(module?.difficulty)"
              size="small"
              class="mr-3"
            >
              {{ module?.difficulty }}
            </v-chip>
            <v-chip size="small" color="info" class="mr-3">
              {{ module?.duration }} min
            </v-chip>
            <v-chip size="small" color="secondary">
              {{ module?.ageGroup }}
            </v-chip>
          </div>
          <p class="text-body-1 mb-4">{{ module?.description }}</p>
          
          <!-- Learning Objectives -->
          <div v-if="module?.learningObjectives" class="mb-4">
            <h4 class="text-h6 mb-2">Learning Objectives:</h4>
            <ul class="text-body-2">
              <li v-for="objective in module.learningObjectives" :key="objective" class="mb-1">
                • {{ objective }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Content Mode vs Quiz Mode Toggle -->
        <div class="mb-6">
          <v-btn-toggle
            v-model="currentMode"
            mandatory
            color="primary"
            class="mb-4"
          >
            <v-btn value="content" prepend-icon="mdi-book-open">
              Module Content
            </v-btn>
            <v-btn value="quiz" prepend-icon="mdi-help-circle">
              Take Quiz
            </v-btn>
          </v-btn-toggle>
        </div>

        <!-- Content Mode -->
        <div v-if="currentMode === 'content'" class="module-content">
          <!-- Module Sections -->
          <div v-if="module?.sections" class="mb-8">
            <h3 class="text-h5 mb-4">📚 Module Sections</h3>
            <div class="space-y-4">
              <v-card
                v-for="(section, index) in module.sections"
                :key="index"
                variant="outlined"
                class="pa-4"
              >
                <div class="d-flex align-center mb-3">
                  <v-icon
                    :icon="getSectionIcon(section.type)"
                    color="primary"
                    class="mr-3"
                  ></v-icon>
                  <h4 class="text-h6 font-weight-medium">{{ section.title }}</h4>
                  <v-chip size="x-small" class="ml-auto">{{ section.duration }}</v-chip>
                </div>
                <p class="text-body-1 mb-3">{{ section.content }}</p>
                <v-chip
                  :color="getSectionTypeColor(section.type)"
                  size="small"
                >
                  {{ section.type }}
                </v-chip>
              </v-card>
            </div>
          </div>

          <!-- Learning Activities -->
          <div v-if="module?.activities" class="mb-8">
            <h3 class="text-h5 mb-4">🎯 Learning Activities</h3>
            <v-row>
              <v-col
                v-for="(activity, index) in module.activities"
                :key="index"
                cols="12"
                md="6"
              >
                <v-card variant="outlined" class="pa-4 h-100">
                  <div class="d-flex align-center mb-3">
                    <v-icon
                      :icon="getActivityIcon(activity.type)"
                      color="orange"
                      class="mr-2"
                    ></v-icon>
                    <h5 class="text-subtitle-1 font-weight-medium">{{ activity.title }}</h5>
                  </div>
                  <p class="text-body-2 mb-3">{{ activity.description }}</p>
                  <div class="d-flex justify-space-between align-center mb-3">
                    <v-chip size="x-small" color="orange">{{ activity.type }}</v-chip>
                    <span class="text-caption">{{ activity.duration }}</span>
                  </div>
                  <div v-if="activity.materials" class="mb-3">
                    <strong class="text-caption">Materials:</strong>
                    <p class="text-caption">{{ activity.materials }}</p>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </div>
        </div>

        <!-- Quiz Mode -->
        <div v-else class="quiz-section">
          <h3 class="text-h5 mb-4">🧠 Knowledge Check</h3>
          
          <div v-if="!quizCompleted">
            <div v-for="(question, index) in module?.quiz" :key="index" class="mb-6">
              <v-card variant="outlined" class="pa-4">
                <h5 class="text-subtitle-1 font-weight-medium mb-3">
                  Q{{ index + 1 }}: {{ question.question }}
                </h5>
                
                <v-radio-group v-model="quizAnswers[index]" class="mb-3">
                  <v-radio
                    v-for="(option, optIndex) in question.options"
                    :key="optIndex"
                    :label="option.text"
                    :value="optIndex"
                    color="primary"
                  ></v-radio>
                </v-radio-group>
                
                <v-alert
                  v-if="showQuizFeedback && quizAnswers[index] !== undefined"
                  :type="isAnswerCorrect(index) ? 'success' : 'error'"
                  variant="tonal"
                  density="compact"
                >
                  <div v-if="isAnswerCorrect(index)">
                    <strong>Correct!</strong> {{ question.explanation }}
                  </div>
                  <div v-else>
                    <strong>Incorrect.</strong> {{ question.explanation }}
                  </div>
                </v-alert>
              </v-card>
            </div>
            
            <div class="d-flex justify-space-between">
              <v-btn
                @click="checkQuiz"
                color="primary"
                size="large"
              >
                <v-icon start>mdi-check-circle</v-icon>
                Check Answers
              </v-btn>
            </div>
          </div>
          
          <!-- Quiz Results -->
          <div v-else class="text-center">
            <v-card variant="outlined" class="pa-6">
              <v-icon
                :icon="quizScore >= 70 ? 'mdi-trophy' : 'mdi-school'"
                :color="quizScore >= 70 ? 'warning' : 'primary'"
                size="64"
                class="mb-4"
              ></v-icon>
              <h4 class="text-h5 mb-2">
                {{ quizScore >= 70 ? 'Great Job!' : 'Good Effort!' }}
              </h4>
              <p class="text-h4 font-weight-bold mb-2" :class="quizScore >= 70 ? 'text-warning' : 'text-primary'">
                {{ quizScore }}%
              </p>
              <p class="text-body-1 mb-4">
                You got {{ correctAnswers }} out of {{ module?.quiz?.length }} questions correct.
              </p>
              <v-btn
                @click="completeModule"
                color="success"
                size="large"
              >
                <v-icon start>mdi-flag-checkered</v-icon>
                Complete Module
              </v-btn>
            </v-card>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Module, ModuleSection, ModuleActivity, QuizQuestion } from '@/stores/teacher'

// Props
interface Props {
  modelValue: boolean
  module: Module | null
}

const props = defineProps<Props>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'module-completed': [module: Module, score: number]
}>()

// Reactive state
const currentMode = ref('content')
const quizAnswers = ref<number[]>([])
const showQuizFeedback = ref(false)
const quizCompleted = ref(false)
const correctAnswers = ref(0)
const quizScore = ref(0)

// Computed
const showDialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Methods
const closeDialog = () => {
  showDialog.value = false
  resetTryMode()
}

const resetTryMode = () => {
  currentMode.value = 'content'
  quizAnswers.value = []
  showQuizFeedback.value = false
  quizCompleted.value = false
  correctAnswers.value = 0
  quizScore.value = 0
}

const getDifficultyColor = (difficulty?: string) => {
  switch (difficulty) {
    case 'beginner': return 'success'
    case 'intermediate': return 'warning'
    case 'advanced': return 'error'
    default: return 'primary'
  }
}

const getSectionIcon = (type: string) => {
  switch (type) {
    case 'lesson': return 'mdi-book-open-variant'
    case 'reading': return 'mdi-file-document'
    case 'video': return 'mdi-video'
    case 'discussion': return 'mdi-forum'
    default: return 'mdi-book'
  }
}

const getSectionTypeColor = (type: string) => {
  switch (type) {
    case 'lesson': return 'primary'
    case 'reading': return 'info'
    case 'video': return 'purple'
    case 'discussion': return 'orange'
    default: return 'grey'
  }
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'exercise': return 'mdi-dumbbell'
    case 'simulation': return 'mdi-gamepad-variant'
    case 'case_study': return 'mdi-briefcase'
    case 'group_work': return 'mdi-account-group'
    case 'project': return 'mdi-folder-multiple'
    default: return 'mdi-lightbulb'
  }
}



const checkQuiz = () => {
  showQuizFeedback.value = true
  
  // Calculate score
  let correct = 0
  props.module?.quiz?.forEach((question, index) => {
    if (isAnswerCorrect(index)) {
      correct++
    }
  })
  
  correctAnswers.value = correct
  quizScore.value = Math.round((correct / (props.module?.quiz?.length || 1)) * 100)
  
  // Auto-complete quiz after showing feedback
  setTimeout(() => {
    quizCompleted.value = true
  }, 3000)
}

const isAnswerCorrect = (index: number) => {
  const question = props.module?.quiz?.[index]
  const answer = quizAnswers.value[index]
  
  if (!question || answer === undefined) return false
  
  return question.options[answer]?.isCorrect || false
}

const completeModule = () => {
  if (props.module) {
    emit('module-completed', props.module, quizScore.value)
  }
  closeDialog()
}

// Watch for module changes
watch(() => props.module, () => {
  if (props.module) {
    resetTryMode()
    // Initialize quiz answers array
    quizAnswers.value = new Array(props.module.quiz?.length || 0).fill(undefined)
  }
})
</script>

<style scoped>
.border-primary {
  border: 2px solid rgb(var(--v-theme-primary)) !important;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-4 > *:first-child {
  margin-top: 0;
}

.h-100 {
  height: 100%;
}

.module-content {
  max-height: 70vh;
  overflow-y: auto;
}

.quiz-section {
  max-height: 70vh;
  overflow-y: auto;
}
</style> 