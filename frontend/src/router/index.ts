import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
import ChildLayout from '@/layouts/ChildLayout.vue'
import TeenLayout from '@/layouts/TeenLayout.vue'

// Child views
import ChildDashboard from '@/views/ChildDashboard.vue'
import ChildGames from '@/views/ChildGames.vue'
import ChildSavings from '@/views/ChildSavings.vue'
import ChildGoals from '@/views/ChildGoals.vue'

// Teen views
import TeenDashboard from '@/views/TeenDashboard.vue'
import TeenBudget from '@/views/TeenBudget.vue'
import TeenGoals from '@/views/TeenGoals.vue'
import TeenActivities from '@/views/TeenActivities.vue'
import TeenExplore from '@/views/TeenExplore.vue'

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
  },
  {
    path: '/teen',
    component: TeenLayout,
    //meta: { requiresAuth: true, role: 'teen' }, #To be added once auth is setup
    redirect: '/teen/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'TeenDashboard',
        component: TeenDashboard
      },
      {
        path: 'budget',
        name: 'TeenBudget',
        component: TeenBudget
      },
      {
        path: 'goals',
        name: 'TeenGoals',
        component: TeenGoals
      },
      {
        path: 'activities',
        name: 'TeenActivities',
        component: TeenActivities
      },
      {
        path: 'explore',
        name: 'TeenExplore',
        component: TeenExplore
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

