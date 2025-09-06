"""
Flask application exposing the HTTP API and serving the Vue web app.

The endpoints defined here are consumed by the front‑end.  They rely on
the database module for data retrieval and reuse the same subscription
logic used by the bot.
"""

from __future__ import annotations

import os
import datetime as _dt
from flask import Flask, jsonify, send_from_directory, abort
from flask_cors import CORS
import requests

from . import config, database


def create_app() -> Flask:
    """Create and configure the Flask application."""
    # Locate the built webapp directory (../webapp/dist relative to this file)
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "webapp", "dist")
    app = Flask(__name__, static_folder=static_dir, static_url_path="/")
    
    # Enable CORS for Telegram Mini App
    CORS(app, origins=[
        "https://web.telegram.org",
        "https://telegram.org",
        "https://t.me",
        "https://*.telegram.org",
        "https://*.t.me"
    ])

    @app.route("/api/books")
    def api_books() -> any:
        try:
            books = database.get_books_summary()
            return jsonify(books)
        except Exception:
            return jsonify([])

    @app.route("/api/book/<int:book_id>")
    def api_book(book_id: int) -> any:
        book = database.get_book_detail(book_id)
        if book is None:
            abort(404)
        return jsonify(book)

    @app.route("/api/book/<int:book_id>/chapter/<int:chapter_id>")
    def api_chapter(book_id: int, chapter_id: int) -> any:
        chapter = database.get_chapter_detail(book_id, chapter_id)
        if chapter is None:
            abort(404)
        return jsonify(chapter)

    @app.route("/api/verify/<int:telegram_user_id>")
    def api_verify(telegram_user_id: int) -> any:
        # Check local allowed users first
        if database.is_allowed_user(telegram_user_id):
            return jsonify({"subscribed": True})
        # Fallback to Tribute API
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
                            expire_dt = _dt.datetime.fromisoformat(
                                expire_str.replace("Z", "+00:00")
                            )
                            if expire_dt > now:
                                return jsonify({"subscribed": True})
                        except Exception:
                            pass
            return jsonify({"subscribed": False})
        except Exception:
            return jsonify({"subscribed": False})

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_vue(path: str) -> any:
        # Serve static assets for the Vue SPA; fall back to index.html
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app