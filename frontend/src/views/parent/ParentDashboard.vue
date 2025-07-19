<template>
<div class="parent-dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="/coin.svg" alt="CoinCraft" class="sidebar-logo" />
        <span class="sidebar-title">CoinCraft</span>
      </div>
      <nav class="sidebar-nav">
        <ul>
          <li :class="{ active: activeNav === 'dashboard' }" @click="setActiveNav('dashboard')">
            <v-icon>mdi-view-dashboard</v-icon>
            <span>Dashboard</span>
          </li>
          <li :class="{ active: activeNav === 'childprogress' }" @click="setActiveNav('childprogress')">
            <v-icon>mdi-account-child</v-icon>
            <span>Child Progress </span>
          </li>
          <li :class="{ active: activeNav === 'tasks' }" @click="setActiveNav('tasks')">
            <v-icon>mdi-format-list-checkbox</v-icon>
            <span>Tasks</span>
          </li>
          <li :class="{ active: activeNav === 'reports' }" @click="setActiveNav('reports')">
            <v-icon>mdi-chart-bar</v-icon>
            <span>Reports</span>
          </li>
          <li :class="{ active: activeNav === 'settings' }" @click="setActiveNav('settings')">
            <v-icon>mdi-cog</v-icon>
            <span>Settings</span>
          </li>
        </ul>
      </nav>

    </aside>
  <v-container fluid class="pa-4">
    <template v-if="currentView === VIEW_DASHBOARD">
    <!-- Header -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <!-- Responsive Card Title -->
            <v-card-title class="pa-4">
              <v-row align="center" class="w-100" no-gutters>
                
                <!-- Avatar and Welcome Text -->
                <v-col cols="12" md="8" class="d-flex align-center mb-3 mb-md-0">
                  <v-avatar color="primary" class="me-3">
                    <v-icon color="white">mdi-account-heart</v-icon>
                  </v-avatar>
                  <div>
                    <h2 class="text-h6 text-md-h5 mb-1">Welcome back, {{ parent.name }}!</h2>
                    <div class="text-subtitle-2 text-md-subtitle-1 text-medium-emphasis">
                      Parent Dashboard
                    </div>
                  </div>
                </v-col>

                <!-- Add Child Button -->
                <v-col cols="12" md="4" class="d-flex justify-end">
                  <v-btn
                    prepend-icon="mdi-plus"
                    color="primary"
                    @click="showAddChildDialog = true"
                    class="w-100 w-md-auto"
                  >
                    Add Child
                  </v-btn>
                </v-col>
              </v-row>
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
                    {{ child.coins }}
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
      <v-col cols="12" md="6">
