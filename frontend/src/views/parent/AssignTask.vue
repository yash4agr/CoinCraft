<template>
  <v-container fluid class="pa-4">
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="orange">mdi-clipboard-text</v-icon>
            Assign Task
            <v-spacer />
            <v-btn
              prepend-icon="mdi-history"
              variant="tonal"
              @click="showTaskHistory = true"
            >
              Task History
            </v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Task Creation Form -->
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Create New Task</v-card-title>
          <v-card-text>
            <v-form ref="taskForm" v-model="taskFormValid">
              <!-- Task Type Selection -->
              <div class="text-subtitle-1 font-weight-medium mb-3">Task Type</div>
              <v-radio-group v-model="task.type" class="mb-4">
                <v-radio
                  v-for="type in taskTypes"
                  :key="type.value"
                  :label="type.title"
                  :value="type.value"
                >
                  <template #label>
                    <div class="d-flex align-center">
                      <v-icon :color="type.color" class="me-2">{{ type.icon }}</v-icon>
                      <div>
                        <div class="font-weight-medium">{{ type.title }}</div>
                        <div class="text-caption text-medium-emphasis">{{ type.description }}</div>
                      </div>
                    </div>
                  </template>
                </v-radio>
              </v-radio-group>

              <!-- Task Details -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="task.title"
                    label="Task Title"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-format-title"
                    variant="outlined"
                    placeholder="e.g., Complete homework, Clean room"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-select="task.assignedTo"
                    label="Assign to"
                    :items="children"
                    item-title="name"
                    item-value="id"
                    :rules="[rules.required]"
                    prepend-inner-icon="mdi-account"
                    variant="outlined"
                    multiple
                    chips
                  />
                </v-col>
              </v-row>

              <v-textarea
                v-model="task.description"
                label="Task Description"
                prepend-inner-icon="mdi-text"
                variant="outlined"
                rows="3"
                placeholder="Provide detailed instructions for the task..."
                class="mb-3"
              />

              <!-- Reward Configuration -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model.number="task.coinReward"
                    label="Coin Reward"
                    type="number"
                    :rules="[rules.required, rules.positive]"
                    prepend-inner-icon="mdi-star"
                    variant="outlined"
                    min="1"
                    max="100"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select
                    v-model="task.priority"
                    label="Priority"
                    :items="priorities"
                    prepend-inner-icon="mdi-flag"
                    variant="outlined"
                  />
                </v-col>
              </v-row>

              <!-- Scheduling -->
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="task.dueDate"
                    label="Due Date (Optional)"
                    type="date"
                    prepend-inner-icon="mdi-calendar"
                    variant="outlined"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="task.dueTime"
                    label="Due Time (Optional)"
                    type="time"
                    prepend-inner-icon="mdi-clock"
                    variant="outlined"
                  />
                </v-col>
              </v-row>

              <!-- Task Options -->
              <div class="text-subtitle-1 font-weight-medium mb-3">Task Options</div>
              <v-row>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="task.requiresApproval"
                    label="Requires parent approval"
                    density="compact"
                  />
                  <v-checkbox
                    v-model="task.recurring"
                    label="Recurring task"
                    density="compact"
                  />
                  <v-checkbox
                    v-model="task.allowPartialCompletion"
                    label="Allow partial completion"
                    density="compact"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-checkbox
                    v-model="task.notifyOnDue"
                    label="Send reminder notifications"
                    density="compact"
                  />
                  <v-checkbox
                    v-model="task.photoRequired"
                    label="Photo proof required"
                    density="compact"
                  />
                  <v-checkbox
                    v-model="task.bonusAvailable"
                    label="Bonus coins for early completion"
                    density="compact"
                  />
                </v-col>
              </v-row>

              <!-- Recurring Task Settings -->
              <v-expand-transition>
                <div v-if="task.recurring" class="mb-4">
                  <v-divider class="mb-3" />
                  <div class="text-subtitle-2 font-weight-medium mb-3">Recurring Settings</div>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-select
                        v-model="task.recurringFrequency"
                        label="Frequency"
                        :items="frequencies"
                        variant="outlined"
                      />
                    </v-col>
                    <v-col cols="12" md="6">
                      <v-text-field
                        v-model="task.recurringEnd"
                        label="End Date (Optional)"
                        type="date"
                        variant="outlined"
                      />
                    </v-col>
                  </v-row>
                </div>
              </v-expand-transition>

              
            </v-form>
          </v-card-text>
          
          <v-card-actions>
            <v-spacer />
            <v-btn @click="resetForm">Reset</v-btn>
            <v-btn
              color="orange"
              variant="tonal"
              prepend-icon="mdi-content-save-outline"
              @click="saveDraft"
            >
              Save as Draft
            </v-btn>
            <v-btn
              color="primary"
              prepend-icon="mdi-send"
              @click="assignTask"
              :loading="assigning"
              :disabled="!taskFormValid"
            >
              Assign Task
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>

      <!-- Quick Actions & Templates -->
      <v-col cols="12" md="4">
        <!-- Quick Templates -->
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="purple">mdi-lightning-bolt</v-icon>
            Quick Templates
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="template in taskTemplates"
                :key="template.id"
                @click="applyTemplate(template)"
                class="mb-1"
              >
                <template #prepend>
                  <v-icon :color="template.color">{{ template.icon }}</v-icon>
                </template>
                <v-list-item-title class="text-body-2">{{ template.title }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption">{{ template.reward }} coins</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Active Tasks Summary -->
        <v-card class="mb-4">
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="info">mdi-chart-donut</v-icon>
            Active Tasks Summary
          </v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="child in children"
                :key="child.id"
                density="compact"
              >
                <template #prepend>
                  <v-avatar size="24" :color="child.color">
                    <span class="text-caption text-white">{{ child.initials }}</span>
                  </v-avatar>
                </template>
                <v-list-item-title class="text-body-2">{{ child.name }}</v-list-item-title>
                <template #append>
                  <v-chip size="small" :color="getTaskStatusColor(child.activeTasks)">
                    {{ child.activeTasks }} tasks
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- Task Tips -->
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="success">mdi-lightbulb</v-icon>
            Task Tips
          </v-card-title>
          <v-card-text>
            <v-alert
              v-for="tip in taskTips"
              :key="tip.id"
              :type="tip.type"
              variant="tonal"
              density="compact"
              class="mb-2"
            >
              {{ tip.message }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Task History Dialog -->
    <v-dialog v-model="showTaskHistory" max-width="800" scrollable>
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="me-2" color="info">mdi-history</v-icon>
          Task History
          <v-spacer />
          <v-btn
            icon="mdi-close"
            variant="text"
            @click="showTaskHistory = false"
          />
        </v-card-title>
        
        <v-card-text>
          <v-data-table
            :headers="historyHeaders"
            :items="taskHistory"
            item-value="id"
            class="elevation-0"
          >
            <template #item.child="{ item }">
              <div class="d-flex align-center">
                <v-avatar size="24" :color="item.childColor" class="me-2">
                  <span class="text-caption text-white">{{ item.childInitials }}</span>
                </v-avatar>
                {{ item.child }}
              </div>
            </template>

            <template #item.status="{ item }">
              <v-chip :color="getHistoryStatusColor(item.status)" size="small">
                {{ item.status }}
              </v-chip>
            </template>

            <template #item.coins="{ item }">
              <div class="d-flex align-center">
                <v-icon color="warning" size="small" class="me-1">mdi-star</v-icon>
                {{ item.coins }}
              </div>
            </template>

            <template #item.assignedDate="{ item }">
              {{ formatDate(item.assignedDate) }}
            </template>

            <template #item.completedDate="{ item }">
              {{ item.completedDate ? formatDate(item.completedDate) : '-' }}
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="showSuccessSnackbar"
      color="success"
      timeout="3000"
    >
      {{ successMessage }}
      <template #actions>
        <v-btn
          variant="text"
          @click="showSuccessSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Task, Child } from '@/types'

// Reactive data
const assigning = ref(false)
const showTaskHistory = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const taskFormValid = ref(false)

// Task form data
const task = reactive<Partial<Task>>({
  type: 'chore',
  title: '',
  description: '',
  assignedTo: [],
  coinReward: 10,
  priority: 'Medium',
  dueDate: '',
  dueTime: '',
  requiresApproval: true,
  recurring: false,
  allowPartialCompletion: false,
  notifyOnDue: true,
  photoRequired: false,
  bonusAvailable: false,
  recurringFrequency: 'Daily',
  recurringEnd: '',
  bonusCoins: 5,
  bonusHours: 24
})

// Mock data
const children = ref([
  {
    id: '1',
    name: 'Luna',
    initials: 'L',
    color: 'purple',
    activeTasks: 3
  },
  {
    id: '2',
    name: 'Harry',
    initials: 'H',
    color: 'blue',
    activeTasks: 2
  }
])

const taskHistory = ref([
  {
    id: '1',
    title: 'Clean bedroom',
    child: 'Luna',
    childInitials: 'L',
    childColor: 'purple',
    status: 'Completed',
    coins: 15,
    assignedDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    completedDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
  },
  {
    id: '2',
    title: 'Finish homework',
    child: 'Harry',
    childInitials: 'H',
    childColor: 'blue',
    status: 'In Progress',
    coins: 20,
    assignedDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    completedDate: null
  },
  {
    id: '3',
    title: 'Take out trash',
    child: 'Luna',
    childInitials: 'L',
    childColor: 'purple',
    status: 'Overdue',
    coins: 10,
    assignedDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    completedDate: null
  }
])

// Static data
const taskTypes = [
  {
    value: 'chore',
    title: 'Chore',
    description: 'Household tasks and responsibilities',
    icon: 'mdi-home-variant',
    color: 'blue'
  },
  {
    value: 'educational',
    title: 'Educational',
    description: 'Learning modules and assignments',
    icon: 'mdi-book-open',
    color: 'green'
  },
  {
    value: 'personal',
    title: 'Personal',
    description: 'Self-care and personal development',
    icon: 'mdi-account-heart',
    color: 'purple'
  },
  {
    value: 'creative',
    title: 'Creative',
    description: 'Art, music, and creative projects',
    icon: 'mdi-palette',
    color: 'orange'
  }
]

const priorities = ['Low', 'Medium', 'High', 'Urgent']
const frequencies = ['Daily', 'Weekly', 'Bi-weekly', 'Monthly']

const taskTemplates = [
  {
    id: '1',
    title: 'Clean bedroom',
    icon: 'mdi-bed',
    color: 'blue',
    reward: 15,
    type: 'chore',
    description: 'Make bed, organize desk, put away clothes'
  },
  {
    id: '2',
    title: 'Complete homework',
    icon: 'mdi-pencil',
    color: 'green',
    reward: 20,
    type: 'educational',
    description: 'Finish all assigned homework and study'
  },
  {
    id: '3',
    title: 'Practice instrument',
    icon: 'mdi-music',
    color: 'purple',
    reward: 10,
    type: 'creative',
    description: 'Practice for 30 minutes'
  },
  {
    id: '4',
    title: 'Exercise/Sports',
    icon: 'mdi-run',
    color: 'orange',
    reward: 12,
    type: 'personal',
    description: 'Physical activity for 45 minutes'
  }
]

const taskTips = [
  {
    id: '1',
    type: 'info',
    message: 'Set clear expectations and deadlines for better completion rates.'
  },
  {
    id: '2',
    type: 'success',
    message: 'Reward systems work best when coins can be saved for meaningful goals.'
  },
  {
    id: '3',
    type: 'warning',
    message: 'Break large tasks into smaller, manageable steps for younger children.'
  }
]

const historyHeaders = [
  { title: 'Task', key: 'title', sortable: true },
  { title: 'Child', key: 'child', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Coins', key: 'coins', sortable: true },
  { title: 'Assigned', key: 'assignedDate', sortable: true },
  { title: 'Completed', key: 'completedDate', sortable: true }
]

// Validation rules
const rules = {
  required: (value: any) => !!value || 'This field is required',
  positive: (value: number) => value > 0 || 'Must be greater than 0'
}

// Methods
const applyTemplate = (template: any) => {
  task.title = template.title
  task.description = template.description
  task.type = template.type
  task.coinReward = template.reward
  
  showSuccessSnackbar.value = true
  successMessage.value = `Template "${template.title}" applied!`
}

const assignTask = async () => {
  if (!taskFormValid.value) return
  
  assigning.value = true
  try {
    // Simulate task assignment
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    showSuccessSnackbar.value = true
    successMessage.value = `Task "${task.title}" assigned successfully!`
    
    resetForm()
  } catch (error) {
    console.error('Failed to assign task:', error)
  } finally {
    assigning.value = false
  }
}

const saveDraft = async () => {
  try {
    // Simulate saving draft
    await new Promise(resolve => setTimeout(resolve, 500))
    
    showSuccessSnackbar.value = true
    successMessage.value = 'Task saved as draft!'
  } catch (error) {
    console.error('Failed to save draft:', error)
  }
}

const resetForm = () => {
  Object.assign(task, {
    type: 'chore',
    title: '',
    description: '',
    assignedTo: [],
    coinReward: 10,
    priority: 'Medium',
    dueDate: '',
    dueTime: '',
    requiresApproval: true,
    recurring: false,
    allowPartialCompletion: false,
    notifyOnDue: true,
    photoRequired: false,
    bonusAvailable: false,
    recurringFrequency: 'Daily',
    recurringEnd: '',
    bonusCoins: 5,
    bonusHours: 24
  })
}

const getTaskStatusColor = (count: number) => {
  if (count === 0) return 'success'
  if (count <= 2) return 'info'
  if (count <= 4) return 'warning'
  return 'error'
}

const getHistoryStatusColor = (status: string) => {
  const colors = {
    'Completed': 'success',
    'In Progress': 'info',
    'Overdue': 'error',
    'Cancelled': 'grey'
  }
  return colors[status as keyof typeof colors] || 'grey'
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date)
}

// Lifecycle
onMounted(() => {
  // Load children and task data
})
</script>

