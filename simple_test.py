#!/usr/bin/env python3
"""
Простой тест для проверки конфигурации проекта.
"""

import os
import sys

def test_project_structure():
    """Проверяет структуру проекта."""
    
    print("🧪 Тестирование структуры проекта...")
    
    required_files = [
        'bot/__init__.py',
        'bot/config.py',
        'bot/database.py',
        'bot/handlers.py',
        'bot/server.py',
        'bot/main.py',
        'webapp/package.json',
        'webapp/vite.config.ts',
        'webapp/src/main.ts',
        'webapp/src/App.vue',
        'requirements.txt',
        'build.sh',
        'deploy.md',
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Отсутствуют файлы: {missing_files}")
        return False
    else:
        print("\n✅ Все файлы на месте!")
        return True

def test_config():
    """Проверяет конфигурацию."""
    
    print("\n⚙️ Проверка конфигурации...")
    
    try:
        # Добавляем путь к модулю bot
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bot'))
        
        import config
        
        print(f"   - SERVER_URL: {config.SERVER_URL}")
        print(f"   - TELEGRAM_BOT_TOKEN: {'✅ Установлен' if config.TELEGRAM_BOT_TOKEN != 'YOUR_TELEGRAM_BOT_TOKEN_HERE' else '❌ Не установлен'}")
        print(f"   - ADMIN_USER_IDS: {config.ADMIN_USER_IDS}")
        print(f"   - TRIBUTE_API_URL: {config.TRIBUTE_API_URL}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка при загрузке конфигурации: {e}")
        return False

def test_vue_structure():
    """Проверяет структуру Vue приложения."""
    
    print("\n📱 Проверка Vue приложения...")
    
    vue_files = [
        'webapp/src/views/CatalogView.vue',
        'webapp/src/views/BookView.vue',
        'webapp/src/views/ChapterView.vue',
        'webapp/src/views/ForbiddenView.vue',
        'webapp/src/stores/auth.ts',
        'webapp/src/stores/books.ts',
        'webapp/src/router/index.ts',
    ]
    
    missing_vue_files = []
    
    for file_path in vue_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_vue_files.append(file_path)
    
    if missing_vue_files:
        print(f"\n❌ Отсутствуют Vue файлы: {missing_vue_files}")
        return False
    else:
        print("\n✅ Все Vue файлы на месте!")
        return True

def test_handlers_update():
    """Проверяет, что обработчики обновлены для веб-приложения."""
    
    print("\n🤖 Проверка обновлений бота...")
    
    try:
        handlers_path = os.path.join(os.path.dirname(__file__), 'bot', 'handlers.py')
        
        with open(handlers_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем наличие web_app в коде
        if 'web_app={"url":' in content:
            print("   ✅ Кнопки веб-приложения добавлены")
        else:
            print("   ❌ Кнопки веб-приложения не найдены")
            return False
        
        # Проверяем наличие команды catalog
        if 'async def catalog(' in content:
            print("   ✅ Команда /catalog добавлена")
        else:
            print("   ❌ Команда /catalog не найдена")
            return False
        
        # Проверяем регистрацию команды catalog
        if 'CommandHandler("catalog", catalog)' in content:
            print("   ✅ Команда /catalog зарегистрирована")
        else:
            print("   ❌ Команда /catalog не зарегистрирована")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка при проверке обработчиков: {e}")
        return False

def main():
    """Основная функция тестирования."""
    
    print("🚀 Запуск простых тестов Book Bot...")
    print("=" * 50)
    
    tests = [
        ("Структура проекта", test_project_structure()),
        ("Конфигурация", test_config()),
        ("Vue приложение", test_vue_structure()),
        ("Обновления бота", test_handlers_update()),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func
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
        print("🎉 Все тесты пройдены! Проект готов к работе.")
        print("\n📋 Следующие шаги:")
        print("   1. Установите зависимости: pip install -r requirements.txt")
        print("   2. Установите Node.js и соберите Vue: ./build.sh")
        print("   3. Настройте TELEGRAM_BOT_TOKEN в bot/config.py")
        print("   4. Запустите бота: python -m bot.main")
    else:
        print("⚠️ Некоторые тесты провалены. Проверьте структуру проекта.")

if __name__ == "__main__":
    main()