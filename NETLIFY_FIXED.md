# Исправления для деплоя на Netlify

## ✅ Проблемы исправлены:

### 1. **Telegram WebApp SDK**

- ❌ Удален несуществующий пакет `@twa-dev/sdk`
- ✅ Используется встроенный `window.Telegram.WebApp` API
- ✅ Создан собственный TypeScript интерфейс

### 2. **SQLite в Serverless функциях**

- ❌ Удален `sqlite3` (проблемы с компиляцией в serverless)
- ✅ Используется `better-sqlite3` (лучше работает в serverless)
- ✅ Обновлен database.js для синхронного API

### 3. **Зависимости**

- ✅ Создан корневой `package.json` с `better-sqlite3`
- ✅ Удален отдельный `package.json` из функций
- ✅ Обновлена команда сборки в `netlify.toml`

## 🚀 Готово к деплою!

### Быстрый старт:

```bash
# 1. Создайте базу данных (если нужно)
sqlite3 app.db < create_tables.sql

# 2. Подготовьте проект
./deploy-netlify.sh

# 3. Загрузите в Git
git add .
git commit -m "Ready for Netlify deployment"
git push origin main

# 4. Подключите к Netlify
# - Создайте сайт в Netlify Dashboard
# - Подключите ваш Git репозиторий
# - Настройте переменные окружения
```

### Переменные окружения в Netlify:

```
TELEGRAM_BOT_TOKEN=8256112334:AAG0D1fDI98c11ljCRD69C_I6BTkvH97Deg
TRIBUTE_API_URL=https://tribute.tg/api/v1/subscribers
TRIBUTE_API_KEY=cf0bee07-b00f-47d4-97f3-fdb65fa1
ADMIN_USER_IDS=793857218
```

### Настройки сборки в Netlify:

- **Build command**: `npm install && cd webapp && npm install && npm run build`
- **Publish directory**: `webapp/dist`
- **Functions directory**: `netlify/functions`

## 📁 Структура после деплоя:

```
your-site.netlify.app/
├── index.html (Vue.js приложение)
├── assets/ (JS, CSS файлы)
└── .netlify/functions/
    ├── books.js (API: /api/books)
    ├── book.js (API: /api/book/{id})
    ├── chapter.js (API: /api/book/{id}/chapter/{id})
    ├── verify.js (API: /api/verify/{uid})
    ├── database.js (модуль для работы с БД)
    └── app.db (SQLite база данных)
```

## 🔧 Что изменилось:

1. **better-sqlite3** вместо sqlite3 - лучше работает в serverless
2. **Синхронный API** - проще и быстрее
3. **Корневой package.json** - Netlify правильно устанавливает зависимости
4. **Встроенный Telegram API** - без внешних зависимостей

## ⚡ Преимущества:

- ✅ Быстрая сборка
- ✅ Надежная работа SQLite в serverless
- ✅ Полная совместимость с Telegram Mini App
- ✅ Автоматические деплои из Git

Теперь ваш проект готов к деплою на Netlify!
