-- Создание таблиц для базы данных книжного бота

-- Таблица книг
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    cover_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица глав
CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
);

-- Таблица разрешенных пользователей
CREATE TABLE IF NOT EXISTS allowed_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_user_id INTEGER UNIQUE NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для оптимизации
CREATE INDEX IF NOT EXISTS idx_chapters_book_id ON chapters(book_id);
CREATE INDEX IF NOT EXISTS idx_allowed_users_telegram_id ON allowed_users(telegram_user_id);

-- Вставка тестовых данных (опционально)
INSERT OR IGNORE INTO books (id, title, description) VALUES 
(1, 'Пример книги', 'Это пример книги для демонстрации работы приложения');

INSERT OR IGNORE INTO chapters (book_id, title, content) VALUES 
(1, 'Глава 1', 'Содержимое первой главы...'),
(1, 'Глава 2', 'Содержимое второй главы...');

INSERT OR IGNORE INTO allowed_users (telegram_user_id) VALUES 
(793857218);
