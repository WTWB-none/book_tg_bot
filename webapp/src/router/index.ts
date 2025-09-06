import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'catalog',
    component: () => import('@/views/CatalogView.vue'),
  },
  {
    path: '/book/:id',
    name: 'book',
    component: () => import('@/views/BookView.vue'),
  },
  {
    path: '/book/:id/chapter/:chapterId',
    name: 'chapter',
    component: () => import('@/views/ChapterView.vue'),
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: () => import('@/views/ForbiddenView.vue'),
  },
  {
    path: '/debug',
    name: 'debug',
    component: () => import('@/views/DebugView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Router guard for subscription check
router.beforeEach(async (to, from, next) => {
  // Пропускаем отладочную страницу и страницу запрета
  if (to.name === 'forbidden' || to.name === 'debug') {
    return next()
  }

  const authStore = useAuthStore()
  
  // Для Mini App получаем UID из Telegram WebApp
  if (authStore.isTelegramReady && authStore.telegramUser?.id) {
    const uid = authStore.telegramUser.id.toString()
    
    // Check subscription if not already checked
    if (!authStore.subscriptionChecked) {
      await authStore.checkSubscription(uid)
    }

    if (!authStore.isSubscribed) {
      return next({ name: 'forbidden' })
    }
    
    return next()
  }
  
  // Fallback: Extract UID from query parameters
  const uid = to.query.uid as string
  if (!uid) {
    return next({ name: 'forbidden' })
  }

  // Check subscription if not already checked
  if (!authStore.subscriptionChecked) {
    await authStore.checkSubscription(uid)
  }

  if (!authStore.isSubscribed) {
    return next({ name: 'forbidden' })
  }

  next()
})

export default router