<script setup>

const emit = defineEmits(["confirm","cancel"])

</script>

<template>

<div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">

  <div class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6">

    <p class="text-lg font-medium text-gray-800 dark:text-gray-100 text-center">
      Are you sure you want to delete this event?
    </p>

    <div class="flex justify-center gap-4 mt-6">

      <button
        @click="emit('cancel')"
        class="px-4 py-2 rounded-lg border border-gray-300
               hover:bg-gray-100
               dark:border-gray-600 dark:hover:bg-gray-700
               text-gray-700 dark:text-gray-200
               transition"
      >
        Cancel
      </button>

      <button
        @click="emit('confirm')"
        class="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-700
               text-white font-medium transition"
      >
        Delete
      </button>

    </div>

  </div>

</div>

</template>
