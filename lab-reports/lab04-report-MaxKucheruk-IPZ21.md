# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди: Соло

- Учасники:
  - Кучерук Максим Сергійович (кодер, тімлід)

## Завдання

### Обрана предметна область

Інтернет-магазин техніки

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [так] Рівень 1: Створено базу даних SQLite з таблицею для відгуків, реалізовано базові CRUD операції, створено адмін-панель для перегляду та видалення відгуків, додано функціональність магазину з таблицями для товарів та замовлень
- [так] Рівень 2: Створено додаткову таблицю, релевантну предметній області, реалізовано роботу з новою таблицею через адмін-панель, інтегровано функціональність у застосунок
- [так] Рівень 3: Розширено функціональність двома додатковими функціями, що суттєво покращують користувацький досвід

## Хід виконання роботи

### Підготовка середовища розробки

- Python 3.11
- Бібліотеки: Flask, Jinja2 (в складі Flask), sqlite3 (стандартна бібліотека)
- Інструменти: VS Code, DB Browser for SQLite (перегляд БД)

### Структура проєкту

```
lab03-flaskProject/
├── app.py
├── models.py
├── requirements.txt
├── init_db.py
├── reset_db.py
├── seed.py
├── static/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── HELP.html
│   ├── market.html
│   ├── cart.html
│   └── admin/
│       ├── index.html
│       ├── login.html
│       ├── products.html
│       ├── orders.html
│       ├── customers.html
│       ├── feedback.html
│       └── promo.html
└── lab-reports/
    └── lab04-report-MaxKucheruk-IPZ21.md
```

### Проєктування бази даних

#### Схема бази даних (SQLite)

Таблиця feedback:
- id INTEGER PK
- name TEXT
- email TEXT
- message TEXT
- created_at TEXT (UTC ISO8601)

Таблиця products:
- id INTEGER PK
- name TEXT NOT NULL
- description TEXT
- price REAL NOT NULL
- stock INTEGER DEFAULT 0
- category TEXT

Таблиця customers:
- id INTEGER PK
- name TEXT
- email TEXT
- phone TEXT

Таблиця orders:
- id INTEGER PK
- customer_id INTEGER FK -> customers(id)
- status TEXT DEFAULT 'new'
- created_at TEXT (UTC ISO8601)
- promo_code TEXT NULL
- discount_amount REAL DEFAULT 0.0

Таблиця order_items:
- id INTEGER PK
- order_id INTEGER FK -> orders(id)
- product_id INTEGER FK -> products(id)
- quantity INTEGER DEFAULT 1
- price REAL (ціна на момент покупки)

Таблиця promo_codes:
- id INTEGER PK
- code TEXT UNIQUE NOT NULL
- discount_percent REAL NOT NULL
- active INTEGER DEFAULT 1
- created_at TEXT (UTC ISO8601)

Початкові дані: промокод 1234 (10%) додається автоматично при ініціалізації БД.

### Опис реалізованої функціональності

#### Система відгуків
- Форма на сторінці HELP, запис у таблицю feedback, повідомлення користувачу.
- В адмін-панелі: список відгуків та видалення записів.

#### Магазин
- Каталог товарів з фільтрами за назвою та ціною.
- Кошик у сесії: додавання/оновлення/видалення позицій.
- Оформлення замовлення: ПІБ, email, телефон. При оформленні створюється customer (або знаходиться за email), створюється order та order_items, зменшується stock.

#### Промокоди (рівень 3)
- В адмін-панелі: створення, активація/деактивація, видалення промокодів.
- У кошику: поле для введення коду, перерахунок підсумку зі знижкою.
- При оформленні замовлення у таблиці orders зберігаються promo_code та discount_amount; у розділі Замовлення показується сума, знижка і сума до сплати.

#### Адміністративна панель
- Вхід за простим паролем (123).
- Розділи: Товари, Замовлення, Клієнти, Відгуки, Промокоди.

## Ключові фрагменти коду

### Ініціалізація БД (фрагмент models.py)

```python
def initialize_db(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    if not cur.fetchone():
        cur.executescript('''
        CREATE TABLE IF NOT EXISTS feedback (...);
        CREATE TABLE IF NOT EXISTS products (...);
        CREATE TABLE IF NOT EXISTS customers (...);
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            status TEXT DEFAULT 'new',
            created_at TEXT,
            promo_code TEXT,
            discount_amount REAL DEFAULT 0.0,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );
        CREATE TABLE IF NOT EXISTS order_items (...);
        CREATE TABLE IF NOT EXISTS promo_codes (...);
        ''' )
        # seed promo 1234
```

### CRUD-приклади

Створення відгуку:
```python
db.execute('INSERT INTO feedback (name,email,message,created_at) VALUES (?,?,?,?)',
           (name, email, message, datetime.utcnow().isoformat()))
```

Оновлення статусу замовлення:
```python
db.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
```

Видалення відгуку:
```python
db.execute('DELETE FROM feedback WHERE id = ?', (fb_id,))
```

Отримання замовлення з товарами (JOIN):
```python
db.execute('''
SELECT oi.*, p.name FROM order_items oi
LEFT JOIN products p ON oi.product_id=p.id
WHERE oi.order_id = ?
''', (order_id,))
```

## Тестування

Сценарії:
1. Додавання/видалення відгуків, перевірка відображення в адмінці.
2. Створення товару, додавання до кошика, оформлення замовлення, зменшення складу.
3. Застосування промокоду 1234 (10%): знижка у кошику та фіксація в orders.
4. Перемикання активності промокодів і перевірка валідації.
5. Зміна статусу замовлення в адмінці.

## Висновки

Успішно реалізовано повноцінну схему БД для інтернет-магазину, включно з промокодами та адмін-панеллю. Отримано практичні навички роботи з SQLite, Flask, SQL-запитами з JOIN, проектуванням зв’язків та обробкою транзакцій, ШІ Copilot. Найбільші труднощі — міграції схеми (додання нових полів/таблиць у вже існуючу БД); вирішено через перевизначення ініціалізації/скидання БД та окремі скрипти. Подальші покращення: -.

Очікувана оцінка: 9/12

Обґрунтування: виконано всі рівні, реалізовано додатковий функціонал (промокоди,фільтрація), наведено приклади коду та схему БД.Орієнтування в проєкті - среднє
