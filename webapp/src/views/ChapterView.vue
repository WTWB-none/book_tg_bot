<template>
  <div class="chapter-view">
    <nav>
      <router-link 
        :to="{ 
          name: 'book', 
          params: { id: route.params.id } 
        }"
      >
        ← Назад к главам
      </router-link>
    </nav>
    
    <div v-if="booksStore.loading" class="loading">
      Загружаем главу...
    </div>
    
    <div v-else-if="booksStore.error" class="error">
      {{ booksStore.error }}
    </div>
    
    <div v-else-if="booksStore.currentChapter" class="reader">
      <h1>{{ booksStore.currentChapter.title }}</h1>
      
      <div 
        class="chapter-content"
        v-html="booksStore.currentChapter.content"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useBooksStore } from '@/stores/books'

const route = useRoute()
const booksStore = useBooksStore()

const loadChapter = () => {
  const bookId = parseInt(route.params.id as string)
  const chapterId = parseInt(route.params.chapterId as string)
  
  if (bookId && chapterId) {
    booksStore.fetchChapter(bookId, chapterId)
  }
}

onMounted(() => {
  loadChapter()
})

watch([() => route.params.id, () => route.params.chapterId], () => {
  loadChapter()
})
</script>

<style scoped>
.chapter-content {
  margin-top: 24px;
}

.chapter-content :deep(h1),
.chapter-content :deep(h2),
.chapter-content :deep(h3),
.chapter-content :deep(h4),
.chapter-content :deep(h5),
.chapter-content :deep(h6) {
  margin-top: 32px;
  margin-bottom: 16px;
  color: #2c3e50;
}

.chapter-content :deep(p) {
  margin-bottom: 16px;
}

.chapter-content :deep(ul),
.chapter-content :deep(ol) {
  margin-bottom: 16px;
  padding-left: 24px;
}

.chapter-content :deep(li) {
  margin-bottom: 8px;
}

.chapter-content :deep(blockquote) {
  margin: 24px 0;
  padding: 16px 20px;
  background: #f8f9fa;
  border-left: 4px solid #007acc;
  border-radius: 0 6px 6px 0;
}

.chapter-content :deep(code) {
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9em;
}

.chapter-content :deep(pre) {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin: 16px 0;
}

.chapter-content :deep(pre code) {
  background: none;
  padding: 0;
}
</style>