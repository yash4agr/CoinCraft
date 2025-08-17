<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-100 via-pink-50 to-blue-100 p-4 pb-20">
    <!-- Back Button -->
    <div class="max-w-3xl mx-auto mb-4 flex justify-start">
      <button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-full font-medium hover:bg-gray-300 transition-colors flex items-center gap-2" @click="showBackModal = true">
        <i class="ri-arrow-left-line"></i> Back to Games
      </button>
    </div>
    <!-- Confirmation Modal -->
    <div v-if="showBackModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full">
        <div class="text-center mb-6">
          <div class="text-4xl mb-3">❓</div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Leave Game?</h3>
          <p class="text-gray-600">Are you sure you want to go back? Your progress in this game will be lost.</p>
        </div>
        <div class="flex gap-3">
          <button @click="showBackModal = false" class="flex-1 py-3 px-4 bg-gray-200 text-gray-800 rounded-lg font-medium hover:bg-gray-300 transition-colors">Cancel</button>
          <button @click="goBackToGames" class="flex-1 py-3 px-4 bg-blue-500 text-white rounded-lg font-medium hover:bg-blue-600 transition-colors">Yes, Go Back</button>
        </div>
      </div>
    </div>
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
        Needs vs Wants Game
      </h1>
      <p class="text-center text-gray-600 mb-8">Drag each item to the correct box!</p>

      <div v-if="!gameOver">
        <div class="flex justify-center gap-8 mb-8">
          <div class="w-1/2 flex flex-col items-center">
            <div class="text-2xl font-bold mb-2">Needs</div>
            <div
              id="needsbox"
              class="w-full h-32 rounded-xl flex flex-wrap items-center justify-center border-2"
              :class="[highlightedBox === 'need' ? 'bg-green-300 border-green-500' : 'bg-green-100 border-green-300']"
            >
              <span v-for="item in needsBoxItems" :key="item.id" class="relative inline-block mx-2">
                <span class="block text-lg mb-1 text-center">
                  {{ item.answer === 'need' ? '✔️' : '❌' }}
                </span>
                <span class="text-4xl mt-1">{{ item.emoji }}</span>
              </span>
            </div>
          </div>
          <div class="w-1/2 flex flex-col items-center">
            <div class="text-2xl font-bold mb-2">Wants</div>
            <div
              id="wantsbox"
              class="w-full h-32 rounded-xl flex flex-wrap items-center justify-center border-2"
              :class="[highlightedBox === 'want' ? 'bg-pink-300 border-pink-500' : 'bg-pink-100 border-pink-300']"
            >
              <span v-for="item in wantsBoxItems" :key="item.id" class="relative inline-block mx-2">
                <span class="block text-lg mb-1 text-center">
                  {{ item.answer === 'want' ? '✔️' : '❌' }}
                </span>
                <span class="text-4xl mt-1">{{ item.emoji }}</span>
              </span>
            </div>
          </div>
        </div>

        <div class="flex flex-col items-center mb-8">
          <div class="text-lg font-semibold mb-4">Question {{ currentIndex + 1 }} of {{ questions.length }}</div>
          <div class="flex flex-col items-center">
            <div
              v-if="currentItem && !answered"
              class="draggable-emoji text-6xl cursor-grab"
              :style="dragStyle"
              @mousedown="startDrag($event, currentItem)"
              @touchstart="startDrag($event, currentItem)"
            >
              {{ currentItem.emoji }}
            </div>
            <div v-else-if="currentItem && answered" class="text-6xl mb-2">{{ currentItem.emoji }}</div>
            <div v-else class="text-gray-500">No more items!</div>
          </div>
          <div v-if="feedback" class="mt-4">
            <span :class="feedback === 'correct' ? 'text-green-600 font-bold text-xl' : 'text-red-600 font-bold text-xl'">
              {{ feedback === 'correct' ? '✅ Correct!' : '❌ Wrong!' }}
            </span>
          </div>
          <div v-if="answered" class="mt-6">
            <button class="px-6 py-2 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="nextQuestion">
              Next
            </button>
          </div>
          <div v-if="!answered" class="mt-6 flex gap-4">
            <button class="px-6 py-2 bg-yellow-400 text-white rounded-full font-medium hover:bg-yellow-500" @click="showHint = true">
              Show Hint
            </button>
            <button class="px-6 py-2 bg-gray-300 text-gray-800 rounded-full font-medium hover:bg-gray-400" @click="skipQuestion">
              Skip Question
            </button>
          </div>
          <div v-if="showHint && !answered" class="mt-4 text-blue-700 font-medium">
            Hint: {{ currentItem ? (currentItem.answer === 'need' ? 'This is something you need to live or learn.' : 'This is something you want for fun or comfort.') : '' }}
          </div>
        </div>
      </div>

      <div v-else class="flex flex-col items-center justify-center mt-16">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Game Over!</h2>
        <div class="text-lg text-gray-700 mb-2">Your Score: <span class="font-bold text-green-600">{{ score }}</span> / {{ questions.length }}</div>
  <div v-if="!alreadyCompleted" class="text-green-700 font-bold mb-2">+10 coins for completing the task!</div>
  <div v-if="!alreadyCompleted && score === questions.length" class="text-blue-700 font-bold mb-4">Bonus: +5 coins for all correct answers!</div>
        <div class="flex justify-center gap-8 mb-8 w-full">
          <div class="w-1/2 flex flex-col items-center">
            <div class="text-xl font-bold mb-2">Your Needs Answers</div>
            <div class="w-full min-h-32 rounded-xl flex flex-wrap items-center justify-center border-2 bg-green-50 border-green-200">
              <span v-for="item in needsBoxItems" :key="item.id" class="relative inline-block mx-2">
                <span class="block text-lg mb-1 text-center">
                  {{ item.answer === 'need' ? '✔️' : '❌' }}
                </span>
                <span class="text-4xl mt-1">{{ item.emoji }}</span>
              </span>
            </div>
          </div>
          <div class="w-1/2 flex flex-col items-center">
            <div class="text-xl font-bold mb-2">Your Wants Answers</div>
            <div class="w-full min-h-32 rounded-xl flex flex-wrap items-center justify-center border-2 bg-pink-50 border-pink-200">
              <span v-for="item in wantsBoxItems" :key="item.id" class="relative inline-block mx-2">
                <span class="block text-lg mb-1 text-center">
                  {{ item.answer === 'want' ? '✔️' : '❌' }}
                </span>
                <span class="text-4xl mt-1">{{ item.emoji }}</span>
              </span>
            </div>
          </div>
        </div>
        <button class="mt-6 px-6 py-3 bg-blue-500 text-white rounded-full font-medium hover:bg-blue-600" @click="restartGame">
          Play Again
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
const showBackModal = ref(false)
const router = useRouter()
function goBackToGames() {
  showBackModal.value = false
  router.push('/child/games')
}
import { useUserStore } from '@/stores/user'
import { useChildStore } from '@/stores/child'
import apiService from '@/services/api'

