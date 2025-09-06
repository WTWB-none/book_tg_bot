"""
Database layer for the book bot.

This module wraps all interactions with the SQLite database.  It
provides functions to initialise the schema, add and retrieve books,
chapters and allowed users.  All connections are opened and closed
inside each function for simplicity; for high‑traffic scenarios you
could consider using a connection pool.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

from . import config


def init_db() -> None:
    """Initialise the SQLite database and create tables if they do not exist."""
    conn = sqlite3.connect(config.DB_FILE)
    cur = conn.cursor()
    # Books table: optional cover_url
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            cover_url TEXT
        )
        """
    )
    # Chapters table referencing books
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
        """
    )
    # Allowed users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS allowed_users (
            telegram_user_id INTEGER PRIMARY KEY
        )
        """
    )
    conn.commit()
    conn.close()


def get_books_summary() -> List[Dict[str, Any]]:
    """Return a list of all books with chapter metadata.

    Each dictionary contains the keys ``id``, ``title``, ``description``,
    ``cover_url`` and a ``chapters`` list of dictionaries with ``id`` and
    ``title`` fields.
    """
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = [dict(row) for row in cur.fetchall()]
    for book in books:
        cur.execute(
            "SELECT id, title FROM chapters WHERE book_id = ? ORDER BY id ASC",
            (book["id"],),
        )
        book["chapters"] = [dict(r) for r in cur.fetchall()]
    conn.close()
    return books


def get_book_detail(book_id: int) -> Optional[Dict[str, Any]]:
    """Return a single book with its chapters or None if not found."""
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cur.fetchone()
    if row is None:
        conn.close()
        return None
    book = dict(row)
    cur.execute(
        "SELECT id, title FROM chapters WHERE book_id = ? ORDER BY id ASC",
        (book_id,),
    )
    book["chapters"] = [dict(r) for r in cur.fetchall()]
    conn.close()
    return book


def get_chapter_detail(book_id: int, chapter_id: int) -> Optional[Dict[str, Any]]:
    """Return the full details of a chapter or None if not found."""
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT c.id AS chapter_id, c.title AS title, c.content AS content, b.id AS book_id "
        "FROM chapters c JOIN books b ON c.book_id = b.id WHERE c.book_id = ? AND c.id = ?",
        (book_id, chapter_id),
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return {
        "bookId": row["book_id"],
        "chapterId": row["chapter_id"],
        "title": row["title"],
        "content": row["content"],
    }


def add_book(title: str, description: str, cover_url: Optional[str]) -> int:
    """Insert a new book into the database and return its ID."""
    conn = sqlite3.connect(config.DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, description, cover_url) VALUES (?, ?, ?)",
        (title, description, cover_url),
    )
    book_id = cur.lastrowid
    conn.commit()
    conn.close()
    return book_id


def add_chapter(book_id: int, title: str, content: str) -> int:
    """Insert a new chapter and return its ID."""
    conn = sqlite3.connect(config.DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chapters (book_id, title, content) VALUES (?, ?, ?)",
        (book_id, title, content),
    )
    chapter_id = cur.lastrowid
    conn.commit()
    conn.close()
    return chapter_id


def add_allowed_user(user_id: int) -> None:
    """Add a user ID to the allowed_users table."""
    conn = sqlite3.connect(config.DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO allowed_users (telegram_user_id) VALUES (?)",
        (user_id,),
    )
    conn.commit()
    conn.close()


def is_allowed_user(user_id: int) -> bool:
    """Return True if the user ID is in the allowed_users table."""
    conn = sqlite3.connect(config.DB_FILE)
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM allowed_users WHERE telegram_user_id = ? LIMIT 1",
        (user_id,),
    )
    result = cur.fetchone()
    conn.close()
    return result is not None