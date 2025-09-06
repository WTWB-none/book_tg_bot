# Развертывание Book Bot на удаленном сервере

## Подготовка сервера

### 1. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python 3.11+
sudo apt install python3 python3-pip python3-venv -y

# Установка Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка nginx (опционально, для продакшена)
sudo apt install nginx -y

# Установка systemd (для автозапуска)
sudo apt install systemd -y
```

### 2. Настройка проекта

```bash
# Клонирование или загрузка проекта
git clone <your-repo> book-bot
cd book-bot

# Создание виртуального окружения Python
python3 -m venv venv
source venv/bin/activate

# Установка Python зависимостей
pip install -r requirements.txt

# Сборка Vue webapp
cd webapp
npm install
npm run build
cd ..
```

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Telegram Bot Token
export TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Server URL (замените на ваш домен)
export SERVER_URL="https://yourdomain.com/"

# Admin User IDs (через запятую)
export ADMIN_USER_IDS="123456789,987654321"

# Tribute API Key (если используется)
export TRIBUTE_API_KEY="your_api_key_here"
```

### 4. Настройка systemd сервиса

Создайте файл `/etc/systemd/system/book-bot.service`:

```ini
[Unit]
Description=Book Bot Telegram Bot
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/book-bot
Environment=PATH=/path/to/book-bot/venv/bin
ExecStart=/path/to/book-bot/venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. Настройка nginx (опционально)

Создайте файл `/etc/nginx/sites-available/book-bot`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL certificates (настройте SSL)
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Serve static files
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API endpoints
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. Запуск сервисов

```bash
# Активация nginx сайта
sudo ln -s /etc/nginx/sites-available/book-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Запуск бота
sudo systemctl enable book-bot
sudo systemctl start book-bot

# Проверка статуса
sudo systemctl status book-bot
```

## Проверка работы

1. **Проверьте логи бота:**

   ```bash
   sudo journalctl -u book-bot -f
   ```

2. **Проверьте доступность веб-приложения:**

   ```bash
   curl https://yourdomain.com/
   ```

3. **Проверьте API:**
   ```bash
   curl https://yourdomain.com/api/books
   ```

## Обновление конфигурации бота

Обновите `bot/config.py`:

```python
# Замените localhost на ваш домен
SERVER_URL = "https://yourdomain.com/"
```

## Мониторинг

- **Логи бота:** `sudo journalctl -u book-bot -f`
- **Логи nginx:** `sudo tail -f /var/log/nginx/access.log`
- **Статус сервисов:** `sudo systemctl status book-bot nginx`

## Резервное копирование

```bash
# Создание бэкапа базы данных
cp app.db app.db.backup.$(date +%Y%m%d_%H%M%S)

# Создание полного бэкапа
tar -czf book-bot-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
    --exclude=venv \
    --exclude=webapp/node_modules \
    --exclude=webapp/dist \
    .
```
