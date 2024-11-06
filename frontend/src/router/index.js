import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LandingPage from '@/components/public/LandingPages/Index.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import TablesAc from '@/components/admin/Accounts/TablesAc.vue'
import TablesEv from '@/components/admin/Events/TablesEv.vue'
import { auth } from './middleware/auth'
import Login from '@/components/public/LandingPages/Login.vue'
import Register from '@/components/public/LandingPages/Register.vue'

const routes = [
  // User
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
    component: Login,
    beforeEnter: auth
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: Register,
    beforeEnter: auth
  },


  // Admin
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    beforeEnter: auth
  },
  {
    path: '/admin/accounts',
    name: 'AdminAccounts',
    component: TablesAc,
    beforeEnter: auth
  },
  {
    path: '/admin/events',
    name: 'EventsAccounts',
    component: TablesEv,
    beforeEnter: auth
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
