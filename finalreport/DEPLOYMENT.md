# 🚀 Посібник розгортання Flask Market

## Передумови

- Python 3.11+
- Docker & Docker Compose (для контейнеризації)
- Git (для контролю версій)
- Доступ до Linux VPS або хостингу

## Чеклист перед розгортанням

### 1. Підготовка коду

```bash
# Перевірити готовність до розгортання
python check_deployment.py

# Запустити тести локально
python test_local.py

# Генерувати безпечні ключи
python generate_secrets.py
```

### 2. Налаштування змінних середовища

Скопіюйте `.env.example` в `.env.production`:

```bash
cp .env.example .env.production
```

Оновіть файл на сервері:

```bash
# Генеруйте SECRET_KEY
python generate_secrets.py

# Заповніть значення в .env.production:
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=<random-key-here>
DATABASE_PATH=/app/data/database.db
ADMIN_PASSWORD=<strong-password>
SECRET_KEY=<your-secret-key>
CORS_ORIGINS=https://yourdomain.com
```

**❌ ВАЖНО: Ніколи не комітьте `.env` у репозиторій!**

### 3. Перевірка Git конфігурації

```bash
# Переконайтеся що .env в .gitignore
cat .gitignore | grep -E "^\.env"

# Видалити .env якщо він був скомічений (не робіть це на production!)
git rm --cached .env 2>/dev/null || true
git rm --cached .env.production 2>/dev/null || true
```

## Розгортання варіанти

### Варіант 1: Docker Compose (рекомендовано)

#### Локально

```bash
# Збірка образу
docker-compose build

# Запуск
docker-compose up -d

# Перегляд логів
docker-compose logs -f

# Тестування
curl http://localhost:5000/health
```

#### На сервері (Linux/DigitalOcean)

```bash
# SSH підключення
ssh user@your_server_ip

# Клонування репозиторію
git clone https://github.com/yourusername/lab03-flaskProject.git
cd lab03-flaskProject

# Копіювання .env.production у .env
cp .env.production .env

# Запуск Docker
docker-compose pull  # Оновити образи
docker-compose up -d

# Перевірка
docker-compose ps
docker-compose logs -f
```

#### Nginx + Docker (з reverse proxy)

```nginx
# /etc/nginx/sites-available/flaskmarket

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/static;
        expires 30d;
    }
}
```

### Варіант 2: Локальний запуск (development)

```bash
# Активація venv
source venv/bin/activate  # Linux/macOS
./venv/Scripts/Activate.ps1  # Windows

# Встановлення залежностей
pip install -r requirements.txt

# Запуск
python app.py
```

### Варіант 3: Gunicorn + Systemd (advanced)

```bash
# Встановлення Gunicorn
pip install gunicorn

# Створення systemd сервісу
sudo tee /etc/systemd/system/flaskmarket.service > /dev/null <<EOF
[Unit]
Description=Flask Market Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/flaskmarket
Environment="PATH=/var/www/flaskmarket/venv/bin"
ExecStart=/var/www/flaskmarket/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
KillSignal=SIGTERM
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Включення сервісу
sudo systemctl daemon-reload
sudo systemctl enable flaskmarket
sudo systemctl start flaskmarket
sudo systemctl status flaskmarket
```

## SSL/HTTPS Налаштування

### Автоматичне з Let's Encrypt

```bash
# Встановлення certbot
sudo apt-get install certbot python3-certbot-nginx

# Отримання сертифіката
sudo certbot --nginx -d yourdomain.com

# Автоматичне поновлення
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Docker + Let's Encrypt

```bash
# Додати Nginx контейнер в docker-compose.yml
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - web
```

## Резервне копіювання

### Автоматичний бекап (cron)

```bash
# Додати в crontab (щоденно о 3:00)
0 3 * * * /path/to/backup.sh

# /path/to/backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/flaskmarket"
mkdir -p $BACKUP_DIR
cp /app/data/database.db $BACKUP_DIR/site_$DATE.db.gz
find $BACKUP_DIR -type f -mtime +30 -delete
```

### Docker бекап

```bash
# Бекап БД з контейнера
docker cp flask_market_app:/app/data/database.db ./backup_$(date +%Y%m%d).db

# Автоматичний бекап
docker run --rm \
  --volumes-from flask_market_app \
  -v $(pwd)/backups:/backup \
  ubuntu tar czf /backup/db_$(date +%Y%m%d).tar.gz /app/data/
```

## Моніторинг & Logging

### Docker логи

```bash
# Реальні логи
docker-compose logs -f

# Останні 100 рядків
docker-compose logs --tail=100

# Логи конкретного сервісу
docker-compose logs -f web
```

### Health check

```bash
# Перевірити статус
curl http://localhost:5000/health

# Очікуємо: {"status": "healthy", "database": "connected"}
```

### Моніторинг з Prometheus (опціонально)

```python
# Додати в requirements.txt
prometheus-flask-exporter==0.23.0

# app.py
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

# Метрики доступні на /metrics
```

## Відновлення з бекапу

```bash
# Зупинення контейнера
docker-compose down

# Восстановлення БД
docker cp ./backup_20250101.db flask_market_app:/app/data/database.db

# Запуск
docker-compose up -d
```

## Оновлення застосунку

```bash
# Git pull новітних змін
git pull origin main

# Оновлення залежностей
pip install -r requirements.txt

# Docker: пересбір образу
docker-compose build --no-cache

# Docker: перезапуск
docker-compose up -d
```

## Розв'язання проблем

### Docker контейнер не запускається

```bash
# Перевірити логи
docker-compose logs web

# Скинути контейнер
docker-compose down -v
docker-compose up -d

# Перевірити образ
docker images | grep flaskmarket
```

### Помилка підключення до БД

```bash
# Перевірити БД права
docker exec flask_market_app ls -la /app/data/

# Перевірити volume
docker volume ls | grep flask

# Пересоздати volume
docker-compose down -v
docker-compose up -d
```

### High CPU/Memory usage

```bash
# Перевірити статистику контейнера
docker stats flask_market_app

# Обмежити ресурси в docker-compose
services:
  web:
    mem_limit: 512m
    cpus: 0.5
```

## Security Best Practices

- ✅ Змініть SECRET_KEY та ADMIN_PASSWORD
- ✅ Включіть HTTPS (SSL сертифікати)
- ✅ Обмежте CORS на дозволені domains
- ✅ Налаштуйте rate limiting
- ✅ Регулярно оновлюйте залежності
- ✅ Установіть fail2ban для DDoS захисту
- ✅ Налаштуйте firewall (UFW)
- ✅ Включіть 2FA для SSH

```bash
# UFW firewall rules
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable
```

## Команди Docker для production

```bash
# Зупинення з очищенням
docker-compose down -v

# Збільшення кількості workers
docker-compose up -d --scale web=3

# Перезапуск одного сервісу
docker-compose restart web

# Інтерактивна оболонка контейнера
docker-compose exec web bash

# Видалення old образів
docker image prune -a
```

## Monitoring Dashboard

Налаштуйте моніторинг через:
- **UptimeRobot**: https://uptimerobot.com
- **Sentry**: https://sentry.io (error tracking)
- **Prometheus + Grafana**: для метрик
- **ELK Stack**: для логування

## Contacts & Support

- 📧 Email: support@flaskmarket.com
- 🐛 Issues: GitHub Issues
- 📱 Telegram: @FlaskMarketBot

---

**Остання оновлення:** 2025-12-14  
**Версія:** 1.0.0
