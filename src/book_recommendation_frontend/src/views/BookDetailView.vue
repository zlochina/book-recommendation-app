<template>
  <div class="p-6">
    <router-link to="/" class="text-blue-600 underline">← Back to search</router-link>

    <div v-if="loading" class="mt-4">Loading book...</div>
    <div v-else-if="book" class="mt-4">
      <h1 class="text-2xl font-bold">{{ book.title }}</h1>
      <p class="text-gray-700 mb-2">By {{ book.author }}</p>
      <img :src="book.image_url_large" class="w-48 my-4" />
      <p><strong>Publisher:</strong> {{ book.publisher }} ({{ book.publication_year }})</p>
      <p><strong>ISBN:</strong> {{ book.ISBN }}</p>
      <p><strong>Average Rating:</strong> {{ book.average_rating ?? "N/A" }}</p>

      <h2 class="text-xl font-semibold mt-6">Ratings</h2>
      <ul>
        <li v-for="rating in ratings" :key="rating.rating_id" class="border-b py-2">
          User {{ rating.user_id }} rated: {{ rating.user_rating }}/10
        </li>
      </ul>

      <h2 class="text-xl font-semibold mt-6">Recommendations</h2>
      <ul class="space-y-2">
        <li v-for="rec in recommendations" :key="rec.book_id">
          <router-link :to="`/book/${rec.book_id}`" class="text-blue-600 hover:underline">
            {{ rec.title }} by {{ rec.author }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { useRoute } from "vue-router"

const route = useRoute()
const book = ref(null)
const ratings = ref([])
const recommendations = ref([])
const loading = ref(true)

async function fetchBook(id) {
  loading.value = true
  try {
    const [bookRes, ratingsRes, recsRes] = await Promise.all([
      fetch(`/api/books/${id}`),
      fetch(`/api/ratings/${id}`),
      fetch(`/api/books/${id}/recommendations`),
    ])

    book.value = await bookRes.json()
    ratings.value = (await ratingsRes.json()).ratings
    recommendations.value = (await recsRes.json()).recommendations
  } catch (err) {
    console.error("Failed to load book:", err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBook(route.params.id)
})

// re-run fetch when route param changes (clicking a recommendation)
watch(
  () => route.params.id,
  (newId) => {
    fetchBook(newId)
  }
)
</script>

