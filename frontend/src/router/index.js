import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingPage from '@/views/LandingPage.vue'
import Login from '@/views/Login.vue'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomeView
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: Login
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
