<template>
  <div class="parent-dashboard-layout">
    <!-- Sidebar Navigation -->
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
          <li :class="{active: activeNav === 'child-progress'}" @click="setActiveNav('child-progress')">
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

    <!-- Main Content -->
    <main class="dashboard-main">
      <template v-if="currentView === VIEW_DASHBOARD">
        <!-- Top Bar -->
        <header class="dashboard-header">
          <h2>Welcome back, {{ parent.name }} <span class="wave">👋</span></h2>
        </header>
        <!-- Summary Cards -->
        <section class="summary-cards">
          <div class="summary-card">
            <div class="summary-title">Total Children</div>
            <div class="summary-value">{{ parentDashboardChildren.length }}</div>
          </div>
          <div class="summary-card">
            <div class="summary-title">Total Coins Awarded</div>
            <div class="summary-value">{{ totalCoinsAwarded }}</div>
          </div>
          <div class="summary-card">
            <div class="summary-title">Tasks Assigned</div>
            <div class="summary-value">{{ totalTasksAssigned }}</div>
          </div>
          <div class="summary-card">
            <div class="summary-title">Pending Redemptions</div>
            <div class="summary-value">{{ pendingRedemptions }}</div>
          </div>
        </section>
        <!-- Children Grid -->
        <section class="children-section">
          <h3>Your Children</h3>
          <div class="children-grid">
            <div class="child-card" v-for="(child, idx) in parentDashboardChildren" :key="child.id">
              <div class="child-header">
                <div class="avatar" :style="{ backgroundColor: avatarColors[idx % avatarColors.length] }">{{ child.name.charAt(0) }}</div>
                <div class="child-info">
                  <div class="child-name">{{ child.name }}</div>
                  <div class="child-age">{{ child.age }} years old</div>
                </div>
              </div>
              <div class="child-stats">
                <div class="stat">
                  <span class="stat-label">Coins</span>
                  <span class="stat-value coins">{{ child.coins }}</span>
                </div>
                <div class="stat">
                  <span class="stat-label">Tasks Done</span>
                  <span class="stat-value tasks">{{ child.completedTasks || 0 }}</span>
                </div>
              </div>
              <div class="child-progress-section">
                <div class="progress-title">Current Goals</div>
                <div v-if="child.currentGoals.length > 0">
                  <div class="goal-progress-card" v-for="goal in child.currentGoals" :key="goal.id">
                    <div class="goal-header">
                      <span class="goal-icon">{{ goal.icon }}</span>
                      <span class="goal-title">{{ goal.title }}</span>
                      <span class="goal-progress">{{ goal.currentAmount }}/{{ goal.targetAmount }}</span>
                    </div>
                    <div class="progress-bar">
                      <div class="fill" :style="{ width: Math.min((goal.currentAmount/goal.targetAmount)*100, 100)+ '%', backgroundColor: goal.color }"></div>
                    </div>
                  </div>
                </div>
                <div v-else class="no-goals">No active goals</div>
              </div>
              <div class="child-actions">
                <v-btn color="primary" size="small" @click="viewChildProgress(child)">
                  <v-icon start>mdi-eye</v-icon> Details
                </v-btn>
                <v-btn color="secondary" size="small" @click="handleAssignTask">
                  <v-icon start>mdi-plus-box</v-icon> Assign Task
                </v-btn>
              </div>
              <div class="recent-activity-section">
                <div class="activity-title">Recent Activity</div>
                <div v-for="activity in child.recentActivity" :key="activity.id" class="activity-item">
                  <span class="activity-icon">{{ activity.icon }}</span>
                  <span class="activity-title">{{ activity.title }}</span>
                  <span class="activity-time">{{ formatRelativeTime(activity.timestamp) }}</span>
                  <span class="activity-points" v-if="activity.coins">+{{ activity.coins }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>
      </template>
      <template v-else>
        <component :is="asyncViews[currentView as Exclude<ParentViewKey, 'dashboard'>]" />
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineAsyncComponent } from 'vue'
import type { Parent, Child, Goal } from '@/types'
import { useRouter } from 'vue-router'
import { formatDistanceToNow } from 'date-fns'

