<template>
    <div class="container" style="align-items: center;">
      
        <div class="row">
          
            <div class="col" style="width: 100%;">
                <div class="nav-card-body">
                    <h2 class="welcome-text"> 📋  Assign Task</h2>
                    <button class="add-child-btn" @click="goToTaskHistory"> 🕒 Task History</button>
                </div>
            </div>
        </div>
      <div class="row" style="border-spacing: 0.1rem;">
          <div class="col">
           <div class="create-task"> 
            <div class="form-container">
              <h2 class="welcome-text" style="display: flex;">Create New Task</h2>
              <form @submit.prevent="assignTask">
                
                <!-- Task Type -->
                <div class="section">
                  <label>Task Type</label>
                  <div class="radio-group">
                    <label 
                      v-for="type in taskTypes"
                      :key="type.value"
                      class="icon-with-text"
                    >
                      <input
                        type="radio"
                        v-model="task.type"
                        :value="type.value"
                        name="taskType"
                      />
                      <span class="logo">{{ type.icon }}</span>
                      <div class="text-block">
                        <div class="title">{{ type.title }}</div>
                        <div class="subtitle">{{ type.description }}</div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Title + Assign To -->
                <div class="row">
                  <div class="field">
                    <label>Task Title</label>
                    <div class="input-icon">
                      <input style="height: 150%;"
                        v-model="task.title"
                        type="text"
                        placeholder="e.g., Complete homework, Clean room"
                        required
                      />
                    </div>
                  </div>

                  <div class="field">
                    <label>Assign to</label>
                    <div class="input-icon">
                      <select style="height: 150%;" v-model="task.assignedTo" required>
                        <option value="" disabled>Select a child</option>
                        <option
                          v-for="child in children"
                          :key="child.id"
                          :value="child.id">
                          {{ child.name }}
                        </option>
                      </select>
                    </div>
                    <div class="chips">
                      <span
                        class="chip"
                        v-for="id in task.assignedTo"
                        :key="id"
                      >
                        {{ getChildName(id) }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Description -->
                <div class="field">
                  <label>Task Description</label>
                  <textarea
                    v-model="task.description"
                    rows="3"
                    placeholder="Provide detailed instructions for the task..."
                  ></textarea>
                </div>

                <!-- Reward & Priority -->
                <div class="row">
                  <div class="field">
                    <label>Coin Reward</label>
                    <div class="input-icon">
              
                      <input style="height: 150%;"
                        v-model.number="task.coinReward"
                        type="number"
                        min="1"
                        max="100"
                        required
                      />
                    </div>
                  </div>
                  <div class="field">
                    <label>Priority</label>
                    <div class="input-icon">

                      <select style="height: 150%;" v-model="task.priority">
                        <option v-for="p in priorities" :key="p" :value="p">
                          {{ p }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>

                <!-- Scheduling -->
                <div class="row">
                  <div class="field">
                    <label>Due Date</label>
                    <div class="input-icon">
                      <input style="height: 150%;" v-model="task.dueDate" type="date" />
                    </div>
                  </div>
                  <div class="field">
                    <label>Due Time</label>
                    <div class="input-icon">
                    <input style="height: 150%;" v-model="task.dueTime" type="time" />
                  </div>
                  </div>
                </div>

                <!-- Task Options -->
                <div class="section">
                  <label class="welcome-text">Task Options</label>
                  <div class="checkbox-grid" style="margin: 10px;">
                    <label><input type="checkbox" v-model="task.requiresApproval" /> Requires parent approval</label>
                    <label><input type="checkbox" v-model="task.recurring" /> Recurring task</label>
                    <label><input type="checkbox" v-model="task.allowPartialCompletion" /> Allow partial completion</label>
                    <label><input type="checkbox" v-model="task.notifyOnDue" /> Send reminders</label>
                    <label><input type="checkbox" v-model="task.photoRequired" /> Photo proof required</label>
                    <label><input type="checkbox" v-model="task.bonusAvailable" /> Bonus coins for early completion</label>
                  </div>
                </div>

                <!-- Recurring Settings -->
                <div v-if="task.recurring" class="section">
                  <label class="welcome-text">Recurring Settings</label>
                  <div class="row">
                    <div class="field">
                      <label>Frequency</label>
                      <div class="input-icon">
                      <select style="height: 150%;" v-model="task.recurringFrequency">
                        <option v-for="f in frequencies" :key="f" :value="f">{{ f }}</option>
                      </select>
                      </div>
                    </div>
                    <div class="field">
                      <label>End Date</label>
                      <div class="input-icon">
                      <input style="height: 150%;" v-model="task.recurringEnd" type="date" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Bonus Settings -->
                <div v-if="task.bonusAvailable" class="section">
                  <label class="welcome-text">Bonus Settings</label>
                  <div class="row">
                    <div class="field">
                      <label>Bonus Coins</label>
                      <div class="input-icon">
                      <input style="height: 150%;" v-model.number="task.bonusCoins" type="number" min="1" />
                      </div>
                    </div>
                    <div class="field">
                      <label>Bonus if completed within (hours)</label>
                      <div class="input-icon">
                      <input style="height: 150%;" v-model.number="task.bonusHours" type="number" min="1" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Buttons -->
                <div class="buttons">
                  <button type="button" @click="resetForm">Reset</button>
                  <button type="button" @click="saveDraft">💾 Save as Draft</button>
                  <button type="submit" :disabled="!taskFormValid">🚀 Assign Task</button>
                </div>
              </form>


              <div v-if="showSuccessSnackbar" class="snackbar">
                <span>{{ successMessage }}</span>
                <button @click="showSuccessSnackbar = false">✖</button>
              </div>
            </div>
          </div>
        </div>
            <div class="col">
               <div class="quick-template">
                    <div class="card mb-4">
                    <div class="card-title">
                        <span class="icon purple">⚡</span>
                        Quick Templates
                    </div>
                    <div class="card-content">
                        <ul class="template-list">
                        <li
                            v-for="template in taskTemplates"
                            :key="template.id"
                            class="template-item"
                            @click="applyTemplate(template)"
                        >
                            <span class="template-icon" :style="{ color: template.color }">
                            {{ template.icon }}
                            </span>
                            <div class="template-info">
                            <div class="template-title">{{ template.title }}</div>
                            <div class="template-subtitle">{{ template.reward }} coins</div>
                            </div>
                        </li>
                        </ul>
                    </div>
                    </div>

                </div>
                        <!-- Active Tasks Summary -->
                <div class="quick-template">
                    <div class="card mb-4">
                    <div class="card-title">
                        <span class="icon">📊</span>
                        <span>Active Tasks Summary</span>
                    </div>
                    <div class="card-content">
                        <ul class="task-list">
                        <li
                            v-for="child in children"
                            :key="child.id"
                            class="task-item"
                        >
                            <span
                            class="avatar"
                            :style="{ backgroundColor: child.color }"
                            >
                            {{ child.initials }}
                            </span>
                            <span class="name">{{ child.name }}</span>
                            <span
                            class="chip"
                            :style="{ backgroundColor: getTaskStatusColor(child.activeTasks) }"
                            >
                            {{ child.activeTasks }} tasks
                            </span>
                        </li>
                        </ul>
                    </div>
                    </div>

                </div>
                <!-- Task Tips -->
                <div class="quick-template">
                    <div class="card">
                        <div class="card-title">
                            <span class="icon">💡</span>
                            <span>Task Tips</span>
                        </div>
                        <div class="card-content">
                            <div
                            v-for="tip in taskTips"
                            :key="tip.id"
                            class="alert"
                            :class="tip.type"
                            >
                            {{ tip.message }}
                            </div>
                        </div>
                        </div>
                </div>
            </div>
        </div>
         <!-- Task History Dialog -->
          <div v-if="showTaskHistory" class="modal-overlay">
            <div class="modal">
              <div class="modal-header">
                <span class="icon">📜</span>
                <span class="title">Task History</span>
                <button class="close" @click="showTaskHistory = false">✖</button>
              </div>

              <div class="modal-body">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>Child</th>
                      <th>Status</th>
                      <th>Coins</th>
                      <th>Assigned</th>
                      <th>Completed</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in taskHistory" :key="item.id">
                      <td>
                        <span class="avatar" :style="{ backgroundColor: item.childColor }">
                          {{ item.childInitials }}
                        </span>
                        {{ item.child }}
                      </td>
                      <td>
                        <span class="chip" :class="getHistoryStatusColor(item.status)">
                          {{ item.status }}
                        </span>
                      </td>
                      <td>
                        <span class="icon small">⭐</span>
                        {{ item.coins }}
                      </td>
                      <td>{{ formatDate(item.assignedDate) }}</td>
                      <td>{{ item.completedDate ? formatDate(item.completedDate) : '-' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
    </div>
    

</template>


<script setup lang="ts">

import { ref, reactive, onMounted } from 'vue'
import type { Task} from '@/types'
import { useRouter } from 'vue-router'


const router = useRouter()

function goToTaskHistory() {
  router.push('/taskhistory')
}
// Reactive data
const assigning = ref(false)
const showTaskHistory = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const taskFormValid = ref(true)

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
    icon: '🏠',
    color: 'blue'
  },
  {
    value: 'educational',
    title: 'Educational',
    description: 'Learning modules and assignments',
    icon: '📖',
    color: 'green'
  },
  {
    value: 'personal',
    title: 'Personal',
    description: 'Self-care and personal development',
    icon: '👥',
    color: 'purple'
  },
  {
    value: 'creative',
    title: 'Creative',
    description: 'Art, music, and creative projects',
    icon: '🎨',
    color: 'orange'
  }
]

const priorities = ['Low', 'Medium', 'High', 'Urgent']
const frequencies = ['Daily', 'Weekly', 'Bi-weekly', 'Monthly']




const taskTemplates = [
  {
    id: '1',
    title: 'Clean bedroom',
    icon: '🧹',
    color: 'blue',
    reward: 15,
    type: 'chore',
    description: 'Make bed, organize desk, put away clothes'
  },
  {
    id: '2',
    title: 'Complete homework',
    icon: '📘',
    color: 'green',
    reward: 20,
    type: 'educational',
    description: 'Finish all assigned homework and study'
  },
  {
    id: '3',
    title: 'Practice instrument',
    icon: '🎵',
    color: 'purple',
    reward: 10,
    type: 'creative',
    description: 'Practice for 30 minutes'
  },
  {
    id: '4',
    title: 'Exercise/Sports',
    icon: '🏃',
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





// Methods
const getChildName = (id: string): string => {
  const child = children.value.find(child => child.id === id) // ✅ Use .value
  return child ? child.name : 'Unknown'
}

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

const getTaskStatusColor = (count) => {
  if (count >= 5) return '#e53935'; // Red
  if (count >= 3) return '#fb8c00'; // Orange
  return '#43a047'; // Green
}


const getHistoryStatusColor = (status) => {
  switch (status.toLowerCase()) {
    case 'completed': return 'completed'
    case 'pending': return 'pending'
    case 'failed': return 'failed'
    default: return ''
  }
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-IN')
}

// Lifecycle
onMounted(() => {
  // Load children and task data
})


</script>

<style scoped>
.nav-card-body {
    background-color: white;
    border-radius: 20px;
    max-width: 100%;
    height: auto;
    margin-top: 20px;
    margin-bottom: 5px;
    margin-left: 20px;
    margin-right: 20px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

  }
.column {
        border: solid;
  }

  .welcome-text {
  font-size: 25px;
  font-weight: normal;
  }

.add-child-btn {
  font-weight: bold;
  padding: 20px 20px;
  border: 2px solid;
  border-radius: 20px;
  cursor: pointer;
  font-size: 15px;
  background-color: rgb(235, 229, 229);
}
.quick-template {
    background-color: white;
    border-radius: 20px;
    height: auto;
    max-width: 335px;
    margin-top: 10px;
    margin-bottom: 20px;
    margin-left: 5px;
    margin-right: 20px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

}

.create-task {
    background-color: white;
    border-radius: 20px;
    height: auto;
    max-width: 750px;
    margin-top: 10px;
    margin-bottom: 20px;
    margin-left: 20px;
    margin-right: 5px;
    box-shadow: var(--shadow-lg);
    transition: all 0.3s ease;
    border: 2px solid transparent;
    align-items: center;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;

  }

.icon-with-text {
  display: flex;
  gap: 2px;
}
.text-block {
  margin-top: 10px;
}
.logo {
  margin: 10px;
  tab-size: 10px;
}
.title {
  display: flex;
  font-weight: 600;
}
.subtitle {
  font-size: 14px;
  color: gray;
}

.form-container {
  width: 750px;
  margin: auto;
  height: auto;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #fff;
}
.section {
  margin-bottom: 1rem;
}
.section-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
  
}
.field {
  flex: 1;
  min-width: 240px;
  margin-bottom: 0.5rem;
  flex-direction: column;
}
.input-icon {
  position: static;
  height: 30px;
  border-radius: 4px;
}

label {
  margin-bottom: 0.25rem;
  font-weight: lighter;
}
.input-icon .icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
}
.input-icon input,
.input-icon select {
  padding-left: 0;
  width: 100%;
}
textarea,
select
{
  padding: 0.5rem;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}


.radio-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.radio-option {
  display: flex;
  align-items: start;
  gap: 0.5rem;
}
.radio-label {
  display: flex;
  flex-direction: column;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.3rem;
}
.chip {
  background: #e0f0ff;
  color: #007acc;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
}
.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 0.5rem;
  font-weight: normal;
}
.buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;

}
button {
  padding: 1rem 1rem;
  border: none;
  background: #007acc;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 80px;
}
button:disabled {
  background: #999;
}
button[type='button'] {
  background: #ddd;
  color: #333;
}

