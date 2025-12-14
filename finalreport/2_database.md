# Документація бази даних

## Зміст
1. [Загальна інформація](#загальна-інформація)
2. [Схема бази даних](#схема-бази-даних)
3. [Таблиці](#таблиці)
4. [Зв'язки між таблицями](#звязки-між-таблицями)
5. [Приклади запитів](#приклади-запитів)

---

## Загальна інформація

**СУБД:** SQLite 3  
**Файл БД:** `site.db`  
**Кодування:** UTF-8  
**Foreign Keys:** Увімкнено

### Статистика
- Кількість таблиць: **6**
- Підтримка транзакцій: **Так (ACID)**
- Тригери: **Відсутні**
- Індекси: **Автоматичні на primary і foreign keys**

---

## Схема бази даних

### ER-діаграма

```
┌──────────────────┐
│    customers     │
│──────────────────│
│ id (PK)          │
│ name             │
│ email            │
│ phone            │
│ address          │
│ created_at       │
└────────┬─────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐          ┌──────────────────┐
│     orders       │          │   promo_codes    │
│──────────────────│          │──────────────────│
│ id (PK)          │          │ id (PK)          │
│ customer_id (FK) │◄─────────│ code             │
│ promo_code (FK)  │   0:N    │ discount_percent │
│ total_amount     │          │ valid_from       │
│ status           │          │ valid_until      │
│ created_at       │          │ active           │
└────────┬─────────┘          └──────────────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐          ┌──────────────────┐
│   order_items    │          │    products      │
│──────────────────│          │──────────────────│
│ id (PK)          │   N:1    │ id (PK)          │
│ order_id (FK)    ├──────────►│ name             │
│ product_id (FK)  │          │ description      │
│ quantity         │          │ price            │
│ price_at_time    │          │ stock            │
│ subtotal         │          │ category         │
└──────────────────┘          │ image_url        │
                              │ created_at       │
                              └──────────────────┘

┌──────────────────┐
│     feedback     │
│──────────────────│
│ id (PK)          │
│ name             │
│ email            │
│ message          │
│ created_at       │
└──────────────────┘
```

---

## Таблиці

### 1. products
**Призначення:** Зберігання інформації про товари в каталозі

| Поле        | Тип          | Обмеження              | Опис                           |
|-------------|--------------|------------------------|--------------------------------|
| id          | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| name        | TEXT         | NOT NULL               | Назва товару                   |
| description | TEXT         | -                      | Детальний опис                 |
| price       | REAL         | NOT NULL               | Ціна товару                    |
| stock       | INTEGER      | NOT NULL, DEFAULT 0    | Кількість на складі            |
| category    | TEXT         | -                      | Категорія товару               |
| image_url   | TEXT         | -                      | URL зображення                 |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TS     | Дата додавання                 |

**Індекси:**
- PRIMARY KEY на `id`
- Рекомендується додати INDEX на `category` для швидшого пошуку

**Приклад:**
```sql
INSERT INTO products (name, description, price, stock, category, image_url)
VALUES (
    'Ноутбук ASUS',
    'Потужний ігровий ноутбук з RTX 4060',
    25999.00,
    15,
    'Ноутбуки',
    '/static/images/laptop.jpg'
);
```

---

### 2. customers
**Призначення:** Дані про покупців

| Поле       | Тип          | Обмеження              | Опис                           |
|------------|--------------|------------------------|--------------------------------|
| id         | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| name       | TEXT         | NOT NULL               | Ім'я покупця                   |
| email      | TEXT         | NOT NULL, UNIQUE       | Електронна пошта               |
| phone      | TEXT         | -                      | Номер телефону                 |
| address    | TEXT         | -                      | Адреса доставки                |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TS     | Дата реєстрації                |

**Індекси:**
- PRIMARY KEY на `id`
- UNIQUE INDEX на `email`

**Приклад:**
```sql
INSERT INTO customers (name, email, phone, address)
VALUES (
    'Іван Петренко',
    'ivan@example.com',
    '+380501234567',
    'Київ, вул. Хрещатик 1, кв. 5'
);
```

---

### 3. orders
**Призначення:** Замовлення покупців

| Поле         | Тип          | Обмеження              | Опис                           |
|--------------|--------------|------------------------|--------------------------------|
| id           | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| customer_id  | INTEGER      | FOREIGN KEY, NOT NULL  | ID покупця                     |
| promo_code   | TEXT         | -                      | Використаний промокод          |
| total_amount | REAL         | NOT NULL               | Загальна сума замовлення       |
| status       | TEXT         | DEFAULT 'pending'      | Статус (pending/completed)     |
| created_at   | TIMESTAMP    | DEFAULT CURRENT_TS     | Дата створення                 |

**Foreign Keys:**
- `customer_id` → `customers(id)` ON DELETE CASCADE

**Статуси:**
- `pending` - очікує обробки
- `processing` - в обробці
- `shipped` - відправлено
- `completed` - виконано
- `cancelled` - скасовано

**Приклад:**
```sql
INSERT INTO orders (customer_id, promo_code, total_amount, status)
VALUES (1, 'SUMMER2024', 23399.10, 'pending');
```

---

### 4. order_items
**Призначення:** Позиції (товари) в замовленнях

| Поле          | Тип          | Обмеження              | Опис                           |
|---------------|--------------|------------------------|--------------------------------|
| id            | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| order_id      | INTEGER      | FOREIGN KEY, NOT NULL  | ID замовлення                  |
| product_id    | INTEGER      | FOREIGN KEY, NOT NULL  | ID товару                      |
| quantity      | INTEGER      | NOT NULL               | Кількість одиниць              |
| price_at_time | REAL         | NOT NULL               | Ціна на момент покупки         |
| subtotal      | REAL         | NOT NULL               | Підсумок (qty * price)         |

**Foreign Keys:**
- `order_id` → `orders(id)` ON DELETE CASCADE
- `product_id` → `products(id)` ON DELETE RESTRICT

**Примітка:** `price_at_time` зберігає ціну товару на момент замовлення, щоб зміна ціни в каталозі не впливала на історичні дані.

**Приклад:**
```sql
INSERT INTO order_items (order_id, product_id, quantity, price_at_time, subtotal)
VALUES (1, 5, 2, 1500.00, 3000.00);
```

---

### 5. promo_codes
**Призначення:** Промокоди для знижок

| Поле             | Тип          | Обмеження              | Опис                           |
|------------------|--------------|------------------------|--------------------------------|
| id               | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| code             | TEXT         | NOT NULL, UNIQUE       | Код промокоду (напр. SALE20)   |
| discount_percent | REAL         | NOT NULL               | Відсоток знижки (0-100)        |
| valid_from       | TIMESTAMP    | -                      | Дата початку дії               |
| valid_until      | TIMESTAMP    | -                      | Дата закінчення дії            |
| active           | INTEGER      | DEFAULT 1              | Активність (0 або 1)           |

**Індекси:**
- PRIMARY KEY на `id`
- UNIQUE INDEX на `code`

**Приклад:**
```sql
INSERT INTO promo_codes (code, discount_percent, valid_from, valid_until, active)
VALUES (
    'WINTER25',
    25.0,
    '2024-12-01 00:00:00',
    '2025-02-28 23:59:59',
    1
);
```

---

### 6. feedback
**Призначення:** Відгуки та зворотній зв'язок від користувачів

| Поле       | Тип          | Обмеження              | Опис                           |
|------------|--------------|------------------------|--------------------------------|
| id         | INTEGER      | PRIMARY KEY, AUTOINCR  | Унікальний ідентифікатор       |
| name       | TEXT         | NOT NULL               | Ім'я автора                    |
| email      | TEXT         | NOT NULL               | Email автора                   |
| message    | TEXT         | NOT NULL               | Текст відгуку                  |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TS     | Дата створення                 |

**Приклад:**
```sql
INSERT INTO feedback (name, email, message)
VALUES (
    'Олена Сидоренко',
    'olena@example.com',
    'Дуже задоволена покупкою! Швидка доставка.'
);
```

---

## Зв'язки між таблицями

### 1. customers → orders (One-to-Many)
Один покупець може мати багато замовлень.

```sql
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;
```

### 2. orders → order_items (One-to-Many)
Одне замовлення містить багато позицій товарів.

```sql
SELECT o.id, COUNT(oi.id) as items_count, SUM(oi.subtotal) as total
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id;
```

### 3. products → order_items (One-to-Many)
Один товар може бути в багатьох замовленнях.

```sql
SELECT p.name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id
ORDER BY total_sold DESC;
```

### 4. promo_codes → orders (One-to-Many)
Один промокод може бути використаний в багатьох замовленнях.

```sql
SELECT pc.code, COUNT(o.id) as usage_count
FROM promo_codes pc
LEFT JOIN orders o ON pc.code = o.promo_code
GROUP BY pc.id;
```

---

## Приклади запитів

### Аналітика

#### Топ-5 товарів за продажами
```sql
SELECT 
    p.name,
    SUM(oi.quantity) as sold_count,
    SUM(oi.subtotal) as revenue
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id
ORDER BY revenue DESC
LIMIT 5;
```

#### Середній чек замовлення
```sql
SELECT AVG(total_amount) as average_order
FROM orders
WHERE status = 'completed';
```

#### Кількість замовлень за місяць
```sql
SELECT 
    strftime('%Y-%m', created_at) as month,
    COUNT(*) as order_count
FROM orders
GROUP BY month
ORDER BY month DESC;
```

#### Найактивніші покупці
```sql
SELECT 
    c.name,
    c.email,
    COUNT(o.id) as orders_count,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.id
ORDER BY total_spent DESC
LIMIT 10;
```

### Інвентар

#### Товари з низьким запасом
```sql
SELECT id, name, stock, price
FROM products
WHERE stock < 5 AND stock > 0
ORDER BY stock ASC;
```

#### Товари, які закінчилися
```sql
SELECT id, name, category, price
FROM products
WHERE stock = 0;
```

### Промокоди

#### Активні промокоди на поточну дату
```sql
SELECT code, discount_percent, valid_until
FROM promo_codes
WHERE active = 1
  AND datetime('now') BETWEEN datetime(valid_from) AND datetime(valid_until);
```

#### Найбільш використовувані промокоди
```sql
SELECT 
    promo_code,
    COUNT(*) as usage_count,
    SUM(total_amount) as total_discounted_sales
FROM orders
WHERE promo_code IS NOT NULL
GROUP BY promo_code
ORDER BY usage_count DESC;
```

---

## Міграції та версіонування

### Поточна версія: 1.0

**Створення таблиць виконується в `models.py` функцією `init_db()`.**

Для майбутніх міграцій рекомендується використовувати **Alembic** або **Flask-Migrate**.

### Приклад міграції (додавання колонки)

```sql
-- Додавання поля rating до products
ALTER TABLE products ADD COLUMN rating REAL DEFAULT 0.0;

-- Додавання індексу
CREATE INDEX idx_products_rating ON products(rating);
```

---

## Резервне копіювання

### Бекап SQLite
```bash
# Копіювання файлу бази даних
cp site.db site_backup_$(date +%Y%m%d).db

# Експорт в SQL
sqlite3 site.db .dump > backup.sql

# Відновлення з SQL
sqlite3 new_site.db < backup.sql
```

### Автоматичний бекап (cron)
```bash
# Щоденний бекап о 3:00 ночі
0 3 * * * cd /path/to/project && cp site.db backups/site_$(date +\%Y\%m\%d_\%H\%M).db
```

---

## Оптимізація

### Рекомендовані індекси для production

```sql
-- Швидкий пошук товарів за категорією
CREATE INDEX idx_products_category ON products(category);

-- Фільтрація замовлень за статусом
CREATE INDEX idx_orders_status ON orders(status);

-- Пошук замовлень за датою
CREATE INDEX idx_orders_created ON orders(created_at);

-- Швидкий lookup промокодів
CREATE INDEX idx_promo_active ON promo_codes(active, valid_until);
```

### VACUUM та ANALYZE

```sql
-- Дефрагментація та оптимізація БД
VACUUM;

-- Оновлення статистики для оптимізатора запитів
ANALYZE;
```

### Налаштування SQLite

```python
# В models.py при підключенні
conn = sqlite3.connect('site.db')
conn.execute('PRAGMA journal_mode=WAL')  # Write-Ahead Logging
conn.execute('PRAGMA synchronous=NORMAL')
conn.execute('PRAGMA cache_size=-64000')  # 64MB cache
conn.execute('PRAGMA temp_store=MEMORY')
```

---

## Обмеження SQLite

### Не підходить для:
- ❌ Високе конкурентне навантаження (багато одночасних записів)
- ❌ Розподілені системи
- ❌ Великі обсяги даних (> 100 GB)
- ❌ Складні транзакції з блокуваннями

### Міграція на PostgreSQL (рекомендовано для production)

```python
# requirements.txt
psycopg2-binary==2.9.9

# Приклад connection string
DATABASE_URL = "postgresql://user:password@localhost:5432/flask_market"
```

---

## Висновок

База даних має просту та ефективну структуру з 6 таблицями, що покриває всі основні потреби інтернет-магазину. SQLite підходить для development та малих проектів, але для масштабованого production варто розглянути PostgreSQL або MySQL.

**Сильні сторони:**
- ✅ Нормалізована структура (3NF)
- ✅ Foreign keys для цілісності даних
- ✅ Простота у підтримці
- ✅ Легке резервне копіювання

**Рекомендації:**
- Додати індекси для популярних запитів
- Впровадити систему міграцій (Alembic)
- Розглянути партиціонування таблиці orders при масштабуванні
- Додати тригери для автоматичного оновлення stock при створенні замовлення