const router = useRouter();
const activeNav = ref('dashboard');

type ParentViewKey = 'dashboard' | 'addchild' | 'assigntask' | 'redemptionsetting' | 'taskhistory';

const VIEW_DASHBOARD: ParentViewKey = 'dashboard';
const VIEW_ADD_CHILD: ParentViewKey = 'addchild';
const VIEW_ASSIGN_TASK: ParentViewKey = 'assigntask';
const VIEW_REDEMPTION: ParentViewKey = 'redemptionsetting';
const VIEW_REPORTS: ParentViewKey = 'taskhistory';

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
      currentView.value = VIEW_DASHBOARD;
      break;
    case 'child-progress':
      // For now, just show dashboard
      currentView.value = VIEW_DASHBOARD;
      break;
    default:
      currentView.value = VIEW_DASHBOARD;
  }
}

const parent = ref<Parent>({
  id: '1',
  name: 'Priya',
  email: 'priya@example.com',
  role: 'parent',
  children: ['1', '2'],
  createdAt: new Date(),
  updatedAt: new Date()
});

function goToAddChild() { router.push('/addchild'); }
function goToAssignTask() { router.push('/assigntask'); }
function goToRedemption() { router.push('/redeptionsetting'); }
function goToReports() { router.push('/childprogress'); }

// Dashboard-specific child data (not part of Child type)
type DashboardChild = Child & {
  completedTasks: number;
  currentGoals: Goal[];
  recentActivity: { id: string; title: string; icon: string; coins: number; timestamp: Date }[];
};

