const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Путь к базе данных
const DB_PATH = path.join(__dirname, '../../app.db');

// Создание подключения к базе данных
function getDb() {
  return new sqlite3.Database(DB_PATH);
}

// Получение списка книг
function getBooksSummary() {
  return new Promise((resolve, reject) => {
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
    
    db.all(query, [], (err, rows) => {
      db.close();
      
      if (err) {
        reject(err);
        return;
      }
      
      // Преобразуем данные в формат, ожидаемый фронтендом
      const books = rows.map(row => ({
        id: row.id,
        title: row.title,
        description: row.description,
        cover_url: row.cover_url,
        chapters: [] // Будет заполнено при запросе деталей книги
      }));
      
      resolve(books);
    });
  });
}

// Получение деталей книги с главами
function getBookDetail(bookId) {
  return new Promise((resolve, reject) => {
    const db = getDb();
    
    const bookQuery = 'SELECT * FROM books WHERE id = ?';
    const chaptersQuery = 'SELECT id, title FROM chapters WHERE book_id = ? ORDER BY id';
    
    db.get(bookQuery, [bookId], (err, book) => {
      if (err) {
        db.close();
        reject(err);
        return;
      }
      
      if (!book) {
        db.close();
        resolve(null);
        return;
      }
      
      db.all(chaptersQuery, [bookId], (err, chapters) => {
        db.close();
        
        if (err) {
          reject(err);
          return;
        }
        
        resolve({
          id: book.id,
          title: book.title,
          description: book.description,
          cover_url: book.cover_url,
          chapters: chapters.map(chapter => ({
            id: chapter.id,
            title: chapter.title
          }))
        });
      });
    });
  });
}

// Получение деталей главы
function getChapterDetail(bookId, chapterId) {
  return new Promise((resolve, reject) => {
    const db = getDb();
    
    const query = `
      SELECT c.*, b.title as book_title
      FROM chapters c
      JOIN books b ON c.book_id = b.id
      WHERE c.book_id = ? AND c.id = ?
    `;
    
    db.get(query, [bookId, chapterId], (err, row) => {
      db.close();
      
      if (err) {
        reject(err);
        return;
      }
      
      if (!row) {
        resolve(null);
        return;
      }
      
      resolve({
        id: row.id,
        title: row.title,
        content: row.content,
        book_title: row.book_title
      });
    });
  });
}

// Проверка, является ли пользователь разрешенным
function isAllowedUser(telegramUserId) {
  return new Promise((resolve, reject) => {
    const db = getDb();
    
    const query = 'SELECT COUNT(*) as count FROM allowed_users WHERE telegram_user_id = ?';
    
    db.get(query, [telegramUserId], (err, row) => {
      db.close();
      
      if (err) {
        reject(err);
        return;
      }
      
      resolve(row.count > 0);
    });
  });
}

module.exports = {
  getBooksSummary,
  getBookDetail,
  getChapterDetail,
  isAllowedUser
};