.snackbar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #198754; /* Bootstrap success color */
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  animation: slide-up 0.3s ease;
}

.snackbar button {
  background: transparent;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.card {
  width: 335px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.1);
  padding: 1rem;
}

.card-title {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.icon.purple {
  color: purple;
  font-size: 1.2rem;
}

.template-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.template-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.template-item:hover {
  background: #f0f0f0;
}

.template-icon {
  font-size: 1.2rem;
}

.template-info {
  display: flex;
  flex-direction: column;
}

.template-title {
  font-weight: 500;
}

.template-subtitle {
  font-size: 0.8rem;
  color: #666;
}

.card {
  background: #fff;
  border-radius: 8px;
  border: 1px solid #ddd;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-weight: bold;
  font-size: 1rem;
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  color: #333;
}

.card-title .icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.6rem;
}

.avatar {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  color: #fff;
  font-size: 0.7rem;
  margin-right: 0.6rem;
}

.name {
  flex: 1;
  margin-left: 0.4rem;
}

.chip {
  padding: 2px 8px;
  border-radius: 12px;
  color: #fff;
  font-size: 0.75rem;
  white-space: nowrap;
}
.card {
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.card-title {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.card-title .icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
  color: green;
}

.alert {
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  background-color: #f5f5f5;
}

.alert.success {
  background-color: #e6f4ea;
  color: #2e7d32;
  border-left: 4px solid #2e7d32;
}

.alert.warning {
  background-color: #fff8e1;
  color: #ff8f00;
  border-left: 4px solid #ff8f00;
}

.alert.error {
  background-color: #fdecea;
  color: #c62828;
  border-left: 4px solid #c62828;
}

.alert.info {
  background-color: #e3f2fd;
  color: #1976d2;
  border-left: 4px solid #1976d2;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  width: 90%;
  max-width: 800px;
  border-radius: 8px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: #f0f0f0;
  font-weight: bold;
}

.modal-header .title {
  flex: 1;
  margin-left: 0.5rem;
}

.modal-header .close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.modal-body {
  padding: 1rem;
}

.data-table {
  width: 50%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.5rem;
  border-bottom: 1px solid #ddd;
}

.avatar {
  display: inline-block;
  width: 24px;
  height: 24px;
  color: white;
  font-size: 0.75rem;
  text-align: center;
  border-radius: 50%;
  margin-right: 6px;
}

.chip.green {
  background: #d4edda;
  color: #155724;
  padding: 2px 6px;
  border-radius: 12px;
  font-size: 0.75rem;
}

</style>