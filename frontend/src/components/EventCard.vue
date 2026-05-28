<script setup>

const props = defineProps ({
    event : Object
})

const emit = defineEmits ([
    "edit",
    "delete"
])

function editEvent(){
    emit("edit",props.event);
}

function deleteEvent(){
    emit("delete",props.event.id);
}

</script>

<template>

<div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-5 shadow-sm hover:shadow-md transition">

  <!-- header -->
  <div class="flex justify-between items-start mb-4">

    <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
      {{ event.title }}
    </h3>

    <div class="flex gap-2">

      <button
        @click="editEvent"
        class="text-sm px-3 py-1 rounded-md border border-gray-300
               hover:bg-gray-100
               dark:border-gray-600 dark:hover:bg-gray-700
               text-gray-700 dark:text-gray-200 transition"
      >
        Edit
      </button>

      <button
        @click="deleteEvent"
        class="text-sm px-3 py-1 rounded-md bg-red-500 hover:bg-red-600 text-white transition"
      >
        Delete
      </button>

    </div>

  </div>


  <!-- body -->
  <div class="flex flex-col gap-2 text-sm">

    <div class="flex justify-between">
      <span class="text-gray-500 dark:text-gray-400">Category</span>
      <span class="text-gray-700 dark:text-gray-200">
        {{ event.category?.title || "No category" }}
      </span>
    </div>

    <div class="flex justify-between">
      <span class="text-gray-500 dark:text-gray-400">Deadline</span>
      <span class="text-gray-700 dark:text-gray-200">
        {{ new Date(event.deadline).toLocaleString() }}
      </span>
    </div>

    <div class="flex justify-between">
      <span class="text-gray-500 dark:text-gray-400">Email Reminder</span>

      <span v-if="event.send_email" class="text-gray-700 dark:text-gray-200">
        {{ event.when_send_email }} hours before
      </span>

      <span v-else class="text-gray-400">
        Disabled
      </span>

    </div>

  </div>

</div>

</template>