<v-card class="pa-4">
  <v-card-title class="text-h6 font-weight-bold mb-4">
    <v-icon left color="orange">mdi-flash</v-icon>
    Child List ({{ children.length }} children)
    <v-spacer />
    <v-btn 
      color="primary" 
      variant="outlined" 
      size="small"
      @click="reloadDashboard"
      :loading="loading"
      class="me-2"
    >
      <v-icon left>mdi-refresh</v-icon>
      Reload
    </v-btn>
    <v-btn 
      color="info" 
      variant="text" 
      size="small"
      @click="showDebugInfo"
    >
      <v-icon left>mdi-bug</v-icon>
      Debug
    </v-btn>
  </v-card-title>

  <div style="overflow-x: auto;">
    <table class="child-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Age</th>
          <th>Email</th>
          <th>Username</th>
          <th>Password</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="children.length === 0">
          <tr>
            <td colspan="6" class="text-center py-4 text-medium-emphasis">
              <v-icon class="mb-2">mdi-account-child-outline</v-icon><br>
              No children added yet. Click "Add Child" to start!
            </td>
          </tr>
        </template>
        <template v-else>
          <tr v-for="(child, index) in children" :key="child.id">
            <td>{{ index + 1 }}</td>
            <td>{{ child.name }}</td>
            <td>{{ child.age }}</td>
            <td>{{ child.email || '—' }}</td>
            <td>{{ child.username || `${child.name.toLowerCase().replace(/\s+/g, '')}${child.age}` }}</td>
            <td>{{ child.password || '******' }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</v-card>

      </v-col>
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
import { ref, reactive, computed, onMounted, defineAsyncComponent, watch } from 'vue'
import { useParentStore } from '@/stores/parent'
import type { Parent, Child } from '@/types'




// Store
const parentStore = useParentStore()

// Reactive data
const loading = ref(false)
const showAddChildDialog = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const childFormValid = ref(false)


const activeNav = ref('dashboard');

type ParentViewKey = 'dashboard' | 'assigntask' | 'redemptionsetting' | 'taskhistory'|'childprogress';

const VIEW_DASHBOARD: ParentViewKey = 'dashboard';
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


const asyncViews: Record<Exclude<ParentViewKey, 'dashboard'>, any> = {
  [VIEW_ASSIGN_TASK]: defineAsyncComponent(() => import('./AssignTask.vue')),
  [VIEW_REDEMPTION]: defineAsyncComponent(() => import('./RedemptionSetting.vue')),
  [VIEW_REPORTS]: defineAsyncComponent(() => import('./TaskHistory.vue')),
  [VIEW_CHILD_PROGRESS]: defineAsyncComponent(() => import('./ChildProgress.vue'))
};


// Parent data
const parent = ref<Parent>({
  id: '1',
  name: 'Parent',
  email: 'parent@example.com',
  role: 'parent',
  children: [],
  createdAt: new Date(),
  updatedAt: new Date()
});

// Use store data (defined below with onMounted)

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
    const childData = {
      name: newChild.name,
      age: newChild.age,
      email: newChild.email || undefined,
      avatarColor: newChild.avatarColor
    }
    
    console.log('👶 [DASHBOARD] Adding child with data:', childData)
    const result = await parentStore.addChildAPI(childData)
    
    console.log('✅ [DASHBOARD] Child added successfully:', result)
    
    showAddChildDialog.value = false
    showSuccessSnackbar.value = true
    successMessage.value = `${newChild.name} added successfully! Username: ${result.username}, Password: ${result.password}`
    
    // Force reload dashboard to update child list
    console.log('🔄 [DASHBOARD] Reloading dashboard...')
    await parentStore.loadDashboard()
    console.log('✅ [DASHBOARD] Dashboard reloaded, children count:', parentStore.children.length)
    
    // Reset form
    Object.assign(newChild, {
      name: '',
      age: 8,
      email: '',
      avatarColor: 'blue'
    })
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to add child:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Failed to add child: ${error instanceof Error ? error.message : 'Unknown error'}`
  } finally {
    loading.value = false
  }
}

function generateRandomPassword(length = 10): string {
  const chars =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  let password = ''
  for (let i = 0; i < length; i++) {
    password += chars[Math.floor(Math.random() * chars.length)]
  }
  return password
}

const reloadDashboard = async () => {
  try {
    loading.value = true
    console.log('🔄 [DASHBOARD] Manually reloading dashboard...')
    
    // Force disable demo mode to ensure we get real API data
    localStorage.removeItem('coincraft_demo_mode')
    console.log('🔄 [DASHBOARD] Disabled demo mode to ensure real data')
    
    await parentStore.loadDashboard()
    console.log('✅ [DASHBOARD] Dashboard reloaded successfully. Children count:', parentStore.children.length)
    showSuccessSnackbar.value = true
    successMessage.value = `Dashboard reloaded! Found ${parentStore.children.length} children.`
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to reload:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Failed to reload dashboard: ${error instanceof Error ? error.message : 'Unknown error'}`
  } finally {
    loading.value = false
  }
}

