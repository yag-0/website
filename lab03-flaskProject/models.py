from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('DATABASE_PATH', os.path.join(BASE_DIR, 'site.db'))


def get_db_connection():
    """Create a new database connection for API requests."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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


# API Helper Functions

def get_products():
    """Get all products from database."""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return products


def get_orders():
    """Get all orders with customer info."""
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT o.*, c.name as customer_name, c.email as customer_email 
        FROM orders o 
        LEFT JOIN customers c ON o.customer_id = c.id
        ORDER BY o.created_at DESC
    ''').fetchall()
    conn.close()
    return orders


def get_order_details(order_id):
    """Get order with items details."""
    conn = get_db_connection()
    
    # Get order info
    order = conn.execute('''
        SELECT o.*, c.name as customer_name, c.email as customer_email, c.phone
        FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE o.id = ?
    ''', (order_id,)).fetchone()
    
    # Get order items
    items = conn.execute('''
        SELECT oi.*, p.name as product_name
        FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    ''', (order_id,)).fetchall()
    
    conn.close()
    return order, items


def add_order(customer_name, customer_email, customer_phone, cart, promo_code=None):
    """Create new order from cart data."""
    conn = get_db_connection()
    
    # Create or find customer
    customer = conn.execute('SELECT * FROM customers WHERE email = ?', (customer_email,)).fetchone()
    if customer:
        customer_id = customer['id']
    else:
        cursor = conn.execute(
            'INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
            (customer_name, customer_email, customer_phone)
        )
        customer_id = cursor.lastrowid
    
    # Calculate total and discount
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    discount = 0.0
    
    if promo_code:
        promo = conn.execute(
            'SELECT discount_percent FROM promo_codes WHERE code = ? AND active = 1',
            (promo_code,)
        ).fetchone()
        if promo:
            discount = total * (promo['discount_percent'] / 100.0)
    
    # Create order
    cursor = conn.execute(
        'INSERT INTO orders (customer_id, status, created_at, promo_code, discount_amount) VALUES (?, ?, ?, ?, ?)',
        (customer_id, 'new', datetime.utcnow().isoformat(), promo_code, discount)
    )
    order_id = cursor.lastrowid
    
    # Add order items
    for item in cart.values():
        conn.execute(
            'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
            (order_id, item['id'], item['quantity'], item['price'])
        )
    
    conn.commit()
    conn.close()
    return order_id


def update_order_status(order_id, status):
    """Update order status. Returns True if updated, False if not found."""
    conn = get_db_connection()
    cur = conn.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated


def delete_order(order_id):
    """Delete order and its items."""
    conn = get_db_connection()
    conn.execute('DELETE FROM order_items WHERE order_id = ?', (order_id,))
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
