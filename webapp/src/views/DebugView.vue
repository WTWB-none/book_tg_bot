<template>
  <div class="debug">
    <h1>Отладка Telegram WebApp</h1>
    
    <div class="debug-section">
      <h2>Состояние Telegram WebApp</h2>
      <p><strong>Готов:</strong> {{ isTelegramReady ? 'Да' : 'Нет' }}</p>
      <p><strong>Пользователь:</strong> {{ telegramUser ? JSON.stringify(telegramUser, null, 2) : 'Не найден' }}</p>
      <p><strong>User ID:</strong> {{ currentUserId || 'Не найден' }}</p>
    </div>

    <div class="debug-section">
      <h2>Проверка подписки</h2>
      <p><strong>Статус:</strong> {{ isSubscribed ? 'Подписан' : 'Не подписан' }}</p>
      <p><strong>Проверено:</strong> {{ subscriptionChecked ? 'Да' : 'Нет' }}</p>
      <p><strong>Загрузка:</strong> {{ loading ? 'Да' : 'Нет' }}</p>
      <button @click="checkSubscription" :disabled="loading">
        {{ loading ? 'Проверяем...' : 'Проверить подписку' }}
      </button>
    </div>

    <div class="debug-section">
      <h2>Тестирование API</h2>
      <button @click="testAPI" :disabled="apiLoading">
        {{ apiLoading ? 'Тестируем...' : 'Тест API' }}
      </button>
      <div v-if="apiResult">
        <h3>Результат API:</h3>
        <pre>{{ apiResult }}</pre>
      </div>
    </div>

    <div class="debug-section">
      <h2>URL параметры</h2>
      <p><strong>Полный URL:</strong> {{ window.location.href }}</p>
      <p><strong>UID из URL:</strong> {{ getUidFromUrl() }}</p>
    </div>

    <div class="debug-section">
      <h2>Telegram WebApp объект</h2>
      <pre>{{ telegramWebAppInfo }}</pre>
    </div>

    <div class="debug-section">
      <h2>Навигация</h2>
      <router-link to="/" class="btn">Каталог</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { isSubscribed, subscriptionChecked, loading, currentUserId, telegramUser, isTelegramReady, checkSubscription } = authStore

const telegramWebAppInfo = ref('')
const apiLoading = ref(false)
const apiResult = ref('')

onMounted(() => {
  if (window.Telegram?.WebApp) {
    const webApp = window.Telegram.WebApp
    telegramWebAppInfo.value = JSON.stringify({
      version: webApp.version,
      platform: webApp.platform,
      colorScheme: webApp.colorScheme,
      themeParams: webApp.themeParams,
      initData: webApp.initData,
      initDataUnsafe: webApp.initDataUnsafe,
      isExpanded: webApp.isExpanded,
      viewportHeight: webApp.viewportHeight,
      viewportStableHeight: webApp.viewportStableHeight
    }, null, 2)
  } else {
    telegramWebAppInfo.value = 'Telegram WebApp не доступен'
  }
})

const getUidFromUrl = () => {
  const urlParams = new URLSearchParams(window.location.search)
  return urlParams.get('uid') || 'Не найден'
}

const testAPI = async () => {
  apiLoading.value = true
  apiResult.value = ''
  
  try {
    const response = await fetch('/api/test')
    const data = await response.json()
    apiResult.value = JSON.stringify(data, null, 2)
  } catch (error) {
    apiResult.value = `Ошибка: ${error.message}`
  } finally {
    apiLoading.value = false
  }
}
</script>

<style scoped>
.debug {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.debug-section {
  background: #f5f5f5;
  padding: 16px;
  margin: 16px 0;
  border-radius: 8px;
}

.debug-section h2 {
  margin-top: 0;
  color: #333;
}

.debug-section p {
  margin: 8px 0;
}

.debug-section pre {
  background: #fff;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.btn {
  display: inline-block;
  padding: 10px 20px;
  background: #007acc;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  margin: 8px 8px 8px 0;
}

button {
  padding: 10px 20px;
  background: #007acc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
