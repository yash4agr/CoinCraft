import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUserStore } from '@/stores/user'
import { useDashboardStore } from '@/stores/dashboard'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
import ChildLayout from '@/layouts/ChildLayout.vue'
import TeenLayout from '@/layouts/TeenLayout.vue'

// Child views
import ChildDashboard from '@/views/child/ChildDashboard.vue'
import ChildGames from '@/views/child/ChildGames.vue'
import ChildSavings from '@/views/child/ChildSavings.vue'
import ChildGoals from '@/views/child/ChildGoals.vue'
import ChildShop from '@/views/child/ChildShop.vue'
import UserProfile from '@/views/UserProfile.vue'

// Teen views
import TeenDashboard from '@/views/teen/TeenDashboard.vue'
import TeenBudget from '@/views/teen/TeenBudget.vue'
import TeenGoals from '@/views/teen/TeenGoals.vue'
import TeenActivities from '@/views/teen/TeenActivities.vue'
import TeenExplore from '@/views/teen/TeenExplore.vue'
import TeenShop from '@/views/teen/TeenShop.vue'

// Auth pages
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'

// Parent views
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
      },
      {
        path: 'shop',
        name: 'ChildShop',
        component: ChildShop
      },
      {
        path: 'profile',
        name: 'ChildProfile',
        component: UserProfile
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
      },
      {
        path: 'shop',
        name: 'TeenShop',
        component: TeenShop
      },
      {
        path: 'profile',
        name: 'TeenProfile',
        component: UserProfile
      }
    ]
  },
  // Parent dashboard and related routes
    {
    path: '/parent',
    meta: { requiresAuth: true, role: 'parent' },
    redirect: '/parent/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'ParentDashboard',
        component: ParentDashboard
      },
      {
        path: 'assigntask',
        name: 'AssignTask',
        component: AssignTask
      },
      {
        path: 'redemptionsetting',
        name: 'RedemptionSetting',
        component: RedemptionSetting
      },
      {
        path: 'taskhistory',
        name: 'TaskHistory',
        component: TaskHistory
      },
      {
        path: 'addchild',
        name: 'AddChild',
        component: AddChild
      },
      {
        path: 'childprogress',
        name: 'ChildProgress',
        component: ChildProgress
      },
      {
        path: 'childprogress/:id',
        name: 'ChildProgressDetail',
        component: ChildProgress,
        props: true
      }
    ]
  },

  // Uncomment and implement teacher routes when ready
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
  const userStore = useUserStore()
  const dashboardStore = useDashboardStore()
  
  console.log('Navigation attempt:', { to: to.path, from: from.path })
  
  // Check authentication status
  await authStore.checkAuth()
  
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.user?.role
  
  console.log('Auth status:', { isAuthenticated, userRole })
  
  // Handle routes that require authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('Redirecting to login - not authenticated')
    next('/auth/login')
    return
  }
  
  // Handle routes that require guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated) {
    // Redirect to appropriate dashboard based on role
    const redirectPath = getRedirectPath(userRole)
    console.log('Redirecting authenticated user to:', redirectPath)
    next(redirectPath)
    return
  }
  
  // Handle role-based access
  if (to.meta.role && userRole && to.meta.role !== userRole) {
    // Redirect to appropriate dashboard based on role
    const redirectPath = getRedirectPath(userRole)
    console.log('Redirecting due to role mismatch:', { expected: to.meta.role, actual: userRole, redirectTo: redirectPath })
    next(redirectPath)
    return
  }
  
  // Load user data and dashboard data when entering authenticated routes
  if (isAuthenticated && authStore.user && to.meta.requiresAuth) {
    // Set user profile in user store
    if (!userStore.profile) {
      userStore.setProfile({
        id: authStore.user.id,
        fullName: authStore.user.fullName,
        email: authStore.user.email,
        username: authStore.user.username,
        role: authStore.user.role,
        coins: authStore.user.coins || 0,
        avatar: authStore.user.avatar || '👤',
        level: 5,
        streak: 12,
        totalCoinsEarned: authStore.user.coins || 0,
        goalsCompleted: 3,
        createdAt: authStore.user.createdAt,
        preferences: {
          soundEnabled: true,
          notificationsEnabled: true,
          theme: 'light'
        }
      })
      
      // Load user-specific data
      await userStore.loadUserData(authStore.user.id)
    }
    
    // Load dashboard data if entering dashboard routes
    if (to.path.includes('/child/') || to.path.includes('/teen/')) {
      await dashboardStore.loadDashboardData(userRole || '')
    }
  }
  
  console.log('Navigation allowed to:', to.path)
  next()
})

function getRedirectPath(role?: string) {
  switch (role) {
    case 'younger_child':
      return '/child/dashboard'
    case 'older_child':
      return '/teen/dashboard'
    case 'parent':
      return '/dashboard/parent'
    case 'teacher':
      return '/dashboard/teacher'
    default:
      return '/'
  }
}

export default router