const parentDashboardChildren = ref<DashboardChild[]>([
  {
    id: '1',
    name: 'Luna',
    email: 'luna@example.com',
    role: 'child',
    age: 9,
    coins: 125,
    level: 1,
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date(),
    completedTasks: 23,
    currentGoals: [
      {
        id: 'g1',
        userId: '1',
        title: 'Magic Hat',
        description: '',
        targetAmount: 50,
        currentAmount: 35,
        icon: '🎩',
        color: 'purple',
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date()
      },
      {
        id: 'g2',
        userId: '1',
        title: 'Art Supplies',
        description: '',
        targetAmount: 30,
        currentAmount: 18,
        icon: '🎨',
        color: 'orange',
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ],
    recentActivity: [
      {
        id: 'a1',
        title: 'Completed homework',
        icon: '✅',
        coins: 15,
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        id: 'a2',
        title: 'Finished "Smart Shopping" module',
        icon: '🎓',
        coins: 25,
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
      }
    ]
  },
  {
    id: '2',
    name: 'Harry',
    email: 'harry@example.com',
    role: 'child',
    age: 12,
    coins: 280,
    level: 1,
    parentId: '1',
    createdAt: new Date(),
    updatedAt: new Date(),
    completedTasks: 24,
    currentGoals: [
      {
        id: 'g3',
        userId: '2',
        title: 'Headphones',
        description: '',
        targetAmount: 120,
        currentAmount: 95,
        icon: '🎧',
        color: 'blue',
        completed: false,
        createdAt: new Date(),
        updatedAt: new Date()
      }
    ],
    recentActivity: [
      {
        id: 'a3',
        title: 'Created budget plan',
        icon: '📝',
        coins: 20,
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
      },
      {
        id: 'a4',
        title: 'Cleaned room',
        icon: '🧹',
        coins: 10,
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
      }
    ]
  }
]);

const totalCoinsAwarded = computed(() => parentDashboardChildren.value.reduce((sum, c) => sum + c.coins, 0));
const totalTasksAssigned = computed(() => parentDashboardChildren.value.reduce((sum, c) => sum + (c.completedTasks || 0), 0));
const pendingRedemptions = computed(() => 2); // Placeholder, replace with real data

function formatRelativeTime(timestamp: Date | string | number): string {
  return formatDistanceToNow(new Date(timestamp), { addSuffix: true })
}
const viewChildProgress = (child: Child) => {
  router.push(`/childprogress/${child.id}`)
}

const avatarColors = ['#9C27B0', '#2196F3', '#FF9800', '#43A047', '#E91E63', '#00BCD4'];

function handleAddChild() {
  setActiveNav('addchild');
}
function handleAssignTask() {
  setActiveNav('tasks');
}
function handleRedemption() {
  setActiveNav('redemptionsetting');
}
function handleReports() {
  setActiveNav('reports');
}

const asyncViews: Record<Exclude<ParentViewKey, 'dashboard'>, any> = {
  [VIEW_ADD_CHILD]: defineAsyncComponent(() => import('./AddChild.vue')),
  [VIEW_ASSIGN_TASK]: defineAsyncComponent(() => import('./AssignTask.vue')),
  [VIEW_REDEMPTION]: defineAsyncComponent(() => import('./RedemptionSetting.vue')),
  [VIEW_REPORTS]: defineAsyncComponent(() => import('./TaskHistory.vue')),
};
</script>

<style scoped>
/* Layout */
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
.dashboard-main {
  flex: 1;
  padding: 32px 48px;
  display: flex;
  flex-direction: column;
}
.dashboard-header {
  margin-bottom: 24px;
}
.dashboard-header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #222;
}
.wave { font-size: 1.5rem; }
.summary-cards {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
}
.summary-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 24px 32px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.summary-title {
  font-size: 1.1rem;
  color: #888;
  margin-bottom: 8px;
}
.summary-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1976d2;
}
.children-section {
  margin-top: 16px;
}
.children-section h3 {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 18px;
  color: #222;
}
.children-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 32px;
}
.child-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 24px 20px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.child-header {
  display: flex;
  align-items: center;
  gap: 16px;
}
.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  color: #fff;
  font-weight: 700;
  font-size: 1.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.child-info {
  display: flex;
  flex-direction: column;
}
.child-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #222;
}
.child-age {
  font-size: 0.98rem;
  color: #888;
}
.child-stats {
  display: flex;
  gap: 32px;
  margin: 8px 0 0 0;
}
.stat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.stat-label {
  font-size: 0.95rem;
  color: #888;
}
.stat-value {
  font-size: 1.3rem;
  font-weight: 700;
}
.stat-value.coins { color: #ff9800; }
.stat-value.tasks { color: #43a047; }
.child-progress-section {
  margin-top: 8px;
}
.progress-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #1976d2;
  margin-bottom: 6px;
}
.goal-progress-card {
  margin-bottom: 8px;
}
.goal-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
}
.goal-icon {
  font-size: 1.2rem;
}
.goal-title {
  font-weight: 600;
  color: #333;
}
.goal-progress {
  margin-left: auto;
  font-size: 0.95rem;
  color: #888;
}
.progress-bar {
  height: 7px;
  background: #eee;
  border-radius: 4px;
  margin-top: 4px;
  overflow: hidden;
}
.progress-bar .fill {
  height: 100%;
  border-radius: 4px;
}
.child-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}
.recent-activity-section {
  margin-top: 10px;
}
.activity-title {
  font-size: 1.02rem;
  font-weight: 600;
  color: #1976d2;
  margin-bottom: 4px;
}
.activity-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.98rem;
  margin-bottom: 4px;
}
.activity-icon {
  font-size: 1.1rem;
}
.activity-time {
  font-size: 0.92rem;
  color: #888;
}
.activity-points {
  font-size: 0.92rem;
  color: #ff9800;
  margin-left: 4px;
}
.no-goals {
  color: #aaa;
  font-size: 0.98rem;
  margin-bottom: 8px;
}
@media (max-width: 900px) {
  .dashboard-main { padding: 24px 8px; }
  .sidebar { width: 60px; padding: 12px 0 0 0; }
  .sidebar-header, .sidebar-title { display: none; }
  .sidebar-nav ul { padding: 0 8px; }
  .sidebar-actions { padding: 8px; }
}
@media (max-width: 600px) {
  .summary-cards { flex-direction: column; gap: 12px; }
  .children-grid { grid-template-columns: 1fr; gap: 16px; }
}
</style>