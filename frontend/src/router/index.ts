import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
import ChildLayout from '@/layouts/ChildLayout.vue'

// Child views
import ChildDashboard from '@/views/ChildDashboard.vue'
import ChildGames from '@/views/ChildGames.vue'
import ChildSavings from '@/views/ChildSavings.vue'
import ChildGoals from '@/views/ChildGoals.vue'

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
    redirect: '/child/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'ChildDashboard',
        component: ChildDashboard
      },
      {
        path: 'games',
        name: 'ChildGames',
        component: ChildGames
      },
      {
        path: 'savings',
        name: 'ChildSavings',
        component: ChildSavings
      },
      {
        path: 'goals',
        name: 'ChildGoals',
        component: ChildGoals
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

