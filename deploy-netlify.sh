#!/bin/bash

# Скрипт для деплоя на Netlify

echo "🚀 Начинаем деплой на Netlify..."

# Проверяем, что мы в правильной директории
if [ ! -f "netlify.toml" ]; then
    echo "❌ Ошибка: netlify.toml не найден. Запустите скрипт из корневой директории проекта."
    exit 1
fi

# Устанавливаем зависимости для веб-приложения
echo "📦 Устанавливаем зависимости веб-приложения..."
cd webapp
npm install

# Собираем веб-приложение
echo "🔨 Собираем веб-приложение..."
npm run build

# Возвращаемся в корневую директорию
cd ..

# Устанавливаем зависимости для serverless функций
echo "📦 Устанавливаем зависимости для serverless функций..."
cd netlify/functions
npm install

# Возвращаемся в корневую директорию
cd ../..

# Проверяем, что база данных существует
if [ ! -f "app.db" ]; then
    echo "⚠️  Предупреждение: app.db не найден. Создайте базу данных перед деплоем."
    echo "   Запустите: python -m bot.main (один раз для создания БД)"
fi

# Копируем базу данных в директорию функций (для serverless)
if [ -f "app.db" ]; then
    echo "📋 Копируем базу данных для serverless функций..."
    cp app.db netlify/functions/
fi

echo "✅ Готово к деплою!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Загрузите проект в Git репозиторий"
echo "2. Подключите репозиторий к Netlify"
echo "3. Настройте переменные окружения в Netlify Dashboard"
echo "4. Обновите SERVER_URL в bot/config.py на ваш Netlify URL"
echo ""
echo "🔗 Полезные ссылки:"
echo "- Netlify Dashboard: https://app.netlify.com"
echo "- Документация по переменным окружения: NETLIFY_ENV_VARS.md"
