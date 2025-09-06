"""
Entry point for running the book bot and web server.

This script initialises the database, starts the Flask web server in a
background thread and launches the Telegram bot using python‑telegram‑bot.
"""

from __future__ import annotations

import threading

from telegram.ext import Application

from . import config, database, server, handlers


def main() -> None:
    # Initialise the database
    database.init_db()

    # Create and start the Flask web server in a separate thread
    flask_app = server.create_app()

    def run_flask() -> None:
        # Bind to all interfaces on port 8000; adjust as needed
        flask_app.run(host="0.0.0.0", port=8000)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Build the Telegram bot application
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Expose the server URL to handlers via bot_data (if needed)
    application.bot_data["server_url"] = config.SERVER_URL

    # Register command and conversation handlers
    handlers.register_handlers(application)

    # Start polling
    application.run_polling()


if __name__ == "__main__":
    main()