import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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

// Auth pages
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  {
    path: '/child',
    component: ChildLayout,
    meta: { requiresAuth: true, role: 'younger_child' },
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
    meta: { requiresAuth: true, role: 'older_child' },
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
  },
  // Additional dashboard routes for other user types
  // {
  //   path: '/dashboard/parent',
  //   name: 'ParentDashboard',
  //   component: () => import('@/views/dashboard/ParentDashboard.vue'),
  //   meta: { requiresAuth: true, roles: ['parent'] }
  // },
  // {
  //   path: '/dashboard/teacher',
  //   name: 'TeacherDashboard',
  //   component: () => import('@/views/dashboard/TeacherDashboard.vue'),
  //   meta: { requiresAuth: true, roles: ['teacher'] }
  // },
  // Catch all route - redirect to landing
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Check authentication status
  await authStore.checkAuth()
  
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.user?.role
  
  // Handle routes that require authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth/login')
    return
  }
  
  // Handle routes that require guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect to appropriate dashboard based on role
    const redirectPath = getRedirectPath(userRole)
    next(redirectPath)
    return
  }
  
  // Handle role-based access
  if (Array.isArray(to.meta.roles) && userRole && !to.meta.roles.includes(userRole)) {
    // Redirect to appropriate dashboard based on role
    const redirectPath = getRedirectPath(userRole)
    next(redirectPath)
    return
  }
  
  next()
})

function getRedirectPath(role?: string) {
  switch (role) {
    case 'younger_child':
    case 'older_child':
      return '/dashboard/child'
    case 'parent':
      return '/dashboard/parent'
    case 'teacher':
      return '/dashboard/teacher'
    default:
      return '/'
  }
}

export default router