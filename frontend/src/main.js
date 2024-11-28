import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootswatch/dist/united/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle'

createApp(App).use(router).mount('#app')
