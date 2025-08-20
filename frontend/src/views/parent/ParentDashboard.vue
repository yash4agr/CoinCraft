<template>
<div class="parent-dashboard-layout">
    <aside class="sidebar">
      <!-- <div class="sidebar-header">
        <img src="/coin.svg" alt="CoinCraft" class="sidebar-logo" />
        <span class="sidebar-title">CoinCraft</span>
      </div> -->
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

      <!-- Logout Section -->
      <div class="sidebar-actions">
        <button class="logout-btn" @click="handleLogout">
          <v-icon color="red">mdi-logout</v-icon>
          <span>Logout</span>
        </button>
      </div>

    </aside>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Top Header with User Info and Logout -->
      <div class="top-header">
        <div class="user-info-header">
          <v-avatar color="primary" size="32" class="me-2">
            <v-icon color="white">mdi-account-heart</v-icon>
          </v-avatar>
          <span class="font-weight-medium">{{ authStore.user?.name || 'Parent' }}</span>
        </div>
        <v-btn
          variant="text"
          color="red"
          prepend-icon="mdi-logout"
          @click="handleLogout"
          class="logout-header-btn"
        >
          Logout
        </v-btn>
      </div>

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
                    <h2 class="text-h6 text-md-h5 mb-1">Welcome back, {{ authStore.user?.name || 'Parent' }}!</h2>
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
            <v-avatar color="primary" class="me-3">
              <span class="text-white font-weight-bold">{{ getChildInitials(child.name) }}</span>
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
            <!-- <v-list density="compact">
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
                  {{ formatRelativeTime(activity.created_at || activity.timestamp) }}
                </v-list-item-subtitle>
                <template #append>
                  <v-chip v-if="activity.coins" size="x-small" color="warning">
                    +{{ activity.coins }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list> -->
             <!-- Last Activity Card -->
              <v-card variant="outlined" class="mb-2 pa-2">
                <div class="d-flex align-center">
                  <v-icon color="info" class="me-2">mdi-clock-outline</v-icon>
                  <v-spacer />
                  <span class="text-caption text-medium-emphasis">
                    {{ child.lastActivity ? new Date(child.lastActivity).toLocaleString() : 'No activity' }}
                  </span>
                </div>
              </v-card>
            <!-- Current Goals -->
            <div v-if="child.currentGoals && child.currentGoals.length > 0" class="mt-3">
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
                    <span class="text-body-2 font-weight-medium">{{ goal.title }}</span>
                    <v-spacer />
                    <span class="text-caption">{{ goal.current_amount }}/{{ goal.target_amount }}</span>
                  </div>
                  <v-progress-linear
                    :model-value="(goal.current_amount / goal.target_amount) * 100"
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
              @click="sendMessage(child as Child)"
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
  <!-- Debug button removed -->
  </v-card-title>

  <div style="overflow-x: auto;">
    <table class="child-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Age</th>
          <th>Email</th>
          <th>Password</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="children.length === 0">
          <tr>
            <td colspan="5" class="text-center py-4 text-medium-emphasis">
              <v-icon class="mb-2">mdi-account-child-outline</v-icon><br>
              No children added yet. Click "Add Child" to start!
            </td>
          </tr>
        </template>
        <template v-else>
          <tr v-for="(child, index) in children" :key="child.id">
            <td>{{ index + 1 }}</td>
            <td>{{ child.name }}</td>
            <td>{{ child.age || '—' }}</td>
            <td>{{ child.email || '—' }}</td>
            <td>{{ child.password || '—' }}</td>
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
    <v-dialog v-model="showAddChildDialog" max-width="600">
      <v-card>
        <v-card-title class="d-flex align-center">
          <v-icon class="me-2" color="primary">mdi-account-plus</v-icon>
          Add New Child
        </v-card-title>
        <v-card-text>
          <v-form ref="childForm" v-model="childFormValid">
            <!-- Child Name Input -->
            <v-text-field
              v-model="newChild.name"
              label="Child's Name"
              :rules="[rules.required]"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              class="mb-3"
              @input="updateGeneratedCredentials"
            />
            
            <!-- Age Input -->
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
            
            <!-- Generated Credentials Preview -->
            <v-card v-if="newChild.name" variant="outlined" class="mb-3 pa-3">
              <v-card-subtitle class="text-subtitle-2 font-weight-medium mb-2">
                <v-icon class="me-1" size="small">mdi-auto-fix</v-icon>
                Auto-Generated Credentials
              </v-card-subtitle>
              
              <v-row>
                <v-col cols="12">
                  <div class="d-flex align-center mb-2">
                    <v-icon class="me-2" size="small" color="primary">mdi-email</v-icon>
                    <span class="text-body-2 font-weight-medium">Email:</span>
                    <v-spacer />
                    <span class="text-body-2 text-primary">{{ generatedEmail }}</span>
                  </div>
                  <div class="d-flex align-center">
                    <v-icon class="me-2" size="small" color="primary">mdi-key</v-icon>
                    <span class="text-body-2 font-weight-medium">Password:</span>
                    <v-spacer />
                    <span class="text-body-2 text-primary font-mono">{{ generatedPassword }}</span>
                    <v-btn 
                      icon="mdi-refresh" 
                      size="x-small" 
                      variant="text"
                      @click="regeneratePassword"
                      class="ml-2"
                    >
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-card>
            
            <!-- Avatar Color Selection -->
            <v-select
              v-model="newChild.avatarColor"
              label="Avatar Color"
              :items="avatarColors"
              prepend-inner-icon="mdi-palette"
              variant="outlined"
            />
            
            <!-- Info Alert -->
            <v-alert 
              type="info" 
              variant="tonal" 
              density="compact"
              class="mt-3"
            >
              <template #prepend>
                <v-icon>mdi-information</v-icon>
              </template>
              Email and password are automatically generated. You can regenerate the password by clicking the refresh button.
            </v-alert>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showAddChildDialog = false">Cancel</v-btn>
          <v-btn
            color="primary"
            @click="addChild"
            :disabled="!childFormValid || !newChild.name"
            :loading="loading"
          >
            <v-icon class="me-1">mdi-plus</v-icon>
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
</div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, defineAsyncComponent, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useParentStore } from '@/stores/parent'
import type { Child } from '@/types'

