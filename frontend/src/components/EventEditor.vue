<script setup>

import { ref, watch,onMounted } from "vue"
import { createEvent, updateEvent,getCategories,createCategories,deleteCategories } from "@/api/events"

const props = defineProps({
  event: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(["saved","close"])

const title = ref("")
const categoryTitle = ref("")
const selectedCategory = ref(null)
const deadline = ref("")
const sendEmail = ref(false)
const remindHoursBefore = ref(1)
const error = ref(null)
const loading = ref(false)

const categories = ref([])
const suggestions = ref([])

const isFocused = ref(false)

watch(
  () => props.event,
  (event) => {
    if(event){
      title.value = event.title
      categoryTitle.value = event.category.title
      selectedCategory.value = event.category.id
      deadline.value = event.deadline?.split("T")[0]
      sendEmail.value = event.send_email ?? false
      remindHoursBefore.value = event.when_send_email ?? 1
    }else{
      title.value = ""
      categoryTitle.value = ""
      selectedCategory.value = null
      deadline.value = ""
      sendEmail.value = false
      remindHoursBefore.value = 1
    }
  },
  { immediate: true }
)

async function loadCategories(){
  const response = await getCategories()
  categories.value = response.data
}

function onInput(){

    selectedCategory.value = null

    const q = categoryTitle.value.toLowerCase()

  suggestions.value = categories.value.filter(c =>
    c.title.toLowerCase().includes(q)
  )
}

async function deleteCategory_(id){
    try{
        const respone = await deleteCategories(id);
    } catch(err){
        error.value = "Something went wrong"
    }
}

function handleFocus(){
    isFocused.value = true;
    loadCategories()
}

function handleBlur(){
    isFocused.value = false;
    suggestions.value = [];
}

async function createNewCategory(){
    if(!categoryTitle.value){
        error.value = "type a title for category"
        return;
    }

    for(let i = 0; i < categories.value.length; i++){
        if (categories.value[i].title == categoryTitle.value){
            error.value = "category already exist";
            return;
        }
    }

    try {
        const respone = await createCategories({
            title : categoryTitle.value
        })
    } catch(error){
        error.value = "Something went wrong";
    }
}

function selectCategory(category){
  categoryTitle.value = category.title
  selectedCategory.value = category.id
  suggestions.value = []
}

async function submit(){

  loading.value = true
  error.value = null

  if(!selectedCategory.value){
    error.value = "Please select a category"
    loading.value = false;
    return
  }

   const payload = {
    title: title.value,
    category_id: selectedCategory.value,
    deadline: deadline.value,
    send_email: sendEmail.value,
    when_send_email: sendEmail.value ? remindHoursBefore.value : 0
  }

  try{

    let response

    if(props.event){
      response = await updateEvent(props.event.id,payload)
    }else{
      response = await createEvent(payload)
    }

    emit("saved", response.data)

  }catch(err){

    console.log(err.response.data)

    if(err.response?.data){
      error.value = Object.values(err.response.data).flat().join(" ")
    }else{
      error.value = "Something went wrong"
    }

  }finally{
    loading.value = false
  }
}

onMounted(loadCategories)

</script>


<template>

<div class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">

  <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-xl p-6 space-y-5">

    <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-100">
      {{ event ? "Edit Event" : "Create Event" }}
    </h2>

    <p v-if="error" class="text-red-500 text-sm">
      {{ error }}
    </p>

    <form @submit.prevent="submit" class="space-y-4">

      <!-- title -->
      <input
        v-model="title"
        placeholder="Title"
        required
        class="w-full rounded-lg border border-gray-300 dark:border-gray-600
               bg-white dark:bg-gray-700
               px-4 py-2
               text-gray-900 dark:text-gray-100
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <!-- category -->
      <div class="relative">

        <input
          v-model="categoryTitle"
          @input="onInput"
          @focus="handleFocus"
          @blur="handleBlur"
          placeholder="Category"
          class="w-full rounded-lg border border-gray-300 dark:border-gray-600
                 bg-white dark:bg-gray-700
                 px-4 py-2
                 text-gray-900 dark:text-gray-100
                 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <ul
          v-if="isFocused"
          class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-700
                 border border-gray-200 dark:border-gray-600
                 rounded-lg shadow-lg max-h-48 overflow-y-auto"
        >

          <li
            v-for="c in suggestions"
            :key="c.id"
            @mousedown="selectCategory(c)"
            class="flex justify-between items-center px-3 py-2 cursor-pointer
                   hover:bg-gray-100 dark:hover:bg-gray-600"
          >
            <span>{{ c.title }}</span>

            <button
              @mousedown.stop="deleteCategory_(c.id)"
              class="text-xs text-red-500 hover:text-red-600"
            >
              delete
            </button>
          </li>

          <li
            @mousedown="createNewCategory"
            class="px-3 py-2 cursor-pointer text-blue-600 hover:bg-gray-100 dark:hover:bg-gray-600"
          >
            + Create "{{ categoryTitle }}"
          </li>

        </ul>

      </div>

      <!-- deadline -->
      <input
        v-model="deadline"
        type="date"
        required
        class="w-full rounded-lg border border-gray-300 dark:border-gray-600
               bg-white dark:bg-gray-700
               px-4 py-2
               text-gray-900 dark:text-gray-100
               focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <!-- checkbox -->
      <label class="flex items-center gap-2 text-sm text-gray-700 dark:text-gray-200">
        <input type="checkbox" v-model="sendEmail" />
        Send reminder email
      </label>

      <!-- hours -->
      <input
        v-model.number="remindHoursBefore"
        type="number"
        min="1"
        placeholder="Hours before reminder"
        :disabled="!sendEmail"
        class="w-full rounded-lg border border-gray-300 dark:border-gray-600
               bg-white dark:bg-gray-700
               px-4 py-2
               text-gray-900 dark:text-gray-100
               focus:outline-none focus:ring-2 focus:ring-blue-500
               disabled:opacity-50"
      />

      <!-- actions -->
      <div class="flex justify-end gap-3 pt-2">

        <button
          type="button"
          @click="emit('close')"
          class="px-4 py-2 rounded-lg border border-gray-300
                 hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
        >
          Cancel
        </button>

        <button
          type="submit"
          :disabled="loading"
          class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700
                 text-white transition disabled:opacity-50"
        >
          {{ loading ? "Saving..." : "Save" }}
        </button>

      </div>

    </form>

  </div>

</div>

</template>
