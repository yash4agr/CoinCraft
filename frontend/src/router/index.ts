import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Landing page
import LandingPage from '@/views/LandingPage.vue'

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
  // TODO: Add dashboard routes for different user types
  // {
  //   path: '/dashboard/child',
  //   name: 'ChildDashboard',
  //   component: () => import('@/views/dashboard/ChildDashboard.vue'),
  //   meta: { requiresAuth: true, roles: ['younger_child', 'older_child'] }
  // },
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
  // Catch all route
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
  if (to.meta.roles && userRole && !to.meta.roles.includes(userRole)) {
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