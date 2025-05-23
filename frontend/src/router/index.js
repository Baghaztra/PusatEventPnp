import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/components/public/LandingPages/Index.vue'
import AdminDashboard from '@/components/admin/AdminDashboard.vue'
import TablesAc from '@/components/admin/Accounts/TablesAc.vue'
import TablesEv from '@/components/admin/Events/TablesEv.vue'
import { auth } from './middleware/auth'
import { admin } from './middleware/admin'
import { eo } from './middleware/eo'
import Login from '@/components/public/LandingPages/Login.vue'
import Register from '@/components/public/LandingPages/Register.vue'
import Eologin from '@/components/public/LandingPages/Eologin.vue'
import Eoregister from '@/components/public/LandingPages/Eoregister.vue'
import HomePage from '@/components/public/MainPages/HomePage.vue'
import Waiting from '@/components/public/LandingPages/Waiting.vue'
import TablesEo from '@/components/admin/Eventorganizers/TablesEo.vue'
import EventDetails from '@/components/public/MainPages/EventDetails.vue'
import EventOrganizer from '@/components/public/MainPages/EventOrganizer.vue'
import CreateEvent from '@/components/public/MainPages/CreateEvent.vue'
import NotFound from '@/views/NotFound.vue'
import EditDescription from '@/components/public/MainPages/EditDescription.vue'
import CalendarComponet from '@/components/public/MainPages/CalendarComponet.vue'

const routes = [
  // Main
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: CalendarComponet
  },
  {
    path: '/home',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/event/:id',
    name: 'EventPage',
    component: EventDetails,
    props: true,
  },
  {
    path: '/organizer/:id',
    name: 'EoPage',
    component: EventOrganizer,
    props: true,
  },
  {
    path: '/404_',
    name: '404_page',
    component: NotFound,
    props: true,
  },
  {
    path: '/:catchAll(.*)',
    redirect: '/404_',
  },

  // User 
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
    path: '/create-event',
    name: 'CreateEventPage',
    component: CreateEvent, 
    beforeEnter: eo
  },
  {
    path: '/edit-event/:id',
    name: 'Edit Event Description',
    component: EditDescription,
    props: true,
    beforeEnter: eo
  },
  {
    path: '/waiting',
    name: 'WaitingPage',
    component: Waiting, 
  },


  // Admin
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    beforeEnter: admin
  },
  {
    path: '/admin/accounts',
    name: 'AdminAccounts',
    component: TablesAc,
    beforeEnter: admin
  },
  {
    path: '/admin/eo',
    name: 'AdminEventorganizers',
    component: TablesEo,
    beforeEnter: admin
  },
  {
    path: '/admin/events',
    name: 'AdminEvents',
    component: TablesEv,
    beforeEnter: admin
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
