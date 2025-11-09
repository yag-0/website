from datetime import datetime


def initialize_db(conn):
    """Create required tables and seed defaults if DB is empty.

    This function is idempotent: it checks for a sentinel table (feedback)
    and only creates the schema when it doesn't exist.
    """
    cur = conn.cursor()
    # Check if any tables exist by probing a sentinel table.
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")
    if not cur.fetchone():
        cur.executescript(r'''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL DEFAULT 0.0,
            stock INTEGER DEFAULT 0,
            category TEXT
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            status TEXT DEFAULT 'new',
            created_at TEXT,
            promo_code TEXT,
            discount_amount REAL DEFAULT 0.0,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1,
            price REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS promo_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL UNIQUE,
            discount_percent REAL NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TEXT
        );
        ''')
        conn.commit()
        # Seed default promo code 1234 with 10% discount if missing
        cur.execute("SELECT COUNT(*) FROM promo_codes WHERE code = '1234'")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO promo_codes (code, discount_percent, active, created_at) VALUES (?, ?, ?, ?)",
                ('1234', 10.0, 1, datetime.utcnow().isoformat()),
            )
            conn.commit()
