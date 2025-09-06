import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface Book {
  id: number
  title: string
  description: string
  cover_url: string | null
  chapters: Chapter[]
}

export interface Chapter {
  id: number
  title: string
  content: string
}

export const useBooksStore = defineStore('books', () => {
  const books = ref<Book[]>([])
  const currentBook = ref<Book | null>(null)
  const currentChapter = ref<Chapter | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchBooks = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get('/api/books')
      books.value = response.data
    } catch (err) {
      error.value = 'Не удалось загрузить каталог книг'
      console.error('Failed to fetch books:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchBook = async (bookId: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`/api/book/${bookId}`)
      currentBook.value = response.data
    } catch (err) {
      error.value = 'Книга не найдена'
      console.error('Failed to fetch book:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchChapter = async (bookId: number, chapterId: number) => {
    loading.value = true
    error.value = null
    try {
      const response = await axios.get(`/api/book/${bookId}/chapter/${chapterId}`)
      currentChapter.value = response.data
    } catch (err) {
      error.value = 'Глава не найдена'
      console.error('Failed to fetch chapter:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    books,
    currentBook,
    currentChapter,
    loading,
    error,
    fetchBooks,
    fetchBook,
    fetchChapter,
  }
})