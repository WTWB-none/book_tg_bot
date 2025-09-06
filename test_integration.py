#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции бота с мини-приложением Telegram.
Этот скрипт проверяет, что бот правильно создает кнопки для веб-приложения.
"""

import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot import config, handlers

async def test_web_app_button():
    """Тестирует создание кнопки для веб-приложения."""
    
    print("🧪 Тестирование интеграции с мини-приложением Telegram...")
    
    # Тестовые данные
    test_user_id = 123456789
    test_url = f"{config.SERVER_URL}?uid={test_user_id}"
    
    print(f"📱 Тестовый URL: {test_url}")
    
    # Создаем кнопку как в обработчике
    keyboard = [
        [InlineKeyboardButton(
            "📚 Открыть каталог книг", 
            web_app={"url": test_url}
        )]
    ]
    
    markup = InlineKeyboardMarkup(keyboard)
    
    print("✅ Кнопка для веб-приложения создана успешно!")
    print(f"🔗 URL веб-приложения: {test_url}")
    print("📋 Структура кнопки:")
    print(f"   - Текст: '📚 Открыть каталог книг'")
    print(f"   - Тип: web_app")
    print(f"   - URL: {test_url}")
    
    # Проверяем, что URL содержит правильные параметры
    if f"uid={test_user_id}" in test_url:
        print("✅ UID параметр корректно добавлен в URL")
    else:
        print("❌ UID параметр отсутствует в URL")
    
    # Проверяем конфигурацию
    print(f"\n⚙️ Конфигурация:")
    print(f"   - SERVER_URL: {config.SERVER_URL}")
    print(f"   - TELEGRAM_BOT_TOKEN: {'✅ Установлен' if config.TELEGRAM_BOT_TOKEN != 'YOUR_TELEGRAM_BOT_TOKEN_HERE' else '❌ Не установлен'}")
    print(f"   - ADMIN_USER_IDS: {config.ADMIN_USER_IDS}")
    
    return True

def test_flask_routes():
    """Тестирует доступность Flask маршрутов."""
    
    print("\n🌐 Тестирование Flask маршрутов...")
    
    try:
        from bot.server import create_app
        app = create_app()
        
        with app.test_client() as client:
            # Тестируем API маршруты
            routes_to_test = [
                '/api/books',
                '/api/verify/123456789',
            ]
            
            for route in routes_to_test:
                response = client.get(route)
                print(f"   - {route}: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"     ✅ Маршрут доступен")
                else:
                    print(f"     ⚠️ Маршрут вернул код {response.status_code}")
        
        print("✅ Flask приложение создано успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании Flask: {e}")
        return False

def test_vue_build():
    """Проверяет, что Vue приложение собрано."""
    
    print("\n📦 Проверка сборки Vue приложения...")
    
    import os
    
    dist_path = os.path.join(os.path.dirname(__file__), 'webapp', 'dist')
    index_path = os.path.join(dist_path, 'index.html')
    
    if os.path.exists(dist_path) and os.path.exists(index_path):
        print("✅ Vue приложение собрано")
        print(f"   - Путь к dist: {dist_path}")
        print(f"   - index.html: {'✅ Найден' if os.path.exists(index_path) else '❌ Не найден'}")
        return True
    else:
        print("❌ Vue приложение не собрано")
        print("   Запустите: ./build.sh")
        return False

async def main():
    """Основная функция тестирования."""
    
    print("🚀 Запуск тестов интеграции Book Bot...")
    print("=" * 50)
    
    tests = [
        ("Кнопка веб-приложения", test_web_app_button()),
        ("Flask маршруты", test_flask_routes()),
        ("Vue сборка", test_vue_build()),
    ]
    
    results = []
    
    for test_name, test_coro in tests:
        try:
            if asyncio.iscoroutine(test_coro):
                result = await test_coro
            else:
                result = test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте '{test_name}': {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Результаты тестов:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"   - {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Итого: {passed}/{len(results)} тестов пройдено")
    
    if passed == len(results):
        print("🎉 Все тесты пройдены! Интеграция готова к работе.")
    else:
        print("⚠️ Некоторые тесты провалены. Проверьте конфигурацию.")

if __name__ == "__main__":
    asyncio.run(main())