let pollingInterval: number | undefined = undefined;
const pollFunctions = async () => {
  await Promise.all([
    parentStore.loadDashboard(),
    parentStore.loadTasks(),
    parentStore.loadRedemptions(),
    (parentStore as any).loadPurchaseRequests?.()
  ])
  // Update each child's completedTasks
  const completedCountByChild: Record<string, number> = {};
  parentStore.tasks.forEach(task => {
    if (task.status === 'approved' && task.assigned_to) {
      completedCountByChild[task.assigned_to] = (completedCountByChild[task.assigned_to] || 0) + 1;
    }
  });
  parentStore.children.forEach(child => {
    child.completedTasks = completedCountByChild[child.id] || 0;
  });
  // Update familyStats.completedTasks as sum of all children's completedTasks
  parentStore.familyStats.completedTasks = parentStore.children.reduce((sum, child) => sum + (child.completedTasks || 0), 0);
};


// Stores and router
const router = useRouter()
const authStore = useAuthStore()
const parentStore = useParentStore()

// Reactive data
const localLoading = ref(false)
const showAddChildDialog = ref(false)
const showSuccessSnackbar = ref(false)
const successMessage = ref('')
const childFormValid = ref(false)

// Combine store and local loading states
const loading = computed(() => parentStore.isLoading || localLoading.value)


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


// Parent data now comes from authStore.user instead of hardcoded object

// Use store data (defined below with onMounted)
// // Family stats
// const familyStats = ref<FamilyStats>({
//   totalChildren: 2,
//   totalCoinsEarned: 485,
//   completedTasks: 47,
//   activeGoals: 5
// })