const userStore = useUserStore()
const childStore = useChildStore()

const ACTIVITY_ID = 2 // Needs vs Wants Game, should match backend id

const questions = [
  { id: 1, emoji: '🍎', label: 'Apple', answer: 'need' },
  { id: 2, emoji: '🎮', label: 'Video Game', answer: 'want' },
  { id: 3, emoji: '👟', label: 'Shoes', answer: 'need' },
  { id: 4, emoji: '🍕', label: 'Pizza', answer: 'want' },
  { id: 5, emoji: '📚', label: 'Books', answer: 'need' },
  { id: 6, emoji: '🧸', label: 'Teddy Bear', answer: 'want' },
]

const currentIndex = ref(0)
const score = ref(0)
const gameOver = ref(false)
const needsBoxItems = ref<any[]>([])
const wantsBoxItems = ref<any[]>([])
const dragging = ref(false)
const dragItem = ref<any>(null)
const dragOffset = reactive({ x: 0, y: 0 })
const dragPosition = reactive({ x: 0, y: 0 })
const dragStyle = computed(() => {
  return dragging.value
    ? `position: fixed; left: ${dragPosition.x}px; top: ${dragPosition.y}px; z-index: 1000; pointer-events: none;`
    : ''
})

const currentItem = computed(() => questions[currentIndex.value])
const answered = ref(false)
const feedback = ref('')
const showHint = ref(false)
const highlightedBox = ref('')
const alreadyCompleted = computed(() => {
  const activity = childStore.activities.find(a => a.id == ACTIVITY_ID)
  return activity?.completed
})

