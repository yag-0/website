# Звіт з контейнеризації проєкту Flask Market

## Огляд проєкту

Flask Market — це веб-застосунок інтернет-магазину, розроблений на Python з використанням фреймворку Flask. Проект включає:

- **Веб-інтерфейс** для перегляду товарів, оформлення замовлень та управління корзиною
- **REST API** з документацією Swagger/Flasgger
- **SQLite базу даних** для зберігання інформації про:
  - Товари (products)
  - Замовлення (orders)
  - Клієнтів (customers)
  - Промо-коди (promo_codes)
  - Зворотний зв'язок (feedback)
- **CORS підтримка** для кросс-доменних запитів
- **Адмін-панель** для управління змістом

## Архітектура контейнерного рішення

### Docker образ

- **Базовий образ**: `python:3.11-slim` (250 МБ)
- **Розмір фінального образу**: 358 МБ
- **Багатоетапна збірка**: Ні (використовується однієтапна збірка для спрощення)
- **Встановлені інструменти**: `wget` для healthcheck

### Docker Compose

- **Кількість сервісів**: 1 (web service)
- **Використовувані volumes**: 
  - Bind mount: `./site.db:/app/data/database.db` — синхронізація бази даних між хостом та контейнером
- **Мережа**: Автоматична внутрішня мережа Docker Compose
- **Порти**: `5000:5000` (HTTP)
- **Healthcheck**: Включений (перевіряє `/` кожні 30 секунд)

### Залежності

```
Flask==3.0.0           # Web framework
Werkzeug==3.0.1        # WSGI utility library
flasgger==0.9.7.1      # Swagger/OpenAPI documentation
Flask-Cors==4.0.0      # Cross-origin resource sharing
rpds-py==0.18.0        # Rust-backed Python data structures
```

## Прийняті рішення та обґрунтування

### Вибір базового образу

**`python:3.11-slim`** обраний замість `python:3.11-alpine` тому що:
- Alpine використовує musl libc, що призводить до проблем із `rpds-py` (ModuleNotFoundError: rpds.rpds)
- Slim базується на Debian з гліб і має готові wheels для всіх пакетів
- Розмір (358 МБ) залишається компактним для production-use

### Організація збереження даних

**Bind mount** замість Docker volume використовується тому що:
- SQLite базу `site.db` можна редагувати локально та в контейнері одночасно
- Дані автоматично синхронізуються в обидві сторони
- Локально запущений Flask app та контейнер використовують одну базу
- Питання: "Якщо я вносити зміни коли запущений через докер, а потім відкрию через app.py — дані синхронізуються?" **Відповідь: Так**

### Налаштування Flask

- **HOST**: `0.0.0.0` — дозволяє підключення з зовні контейнера
- **DEBUG mode**: Включений для розробки (замінити на `False` для production)
- **환境 змінні**:
  - `FLASK_APP=app.py`
  - `FLASK_ENV=production`
  - `DATABASE_PATH=/app/data/database.db`
  - `SECRET_KEY=default-secret-key` (змінити для production)

### Оптимізації

1. **Кеш pip**: `--no-cache-dir` зменшує розмір образу
2. **Мінімальна система**: `apt-get` очищується після встановлення `wget`
3. **Healthcheck**: Автоматична перевірка доступності сервісу
4. **Single-stage build**: Спростити процес, оскільки multi-stage не давав переваг

## Інструкції з розгортанням

### Передумови

- Docker Desktop або Docker Engine
- Docker Compose
- (Опціонально) Python 3.11+ для локального розвитку

### Швидкий старт

```bash
# 1. Перейдіть в директорію проекту
cd lab03-flaskProject

# 2. Запустіть контейнер
docker-compose up -d

# 3. Перевірте статус
docker-compose ps

# 4. Переходьте на http://localhost:5000
```

### Детальні кроки

#### Побудова образу з нуля

```bash
# Видалити всі старі контейнери та volumes
docker-compose down -v

# Перебудувати образ без кешу
docker-compose build --no-cache

# Запустити контейнер
docker-compose up -d
```

#### Перевірка логів

```bash
# Остання 50 рядків логів
docker-compose logs -n 50 web

# Слідкування за логами в реальному часі
docker-compose logs -f web
```

