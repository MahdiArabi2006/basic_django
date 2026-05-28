<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/client"
import {register} from "@/api/auth"

const router = useRouter()

const email = ref("")
const password = ref("")
const password2 = ref("")

const loading = ref(false)
const error = ref(null)

const registerUser = async () => {
  error.value = null

  if (password.value != password2.value){
    error.value = "Password does not match"
    return;
  }
  loading.value = true

  try {
    const response = await register({
        email : email.value,
        password : password.value
    })

    if (response.status == 201 || response.status == 200){
        router.push("/login")
    }
    else{
        error.value = "Registration failed. Please try again."
    }

  } 
  catch (err) {
    if (err.response?.data) {
        error.value = Object.values(err.response.data)
        .flat()
        .join(" ")
    } else {
        error.value = "Something went wrong"
    }
  }
   finally {
    loading.value = false
  }
}
</script>
<template>
  <div class="min-h-screen w-full flex items-center justify-center bg-gray-100 dark:bg-gray-900 px-4">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-6 sm:p-8 space-y-6">
      <h1 class="text-2xl font-bold text-center text-gray-800 dark:text-white">Create Account</h1>

      <form @submit.prevent="registerUser" class="space-y-5">
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          required
          class="w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 transition duration-150 ease-in-out"
        />

        <input
          v-model="password"
          type="password"
          placeholder="Password"
          required
          class="w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 transition duration-150 ease-in-out"
        />

        <input
          v-model="password2"
          type="password"
          placeholder="Confirm Password"
          required
          class="w-full px-4 py-2 rounded-lg bg-gray-50 border border-gray-300 focus:border-indigo-500 focus:ring focus:ring-indigo-200 text-gray-800 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 transition duration-150 ease-in-out"
        />

        <button
          :disabled="loading"
          class="w-full py-2 font-semibold text-white rounded-lg transition duration-200"
          :class="loading 
            ? 'bg-indigo-400 cursor-not-allowed' 
            : 'bg-indigo-600 hover:bg-indigo-700'"
        >
          {{ loading ? "Creating..." : "Register" }}
        </button>

        <p v-if="error" class="text-red-600 dark:text-red-400 text-sm text-center mt-2">
          {{ error }}
        </p>

        <p class="text-center text-sm text-gray-600 dark:text-gray-400">
          Already have an account?
          <router-link to="/login" class="text-indigo-600 hover:text-indigo-700 font-medium">
            Log in
          </router-link>
        </p>
      </form>
    </div>
  </div>
</template>
