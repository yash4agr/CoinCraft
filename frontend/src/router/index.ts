import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'
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
    component: LoginView
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: RegisterView
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