// // Children data
// const children = ref<Child[]>([
//   {
//     id: '1',
//     name: 'Luna',
//     age: 9,
//     email: 'luna@example.com',
//     password: generateRandomPassword(6),
//     initials: 'L',
//     avatarColor: 'purple',
//     coins: 125,
//     completedTasks: 23,
//     currentGoals: [
//       {
//         id: '1',
//         name: 'Magic Hat',
//         target: 50,
//         saved: 35,
//         icon: 'mdi-hat-fedora',
//         color: 'purple'
//       },
//       {
//         id: '2',
//         name: 'Art Supplies',
//         target: 30,
//         saved: 18,
//         icon: 'mdi-palette',
//         color: 'orange'
//       }
//     ],
//     recentActivity: [
//       {
//         id: '1',
//         title: 'Completed homework',
//         icon: 'mdi-check-circle',
//         color: 'success',
//         coins: 15,
//         timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
//       },
//       {
//         id: '2',
//         title: 'Finished "Smart Shopping" module',
//         icon: 'mdi-graduation-cap',
//         color: 'info',
//         coins: 25,
//         timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
//       }
//     ],
//     parentId: '1',
//     createdAt: new Date(),
//     updatedAt: new Date()
//   },
//   {
//     id: '2',
//     name: 'Harry',
//     age: 12,
//     email: 'harry@example.com',
//     password: generateRandomPassword(6),
//     initials: 'H',
//     avatarColor: 'blue',
//     coinBalance: 280,
//     completedTasks: 24,
//     currentGoals: [
//       {
//         id: '3',
//         name: 'Headphones',
//         target: 120,
//         saved: 95,
//         icon: 'mdi-headphones',
//         color: 'blue'
//       }
//     ],
//     recentActivity: [
//       {
//         id: '3',
//         title: 'Created budget plan',
//         icon: 'mdi-calculator',
//         color: 'primary',
//         coins: 20,
//         timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
//       },
//       {
//         id: '4',
//         title: 'Cleaned room',
//         icon: 'mdi-broom',
//         color: 'success',
//         coins: 10,
//         timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
//       }
//     ],
//     parentId: '1',
//     createdAt: new Date(),
//     updatedAt: new Date()
//   }
// ])

// Alerts and notifications - computed from real data
const alerts = computed(() => {
  const alertsList: Array<{
    id: string;
    type: 'info' | 'success' | 'warning' | 'error';
    title: string;
    message: string;
  }> = []

  // Add alerts for pending tasks needing approval
  const completedTasks = parentStore.tasks.filter(task => task.status === 'completed')
  if (completedTasks.length > 0) {
    alertsList.push({
      id: 'pending-tasks',
      type: 'info',
      title: 'Tasks Need Approval',
      message: `${completedTasks.length} completed task${completedTasks.length > 1 ? 's' : ''} waiting for approval`
    })
  }

  // Add alerts for pending redemptions
  const pendingRedemptionsCount = parentStore.pendingRedemptions.length
  if (pendingRedemptionsCount > 0) {
    alertsList.push({
      id: 'pending-redemptions',
      type: 'warning',
      title: 'Redemption Requests',
      message: `${pendingRedemptionsCount} redemption request${pendingRedemptionsCount > 1 ? 's' : ''} need your approval`
    })
  }

  // Add alerts for purchase requests
  const purchasePending = (parentStore as any).purchaseRequests?.filter((r: any) => r.status === 'pending')?.length || 0
  if (purchasePending > 0) {
    alertsList.push({
      id: 'pending-purchases',
      type: 'warning',
      title: 'Shop Purchases',
      message: `${purchasePending} purchase request${purchasePending > 1 ? 's' : ''} need your approval`
    })
  }

  // Add success alert for new children
  if (parentStore.children.length > 0) {
    alertsList.push({
      id: 'children-active',
      type: 'success',
      title: 'Family Active',
      message: `${parentStore.children.length} child${parentStore.children.length > 1 ? 'ren' : ''} actively earning coins`
    })
  }

  // Add alert for completed goals
  const completedGoalsCount = (parentStore as any).allChildrenGoals?.filter((g: any) => g.is_completed)?.length || 0
  if (completedGoalsCount > 0) {
    alertsList.push({
      id: 'goals-completed',
      type: 'success',
      title: 'Goals Achieved',
      message: `${completedGoalsCount} goal${completedGoalsCount > 1 ? 's' : ''} completed by children! 🎉`
    })
  }

  return alertsList
})

