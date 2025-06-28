import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
import ChildDashboard from '@/views/ChildDashboard.vue'
import ChildLayout from '@/layouts/ChildLayout.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/child',
    component: ChildLayout,
    //meta: { requiresAuth: true, role: 'child' }, #To be added once auth is setup
    children: [
      {
        path: 'dashboard',
        name: 'ChildDashboard',
        component: ChildDashboard
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

