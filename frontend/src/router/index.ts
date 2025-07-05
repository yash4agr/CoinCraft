import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
import ParentDashboard from '@/views/ParentDashboard.vue'
import AssignTask from '../views/AssignTask.vue'
import RedemptionSetting from '../views/RedemptionSetting.vue'
import TaskHistory from '../views/TaskHistory.vue'
import AddChild from '../views/AddChild.vue'
import ChildProgress from '../views/ChildProgress.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/parentdashboard',
    name: 'ParentDashboard',
    component: ParentDashboard
  },
  {
    path: '/assigntask',
    name: 'AssignTask',
    component: AssignTask
  },
  {
    path: '/redeptionsetting',
    name: 'RedeptionSetting',
    component: RedemptionSetting
  },
  {
    path: '/taskhistory',
    name: 'TaskHistory',
    component: TaskHistory
  },
  {
    path: '/addchild',
    name: 'AddChild',
    component: AddChild
  },
  {
    path: '/childprogress',
    name: 'ChildProgress',
    component: ChildProgress
  },
  {
    path: '/childprogress/:id',
    name: 'ChildProgress',
    component: ChildProgress,
    props: true // Pass route params as props
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

