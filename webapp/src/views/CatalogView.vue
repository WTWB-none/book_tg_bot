<template>
  <div class="catalog">
    <h1>Каталог книг</h1>
    
    <div v-if="authStore.loading" class="loading">
      Проверяем подписку...
    </div>
    
    <div v-else-if="!authStore.isSubscribed" class="error">
      <h2>Доступ ограничен</h2>
      <p>Для доступа к библиотеке необходима активная подписка.</p>
      <p>Обратитесь к администратору для получения доступа.</p>
    </div>
    
    <div v-else-if="booksStore.loading" class="loading">
      Загружаем каталог...
    </div>
    
    <div v-else-if="booksStore.error" class="error">
      {{ booksStore.error }}
    </div>
    
    <div v-else-if="booksStore.books.length === 0" class="loading">
      В каталоге пока нет книг
    </div>
    
    <div v-else>
      <div 
        v-for="book in booksStore.books" 
        :key="book.id" 
        class="book-card"
      >
        <div v-if="book.cover_url" class="book-cover-container">
          <img 
            :src="book.cover_url" 
            :alt="`Обложка ${book.title}`"
            class="book-cover"
            @error="handleImageError"
          />
        </div>
        
        <h2>{{ book.title }}</h2>
        
        <p v-if="book.description" class="book-description">
          {{ book.description }}
        </p>
        
        <router-link 
          :to="{ name: 'book', params: { id: book.id } }"
          class="book-link"
        >
          Открыть книгу
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useBooksStore } from '@/stores/books'
import { useAuthStore } from '@/stores/auth'

const booksStore = useBooksStore()
const authStore = useAuthStore()

onMounted(async () => {
  // Проверяем подписку пользователя
  await authStore.checkSubscription()
  
  // Загружаем книги только если пользователь подписан
  if (authStore.isSubscribed) {
    booksStore.fetchBooks()
  }
})

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}
</script>

<style scoped>
.book-cover-container {
  margin-bottom: 16px;
}

.book-description {
  color: #666;
  margin: 12px 0;
  line-height: 1.5;
}

.book-link {
  display: inline-block;
  padding: 10px 20px;
  background: #007acc;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.book-link:hover {
  background: #005a9e;
  text-decoration: none;
}
</style>