#### Доступ до контейнера

```bash
# Запустити shell команду в контейнері
docker-compose exec web sh

# Запустити Python скрипт
docker-compose exec web python -c "import sqlite3; ..."
```

#### Копіювання файлів

```bash
# Скопіювати файл з контейнера на хост
docker cp flask_app:/app/data/database.db ./backup.db

# Скопіювати файл з хосту в контейнер
docker cp ./site.db flask_app:/app/data/database.db
```

### Доступні URL

- **Домашня сторінка**: http://localhost:5000/
- **API документація**: http://localhost:5000/apidocs/
- **Health endpoint**: http://localhost:5000/health
- **Про сайт**: http://localhost:5000/about

### Локальний розвиток (без Docker)

```bash
# 1. Створити віртуальне середовище
python -m venv .venv

# 2. Активувати середовище
.\.venv\Scripts\Activate  # Windows
source .venv/bin/activate # Linux/Mac

# 3. Встановити залежності
pip install -r requirements.txt

# 4. Запустити додаток
python app.py

# Додаток буде доступний на http://localhost:5000
```

## Можливі покращення

### Для Production

1. **WSGI сервер**: Замінити Flask dev server на Gunicorn або uWSGI
   ```dockerfile
   RUN pip install gunicorn
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. **Відокремлення змінних**: Використовувати `.env` з хоста
   ```yaml
   env_file:
     - .env.production
   ```

3. **Database**: Замінити SQLite на PostgreSQL для production
   ```yaml
   services:
     postgres:
       image: postgres:15-alpine
       environment:
         POSTGRES_PASSWORD: secret
   ```

4. **Nginx reverse proxy**: Додати фронтенд прокси
   ```yaml
   services:
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
   ```

5. **Security**:
   - Змінити `DEBUG=False`
   - Встановити `SECRET_KEY` з середовища
   - Додати HTTPS сертифікати
   - Використовувати читання-тільки (ro) для певних volumes

6. **Logging**: Налаштувати centralised logging (ELK stack, Splunk)

7. **監視**: Додати Prometheus metrics та Grafana dashboard

### Для розвитку

1. **Volume для hot-reload**: 
   ```yaml
   volumes:
     - ./app.py:/app/app.py
   ```

2. **Database migration tool**: Alembic для версіонування схеми

3. **Testing**: Docker service для запуску тестів
   ```bash
   docker-compose exec web pytest
   ```

4. **Lint/Format**: Pre-commit hooks для перевірки коду
   ```bash
   pip install pre-commit black flake8
   ```

## Результати тестування

### Холодний старт (з нуля)

```
✓ Видалення контейнерів та volumes
✓ Побудова образу без кешу (21 сек)
✓ Запуск контейнера (0.5 сек)
✓ Healthcheck проходить (healthy)
✓ API доступний на http://localhost:5000
✓ Дані в БД синхронізовані
```

### Розмір образу

```
Repository            Tag    Size
lab03-flaskproject-web latest 358MB
```

### Здоров'я контейнера

```
Status: Up 12 seconds (healthy)
Ports:  0.0.0.0:5000->5000/tcp
```

## Висновки

### Що було досягнуто

1. ✅ **Успішна контейнеризація**: Flask додаток працює в Docker
2. ✅ **Синхронізація даних**: SQLite база синхронізується між хостом та контейнером
3. ✅ **Zero-to-production**: Проект запускається з нуля без помилок
4. ✅ **Healthcheck**: Автоматична перевірка доступності
5. ✅ **Зручність**: Один команда `docker-compose up -d` запускає все

### Виклики та вирішення

| Виклик | Рішення |
|--------|---------|
| rpds.rpds ModuleNotFoundError | Замінити alpine на slim image |
| Flask слухає тільки на localhost | Встановити FLASK_RUN_HOST=0.0.0.0 |
| Пусті дані в контейнері | Використати bind mount для site.db |
| Healthcheck не працює | Встановити wget в Dockerfile |

### Практичне застосування

Цей setup готовий для:
- **Розробки**: Дані синхронізуються, дебаг режим включений
- **Тестування**: Швидко спинути та запустити чисту копію
- **Demo**: Одна команда для розгортання
- **Migration to production**: Достатньо додати WSGI сервер та database

---

