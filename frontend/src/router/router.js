import { createRouter, createWebHistory } from "vue-router"
import { useAuthStore } from "@/stores/authStrore"
import Dashboard from "@/views/Dashboard.vue"
import Login from "@/views/Login.vue"
import Register from "@/views/Register.vue"

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: { guestOnly: true }
  },
  {
    path: "/register",
    name: "register",
    component: Register
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (!authStore.authChecked) return
  
  if (to.meta.requiresAuth && !authStore.accessToken) {
    return "/login"
  }

  if (to.meta.guestOnly && authStore.accessToken) {
    return "/"
  }
})

export default router
