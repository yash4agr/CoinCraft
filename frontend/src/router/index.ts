import { createRouter, createWebHistory } from 'vue-router'

// Landing page
import LandingPage from '@/views/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