function startDrag(event: MouseEvent | TouchEvent, item: any) {
  if (answered.value) return
  dragging.value = true
  dragItem.value = item
  highlightedBox.value = ''
  if (event instanceof MouseEvent) {
    dragOffset.x = event.clientX
    dragOffset.y = event.clientY
    dragPosition.x = event.clientX
    dragPosition.y = event.clientY
    window.addEventListener('mousemove', onDrag)
    window.addEventListener('mouseup', endDrag)
  } else if (event instanceof TouchEvent) {
    dragOffset.x = event.touches[0]?.clientX || 0
    dragOffset.y = event.touches[0]?.clientY || 0
    dragPosition.x = event.touches[0]?.clientX || 0
    dragPosition.y = event.touches[0]?.clientY || 0
    window.addEventListener('touchmove', onDrag)
    window.addEventListener('touchend', endDrag)
  }
}

function onDrag(event: MouseEvent | TouchEvent) {
  if (!dragging.value) return
  if (event instanceof MouseEvent) {
    dragPosition.x = event.clientX
    dragPosition.y = event.clientY
  } else if (event instanceof TouchEvent) {
    dragPosition.x = event.touches[0]?.clientX || 0
    dragPosition.y = event.touches[0]?.clientY || 0
  }
  highlightedBox.value = ''
  const needsBox = document.getElementById('needsbox') as HTMLElement
  const wantsBox = document.getElementById('wantsbox') as HTMLElement
  const x = dragPosition.x
  const y = dragPosition.y
  if (needsBox) {
    const rect = needsBox.getBoundingClientRect()
    if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom) {
      highlightedBox.value = 'need'
    }
  }
  if (wantsBox) {
    const rect = wantsBox.getBoundingClientRect()
    if (x > rect.left && x < rect.right && y > rect.top && y < rect.bottom) {
      highlightedBox.value = 'want'
    }
  }
}

function endDrag(event: MouseEvent | TouchEvent) {
  if (!dragging.value) return
  dragging.value = false
  let droppedIn = highlightedBox.value
  highlightedBox.value = ''
  if (droppedIn && dragItem.value) {
    answered.value = true
    showHint.value = false
    if (droppedIn === dragItem.value.answer) {
      score.value++
      feedback.value = 'correct'
    } else {
      feedback.value = 'wrong'
    }
    if (droppedIn === 'need') {
      needsBoxItems.value.push(dragItem.value)
    } else if (droppedIn === 'want') {
      wantsBoxItems.value.push(dragItem.value)
    }
  }
  dragItem.value = null
  window.removeEventListener('mousemove', onDrag)
  window.removeEventListener('mouseup', endDrag)
  window.removeEventListener('touchmove', onDrag)
  window.removeEventListener('touchend', endDrag)
}

async function handleGameOver() {
  if (alreadyCompleted.value) return
  // Mark activity as complete and award coins
  await apiService.completeActivity(ACTIVITY_ID)
  await childStore.loadActivities() // Refresh status
  await userStore.addCoins(10, 'Completed Needs vs Wants Game', 'activity')
  if (score.value === questions.length) {
    await userStore.addCoins(5, 'Bonus: All answers correct in Needs vs Wants Game', 'activity')
  }
}

watch(() => gameOver.value, async (val) => {
  if (val) {
    await handleGameOver()
  }
})

function nextQuestion() {
  answered.value = false
  feedback.value = ''
  showHint.value = false
  currentIndex.value++
  if (currentIndex.value >= questions.length) {
    gameOver.value = true
  }
}

function skipQuestion() {
  answered.value = false
  feedback.value = ''
  showHint.value = false
  currentIndex.value++
  if (currentIndex.value >= questions.length) {
    gameOver.value = true
  }
}

function restartGame() {
  currentIndex.value = 0
  score.value = 0
  gameOver.value = false
  needsBoxItems.value = []
  wantsBoxItems.value = []
  answered.value = false
  feedback.value = ''
  showHint.value = false
}

</script>

<style scoped>
.draggable-emoji {
  user-select: none;
}
</style>