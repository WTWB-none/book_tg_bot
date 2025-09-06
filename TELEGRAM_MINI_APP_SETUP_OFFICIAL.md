# Официальная настройка Telegram Mini App

## Проблема: "Not running in Telegram WebApp"

Эта ошибка возникает, когда приложение не правильно настроено как Mini App в Telegram.

## 🔧 Пошаговая настройка:

### 1. Настройка бота в BotFather

1. **Откройте [@BotFather](https://t.me/BotFather)**
2. **Выберите вашего бота** (команда `/mybots`)
3. **Bot Settings** → **Menu Button** → **Configure Menu Button**
4. **Введите URL вашего Mini App:**
   ```
   https://your-site.netlify.app/
   ```
5. **Введите текст кнопки:**
   ```
   📚 Библиотека
   ```

### 2. Проверка настроек бота

Убедитесь, что в BotFather:

- ✅ Bot Token получен
- ✅ Menu Button настроен
- ✅ URL указан правильно (HTTPS)
- ✅ Сайт доступен

### 3. Тестирование Mini App

1. **Откройте бота в Telegram**
2. **Нажмите `/start`** - должна появиться кнопка "📚 Библиотека"
3. **Нажмите на кнопку** - откроется Mini App
4. **Проверьте отладочную страницу:** `/debug`

### 4. Отладка проблем

#### Проблема: "initData is empty"

**Причина:** Mini App не настроен в BotFather
**Решение:** Настройте Menu Button в BotFather

#### Проблема: "window.Telegram not available"

**Причина:** Открыто не через Telegram
**Решение:** Откройте через кнопку в боте

#### Проблема: 500 ошибка API

**Причина:** Проблемы с serverless функциями
**Решение:** Проверьте логи в Netlify Dashboard

### 5. Проверка в отладочной странице

Откройте `https://your-site.netlify.app/debug` и проверьте:

1. **Состояние Telegram WebApp:**

   - Готов: Да
   - Пользователь: должен содержать ID
   - User ID: должен быть числом

2. **Тестирование API:**

   - Нажмите "Тест API"
   - Должен вернуть успешный ответ

3. **Telegram WebApp объект:**
   - Должен содержать все данные

### 6. Логи для отладки

В консоли браузера должны быть сообщения:

```
Telegram WebApp initialized: { user: {...}, platform: "...", ... }
Using Telegram user ID: 793857218
Checking subscription for user ID: 793857218
```

### 7. Проверка в Netlify

1. **Netlify Dashboard** → **Functions** → **View logs**
2. Ищите ошибки в функциях
3. Проверьте, что база данных скопирована

### 8. Альтернативное тестирование

Если Mini App не работает, протестируйте с URL параметром:

```
https://your-site.netlify.app/?uid=793857218
```

## 🚨 Частые ошибки:

### ❌ Неправильный URL в BotFather

```
❌ http://your-site.netlify.app/
✅ https://your-site.netlify.app/
```

### ❌ Не настроен Menu Button

- В BotFather: Bot Settings → Menu Button → Configure Menu Button

### ❌ Сайт недоступен

- Проверьте, что сайт работает
- Проверьте HTTPS сертификат

### ❌ Проблемы с CORS

- Убедитесь, что в netlify.toml настроены правильные заголовки

## ✅ Правильная последовательность:

1. **Создайте бота** в BotFather
2. **Настройте Menu Button** с HTTPS URL
3. **Деплойте сайт** на Netlify
4. **Протестируйте** через кнопку в боте
5. **Отладьте** через `/debug` страницу

## 📞 Если ничего не помогает:

1. Проверьте, что бот работает: `/start` в Telegram
2. Проверьте, что кнопка появляется после `/start`
3. Проверьте, что URL в BotFather правильный
4. Проверьте логи Netlify Functions
5. Проверьте отладочную страницу `/debug`
