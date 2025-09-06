const Database = require('better-sqlite3');
const path = require('path');

// Путь к базе данных
const DB_PATH = path.join(__dirname, 'app.db');

// Создание подключения к базе данных
function getDb() {
  return new Database(DB_PATH);
}

// Получение списка книг
function getBooksSummary() {
  try {
    const db = getDb();
    
    const query = `
      SELECT 
        b.id,
        b.title,
        b.description,
        b.cover_url,
        COUNT(c.id) as chapter_count
      FROM books b
      LEFT JOIN chapters c ON b.id = c.book_id
      GROUP BY b.id, b.title, b.description, b.cover_url
      ORDER BY b.title
    `;
    
    const rows = db.prepare(query).all();
    db.close();
    
    // Преобразуем данные в формат, ожидаемый фронтендом
    const books = rows.map(row => ({
      id: row.id,
      title: row.title,
      description: row.description,
      cover_url: row.cover_url,
      chapters: [] // Будет заполнено при запросе деталей книги
    }));
    
    return books;
  } catch (error) {
    console.error('Error in getBooksSummary:', error);
    throw error;
  }
}

// Получение деталей книги с главами
function getBookDetail(bookId) {
  try {
    const db = getDb();
    
    const bookQuery = 'SELECT * FROM books WHERE id = ?';
    const chaptersQuery = 'SELECT id, title FROM chapters WHERE book_id = ? ORDER BY id';
    
    const book = db.prepare(bookQuery).get(bookId);
    
    if (!book) {
      db.close();
      return null;
    }
    
    const chapters = db.prepare(chaptersQuery).all(bookId);
    db.close();
    
    return {
      id: book.id,
      title: book.title,
      description: book.description,
      cover_url: book.cover_url,
      chapters: chapters.map(chapter => ({
        id: chapter.id,
        title: chapter.title
      }))
    };
  } catch (error) {
    console.error('Error in getBookDetail:', error);
    throw error;
  }
}

// Получение деталей главы
function getChapterDetail(bookId, chapterId) {
  try {
    const db = getDb();
    
    const query = `
      SELECT c.*, b.title as book_title
      FROM chapters c
      JOIN books b ON c.book_id = b.id
      WHERE c.book_id = ? AND c.id = ?
    `;
    
    const row = db.prepare(query).get(bookId, chapterId);
    db.close();
    
    if (!row) {
      return null;
    }
    
    return {
      id: row.id,
      title: row.title,
      content: row.content,
      book_title: row.book_title
    };
  } catch (error) {
    console.error('Error in getChapterDetail:', error);
    throw error;
  }
}

// Проверка, является ли пользователь разрешенным
function isAllowedUser(telegramUserId) {
  try {
    const db = getDb();
    
    const query = 'SELECT COUNT(*) as count FROM allowed_users WHERE telegram_user_id = ?';
    
    const row = db.prepare(query).get(telegramUserId);
    db.close();
    
    return row.count > 0;
  } catch (error) {
    console.error('Error in isAllowedUser:', error);
    throw error;
  }
}

module.exports = {
  getBooksSummary,
  getBookDetail,
  getChapterDetail,
  isAllowedUser
};
