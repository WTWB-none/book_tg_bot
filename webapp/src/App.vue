<template>
  <div id="app" :class="{ 'telegram-app': isTelegramReady }">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const isTelegramReady = ref(false)
const telegramUser = ref<any>(null)

onMounted(() => {
  // Проверяем, что мы в Telegram WebApp
  if (window.Telegram?.WebApp) {
    const webApp = window.Telegram.WebApp
    
    // Расширяем приложение на весь экран
    webApp.expand()
    
    // Настраиваем тему
    webApp.ready()
    
    // Получаем данные пользователя
    telegramUser.value = webApp.initDataUnsafe?.user || null
    isTelegramReady.value = true
    
    console.log('Telegram WebApp initialized:', {
      user: telegramUser.value,
      platform: webApp.platform,
      version: webApp.version,
      initData: webApp.initData,
      initDataUnsafe: webApp.initDataUnsafe
    })
  } else {
    console.log('Not running in Telegram WebApp')
    // Для тестирования вне Telegram
    isTelegramReady.value = true
  }
})
</script>

<style>
#app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: var(--tg-theme-bg-color, #ffffff);
  color: var(--tg-theme-text-color, #000000);
}

/* Стили для Telegram Mini App */
.telegram-app {
  padding: 0;
  margin: 0;
  max-width: 100%;
  min-height: 100vh;
}

/* Адаптация под тему Telegram */
.telegram-app * {
  box-sizing: border-box;
}

/* Кнопки в стиле Telegram */
.telegram-app .btn {
  background-color: var(--tg-theme-button-color, #2481cc);
  color: var(--tg-theme-button-text-color, #ffffff);
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.telegram-app .btn:hover {
  opacity: 0.8;
}

.telegram-app .btn:active {
  opacity: 0.6;
}

/* Карточки в стиле Telegram */
.telegram-app .card {
  background-color: var(--tg-theme-secondary-bg-color, #f8f8f8);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Заголовки */
.telegram-app h1,
.telegram-app h2,
.telegram-app h3 {
  color: var(--tg-theme-text-color, #000000);
  margin-bottom: 16px;
}

/* Ссылки */
.telegram-app a {
  color: var(--tg-theme-link-color, #2481cc);
  text-decoration: none;
}

.telegram-app a:hover {
  text-decoration: underline;
}
</style>