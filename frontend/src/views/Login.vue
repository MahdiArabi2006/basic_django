<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import {login} from "@/api/auth"
import {useAuthStore} from "@/stores/authStrore"

const router = useRouter()
const auth = useAuthStore()

const email = ref("")
const password = ref("")

const loading = ref(false)
const error = ref(null)

const loginUser = async () => {
  error.value = null
  loading.value = true

  try {
    const response = await login({
        email : email.value,
        password : password.value
    })
    
    auth.accessToken = response.data.access;
    localStorage.setItem("refresh",response.data.refresh);
    auth.user = {
      email : email.value,
    }
    router.push("/")
  } 
  catch (err) {
    if (err.response?.data) {
        error.value = Object.values(err.response.data)
        .flat()
        .join(" ")
    } else {
        error.value = "Something went wrong"
    }
    auth.accessToken = null;
    auth.user = null;
  }
   finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 px-4">

    <div class="w-full max-w-md bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 sm:p-8 space-y-6">

      <h1 class="text-2xl font-bold text-center text-gray-800 dark:text-gray-100">
        Login Account
      </h1>

      <form @submit.prevent="loginUser" class="space-y-4">

        <input
          v-model="email"
          type="email"
          placeholder="Email"
          required
          class="w-full rounded-lg border border-gray-300 dark:border-gray-600
                 bg-white dark:bg-gray-700
                 px-4 py-2
                 text-gray-900 dark:text-gray-100
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          class="w-full rounded-lg border border-gray-300 dark:border-gray-600
                 bg-white dark:bg-gray-700
                 px-4 py-2
                 text-gray-900 dark:text-gray-100
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <button
          :disabled="loading"
          class="w-full rounded-lg bg-blue-600 hover:bg-blue-700
                 text-white font-medium py-2
                 transition disabled:opacity-50"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>

        <p
          v-if="error"
          class="text-red-500 text-sm text-center"
        >
          {{ error }}
        </p>

        <p class="text-center text-sm text-gray-600 dark:text-gray-400">
          Don't have an account?
          <router-link to="/register" class="text-indigo-600 hover:text-indigo-700 font-medium">
            register
          </router-link>
        </p>

      </form>

    </div>

  </div>
</template>