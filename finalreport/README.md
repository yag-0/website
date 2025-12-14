# Flask Market - Інтернет-магазин електроніки

![Flask](https://img.shields.io/badge/Flask-3.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

Сучасний веб-застосунок для інтернет-магазину електроніки з інтуїтивним інтерфейсом, REST API та підтримкою темної теми.

---

## 📋 Зміст
- [Огляд](#огляд)
- [Особливості](#особливості)
- [Технології](#технології)
- [Швидкий старт](#швидкий-старт)
- [Встановлення](#встановлення)
- [Використання](#використання)
- [API](#api)
- [Docker](#docker)
- [Структура проекту](#структура-проекту)
- [Конфігурація](#конфігурація)
- [Тестування](#тестування)
- [Документація](#документація)
- [Ліцензія](#ліцензія)

---

## 🎯 Огляд

**Flask Market** - це повнофункціональний інтернет-магазин з підтримкою:
- 🛒 Каталогу товарів з фільтрацією
- 🛍️ Системи кошика покупок
- 🎟️ Промокодів та знижок
- 💬 Відгуків користувачів
- 🌙 Темної/світлої теми
- ⌨️ Клавіатурної навігації
- 🔌 RESTful API
- 📱 Адаптивного дизайну

**Demo:** http://localhost:5000  
**API Docs:** http://localhost:5000/apidocs

---

## ✨ Особливості

### Для користувачів
- ✅ **Зручний каталог** - перегляд товарів з категоріями та пошуком
- ✅ **Кошик покупок** - додавання, зміна кількості, видалення товарів
- ✅ **Промокоди** - система знижок з валідацією
- ✅ **Відгуки** - можливість залишати відгуки про покупки
- ✅ **Темна тема** - комфортна робота вночі з збереженням налаштувань
- ✅ **Гарячі клавіші** - навігація за допомогою `Alt + H/M/C/R/A/D/T`
- ✅ **Адаптивний дизайн** - працює на всіх пристроях

### Для розробників
- ✅ **REST API** - повний CRUD для products, orders, feedback
- ✅ **Swagger UI** - інтерактивна документація API
- ✅ **Docker** - контейнеризація для легкого розгортання
- ✅ **SQLite** - легка БД (легко мігрувати на PostgreSQL)
- ✅ **CORS** - підтримка cross-origin requests
- ✅ **Модульна структура** - легко розширювати та підтримувати

### Для адміністраторів
- ✅ **Адмін-панель** - управління товарами, замовленнями, промокодами
- ✅ **Статистика** - аналітика продажів
- ✅ **Простота розгортання** - Docker Compose або локальний запуск

---

## 🛠 Технології

### Backend
| Технологія | Версія | Призначення |
|------------|--------|-------------|
| Python | 3.11+ | Мова програмування |
| Flask | 3.0.0 | Веб-фреймворк |
| Werkzeug | 3.0.1 | WSGI утиліти |
| SQLite | 3 | База даних |
| Flasgger | 0.9.7.1 | Swagger/OpenAPI документація |
| Flask-CORS | 4.0.0 | CORS підтримка |

### Frontend
| Технологія | Призначення |
|------------|-------------|
| Jinja2 | Шаблонізатор |
| Tailwind CSS | CSS фреймворк |
| Vanilla JS | Клієнтська логіка |
| HTML5 | Розмітка |

### DevOps
| Технологія | Призначення |
|------------|-------------|
| Docker | Контейнеризація |
| Docker Compose | Оркестрація контейнерів |
| Git | Контроль версій |

---

## 🚀 Швидкий старт

### Варіант 1: Docker (рекомендовано)

```bash
# Клонування репозиторію
git clone https://github.com/yag-0/website
cd lab03-flaskProject

# Запуск через Docker Compose
docker-compose up -d

# Відкрити в браузері
http://localhost:5000
```

### Варіант 2: Локально

```bash
# Клонування
git clone https://github.com/yag-0/website
cd lab03-flaskProject

# Створення віртуального середовища
python -m venv venv

# Активація (Windows)
.\venv\Scripts\Activate.ps1

# Активація (Linux/macOS)
source venv/bin/activate

# Встановлення залежностей
pip install -r requirements.txt

# Запуск
python app.py
```

Відкрийте http://localhost:5000 в браузері.

---

## 📦 Встановлення

### Передумови

**Обов'язково:**
- Python 3.11 або новіший
- pip (зазвичай встановлюється з Python)

**Опціонально:**
- Docker & Docker Compose (для контейнеризації)
- Git (для клонування репозиторію)

### Детальна інструкція

#### 1. Клонування проекту

```bash
git clone https://github.com/yag-0/website
cd lab03-flaskProject
```

#### 2. Налаштування Python

**Windows:**
```powershell
# Перевірка версії Python
python --version

# Створення venv
python -m venv venv

# Активація
.\venv\Scripts\Activate.ps1

# Якщо помилка ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/macOS:**
```bash
# Перевірка версії
python3 --version

# Створення venv
python3 -m venv venv

# Активація
source venv/bin/activate
```

#### 3. Встановлення залежностей

```bash
# Оновлення pip
pip install --upgrade pip

# Встановлення пакетів
pip install -r requirements.txt

# Перевірка встановлення
pip list
```

**requirements.txt:**
```txt
Flask==3.0.0
Werkzeug==3.0.1
flasgger==0.9.7.1
Flask-CORS==4.0.0
rpds-py==0.18.0
```

#### 4. Ініціалізація бази даних

```bash
# Автоматично при першому запуску app.py
# Або вручну:
python
>>> from models import init_db
>>> init_db()
>>> exit()
```

#### 5. Запуск застосунку

```bash
# Development режим
python app.py

# Або через Flask CLI
flask run

# З вказанням host і port
flask run --host=0.0.0.0 --port=5000 --debug
```

#### 6. Перевірка роботи

```bash
# Перевірка головної сторінки
curl http://localhost:5000

# Перевірка API
curl http://localhost:5000/api/products

# Або відкрийте в браузері
# http://localhost:5000
```

---

## 💻 Використання

### Веб-інтерфейс

#### Навігація
Використовуйте верхнє меню або гарячі клавіші:

| Клавіша | Дія |
|---------|-----|
| `Alt + H` | Головна сторінка |
| `Alt + M` | Каталог товарів |
| `Alt + C` | Кошик |
| `Alt + R` | Відгуки |
| `Alt + A` | Про нас |
| `Alt + D` | API документація |
| `Alt + T` | Перемкнути тему |

#### Каталог товарів
1. Перейдіть у "Каталог" (Alt + M)
2. Переглядайте товари
3. Фільтруйте за категоріями
4. Додавайте товари в кошик

#### Оформлення замовлення
1. Додайте товари в кошик
2. Перейдіть у кошик (Alt + C)
3. Перевірте вміст і кількість
4. Натисніть "Оформити замовлення"
5. Заповніть форму:
   - Ім'я
   - Email
   - Телефон
   - Адреса
   - Промокод (опціонально)
6. Підтвердіть замовлення

#### Промокоди
Приклади тестових промокодів:
- `WINTER25` - 25% знижка
- `SPRING20` - 20% знижка
- `FIRST10` - 10% знижка

#### Відгуки
1. Перейдіть у "Відгуки" (Alt + R)
2. Заповніть форму (ім'я, email, текст)
3. Натисніть "Надіслати відгук"
4. Відгук з'явиться на сторінці

#### Темна тема
- Натисніть іконку 🌙 у правому верхньому куті
- Або використайте `Alt + T`
- Налаштування зберігається в localStorage

---

## 🔌 API

### Базовий URL
```
http://localhost:5000/api
```

### Endpoints

#### Products
```http
# Отримати всі товари
GET /api/products

# Приклад відповіді
[
  {
    "id": 1,
    "name": "Ноутбук ASUS",
    "price": 25999.99,
    "stock": 15,
    "category": "Ноутбуки"
  }
]
```

#### Orders
```http
# Отримати всі замовлення
GET /api/orders

# Отримати замовлення за ID
GET /api/orders/{id}

# Створити замовлення
POST /api/orders
Content-Type: application/json

{
  "customer_name": "Іван Петренко",
  "customer_email": "ivan@example.com",
  "customer_phone": "+380501234567",
  "cart": { ... }
}

# Оновити статус замовлення
PUT /api/orders/{id}
Content-Type: application/json

{
  "status": "processing"
}

# Видалити замовлення
DELETE /api/orders/{id}
```

#### Feedback
```http
# Отримати всі відгуки
GET /api/feedback

# Створити відгук
POST /api/feedback
Content-Type: application/json

{
  "name": "Олена",
  "email": "olena@example.com",
  "message": "Чудовий магазин!"
}

# Видалити відгук
DELETE /api/feedback/{id}
```

### Swagger документація
Інтерактивна документація доступна за адресою:
```
http://localhost:5000/apidocs
```

### Приклади використання

**Python:**
```python
import requests

# Отримати товари
response = requests.get('http://localhost:5000/api/products')
products = response.json()

# Створити замовлення
order = {
    'customer_name': 'Тест',
    'customer_email': 'test@example.com',
    'customer_phone': '+380501234567',
    'cart': { ... }
}
response = requests.post('http://localhost:5000/api/orders', json=order)
```

**JavaScript:**
```javascript
// Отримати товари
fetch('http://localhost:5000/api/products')
  .then(res => res.json())
  .then(data => console.log(data));

// Створити відгук
fetch('http://localhost:5000/api/feedback', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Іван',
    email: 'ivan@example.com',
    message: 'Чудово!'
  })
});
```

**cURL:**
```bash
# Отримати товари
curl http://localhost:5000/api/products

# Створити замовлення
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Іван", ...}'
```

---

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### docker-compose.yml

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
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    restart: unless-stopped
```

### Команди Docker

```bash
# Збірка образу
docker-compose build

# Запуск контейнера
docker-compose up -d

# Перегляд логів
docker-compose logs -f

# Зупинка
docker-compose down

# Перезапуск
docker-compose restart

# Виконання команд в контейнері
docker-compose exec web bash

# Резервна копія БД
docker cp flask_market:/app/site.db ./backup.db
```

---

## 📁 Структура проекту

```
lab03-flaskProject/
│
├── app.py                 # Головний файл застосунку
├── models.py              # Моделі БД та функції
├── api.py                 # REST API Blueprint
├── requirements.txt       # Python залежності
├── site.db               # SQLite база даних
│
├── static/               # Статичні файли
│   ├── css/             # Стилі
│   ├── js/              # JavaScript
│   └── images/          # Зображення товарів
│
├── templates/            # Jinja2 шаблони
│   ├── base.html        # Базовий шаблон (навігація, теми)
│   ├── home.html        # Головна сторінка
│   ├── market.html      # Каталог товарів
│   ├── cart.html        # Кошик покупок
│   ├── reviews.html     # Відгуки (раніше HELP.html)
│   ├── about.html       # Про нас
│   ├── api-demo.html    # API демонстрація
│   └── admin/           # Адмін панель
│       ├── login.html
│       ├── index.html
│       ├── products.html
│       ├── orders.html
│       └── promo.html
│
├── finalreport/         # Документація
│   ├── 1_technical.md   # Технічна документація
│   ├── 2_database.md    # Схема БД
│   ├── 3_api.md         # API документація
│   ├── 4_user-guide.md  # Посібник користувача
│   ├── 5_deployment.md  # Посібник з розгортання
│   └── README.md        # Цей файл
│
├── Dockerfile            # Docker конфігурація
├── docker-compose.yml    # Docker Compose
├── .dockerignore        # Виключення для Docker
├── .gitignore           # Git виключення
├── .env.example         # Приклад змінних середовища
└── README.md            # Документація проекту
```

---

## ⚙️ Конфігурація

### Змінні середовища

Створіть файл `.env` на основі `.env.example`:

```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this

# Database
DATABASE_URL=sqlite:///site.db

# Admin
ADMIN_PASSWORD=secure-password-123

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### app.py конфігурація

```python
import os

# Secret key для сесій
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# База даних
app.config['DATABASE'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')

# Debug режим
app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
```

---

## 🧪 Тестування

### Ручне тестування

```bash
# Запуск застосунку
python app.py

# В іншому терміналі:
# Тест головної сторінки
curl http://localhost:5000

# Тест API products
curl http://localhost:5000/api/products

# Тест створення відгуку
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"name":"Тест","email":"test@test.com","message":"Тест"}'
```

### Unit тести (приклад)

```python
# test_app.py
import unittest
from app import app
from models import get_db_connection

class FlaskMarketTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_products(self):
        response = self.app.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

if __name__ == '__main__':
    unittest.main()
```

**Запуск тестів:**
```bash
python -m unittest test_app.py
```

---

## 📚 Документація

Повна документація знаходиться в папці `finalreport/`:

1. **[Технічна документація](finalreport/1_technical.md)** - архітектура системи, компоненти, технологічний стек
2. **[База даних](finalreport/2_database.md)** - схема БД, таблиці, зв'язки, приклади запитів
3. **[API документація](finalreport/3_api.md)** - всі endpoints з прикладами запитів/відповідей
4. **[Посібник користувача](finalreport/4_user-guide.md)** - інструкції з використання для кінцевих користувачів
5. **[Посібник з розгортання](finalreport/5_deployment.md)** - deployment на різних платформах

### Swagger API Docs
Інтерактивна документація API:
```
http://localhost:5000/apidocs
```

---

## 🤝 Внесок

Якщо ви хочете внести зміни:

1. Fork проекту
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit змін (`git commit -m 'Add some AmazingFeature'`)
4. Push до branch (`git push origin feature/AmazingFeature`)
5. Створіть Pull Request

### Coding Standards
- Python: PEP 8
- JavaScript: ESLint
- Commits: Conventional Commits

---

## 📝 Ліцензія

Distributed under the MIT License. See `LICENSE` for more information.

```
MIT License

Copyright (c) 2024 Flask Market

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Автор

**Maksym Kucheruk**  
- GitHub: [@yag-0](https://github.com/yag-0)
- Email: max.kucheruk.09gmail.com

**Група:** IPZ-21  

---

## 🙏 Подяки

- Flask документація: https://flask.palletsprojects.com/
- Tailwind CSS: https://tailwindcss.com/
- Flasgger: https://github.com/flasgger/flasgger
- Docker: https://www.docker.com/

---


## 📊 Статус проекту

**Версія:** 1.0.0  
**Підтримка:** Активна

**⭐ Якщо проект був корисним, поставте зірку на GitHub!**

**🐛 Знайшли баг? Створіть Issue!**

**💡 Є ідеї для покращення? Pull Request вітається!**
