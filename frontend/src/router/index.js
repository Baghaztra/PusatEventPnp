import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/components/public/LandingPages/Index.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import TablesAc from '@/components/admin/Accounts/TablesAc.vue'
import TablesEv from '@/components/admin/Events/TablesEv.vue'
import { auth } from './middleware/auth'
import Login from '@/components/public/LandingPages/Login.vue'
import Register from '@/components/public/LandingPages/Register.vue'
import Eologin from '@/components/public/LandingPages/Eologin.vue'
import Eoregister from '@/components/public/LandingPages/Eoregister.vue'
import HomePage from '@/components/public/MainPages/HomePage.vue'
import Waiting from '@/components/public/LandingPages/Waiting.vue'

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
    component: HomePage
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

  // Event organizer
  {
    path: '/eo-login',
    name: 'EoLoginPage',
    component: Eologin,
    beforeEnter: auth
  },
  {
    path: '/eo-register',
    name: 'EoRegisterPage',
    component: Eoregister,
    beforeEnter: auth
  },
  {
    path: '/waiting',
    name: 'EoWaitingPage',
    component: Waiting,
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