const showDebugInfo = () => {
  console.log('🐛 [DEBUG] Parent store children:', parentStore.children)
  console.log('🐛 [DEBUG] Component children:', children.value)
  
  // Check authentication status
  const token = localStorage.getItem('auth_token')
  const user = localStorage.getItem('coincraft_user')
  const demoMode = localStorage.getItem('coincraft_demo_mode')
  
  console.log('🐛 [DEBUG] Auth status:', {
    token: token ? 'Present' : 'Missing',
    user: user ? JSON.parse(user) : 'Missing',
    demoMode: demoMode === 'true' ? 'ON' : 'OFF'
  })
  
  // Show debug info in UI
  showSuccessSnackbar.value = true
  successMessage.value = `Debug info in console. Children: ${parentStore.children.length}, Auth: ${token ? 'Yes' : 'No'}, Demo: ${demoMode === 'true' ? 'Yes' : 'No'}`
  
  // Force update children array if needed
  if (parentStore.children.length > 0 && children.value.length === 0) {
    console.log('🔧 [DEBUG] Fixing reactivity issue...')
    // Force a reactive update by creating a new array
    parentStore.$patch({ children: [...parentStore.children] })
  }
  
  // If we're in demo mode, disable it and reload
  if (demoMode === 'true') {
    console.log('🔧 [DEBUG] Disabling demo mode and reloading...')
    localStorage.removeItem('coincraft_demo_mode')
    setTimeout(() => reloadDashboard(), 100)
  }
}

// Use store data with computed for reactivity
const children = computed(() => {
  console.log('🔍 [DASHBOARD] Children array in component:', parentStore.children.length, 'items')
  return parentStore.children
})
const familyStats = computed(() => parentStore.familyStats)

// Watch for changes in the children array
watch(() => parentStore.children, (newChildren) => {
  console.log('👀 [DASHBOARD] Children array updated:', newChildren.length, 'items')
}, { deep: true })

// Lifecycle
onMounted(async () => {
  // Load parent dashboard data
  try {
    console.log('🔄 [DASHBOARD] Loading dashboard on mount...')
    
    // Check if we have a valid auth token
    const token = localStorage.getItem('auth_token')
    console.log('🔑 [DASHBOARD] Auth token present:', !!token)
    
    // Ensure we're not in demo mode for real data
    if (localStorage.getItem('coincraft_demo_mode') === 'true') {
      console.log('⚠️ [DASHBOARD] Demo mode detected, disabling for real data')
      localStorage.removeItem('coincraft_demo_mode')
    }
    
    await parentStore.loadDashboard()
    console.log('✅ [DASHBOARD] Dashboard loaded on mount, children count:', parentStore.children.length)
    
    // Force reload if children array is empty but API returned data
    if (parentStore.children.length === 0) {
      console.log('⚠️ [DASHBOARD] Children array is empty, forcing reload...')
      setTimeout(() => reloadDashboard(), 500)
    }
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to load parent dashboard:', error)
  }
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

.table-responsive {
  overflow-x: auto;
}

.child-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.child-table th,
.child-table td {
  padding: 12px 8px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.child-table th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.child-table tbody tr:hover {
  background-color: #f9f9f9;
}

.child-table tbody tr:last-child td {
  border-bottom: none;
}

.table-responsive table {
  width: 100%;
  border-collapse: collapse;
  min-width: 600px;
}

table th, table td {
  padding: 8px 12px;
  border: 1px solid #ddd;
  text-align: left;
}

/* 🔻 MOBILE STYLES */
@media (max-width: 768px) {
  .parent-dashboard-layout {
    flex-direction: column-reverse;
  }

  .sidebar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background-color: white;
    z-index: 100;
    border-top: 1px solid #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .sidebar-header,
  .sidebar-title {
    display: none;
  }

  .sidebar-nav ul {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 0;
    margin: 0;
    gap: 35px;
  }

  .sidebar-nav li {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 6px 0;
    font-size: 20px;
  }

  .sidebar-nav li span {
    display: none !important; /* ✅ Hide text */
  }

  .sidebar-nav li v-icon {
    font-size: 24px;
  }

  .v-container {
    margin-bottom: 60px; /* Prevent overlap */
  }
}
</style>
