"""
Configuration for the book bot.

Place your sensitive values such as the Telegram bot token and Tribute API
key into environment variables.  You can also hard‑code values here, but
this is not recommended for production.
"""

import os


# Telegram bot token.  You should set an environment variable
# ``TELEGRAM_BOT_TOKEN`` or replace the placeholder below with your
# actual token.
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

# Tribute API configuration.  In order to verify subscriptions via the
# remote service the bot makes authenticated HTTP requests using this
# API key.
TRIBUTE_API_URL = "https://tribute.tg/api/v1/subscribers"
TRIBUTE_API_KEY = os.environ.get("TRIBUTE_API_KEY", "")

# List of administrator Telegram user IDs.  Only these users can add
# books, chapters or manual subscribers.  Populate this list with your
# own Telegram ID(s).
ADMIN_USER_IDS: list[int] = [793857218]

# The URL where the web application will be accessible.  The bot
# appends a ``?uid=<telegram_id>`` query parameter when sending this
# link to users.
# For production, replace with your actual domain:
# SERVER_URL = "https://yourdomain.com/"
# For Telegram Mini App, use HTTPS URL (required by Telegram)
# For Netlify deployment:
SERVER_URL = "https://your-site-name.netlify.app/"  # Replace with your Netlify site URL
# For local development with ngrok or similar:
# SERVER_URL = "https://your-ngrok-url.ngrok.io/"

# Path to the SQLite database.  The database stores books, chapters and
# allowed subscribers.  It is created automatically on first run.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_FILE = os.path.join(BASE_DIR, "app.db")