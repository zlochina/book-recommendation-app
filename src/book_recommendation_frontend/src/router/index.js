import { createRouter, createWebHistory } from "vue-router"
import SearchView from "../views/SearchView.vue"
import BookDetailView from "../views/BookDetailView.vue"

const routes = [
  { path: "/", name: "search", component: SearchView },
  { path: "/book/:id", name: "book", component: BookDetailView, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})

