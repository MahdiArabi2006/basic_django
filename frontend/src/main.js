import './assets/main.css'
import './style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/authStrore'
import axios from 'axios'

import App from './App.vue'
import router from './router/router'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

const auth = useAuthStore()
await auth.restoreSession()

app.use(router)

app.mount('#app')