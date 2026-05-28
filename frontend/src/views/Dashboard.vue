<script setup>
import EventCard from "@/components/EventCard.vue"
import EventEditor from "@/components/EventEditor.vue"
import { ref,onMounted } from "vue"
import {getEvents,getCategories, deleteEvent} from "@/api/events"
import {useAuthStore} from "@/stores/authStrore"
import { useRouter } from "vue-router"
import ConfirmDialog from "@/components/ConfirmDialoge.vue"

const events = ref([])
const error = ref(null)
const auth = useAuthStore()
const router = useRouter()
const showConfirm = ref(false)
const eventToDelete = ref(null)
const showEditor = ref(false)
const editingEvent = ref(null)

function openCreateEvent(){
  showEditor.value = true;
  editingEvent.value = null;
}

function editEvent(event){
  showEditor.value = true;
  editingEvent.value = event;
}

async function loadEvents(){
  try{
    const response = await getEvents()
    events.value = response.data
  }
  catch(err){
    if (err.response?.data) {
      error.value = Object.values(err.response.data)
        .flat()
        .join(" ")
    } else {
      error.value = "Something went wrong"
    }
  }
}

onMounted(loadEvents)

async function confirmDelete(){
  try {
    await deleteEvent(eventToDelete.value)

    events.value = events.value.filter(
      event => event.id != eventToDelete.value
    )

     showConfirm.value = false
    eventToDelete.value = null
  }catch(error){
    error.value = "Something went wrong"
  }
}

function onSaved(savedEvent){

  const index = events.value.findIndex(
    e => e.id === savedEvent.id
  )

  if(index !== -1){
    events.value[index] = savedEvent
  }else{
    events.value.unshift(savedEvent)
  }

  showEditor.value = false
  editingEvent.value = null
}

function deleteEvent_(id){
  eventToDelete.value = id;
  showConfirm.value = true;
}

async function logoutUser(){
  const logedout = await auth.logout();
  if (logedout){
    router.push("/login");
  }
  else{
    error.value = "Something went wrong"
  }
}

</script>

<template>

<div class="min-h-screen bg-gray-100 dark:bg-gray-900">

  <!-- header -->
  <div class="max-w-6xl mx-auto px-4 py-6 flex justify-between items-center">

    <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
      Dashboard
    </h1>

    <div class="flex gap-3">

      <button
        @click="openCreateEvent"
        class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white transition"
      >
        Create Event
      </button>

      <button
        @click="logoutUser"
        class="px-4 py-2 rounded-lg bg-red-500 hover:bg-red-600 text-white transition"
      >
        Logout
      </button>

    </div>

  </div>


  <!-- content -->
  <div class="max-w-6xl mx-auto px-4 pb-10">

    <!-- error -->
    <p
      v-if="error"
      class="mb-4 text-red-500 text-sm"
    >
      {{ error }}
    </p>

    <!-- empty state -->
    <div
      v-if="!events.length"
      class="text-center text-gray-500 dark:text-gray-400 py-20"
    >
      No events yet
    </div>

    <!-- events grid -->
    <div
      v-else
      class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
    >

      <EventCard
        v-for="event in events"
        :key="event.id"
        :event="event"
        @edit="editEvent"
        @delete="deleteEvent_"
      />

    </div>

  </div>


  <!-- editor modal -->
  <EventEditor
    v-if="showEditor"
    :event="editingEvent"
    @saved="onSaved"
    @close="showEditor=false"
  />

  <!-- confirm dialog -->
  <ConfirmDialog
    v-if="showConfirm"
    @confirm="confirmDelete"
    @cancel="showConfirm=false"
  />

</div>

</template>
