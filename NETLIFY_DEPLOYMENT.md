# Деплой на Netlify

## Обзор архитектуры

После деплоя на Netlify ваше приложение будет работать следующим образом:

- **Фронтенд**: Vue.js приложение, собранное в статические файлы
- **API**: Serverless функции (AWS Lambda) для работы с базой данных
- **База данных**: SQLite файл, встроенный в serverless функции
- **Бот**: Остается на вашем сервере/VPS для работы с Telegram

## Пошаговая инструкция

### 1. Подготовка проекта

```bash
# Создайте базу данных (если еще не создана)
sqlite3 app.db < create_tables.sql

# Запустите скрипт подготовки
./deploy-netlify.sh
```

Этот скрипт:

- Установит зависимости веб-приложения
- Соберет Vue.js приложение
- Установит зависимости для serverless функций (better-sqlite3)
- Скопирует базу данных в serverless функции

### 2. Создание Git репозитория

```bash
# Инициализируйте Git (если еще не сделано)
git init

# Добавьте все файлы
git add .

# Сделайте первый коммит
git commit -m "Initial commit for Netlify deployment"

# Создайте репозиторий на GitHub/GitLab
# И добавьте remote:
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

### 3. Настройка Netlify

1. **Создайте аккаунт** на [netlify.com](https://netlify.com)

2. **Подключите репозиторий**:

   - Нажмите "New site from Git"
   - Выберите ваш Git провайдер
   - Выберите репозиторий
   - Настройки сборки:
     - Build command: `cd webapp && npm install && npm run build`
     - Publish directory: `webapp/dist`

3. **Настройте переменные окружения**:
   - Перейдите в Site settings → Environment variables
   - Добавьте переменные из `NETLIFY_ENV_VARS.md`

### 4. Обновление конфигурации бота

После получения URL вашего Netlify сайта (например: `https://amazing-book-bot.netlify.app`):

1. Обновите `bot/config.py`:

```python
SERVER_URL = "https://amazing-book-bot.netlify.app/"
```

2. Перезапустите бота

### 5. Настройка Telegram Mini App

1. Откройте [@BotFather](https://t.me/BotFather)
2. Выберите вашего бота
3. Bot Settings → Menu Button → Configure Menu Button
4. Введите URL: `https://amazing-book-bot.netlify.app/`
5. Введите текст: "📚 Библиотека"

## Структура файлов после деплоя

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

## API Endpoints

После деплоя будут доступны следующие API:

- `GET /api/books` - список всех книг
- `GET /api/book/{id}` - детали книги с главами
- `GET /api/book/{id}/chapter/{chapter_id}` - содержимое главы
- `GET /api/verify/{telegram_user_id}` - проверка подписки

## Мониторинг и логи

### Просмотр логов

- Netlify Dashboard → Functions → View logs
- Или через Netlify CLI: `netlify functions:log`

### Мониторинг производительности

- Netlify Dashboard → Analytics
- Отслеживание времени выполнения функций

## Обновление базы данных

Для обновления базы данных:

1. Обновите локальную базу данных
2. Скопируйте новый `app.db` в `netlify/functions/`
3. Сделайте коммит и пуш:

```bash
git add netlify/functions/app.db
git commit -m "Update database"
git push
```

## Ограничения Netlify

### Serverless функции:

- Максимум 10 секунд выполнения
- 128MB памяти
- 1024MB дискового пространства

### База данных:

- SQLite файл должен быть меньше 1GB
- Для больших баз данных рассмотрите внешние решения (PlanetScale, Supabase)

## Альтернативы для базы данных

Если SQLite не подходит, рассмотрите:

1. **PlanetScale** (MySQL)
2. **Supabase** (PostgreSQL)
3. **FaunaDB** (NoSQL)
4. **MongoDB Atlas**

## Troubleshooting

### Ошибка "Function not found"

- Проверьте, что файлы функций находятся в `netlify/functions/`
- Убедитесь, что `netlify.toml` правильно настроен

### Ошибка "Database not found"

- Убедитесь, что `app.db` скопирован в `netlify/functions/`
- Проверьте права доступа к файлу

### CORS ошибки

- Проверьте настройки CORS в serverless функциях
- Убедитесь, что заголовки правильно установлены

### Медленная работа

- Оптимизируйте SQL запросы
- Рассмотрите кэширование
- Проверьте размер базы данных
