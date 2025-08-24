<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Book Search</h1>
    <input
      v-model="query"
      @input="searchBooks"
      class="border p-2 rounded w-full"
      placeholder="Search books..."
    />

    <div v-if="loading" class="mt-4">Loading...</div>
    <ul v-else class="mt-4 space-y-2">
      <li
        v-for="book in results"
        :key="book.book_id"
        class="border p-3 rounded shadow-sm hover:bg-gray-50"
      >
        <router-link :to="`/book/${book.book_id}`" class="flex items-center gap-4">
          <img :src="book.image_url_thumb" class="w-12 h-16 object-cover" />
          <div>
            <h2 class="font-semibold">{{ book.title }}</h2>
            <p class="text-sm text-gray-600">{{ book.author }}</p>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from "vue"

const query = ref("")
const results = ref([])
const loading = ref(false)

// this keeps track of the latest query sent
let lastQuery = ""

async function searchBooks() {
  if (!query.value) {
    results.value = []
    return
  }

  loading.value = true
  const currentQuery = query.value
  lastQuery = currentQuery

  try {
    const res = await fetch(`/api/books?query=${encodeURIComponent(currentQuery)}`)
    const data = await res.json()

    // only update results if query hasn’t changed
    if (lastQuery === currentQuery) {
      results.value = data
    }
  } catch (err) {
    console.error("Search failed:", err)
  } finally {
    // also check to not hide loading for outdated responses
    if (lastQuery === currentQuery) {
      loading.value = false
    }
  }
}
</script>

