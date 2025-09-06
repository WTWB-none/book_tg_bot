import { ref, onMounted } from 'vue'
import { WebApp } from '@twa-dev/sdk'

export interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  language_code?: string
  is_premium?: boolean
}

export function useTelegram() {
  const webApp = ref<WebApp | null>(null)
  const user = ref<TelegramUser | null>(null)
  const isReady = ref(false)
  const isExpanded = ref(false)

  onMounted(() => {
    // Проверяем, что мы в Telegram WebApp
    if (window.Telegram?.WebApp) {
      webApp.value = window.Telegram.WebApp
      user.value = webApp.value.initDataUnsafe?.user || null
      isReady.value = true
      
      // Расширяем приложение на весь экран
      webApp.value.expand()
      isExpanded.value = true
      
      // Настраиваем тему
      webApp.value.ready()
      
      // Отключаем кнопку закрытия (опционально)
      // webApp.value.disableClosingConfirmation()
      
      console.log('Telegram WebApp initialized:', {
        user: user.value,
        platform: webApp.value.platform,
        version: webApp.value.version
      })
    } else {
      console.log('Not running in Telegram WebApp')
    }
  })

  const showAlert = (message: string) => {
    if (webApp.value) {
      webApp.value.showAlert(message)
    } else {
      alert(message)
    }
  }

  const showConfirm = (message: string, callback?: (confirmed: boolean) => void) => {
    if (webApp.value) {
      webApp.value.showConfirm(message, callback)
    } else {
      const confirmed = confirm(message)
      callback?.(confirmed)
    }
  }

  const showPopup = (params: {
    title?: string
    message: string
    buttons?: Array<{
      id?: string
      type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive'
      text?: string
    }>
  }) => {
    if (webApp.value) {
      webApp.value.showPopup(params)
    } else {
      alert(params.message)
    }
  }

  const close = () => {
    if (webApp.value) {
      webApp.value.close()
    }
  }

  const sendData = (data: any) => {
    if (webApp.value) {
      webApp.value.sendData(JSON.stringify(data))
    }
  }

  const openLink = (url: string, options?: { try_instant_view?: boolean }) => {
    if (webApp.value) {
      webApp.value.openLink(url, options)
    } else {
      window.open(url, '_blank')
    }
  }

  const openTelegramLink = (url: string) => {
    if (webApp.value) {
      webApp.value.openTelegramLink(url)
    } else {
      window.open(url, '_blank')
    }
  }

  return {
    webApp,
    user,
    isReady,
    isExpanded,
    showAlert,
    showConfirm,
    showPopup,
    close,
    sendData,
    openLink,
    openTelegramLink
  }
}

// Расширяем глобальный объект Window для TypeScript
declare global {
  interface Window {
    Telegram?: {
      WebApp: WebApp
    }
  }
}
