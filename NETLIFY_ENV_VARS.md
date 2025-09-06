# Переменные окружения для Netlify

## Настройка в Netlify Dashboard

Перейдите в настройки вашего сайта в Netlify:

1. Откройте ваш сайт в Netlify Dashboard
2. Перейдите в **Site settings** → **Environment variables**
3. Добавьте следующие переменные:

### Обязательные переменные:

```
TELEGRAM_BOT_TOKEN=8256112334:AAG0D1fDI98c11ljCRD69C_I6BTkvH97Deg
TRIBUTE_API_URL=https://tribute.tg/api/v1/subscribers
TRIBUTE_API_KEY=cf0bee07-b00f-47d4-97f3-fdb65fa1
ADMIN_USER_IDS=793857218
```

### Автоматические переменные:

Netlify автоматически предоставляет:

- `URL` - URL вашего сайта (например: `https://your-site.netlify.app`)
- `DEPLOY_URL` - URL текущего деплоя

## Использование в коде

В serverless функциях переменные доступны через `process.env`:

```javascript
const token = process.env.TELEGRAM_BOT_TOKEN;
const apiKey = process.env.TRIBUTE_API_KEY;
const siteUrl = process.env.URL;
```

## Безопасность

⚠️ **Важно**: Никогда не коммитьте реальные токены в репозиторий!

- Используйте `.env.example` для шаблона
- Добавляйте `.env` в `.gitignore`
- Настройте переменные только в Netlify Dashboard
