<template>
<div class="parent-dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="/coin.svg" alt="CoinCraft" class="sidebar-logo" />
        <span class="sidebar-title">CoinCraft</span>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li :class="{active: activeNav === 'dashboard'}" @click="setActiveNav('dashboard')">
            <v-icon>mdi-view-dashboard</v-icon> Dashboard
          </li>
          <li :class="{active: activeNav === 'childprogress'}" @click="setActiveNav('childprogress')">
            <v-icon>mdi-account-child</v-icon> Child Progress
          </li>
          <li :class="{active: activeNav === 'tasks'}" @click="setActiveNav('tasks')">
            <v-icon>mdi-format-list-checkbox</v-icon> Tasks
          </li>
          <li :class="{active: activeNav === 'reports'}" @click="setActiveNav('reports')">
            <v-icon>mdi-chart-bar</v-icon> Reports
          </li>
          <li :class="{active: activeNav === 'settings'}" @click="setActiveNav('settings')">
            <v-icon>mdi-cog</v-icon> Settings
          </li>
        </ul>
      </nav>
      <div class="sidebar-actions">
        <v-btn color="primary" block class="mb-2" @click="handleAddChild">
          <v-icon start>mdi-account-plus</v-icon> Add Child
        </v-btn>
        <v-btn color="secondary" block class="mb-2" @click="handleAssignTask">
          <v-icon start>mdi-plus-box</v-icon> Assign Task
        </v-btn>
        <v-btn color="success" block class="mb-2" @click="handleRedemption">
          <v-icon start>mdi-gift</v-icon> Redemption
        </v-btn>
        <v-btn color="info" block @click="handleReports">
          <v-icon start>mdi-chart-bar</v-icon> Reports
        </v-btn>
      </div>
    </aside>
  <v-container fluid class="pa-4">
    <template v-if="currentView === VIEW_DASHBOARD">
    <!-- Header -->
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-avatar color="primary" class="me-3">
              <v-icon color="white">mdi-account-heart</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-h5">Welcome back, {{ parent.name }}!</h2>
              <div class="text-subtitle-1 text-medium-emphasis">
                Family Dashboard
              </div>
            </div>
            <v-spacer />
            <v-btn
              prepend-icon="mdi-plus"
              color="primary"
              @click="showAddChildDialog = true"
            >
              Add Child
            </v-btn>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Family Overview Stats -->
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon color="primary" size="48" class="me-3">mdi-account-group</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ familyStats.totalChildren }}</div>
                <div class="text-subtitle-2 text-medium-emphasis">Children</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon color="warning" size="48" class="me-3">mdi-star</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ familyStats.totalCoinsEarned }}</div>
                <div class="text-subtitle-2 text-medium-emphasis">Coins Earned</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon color="success" size="48" class="me-3">mdi-check-circle</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ familyStats.completedTasks }}</div>
                <div class="text-subtitle-2 text-medium-emphasis">Tasks Completed</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" sm="6" md="3">
        <v-card>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon color="purple" size="48" class="me-3">mdi-target</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ familyStats.activeGoals }}</div>
                <div class="text-subtitle-2 text-medium-emphasis">Active Goals</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Children Overview -->
    <v-row>
      <v-col
        v-for="child in children"
        :key="child.id"
        cols="12" md="6" lg="4"
      >
        <v-card class="h-100">
          <!-- Child Header -->
          <v-card-title class="d-flex align-center">
            <v-avatar :color="child.avatarColor" class="me-3">
              <span class="text-white font-weight-bold">{{ child.initials }}</span>
            </v-avatar>
            <div>
              <div class="font-weight-bold">{{ child.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ child.age }} years old</div>
            </div>
            <v-spacer />
            
          </v-card-title>

          <!-- Child Stats -->
          <v-card-text>
            <v-row class="mb-3">
              <v-col cols="6">
                <div class="text-center">
                  <div class="text-h6 font-weight-bold text-warning">
                    {{ child.coinBalance }}
                  </div>
                  <div class="text-caption text-medium-emphasis">Coins</div>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="text-center">
                  <div class="text-h6 font-weight-bold text-success">
                    {{ child.completedTasks }}
                  </div>
                  <div class="text-caption text-medium-emphasis">Tasks Done</div>
                </div>
              </v-col>
            </v-row>

            <!-- Recent Activity -->
            <div class="text-subtitle-2 font-weight-medium mb-2">Recent Activity</div>
            <v-list density="compact">
              <v-list-item
                v-for="activity in child.recentActivity"
                :key="activity.id"
                density="compact"
              >
                <template #prepend>
                  <v-icon :color="activity.color" size="small">{{ activity.icon }}</v-icon>
                </template>
                <v-list-item-title class="text-body-2">{{ activity.title }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption">
                  {{ formatRelativeTime(activity.timestamp) }}
                </v-list-item-subtitle>
                <template #append>
                  <v-chip v-if="activity.coins" size="x-small" color="warning">
                    +{{ activity.coins }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>

            <!-- Current Goals -->
            <div v-if="child.currentGoals.length > 0" class="mt-3">
              <div class="text-subtitle-2 font-weight-medium mb-2">Current Goals</div>
              <v-card
                v-for="goal in child.currentGoals"
                :key="goal.id"
                variant="outlined"
                class="mb-2"
              >
                <v-card-text class="py-2">
                  <div class="d-flex align-center mb-1">
                    <v-icon :color="goal.color" size="small" class="me-1">{{ goal.icon }}</v-icon>
                    <span class="text-body-2 font-weight-medium">{{ goal.name }}</span>
                    <v-spacer />
                    <span class="text-caption">{{ goal.saved }}/{{ goal.target }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="(goal.saved / goal.target) * 100"
                    :color="goal.color"
                    height="4"
                    rounded
                  />
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>

          <!-- Child Actions -->
          <v-card-actions>
            <v-btn
              size="small"
              variant="tonal"
              prepend-icon="mdi-message"
              @click="sendMessage(child)"
            >
              Message
            </v-btn>
            <v-spacer />
            <v-btn
              size="small"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-eye"
              class="{active: activeNav === 'childprogress'}" @click="setActiveNav('childprogress')"
            >
              Details
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>  

    <!-- Quick Actions & Alerts -->
    <v-row>
      <!-- Quick Actions -->
      

      <!-- Alerts & Notifications -->
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="d-flex align-center">
            <v-icon class="me-2" color="warning">mdi-bell</v-icon>
            Alerts & Notifications
          </v-card-title>
          <v-card-text>
            <v-alert
              v-for="alert in alerts"
              :key="alert.id"
              :type="alert.type"
              variant="tonal"
              density="compact"
              class="mb-2"
            >
              <div class="font-weight-medium">{{ alert.title }}</div>
              <div class="text-caption">{{ alert.message }}</div>
            </v-alert>

            <v-divider class="my-3" />

            <div class="text-subtitle-2 font-weight-medium mb-2">Pending Approvals</div>
            <v-list v-if="pendingApprovals.length > 0" density="compact">
              <v-list-item
                v-for="approval in pendingApprovals"
                :key="approval.id"
              >
                <v-list-item-title class="text-body-2">{{ approval.title }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption">{{ approval.child }}</v-list-item-subtitle>
                <template #append>
                  <div class="d-flex gap-1">
                    <v-btn
                      icon="mdi-check"
                      size="x-small"
                      color="success"
                      variant="tonal"
                      @click="approveItem(approval)"
                    />
                    <v-btn
                      icon="mdi-close"
                      size="x-small"
                      color="error"
                      variant="tonal"
                      @click="rejectItem(approval)"
                    />
                  </div>
                </template>
              </v-list-item>
            </v-list>
            <div v-else class="text-center text-medium-emphasis py-2">
              No pending approvals
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Add Child Dialog -->
    <v-dialog v-model="showAddChildDialog" max-width="500">
      <v-card>
        <v-card-title>Add New Child</v-card-title>
        <v-card-text>
          <v-form ref="childForm" v-model="childFormValid">
            <v-text-field
              v-model="newChild.name"
              label="Child's Name"
              :rules="[rules.required]"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              class="mb-3"
            />
            
            <v-text-field
              v-model.number="newChild.age"
              label="Age"
              type="number"
              :rules="[rules.required, rules.ageRange]"
              prepend-inner-icon="mdi-cake"
              variant="outlined"
              min="3"
              max="18"
              class="mb-3"
            />
            
            <v-text-field
              v-model="newChild.email"
              label="Email (Optional)"
              type="email"
              prepend-inner-icon="mdi-email"
              variant="outlined"
              class="mb-3"
            />
            
            <v-select
              v-model="newChild.avatarColor"
              label="Avatar Color"
              :items="avatarColors"
              prepend-inner-icon="mdi-palette"
              variant="outlined"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showAddChildDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="addChild"
            :disabled="!childFormValid"
          >
            Add Child
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Loading Overlay -->
    <v-overlay v-model="loading" class="align-center justify-center">
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      />
    </v-overlay>

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
    </template>
      <template v-else>
        <component :is="asyncViews[currentView as Exclude<ParentViewKey, 'dashboard'>]" />
      </template>
  </v-container>
</div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, defineAsyncComponent } from 'vue'
import { useRouter } from 'vue-router'
import type { Parent, Child, FamilyStats } from '@/types'




// Reactive data
const loading = ref(false)
const showAddChildDialog = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const childFormValid = ref(false)

const router = useRouter();
const activeNav = ref('dashboard');

type ParentViewKey = 'dashboard' | 'addchild' | 'assigntask' | 'redemptionsetting' | 'taskhistory'|'childprogress';

const VIEW_DASHBOARD: ParentViewKey = 'dashboard';
const VIEW_ADD_CHILD: ParentViewKey = 'addchild';
const VIEW_ASSIGN_TASK: ParentViewKey = 'assigntask';
const VIEW_REDEMPTION: ParentViewKey = 'redemptionsetting';
const VIEW_REPORTS: ParentViewKey = 'taskhistory';
const VIEW_CHILD_PROGRESS: ParentViewKey = 'childprogress';

const currentView = ref<ParentViewKey>(VIEW_DASHBOARD);

function setActiveNav(nav: string) {
  activeNav.value = nav;
  switch (nav) {
    case 'dashboard':
      currentView.value = VIEW_DASHBOARD;
      break;
    case 'addchild':
      currentView.value = VIEW_ADD_CHILD;
      break;
    case 'tasks':
      currentView.value = VIEW_ASSIGN_TASK;
      break;
    case 'reports':
      currentView.value = VIEW_REPORTS;
      break;
    case 'settings':
      // For now, just show dashboard
      currentView.value = VIEW_REDEMPTION;
      break;
    case 'childprogress':
      // For now, just show dashboard
      currentView.value = VIEW_CHILD_PROGRESS;
      break;
    default:
      currentView.value = VIEW_DASHBOARD;
  }
}

function handleAddChild() {
  setActiveNav('addchild');
}
function handleAssignTask() {
  setActiveNav('tasks');
}
function handleRedemption() {
  setActiveNav('settings');
}
function handleReports() {
  setActiveNav('reports');
}
function handleChildProgress() {
  setActiveNav('childprogress');
}

const asyncViews: Record<Exclude<ParentViewKey, 'dashboard'>, any> = {
  [VIEW_ADD_CHILD]: defineAsyncComponent(() => import('./AddChild.vue')),
  [VIEW_ASSIGN_TASK]: defineAsyncComponent(() => import('./AssignTask.vue')),
  [VIEW_REDEMPTION]: defineAsyncComponent(() => import('./RedemptionSetting.vue')),
  [VIEW_REPORTS]: defineAsyncComponent(() => import('./TaskHistory.vue')),
  [VIEW_CHILD_PROGRESS]: defineAsyncComponent(() => import('./ChildProgress.vue'))
};

const viewChildProgress = (child: Child) => {
  router.push(`/childprogress/${child.id}`)
}

// Parent data
const parent = ref<Parent>({
  id: '1',
  name: 'Priya',
  email: 'priya@example.com',
  role: 'parent',
  children: ['1', '2'],
  createdAt: new Date(),
  updatedAt: new Date()
});

// Family stats
const familyStats = ref<FamilyStats>({
  totalChildren: 2,
  totalCoinsEarned: 485,
  completedTasks: 47,
  activeGoals: 5
})

// Children data
const children = ref<Child[]>([
  {
    id: '1',
    name: 'Luna',
    age: 9,
    email: 'luna@example.com',
    initials: 'L',
    avatarColor: 'purple',
    coinBalance: 125,
    completedTasks: 23,
    currentGoals: [
      {
        id: '1',
        name: 'Magic Hat',
        target: 50,
        saved: 35,
        icon: 'mdi-hat-fedora',
        color: 'purple'
      },
      {
        id: '2',
        name: 'Art Supplies',
        target: 30,
        saved: 18,
        icon: 'mdi-palette',
        color: 'orange'
      }
    ],
    recentActivity: [
      {
        id: '1',
        title: 'Completed homework',
        icon: 'mdi-check-circle',
        color: 'success',
        coins: 15,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        id: '2',
        title: 'Finished "Smart Shopping" module',
        icon: 'mdi-graduation-cap',
        color: 'info',
        coins: 25,
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      }
    ],
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date()
  },
  {
    id: '2',
    name: 'Harry',
    age: 12,
    email: 'harry@example.com',
    initials: 'H',
    avatarColor: 'blue',
    coinBalance: 280,
    completedTasks: 24,
    currentGoals: [
      {
        id: '3',
        name: 'Headphones',
        target: 120,
        saved: 95,
        icon: 'mdi-headphones',
        color: 'blue'
      }
    ],
    recentActivity: [
      {
        id: '3',
        title: 'Created budget plan',
        icon: 'mdi-calculator',
        color: 'primary',
        coins: 20,
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
      },
      {
        id: '4',
        title: 'Cleaned room',
        icon: 'mdi-broom',
        color: 'success',
        coins: 10,
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      }
    ],
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date()
  }
])

// Alerts and notifications
const alerts = ref([
  {
    id: '1',
    type: 'info',
    title: 'New Achievement',
    message: 'Luna earned a 7-day activity streak!'
  },
  {
    id: '2',
    type: 'warning',
    title: 'Goal Almost Reached',
    message: 'Harry is 25 coins away from his headphones goal'
  },
  {
    id: '3',
    type: 'success',
    title: 'Task Completed',
    message: 'All homework tasks completed this week'
  }
])

const pendingApprovals = ref([
  {
    id: '1',
    title: 'Redeem 30 coins for toy',
    child: 'Luna',
    type: 'redemption'
  },
  {
    id: '2',
    title: 'Mark task as complete',
    child: 'Harry',
    type: 'task'
  }
])

// New child form
const newChild = reactive({
  name: '',
  age: 8,
  email: '',
  avatarColor: 'blue'
})

// Static data
const avatarColors = ['blue', 'green', 'purple', 'orange', 'red', 'teal', 'pink', 'indigo']

// Validation rules
const rules = {
  required: (value: any) => !!value || 'This field is required',
  ageRange: (value: number) => (value >= 3 && value <= 18) || 'Age must be between 3 and 18'
}

// Methods
const formatRelativeTime = (date: Date) => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`
  return 'Just now'
}

const sendMessage = (child: Child) => {
  showSuccessSnackbar.value = true
  successMessage.value = `Message sent to ${child.name}`
}

const approveItem = async (item: any) => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const index = pendingApprovals.value.findIndex(a => a.id === item.id)
    if (index > -1) {
      pendingApprovals.value.splice(index, 1)
    }
    
    showSuccessSnackbar.value = true
    successMessage.value = `${item.title} approved!`
  } catch (error) {
    console.error('Failed to approve item:', error)
  } finally {
    loading.value = false
  }
}

const rejectItem = async (item: any) => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const index = pendingApprovals.value.findIndex(a => a.id === item.id)
    if (index > -1) {
      pendingApprovals.value.splice(index, 1)
    }
    
    showSuccessSnackbar.value = true
    successMessage.value = `${item.title} rejected.`
  } catch (error) {
    console.error('Failed to reject item:', error)
  } finally {
    loading.value = false
  }
}

const addChild = async () => {
  if (!childFormValid.value) return
  
  loading.value = true
  try {
    // Simulate adding child
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const child: Child = {
      id: Date.now().toString(),
      name: newChild.name,
      age: newChild.age,
      email: newChild.email || undefined,
      initials: newChild.name.charAt(0).toUpperCase(),
      avatarColor: newChild.avatarColor,
      coinBalance: 0,
      completedTasks: 0,
      currentGoals: [],
      recentActivity: [],
      parentId: parent.value.id,
      createdAt: new Date(),
      updatedAt: new Date()
    }
    
    children.value.push(child)
    familyStats.value.totalChildren++
    
    showAddChildDialog.value = false
    showSuccessSnackbar.value = true
    successMessage.value = `${newChild.name} added successfully!`
    
    // Reset form
    Object.assign(newChild, {
      name: '',
      age: 8,
      email: '',
      avatarColor: 'blue'
    })
  } catch (error) {
    console.error('Failed to add child:', error)
  } finally {
    loading.value = false
  }
}



// Lifecycle
onMounted(() => {
  // Load parent dashboard data
})
</script>

<style scoped>
.parent-dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f8f9fb;
}
.sidebar {
  width: 260px;
  background: #fff;
  box-shadow: 2px 0 8px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  padding: 24px 0 0 0;
}
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px 24px 24px;
}
.sidebar-logo {
  width: 36px;
  height: 36px;
}
.sidebar-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ff9800;
}
.sidebar-nav ul {
  list-style: none;
  padding: 0 24px;
  margin: 0;
}
.sidebar-nav li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  font-size: 1.08rem;
  color: #333;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.2s;
}
.sidebar-nav li.active, .sidebar-nav li:hover {
  background: #f5f5f5;
  color: #1976d2;
}
.sidebar-actions {
  margin-top: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

</style>
