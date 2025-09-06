<template>
  <div class="book-view">
    <nav>
      <router-link to="/">← Назад к каталогу</router-link>
    </nav>
    
    <div v-if="booksStore.loading" class="loading">
      Загружаем книгу...
    </div>
    
    <div v-else-if="booksStore.error" class="error">
      {{ booksStore.error }}
    </div>
    
    <div v-else-if="booksStore.currentBook">
      <div v-if="booksStore.currentBook.cover_url" class="book-cover-container">
        <img 
          :src="booksStore.currentBook.cover_url" 
          :alt="`Обложка ${booksStore.currentBook.title}`"
          class="book-cover"
          @error="handleImageError"
        />
      </div>
      
      <h1>{{ booksStore.currentBook.title }}</h1>
      
      <p v-if="booksStore.currentBook.description" class="book-description">
        {{ booksStore.currentBook.description }}
      </p>
      
      <h3>Главы</h3>
      
      <div class="chapter-list">
        <div v-if="booksStore.currentBook.chapters.length === 0" class="no-chapters">
          Глав пока нет
        </div>
        
        <div 
          v-else
          v-for="chapter in booksStore.currentBook.chapters" 
          :key="chapter.id"
          class="chapter-item"
        >
          <router-link 
            :to="{ 
              name: 'chapter', 
              params: { 
                id: booksStore.currentBook!.id, 
                chapterId: chapter.id 
              } 
            }"
            class="chapter-link"
          >
            {{ chapter.title }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBooksStore } from '@/stores/books'

const route = useRoute()
const booksStore = useBooksStore()

const loadBook = () => {
  const bookId = parseInt(route.params.id as string)
  if (bookId) {
    booksStore.fetchBook(bookId)
  }
}

onMounted(() => {
  loadBook()
})

watch(() => route.params.id, () => {
  loadBook()
})

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}
</script>

<style scoped>
.book-description {
  color: #666;
  margin: 16px 0;
  line-height: 1.6;
}

.chapter-list {
  margin-top: 20px;
}

.chapter-item {
  margin: 8px 0;
}

.chapter-link {
  display: block;
  padding: 12px 16px;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  color: #495057;
  text-decoration: none;
  transition: all 0.2s ease;
}

.chapter-link:hover {
  background: #e9ecef;
  border-color: #007acc;
  color: #007acc;
  text-decoration: none;
}

.no-chapters {
  color: #666;
  font-style: italic;
  padding: 20px;
  text-align: center;
}
</style>