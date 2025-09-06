"""
Telegram command and callback handlers for the book bot.

This module contains all of the asynchronous handler functions used by the
Telegram bot.  They rely on the database layer for persistent storage
and the configuration module for API keys and other settings.
"""

from __future__ import annotations

import asyncio
import datetime as _dt
from typing import Optional

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from . import config, database

# Conversation state enumerations
ADD_BOOK_TITLE, ADD_BOOK_DESCRIPTION, ADD_BOOK_COVER = range(3)
CHOOSE_BOOK, CHAPTER_TITLE, CHAPTER_CONTENT = range(3)
ADD_ALLOWED_USER_ID = 100


async def is_user_subscribed(telegram_user_id: int) -> bool:
    """Return True if the user has an active subscription.

    First checks the local allowed_users table.  If the user is not
    found there, the function queries the Tribute API.  Only entries
    with status ``active`` and an ``expireAt`` timestamp later than
    the current time count as subscribed.
    """
    # Check the local database
    if database.is_allowed_user(telegram_user_id):
        return True
    try:
        response = requests.get(
            config.TRIBUTE_API_URL,
            headers={"Api-Key": config.TRIBUTE_API_KEY},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        now = _dt.datetime.utcnow().replace(tzinfo=_dt.timezone.utc)
        for entry in data.get("result", []):
            if entry.get("telegramUserId") == telegram_user_id:
                if entry.get("status") == "active":
                    expire_str = entry.get("expireAt")
                    try:
                        expire_dt = _dt.datetime.fromisoformat(expire_str.replace("Z", "+00:00"))
                        if expire_dt > now:
                            return True
                    except Exception:
                        pass
        return False
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command.

    Sends a welcome message and web app button if the subscription check passes. 
    Otherwise instructs the user to subscribe.
    """
    user = update.effective_user
    if user is None:
        return
    subscribed = await asyncio.get_event_loop().run_in_executor(
        None, is_user_subscribed, user.id
    )
    if subscribed:
        # Compose the URL with the UID parameter
        base_url = config.SERVER_URL
        if not base_url.endswith("/"):
            base_url += "/"
        url = f"{base_url}?uid={user.id}"
        
        # Create inline keyboard with Mini App button
        keyboard = [
            [InlineKeyboardButton(
                "📚 Открыть библиотеку", 
                web_app={"url": url}
            )]
        ]
        
        await update.message.reply_text(
            f"Привет, {user.first_name}! Добро пожаловать в библиотеку. "
            f"Нажмите на кнопку ниже, чтобы открыть каталог:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            "К сожалению, у вас нет активной подписки. Чтобы читать книги, "
            "оформите подписку и попробуйте снова."
        )


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /catalog command - quick access to book catalog."""
    user = update.effective_user
    if user is None:
        return
    subscribed = await asyncio.get_event_loop().run_in_executor(
        None, is_user_subscribed, user.id
    )
    if subscribed:
        # Compose the URL with the UID parameter
        base_url = config.SERVER_URL
        if not base_url.endswith("/"):
            base_url += "/"
        url = f"{base_url}?uid={user.id}"
        
        # Create inline keyboard with web app button
        keyboard = [
            [InlineKeyboardButton(
                "📚 Открыть каталог", 
                web_app={"url": url}
            )]
        ]
        
        await update.message.reply_text(
            "Откройте каталог книг:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            "К сожалению, у вас нет активной подписки. Чтобы читать книги, "
            "оформите подписку и попробуйте снова."
        )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Entry point for admin commands."""
    user = update.effective_user
    if user is None or user.id not in config.ADMIN_USER_IDS:
        await update.message.reply_text("У вас нет доступа к админ панели.")
        return
    keyboard = [
        [InlineKeyboardButton("Добавить книгу", callback_data="admin_addbook")],
        [InlineKeyboardButton("Добавить главу", callback_data="admin_addchapter")],
        [InlineKeyboardButton("Добавить подписчика", callback_data="admin_addsubscriber")],
    ]
    await update.message.reply_text(
        "Выберите действие:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Book creation flow
async def add_book_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Введите название книги:")
    return ADD_BOOK_TITLE


async def add_book_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["new_book_title"] = update.message.text.strip()
    await update.message.reply_text(
        "Введите краткое описание (можно оставить пустым):"
    )
    return ADD_BOOK_DESCRIPTION


async def add_book_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["new_book_description"] = update.message.text.strip()
    await update.message.reply_text(
        "Если у книги есть обложка, отправьте URL обложки. "
        "Если обложка не нужна, отправьте 'нет'."
    )
    return ADD_BOOK_COVER


async def add_book_cover(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = context.user_data.pop("new_book_title", None)
    description = context.user_data.pop("new_book_description", "").strip()
    cover_input = update.message.text.strip()
    if cover_input.lower() in {"нет", "no", "none", ""}:
        cover_url: Optional[str] = None
    else:
        cover_url = cover_input
    if not title:
        await update.message.reply_text(
            "Название книги не найдено. Попробуйте снова."
        )
        return ConversationHandler.END
    try:
        book_id = database.add_book(title, description, cover_url)
        await update.message.reply_text(
            f"Книга '{title}' добавлена с id {book_id}."
        )
    except Exception:
        await update.message.reply_text(
            "Не удалось добавить книгу. Произошла ошибка."
        )
    return ConversationHandler.END


# Chapter creation flow
async def add_chapter_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    # Build inline keyboard with available books
    try:
        books = database.get_books_summary()
    except Exception:
        books = []
    keyboard: list[list[InlineKeyboardButton]] = []
    for book in books:
        keyboard.append([
            InlineKeyboardButton(book["title"], callback_data=f"choose_book_{book['id']}")
        ])
    if not keyboard:
        await update.callback_query.edit_message_text(
            "Нет книг. Сначала добавьте книгу."
        )
        return ConversationHandler.END
    await update.callback_query.edit_message_text(
        "Выберите книгу:", reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHOOSE_BOOK


async def choose_book(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data
    book_id = int(data.split("_")[-1])
    context.user_data["chapter_book_id"] = book_id
    await query.edit_message_text("Введите название главы:")
    return CHAPTER_TITLE


async def chapter_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["chapter_title"] = update.message.text.strip()
    await update.message.reply_text(
        "Введите текст главы (поддерживается Markdown или HTML, будет показан как есть):"
    )
    return CHAPTER_CONTENT


async def chapter_content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    book_id = context.user_data.pop("chapter_book_id", None)
    title = context.user_data.pop("chapter_title", None)
    content = update.message.text
    if book_id is None or not title:
        await update.message.reply_text(
            "Что‑то пошло не так. Глава не сохранена. Попробуйте снова."
        )
        return ConversationHandler.END
    # Verify book exists and insert chapter
    if database.get_book_detail(book_id) is None:
        await update.message.reply_text("Книга не найдена. Попробуйте снова.")
        return ConversationHandler.END
    try:
        chapter_id = database.add_chapter(book_id, title, content)
        await update.message.reply_text(
            f"Глава '{title}' добавлена в книгу с id {book_id}. Id главы: {chapter_id}."
        )
    except Exception:
        await update.message.reply_text(
            "Не удалось добавить главу. Произошла ошибка."
        )
    return ConversationHandler.END


# Manual subscriber flow
async def add_subscriber_entry(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Введите Telegram user ID пользователя, которого вы хотите добавить в список подписчиков:"
    )
    return ADD_ALLOWED_USER_ID


async def add_subscriber_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    try:
        uid = int(text)
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите числовой Telegram ID (целое число). Попробуйте снова:"
        )
        return ADD_ALLOWED_USER_ID
    try:
        if database.is_allowed_user(uid):
            await update.message.reply_text(
                f"Пользователь {uid} уже находится в списке подписчиков."
            )
        else:
            database.add_allowed_user(uid)
            await update.message.reply_text(
                f"Пользователь {uid} добавлен в список подписчиков."
            )
    except Exception:
        await update.message.reply_text(
            "Произошла ошибка при добавлении пользователя."
        )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END


def register_handlers(application: Application) -> None:
    """Register all command, conversation and callback handlers with the application."""
    # Core commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("catalog", catalog))
    application.add_handler(CommandHandler("admin", admin_panel))

    # Add book conversation
    addbook_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_book_entry, pattern="^admin_addbook$")],
        states={
            ADD_BOOK_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_title)],
            ADD_BOOK_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_description)],
            ADD_BOOK_COVER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_book_cover)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(addbook_conv)

    # Add chapter conversation
    addchapter_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_chapter_entry, pattern="^admin_addchapter$")],
        states={
            CHOOSE_BOOK: [CallbackQueryHandler(choose_book, pattern=r"^choose_book_\d+$")],
            CHAPTER_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_title)],
            CHAPTER_CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, chapter_content)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(addchapter_conv)

    # Add subscriber conversation
    addsubscriber_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_subscriber_entry, pattern="^admin_addsubscriber$")],
        states={
            ADD_ALLOWED_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_subscriber_id)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(addsubscriber_conv)