const pendingApprovals = computed(() => {
  const approvals: Array<{
    id: string;
    title: string;
    child: string;
    type: string;
  }> = []

  // Add completed tasks needing approval
  parentStore.tasks
    .filter(task => task.status === 'completed')
    .forEach(task => {
      const childName = parentStore.getChildName(task.assigned_to)
      approvals.push({
        id: task.id,
        title: `Task: ${task.title}`,
        child: childName,
        type: 'task'
      })
    })

  // Add pending purchase requests
  ;((parentStore as any).purchaseRequests || [])
    .filter((req: any) => req.status === 'pending')
    .forEach((req: any) => {
      const childName = parentStore.getChildName(req.user_id)
      approvals.push({
        id: req.id,
        title: `Buy: ${(req.item_info?.name || req.item?.name) || 'Item'} (${req.price} coins)`,
        child: childName,
        type: 'purchase'
      })
    })

  // Add pending redemption requests
  parentStore.pendingRedemptions.forEach(redemption => {
    const childName = parentStore.getChildName(redemption.user_id)
    approvals.push({
      id: redemption.id,
      title: `Redeem ${redemption.coins_amount} coins`,
      child: childName,
      type: 'redemption'
    })
  })

  return approvals
})

// New child form with auto-generated credentials
const newChild = reactive({
  name: '',
  age: 8,
  email: '',
  avatarColor: 'blue'
})

// Auto-generated credentials for preview
const generatedPassword = ref('')
const generatedEmail = computed(() => {
  if (!newChild.name) return ''
  const parentName = (authStore.user?.name || 'parent').toLowerCase().replace(/\s+/g, '')
  const childName = newChild.name.toLowerCase().replace(/\s+/g, '')
  return `${parentName}+${childName}@cc.com`
})

// Static data
const avatarColors = ['blue', 'green', 'purple', 'orange', 'red', 'teal', 'pink', 'indigo']

// Validation rules
const rules = {
  required: (value: any) => !!value || 'This field is required',
  ageRange: (value: number) => (value >= 3 && value <= 18) || 'Age must be between 3 and 18'
}

// Methods
const updateGeneratedCredentials = () => {
  generatedPassword.value = generateRandomPassword()
}

const regeneratePassword = () => {
  generatedPassword.value = generateRandomPassword()
}


const sendMessage = (child: Child) => {
  showSuccessSnackbar.value = true
  successMessage.value = `Message sent to ${child.name}`
}

// Helper function to get child initials from name
const getChildInitials = (name: string) => {
  if (!name) return '?'
  return name.split(' ').map(n => n.charAt(0)).join('').toUpperCase().slice(0, 2)
}

const approveItem = async (item: any) => {
  localLoading.value = true
  try {
    if (item.type === 'task') {
      const ok = await parentStore.approveTask(item.id)
      if (!ok) throw new Error('Approve task failed')
    } else if (item.type === 'redemption') {
      const ok = await parentStore.approveRedemption(item.id)
      if (!ok) throw new Error('Approve redemption failed')
    } else if (item.type === 'purchase') {
      const ok = await (parentStore as any).approvePurchase?.(item.id)
      if (!ok) throw new Error('Approve purchase failed')
    }

    // Refresh store data so computed pendingApprovals updates
    await Promise.all([
      parentStore.loadTasks(),
      parentStore.loadRedemptions(),
      (parentStore as any).loadPurchaseRequests?.(),
      parentStore.loadDashboard(),
    ])

    showSuccessSnackbar.value = true
    successMessage.value = `${item.title} approved!`
  } catch (error) {
    console.error('Failed to approve item:', error)
  } finally {
    localLoading.value = false
  }
}

