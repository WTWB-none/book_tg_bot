import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import { useTelegram } from '../composables/useTelegram'

export const useAuthStore = defineStore('auth', () => {
  const isSubscribed = ref(false)
  const subscriptionChecked = ref(false)
  const loading = ref(false)
  
  const { user: telegramUser, isReady: isTelegramReady } = useTelegram()
  
  // Получаем UID из Telegram или из URL параметров
  const currentUserId = computed(() => {
    if (telegramUser.value?.id) {
      console.log('Using Telegram user ID:', telegramUser.value.id)
      return telegramUser.value.id.toString()
    }
    
    // Fallback: получаем из URL параметров
    const urlParams = new URLSearchParams(window.location.search)
    const uidFromUrl = urlParams.get('uid') || ''
    console.log('Using URL UID:', uidFromUrl)
    return uidFromUrl
  })

  const checkSubscription = async (uid?: string) => {
    // Если передан конкретный UID, используем его
    if (uid) {
      loading.value = true
      try {
        const response = await axios.get(`/api/verify/${uid}`)
        isSubscribed.value = response.data.subscribed
      } catch (error) {
        console.error('Subscription check failed:', error)
        isSubscribed.value = false
      } finally {
        subscriptionChecked.value = true
        loading.value = false
      }
      return
    }

    // Ждем инициализации Telegram WebApp
    if (!isTelegramReady.value) {
      console.log('Waiting for Telegram WebApp initialization...')
      return
    }

    const userId = currentUserId.value
    console.log('Checking subscription for user ID:', userId)
    
    if (!userId) {
      console.log('No user ID available')
      return
    }
    
    if (subscriptionChecked.value) {
      console.log('Subscription already checked')
      return
    }

    loading.value = true
    try {
      const response = await axios.get(`/api/verify/${userId}`)
      isSubscribed.value = response.data.subscribed
    } catch (error) {
      console.error('Subscription check failed:', error)
      isSubscribed.value = false
    } finally {
      subscriptionChecked.value = true
      loading.value = false
    }
  }

  const reset = () => {
    isSubscribed.value = false
    subscriptionChecked.value = false
    loading.value = false
  }

  return {
    isSubscribed,
    subscriptionChecked,
    loading,
    currentUserId,
    telegramUser,
    isTelegramReady,
    checkSubscription,
    reset,
  }
})