#!/usr/bin/env python3
"""
Запуск только веб-сервера без Telegram бота.
Полезно для разработки или если нужен только веб-интерфейс.
"""

from bot import database, server

def main():
    # Инициализация базы данных
    database.init_db()
    
    # Создание и запуск Flask приложения
    app = server.create_app()
    
    print("Запуск веб-сервера на http://localhost:8000")
    print("Веб-приложение будет доступно по адресу http://localhost:8000")
    
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == "__main__":
    main()