const rejectItem = async (item: any) => {
  localLoading.value = true
  try {
    if (item.type === 'task') {
      const ok = await parentStore.rejectTask(item.id)
      if (!ok) throw new Error('Reject task failed')
    } else if (item.type === 'redemption') {
      const ok = await parentStore.rejectRedemption(item.id)
      if (!ok) throw new Error('Reject redemption failed')
    } else if (item.type === 'purchase') {
      const ok = await (parentStore as any).rejectPurchase?.(item.id)
      if (!ok) throw new Error('Reject purchase failed')
    }

    await Promise.all([
      parentStore.loadTasks(),
      parentStore.loadRedemptions(),
      (parentStore as any).loadPurchaseRequests?.(),
      parentStore.loadDashboard(),
    ])

    showSuccessSnackbar.value = true
    successMessage.value = `${item.title} rejected.`
  } catch (error) {
    console.error('Failed to reject item:', error)
  } finally {
    localLoading.value = false
  }
}

const addChild = async () => {
  if (!childFormValid.value) return
  
  try {
    // Generate password
    const password = generatedPassword.value || generateRandomPassword()
    
    // Generate email using parent name + child name + @cc.com
    const parentName = (authStore.user?.name || 'parent').toLowerCase().replace(/\s+/g, '')
    const childName = newChild.name.toLowerCase().replace(/\s+/g, '')
  const generatedEmail = `${parentName}+${childName}@cc.com`
    
    const childData = {
      name: newChild.name,
      email: newChild.email || generatedEmail,
      password,
      age: newChild.age,
      role: newChild.age < 13 ? 'younger_child' as const : 'older_child' as const
    }
    
    console.log('👶 [DASHBOARD] Adding child with data:', childData)
    const result = await parentStore.createChild(childData)
    
    if (result) {
      console.log('✅ [DASHBOARD] Child added successfully:', result)
      
      showAddChildDialog.value = false
      showSuccessSnackbar.value = true
      successMessage.value = `${newChild.name} added successfully! Password: ${password}`
      
      // Force reload all data to update child list and other data
      console.log('🔄 [DASHBOARD] Reloading all data...')
      await reloadDashboard()
      console.log('✅ [DASHBOARD] All data reloaded, children count:', parentStore.children.length)
      
      // Reset form
      Object.assign(newChild, {
        name: '',
        age: 8,
        email: '',
        avatarColor: 'blue'
      })
    }
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to add child:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Failed to add child: ${error instanceof Error ? error.message : 'Unknown error'}`
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

// Logout handler
const handleLogout = async () => {
  try {
    await authStore.logout()
    router.push('/')
  } catch (error) {
    console.error('Logout failed:', error)
    // Even if logout fails, redirect to home page
    router.push('/')
  }
}

const reloadDashboard = async () => {
  try {
    localLoading.value = true
    console.log('🔄 [DASHBOARD] Manually reloading dashboard...')
    
    // Force disable demo mode to ensure we get real API data
    localStorage.removeItem('coincraft_demo_mode')
    console.log('🔄 [DASHBOARD] Disabled demo mode to ensure real data')
    
    // Reload all parent data
    await Promise.all([
      parentStore.loadDashboard(),
      parentStore.loadTasks(),
      parentStore.loadRedemptions(),
      (parentStore as any).loadPurchaseRequests?.()
    ])
    
    console.log('✅ [DASHBOARD] All data reloaded successfully:', {
      children: parentStore.children.length,
      tasks: parentStore.tasks.length,
      redemptions: parentStore.redemptionRequests.length
    })
    
    showSuccessSnackbar.value = true
    successMessage.value = `Dashboard reloaded! Found ${parentStore.children.length} children, ${parentStore.tasks.length} tasks, ${parentStore.redemptionRequests.length} redemptions.`
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to reload:', error)
    showSuccessSnackbar.value = true
    successMessage.value = `Failed to reload dashboard: ${error instanceof Error ? error.message : 'Unknown error'}`
  } finally {
    localLoading.value = false
  }
}

// Debug info function removed

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
    
    // Load all parent-related data
    await Promise.all([
      parentStore.loadDashboard(),
      parentStore.loadTasks(),
      parentStore.loadRedemptions(),
      (parentStore as any).loadPurchaseRequests?.()
    ])
    
    console.log('✅ [DASHBOARD] All data loaded on mount:', {
      children: parentStore.children.length,
      tasks: parentStore.tasks.length,
      redemptions: parentStore.redemptionRequests.length
    })
    
    // Force reload if children array is empty but API returned data
    if (parentStore.children.length === 0) {
      console.log('⚠️ [DASHBOARD] Children array is empty, forcing reload...')
      setTimeout(() => reloadDashboard(), 500)
    }
    // Set completedTasks for each child after initial load
    const completedCountByChild: Record<string, number> = {}
    parentStore.tasks.forEach(task => {
      if (task.status === 'approved' && task.assigned_to) {
        completedCountByChild[task.assigned_to] = (completedCountByChild[task.assigned_to] || 0) + 1
      }
    })
    parentStore.children.forEach(child => {
      child.completedTasks = completedCountByChild[child.id] || 0
    })
    // Update familyStats.completedTasks as sum of all children's completedTasks
    parentStore.familyStats.completedTasks = parentStore.children.reduce((sum, child) => sum + (child.completedTasks || 0), 0)
    pollingInterval =  window.setInterval(pollFunctions, 10000);
  } catch (error) {
    console.error('❌ [DASHBOARD] Failed to load parent dashboard:', error)
  }
})
watch(parentStore.tasks, (newTasks,oldTasks) => {

  // Build maps of completed tasks by assigned_to for old and new
  const oldCompleted: Record<string, number> = {}
  const newCompleted: Record<string, number> = {}

  if (Array.isArray(oldTasks)) {
    oldTasks.forEach(task => {
      if (task.status === 'approved' && task.assigned_to) {
        oldCompleted[task.assigned_to] = (oldCompleted[task.assigned_to] || 0) + 1
      }
    })
  }
  newTasks.forEach(task => {
    if (task.status === 'completed' && task.assigned_to) {
      newCompleted[task.assigned_to] = (newCompleted[task.assigned_to] || 0) + 1
    }
  })

  // Update only children whose completed count increased
  parentStore.children.forEach(child => {
    const oldCount = oldCompleted[child.id] || 0
    const newCount = newCompleted[child.id] || 0
    if (newCount !== oldCount) {
      child.completedTasks = newCount
    }
  })
    // Update familyStats.completedTasks as sum of all children's completedTasks
    parentStore.familyStats.completedTasks = parentStore.children.reduce((sum, child) => sum + (child.completedTasks || 0), 0)
}, { deep: true })

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval);
  }
});
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

.logout-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  font-size: 1.08rem;
  color: #d32f2f;
  cursor: pointer;
  border: none;
  background: none;
  border-radius: 8px;
  transition: background 0.2s;
  width: 100%;
  text-align: left;
}

.logout-btn:hover {
  background: #ffebee;
  color: #c62828;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-header {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 64px;
}

.user-info-header {
  display: flex;
  align-items: center;
}

.logout-header-btn {
  text-transform: none;
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
  .sidebar-title,
  .sidebar-actions {
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

  .top-header {
    padding: 8px 16px;
    min-height: 56px;
  }

  .user-info-header span {
    font-size: 0.9rem;
  }

  .logout-header-btn {
    font-size: 0.8rem;
    min-width: auto;
    padding: 4px 8px;
  }
}
</style>
