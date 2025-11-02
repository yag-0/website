from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
from types import SimpleNamespace
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'site.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')
# Ми видалили тут прапорець SETUP_COMPLETED та логіку ініціалізації БД,
# оскільки тепер вона відбувається окремим скриптом.


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


app.teardown_appcontext(close_db)


def row_to_obj(row):
    if row is None:
        return None
    return SimpleNamespace(**dict(row))


def init_db():
    db = get_db()
    cur = db.cursor()
    # Ініціалізація бази даних. Цю функцію ми тепер викликатимемо вручну.
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
    ''')
    db.commit()


# Ми видалили функцію ensure_db_once та декоратор @app.before_request.
# База даних тепер ініціалізується окремим скриптом.
# --------------------------------------------------------------------------


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/HELP', methods=['GET'])
def helppage():
    return render_template('HELP.html')


@app.route('/feedback', methods=['POST'])
def create_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    if not message:
        flash('Повідомлення не може бути порожнім', 'error')
        return redirect(url_for('helppage'))
    db = get_db()
    db.execute('INSERT INTO feedback (name,email,message,created_at) VALUES (?,?,?,?)',
               (name, email, message, datetime.utcnow().isoformat()))
    db.commit()
    flash('Дякуємо за відгук!', 'success')
    return redirect(url_for('helppage'))


@app.route('/market')
def market():
    q = request.args.get('q', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    db = get_db()
    sql = 'SELECT * FROM products WHERE 1=1'
    params = []
    if q:
        sql += ' AND name LIKE ?'
        params.append(f'%{q}%')
    if min_price:
        try:
            float(min_price)
            sql += ' AND price >= ?'
            params.append(min_price)
        except ValueError:
            pass
    if max_price:
        try:
            float(max_price)
            sql += ' AND price <= ?'
            params.append(max_price)
        except ValueError:
            pass
    cur = db.execute(sql, params)
    rows = cur.fetchall()
    products = [row_to_obj(r) for r in rows]
    return render_template('market.html', products=products, q=q, min_price=min_price or '', max_price=max_price or '')


@app.route('/order/create', methods=['POST'])
def create_order():
    try:
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 1))
    except (TypeError, ValueError):
        flash('Невірні дані замовлення', 'error')
        return redirect(url_for('market'))

    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    db = get_db()
    cur = db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    prod = cur.fetchone()
    if not prod:
        flash('Товар не знайдено', 'error')
        return redirect(url_for('market'))

    # find or create customer by email
    customer = None
    if email:
        cur = db.execute('SELECT * FROM customers WHERE email = ?', (email,))
        customer = cur.fetchone()
    if not customer:
        cur = db.execute('INSERT INTO customers (name,email,phone) VALUES (?,?,?)', (name, email, phone))
        db.commit()
        customer_id = cur.lastrowid
    else:
        customer_id = customer['id']

    cur = db.execute('INSERT INTO orders (customer_id,status,created_at) VALUES (?,?,?)',
                     (customer_id, 'new', datetime.utcnow().isoformat()))
    db.commit()
    order_id = cur.lastrowid

    db.execute('INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (?,?,?,?)',
               (order_id, product_id, quantity, prod['price']))
    # Optionally reduce stock
    try:
        new_stock = prod['stock'] - quantity
        if new_stock < 0:
            new_stock = 0
        db.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
    except Exception:
        pass
    db.commit()

    flash('Замовлення створено. Дякуємо!', 'success')
    return redirect(url_for('market'))


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/feedback')
def admin_feedback():
    db = get_db()
    cur = db.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedbacks = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/feedback.html', feedbacks=feedbacks)


@app.route('/admin/feedback/delete/<int:fb_id>', methods=['POST'])
def admin_feedback_delete(fb_id):
    db = get_db()
    db.execute('DELETE FROM feedback WHERE id = ?', (fb_id,))
    db.commit()
    flash('Відгук видалено', 'success')
    return redirect(url_for('admin_feedback'))


@app.route('/admin/products')
def admin_products():
    db = get_db()
    cur = db.execute('SELECT * FROM products')
    products = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/products.html', products=products)


@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
def admin_products_delete(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    flash('Товар видалено', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/orders')
def admin_orders():
    db = get_db()
    cur = db.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = []
    for o in cur.fetchall():
        order = dict(o)
        # get customer
        c = db.execute('SELECT * FROM customers WHERE id = ?', (order['customer_id'],)).fetchone()
        order['customer'] = dict(c) if c else {}
        items_cur = db.execute('SELECT oi.*, p.name FROM order_items oi LEFT JOIN products p ON oi.product_id=p.id WHERE oi.order_id = ?', (order['id'],))
        order['items'] = [dict(i) for i in items_cur.fetchall()]
        orders.append(SimpleNamespace(**order))
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/update_status/<int:order_id>', methods=['POST'])
def admin_orders_update_status(order_id):
    new_status = request.form.get('status')
    db = get_db()
    db.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    db.commit()
    flash('Статус замовлення оновлено', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/admin/customers')
def admin_customers():
    db = get_db()
    cur = db.execute('SELECT * FROM customers')
    customers = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/customers.html', customers=customers)


@app.route('/admin/customers/delete/<int:customer_id>', methods=['POST'])
def admin_customers_delete(customer_id):
    db = get_db()
    db.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    db.commit()
    flash('Клієнт видалений', 'success')
    return redirect(url_for('admin_customers'))


if __name__ == '__main__':
    app.run(debug=True)
