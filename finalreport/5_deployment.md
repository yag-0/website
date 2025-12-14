# Посібник з розгортання Flask Market

## Зміст
1. [Системні вимоги](#системні-вимоги)
2. [Встановлення локально](#встановлення-локально)
3. [Розгортання через Docker](#розгортання-через-docker)
4. [Розгортання на хостингу](#розгортання-на-хостингу)
5. [Змінні середовища](#змінні-середовища)
6. [Налаштування production](#налаштування-production)
7. [Резервне копіювання](#резервне-копіювання)
8. [Моніторинг](#моніторинг)

---

## Системні вимоги

### Мінімальні вимоги
- **OS:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+, Debian 10+)
- **CPU:** 1 core (2+ рекомендовано)
- **RAM:** 512 MB (2 GB+ рекомендовано)
- **Диск:** 1 GB вільного місця
- **Python:** 3.11 або новіший
- **Docker:** 20.10+ (для контейнеризації)

### Рекомендовані вимоги для production
- **CPU:** 4 cores
- **RAM:** 4 GB+
- **Диск:** SSD з 20 GB+
- **Мережа:** 100 Mbps+

---

## Встановлення локально

### Крок 1: Клонування репозиторію

```bash
# HTTPS
git clone https://github.com/yag-0/website

# SSH
git clone git@github.com:yag-0/website

cd lab03-flaskProject
```

### Крок 2: Створення віртуального середовища

**Windows:**
```powershell
# Створення venv
python -m venv venv

# Активація
.\venv\Scripts\Activate.ps1

# Якщо помилка ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/macOS:**
```bash
# Створення venv
python3 -m venv venv

# Активація
source venv/bin/activate
```

### Крок 3: Встановлення залежностей

```bash
# Оновлення pip
pip install --upgrade pip

# Встановлення пакетів
pip install -r requirements.txt
```

**Список залежностей (requirements.txt):**
```txt
Flask==3.0.0
Werkzeug==3.0.1
flasgger==0.9.7.1
Flask-CORS==4.0.0
rpds-py==0.18.0
```

### Крок 4: Ініціалізація бази даних

```bash
# Запуск Python REPL
python

# В Python shell:
>>> from models import init_db
>>> init_db()
>>> exit()
```

Або автоматично при першому запуску:
```bash
python app.py
```

### Крок 5: Запуск сервера

**Development режим:**
```bash
# Запуск з auto-reload
python app.py

# Або через Flask CLI
flask run

# З вказанням host і port
flask run --host=0.0.0.0 --port=5000
```

**Відкриття в браузері:**
```
http://localhost:5000
```

### Крок 6: Перевірка роботи

1. Відкрийте http://localhost:5000
2. Перейдіть в каталог товарів
3. Додайте товар в кошик
4. Перевірте API: http://localhost:5000/apidocs

**Тестовий запит:**
```bash
curl http://localhost:5000/api/products
```

---

## Розгортання через Docker

### Переваги Docker
- ✅ Ізольоване середовище
- ✅ Легке розгортання
- ✅ Однакова поведінка на всіх системах
- ✅ Швидке масштабування

### Крок 1: Встановлення Docker

**Windows/macOS:**
- Завантажте Docker Desktop: https://www.docker.com/products/docker-desktop

**Linux (Ubuntu/Debian):**
```bash
# Оновлення пакетів
sudo apt update

# Встановлення Docker
sudo apt install docker.io docker-compose -y

# Додавання користувача до групи docker
sudo usermod -aG docker $USER

# Перезавантаження сесії
newgrp docker
```

### Крок 2: Структура Docker файлів

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: flask_market
    ports:
      - "5000:5000"
    volumes:
      - ./site.db:/app/site.db
      - ./static:/app/static
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-dev-secret-key-change-in-production}
    restart: unless-stopped
```

**.dockerignore:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.env
.git/
.gitignore
*.md
Dockerfile
docker-compose.yml
```

### Крок 3: Збірка і запуск

**Збірка образу:**
```bash
docker-compose build
```

**Запуск контейнера:**
```bash
# Запуск в фоновому режимі
docker-compose up -d

# Перегляд логів
docker-compose logs -f

# Зупинка
docker-compose down
```

**Перевірка стану:**
```bash
# Список контейнерів
docker ps

# Статус сервісу
docker-compose ps
```

### Крок 4: Управління Docker контейнером

```bash
# Перезапуск
docker-compose restart

# Зупинка
docker-compose stop

# Видалення контейнера і образів
docker-compose down --rmi all

# Перегляд логів останніх 100 рядків
docker-compose logs --tail=100

# Виконання команд в контейнері
docker-compose exec web bash

# Резервна копія БД
docker cp flask_market:/app/site.db ./backup_site.db
```

---

## Розгортання на хостингу

### Heroku

**Крок 1: Підготовка файлів**

**Procfile:**
```
web: gunicorn app:app
```

**runtime.txt:**
```
python-3.11.7
```

**requirements.txt (додати):**
```
gunicorn==21.2.0
```

**Крок 2: Розгортання**
```bash
# Встановлення Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Логін
heroku login

# Створення додатку
heroku create flask-market-app

# Розгортання
git push heroku main

# Відкриття в браузері
heroku open

# Перегляд логів
heroku logs --tail
```

### DigitalOcean (VPS)

**Крок 1: Створення Droplet**
1. Зареєструйтеся на DigitalOcean
2. Створіть Droplet (Ubuntu 22.04, Basic plan)
3. Підключіться через SSH

**Крок 2: Налаштування сервера**
```bash
# Підключення
ssh root@your_server_ip

# Оновлення системи
apt update && apt upgrade -y

# Встановлення Python та залежностей
apt install python3 python3-pip python3-venv nginx -y

# Створення користувача
adduser flaskapp
usermod -aG sudo flaskapp
su - flaskapp
```

**Крок 3: Клонування проекту**
```bash
cd /home/flaskapp
git clone https://github.com/yag-0/website
cd lab03-flaskProject

# Налаштування venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

**Крок 4: Налаштування Gunicorn**

**gunicorn.service:**
```ini
[Unit]
Description=Gunicorn instance for Flask Market
After=network.target

[Service]
User=flaskapp
Group=www-data
WorkingDirectory=/home/flaskapp/lab03-flaskProject
Environment="PATH=/home/flaskapp/lab03-flaskProject/venv/bin"
ExecStart=/home/flaskapp/lab03-flaskProject/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

**Встановлення сервісу:**
```bash
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

**Крок 5: Налаштування Nginx**

**/etc/nginx/sites-available/flaskmarket:**
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/flaskapp/lab03-flaskProject/static;
        expires 30d;
    }
}
```

**Активація:**
```bash
sudo ln -s /etc/nginx/sites-available/flaskmarket /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Крок 6: SSL сертифікат (Let's Encrypt)**
```bash
# Встановлення certbot
sudo apt install certbot python3-certbot-nginx -y

# Отримання сертифіката
sudo certbot --nginx -d your_domain.com

# Автоматичне оновлення
sudo systemctl status certbot.timer
```

### Railway.app (найпростіший варіант)

1. Зареєструйтеся на https://railway.app
2. Підключіть GitHub репозиторій
3. Railway автоматично визначить Flask проект
4. Додайте змінні середовища
5. Розгортання відбудеться автоматично

---

## Змінні середовища

### .env файл

**Приклад .env:**
```bash
# Flask налаштування
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this-in-production

# База даних
DATABASE_URL=sqlite:///site.db

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Admin панель
ADMIN_PASSWORD=change-this-strong-password

# Email (для сповіщень)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Завантаження змінних у Python

**app.py:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '123')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///site.db')
```

**Встановлення python-dotenv:**
```bash
pip install python-dotenv
```

---

## Налаштування production

### 1. Безпека

**app.py (додати):**
```python
from flask_talisman import Talisman

# HTTPS примус
if os.getenv('FLASK_ENV') == 'production':
    Talisman(app, force_https=True)

# Безпечні cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Захист від CSRF
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)
```

### 2. Logging

**logging_config.py:**
```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not app.debug:
        # Файловий handler
        file_handler = RotatingFileHandler(
            'app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask Market startup')
```

**Використання:**
```python
from logging_config import setup_logging
setup_logging(app)
```

### 3. Database

**Міграція на PostgreSQL:**
```python
# requirements.txt
psycopg2-binary==2.9.9

# models.py
import os
from urllib.parse import urlparse

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///site.db')

if DATABASE_URL.startswith('postgres://'):
    # Heroku postgres URL fix
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
```

### 4. Caching

**Додати Redis кешування:**
```python
# requirements.txt
redis==5.0.1
flask-caching==2.1.0

# app.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0')
})

@app.route('/api/products')
@cache.cached(timeout=300)  # 5 хвилин
def get_products():
    # ...
```

### 5. Rate Limiting

```python
# requirements.txt
flask-limiter==3.5.0

# app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)

@app.route('/api/orders', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    # ...
```

---

## Резервне копіювання

### Автоматичний бекап SQLite

**backup.sh:**
```bash
#!/bin/bash

# Конфігурація
DB_PATH="/home/flaskapp/lab03-flaskProject/site.db"
BACKUP_DIR="/home/flaskapp/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/site_$DATE.db"

# Створення директорії
mkdir -p $BACKUP_DIR

# Копіювання БД
cp $DB_PATH $BACKUP_FILE

# Стискання
gzip $BACKUP_FILE

# Видалення старих бекапів (старіші 30 днів)
find $BACKUP_DIR -type f -name "*.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

**Налаштування cron:**
```bash
# Редагування crontab
crontab -e

# Додати рядок (щоденний бекап о 3:00 ночі)
0 3 * * * /home/flaskapp/backup.sh >> /home/flaskapp/backup.log 2>&1
```

### Бекап через Docker

```bash
# Скрипт для бекапу Docker volume
docker run --rm \
  --volumes-from flask_market \
  -v $(pwd)/backups:/backup \
  ubuntu tar czf /backup/site_$(date +%Y%m%d).tar.gz /app/site.db
```

---

## Моніторинг

### 1. Health Check Endpoint

**app.py:**
```python
@app.route('/health')
def health():
    try:
        # Перевірка БД
        conn = get_db_connection()
        conn.execute('SELECT 1').fetchone()
        conn.close()
        return {'status': 'healthy', 'database': 'ok'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### 2. Prometheus Metrics

```python
# requirements.txt
prometheus-flask-exporter==0.23.0

# app.py
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)

# Метрики доступні на /metrics
```

### 3. Uptime Monitoring

Використовуйте сервіси:
- **UptimeRobot** (безкоштовно): https://uptimerobot.com
- **Pingdom**: https://www.pingdom.com
- **StatusCake**: https://www.statuscake.com

### 4. Error Tracking

**Sentry інтеграція:**
```python
# requirements.txt
sentry-sdk[flask]==1.40.0

# app.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

---

## Troubleshooting

### Проблема: Port 5000 вже зайнятий

**Рішення:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5000
kill -9 <PID>

# Або використайте інший порт
flask run --port=5001
```

### Проблема: Permission denied на Linux

**Рішення:**
```bash
# Надати права на виконання
chmod +x app.py

# Або запустити з sudo (не рекомендовано)
sudo python3 app.py
```

### Проблема: Docker image занадто великий

**Рішення - Multi-stage build:**
```dockerfile
# Етап 1: Збірка
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Етап 2: Production
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

---

## Чеклист перед Production

- [ ] Змінити SECRET_KEY
- [ ] Змінити ADMIN_PASSWORD
- [ ] Налаштувати HTTPS (SSL)
- [ ] Увімкнути CSRF захист
- [ ] Налаштувати logging
- [ ] Налаштувати бекапи
- [ ] Додати health check endpoint
- [ ] Налаштувати моніторинг
- [ ] Протестувати навантаження
- [ ] Налаштувати firewall
- [ ] Оновити DNS записи
- [ ] Додати rate limiting
- [ ] Перевірити CORS налаштування
- [ ] Налаштувати CDN для статики
- [ ] Додати error tracking (Sentry)

---

## Висновок

Flask Market можна розгорнути різними способами - від локального запуску для розробки до повноцінного production deployment на хостингу. Docker спрощує процес розгортання та забезпечує однакову поведінку на всіх платформах.

**Рекомендації:**
- Для розробки: локальний запуск з auto-reload
- Для тестування: Docker Compose
- Для production: VPS (DigitalOcean) з Nginx + Gunicorn + SSL

Не забувайте про безпеку, моніторинг та регулярні бекапи! 🚀
