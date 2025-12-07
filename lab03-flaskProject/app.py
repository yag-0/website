from flask import Flask, render_template, request, redirect, url_for, flash, g, session
from flask_cors import CORS
import sqlite3
from types import SimpleNamespace
from datetime import datetime
import os
from models import initialize_db
from flasgger import Swagger
from api import api_bp


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'site.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret')

CORS(app)

# Налаштування Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "info": {
        "title": "Flask Market API",
        "description": "REST API для інтернет-магазину",
        "version": "1.0.0"
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Реєстрація API Blueprint
app.register_blueprint(api_bp)

# Глобальний прапорець для ініціалізації БД (одноразово)
_db_initialized = False


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
        # Автоматична ініціалізація таблиць при першому підключенні
        global _db_initialized
        if not _db_initialized:
            initialize_db(conn)
            _db_initialized = True
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


"""Проєкт спрощено: прибрано користувацькі акаунти, залишено лише просту адмін авторизацію паролем."""


def admin_required(f):
    """Декоратор для захисту адмін-панелі паролем"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# База даних автоматично ініціалізується в get_db() при першому підключенні


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api-demo')
def api_demo():
    """Landing page that showcases calling the REST API from frontend."""
    return render_template('api-demo.html')


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


# === CART ROUTES ===
@app.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    """Додати товар до кошика"""
    quantity = int(request.form.get('quantity', 1))
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    # Зберігаємо як рядок (JSON-serializable)
    pid = str(product_id)
    if pid in cart:
        cart[pid] += quantity
    else:
        cart[pid] = quantity
    session.modified = True
    flash('Товар додано до кошика', 'success')
    return redirect(url_for('market'))


@app.route('/cart')
def cart_view():
    """Перегляд кошика"""
    cart = session.get('cart', {})
    items = []
    total = 0.0
    discount = 0.0
    promo_code = session.get('promo_code')
    promo_discount_percent = 0.0

    if cart:
        db = get_db()
        for pid, qty in cart.items():
            cur = db.execute('SELECT * FROM products WHERE id = ?', (int(pid),))
            p = cur.fetchone()
            if p:
                prod = dict(p)
                prod['cart_quantity'] = qty
                prod['subtotal'] = prod['price'] * qty
                total += prod['subtotal']
                items.append(prod)
        
        # Якщо є промокод — рахуємо знижку
        if promo_code:
            cur = db.execute('SELECT discount_percent FROM promo_codes WHERE code = ? AND active = 1', (promo_code,))
            promo_row = cur.fetchone()
            if promo_row:
                promo_discount_percent = promo_row['discount_percent']
                discount = total * (promo_discount_percent / 100.0)
    
    final_total = total - discount
    return render_template('cart.html', items=items, total=total, discount=discount, 
                           final_total=final_total, promo_code=promo_code, 
                           promo_discount_percent=promo_discount_percent)


@app.route('/cart/update/<int:product_id>', methods=['POST'])
def cart_update(product_id):
    """Оновити кількість товару в кошику"""
    quantity = int(request.form.get('quantity', 1))
    if 'cart' in session:
        pid = str(product_id)
        if quantity > 0:
            session['cart'][pid] = quantity
        else:
            session['cart'].pop(pid, None)
        session.modified = True
        flash('Кошик оновлено', 'success')
    return redirect(url_for('cart_view'))


@app.route('/cart/remove/<int:product_id>', methods=['POST'])
def cart_remove(product_id):
    """Видалити товар з кошика"""
    if 'cart' in session:
        session['cart'].pop(str(product_id), None)
        session.modified = True
        flash('Товар видалено з кошика', 'success')
    return redirect(url_for('cart_view'))


@app.route('/cart/apply_promo', methods=['POST'])
def cart_apply_promo():
    """Застосувати промокод"""
    code = request.form.get('promo_code', '').strip()
    if not code:
        flash('Введіть промокод', 'error')
        return redirect(url_for('cart_view'))
    
    db = get_db()
    cur = db.execute('SELECT * FROM promo_codes WHERE code = ? AND active = 1', (code,))
    promo = cur.fetchone()
    
    if promo:
        session['promo_code'] = code
        session.modified = True
        flash(f'Промокод "{code}" застосовано! Знижка {promo["discount_percent"]}%', 'success')
    else:
        flash('Промокод недійсний або неактивний', 'error')
    
    return redirect(url_for('cart_view'))


@app.route('/cart/remove_promo', methods=['POST'])
def cart_remove_promo():
    """Видалити промокод"""
    session.pop('promo_code', None)
    session.modified = True
    flash('Промокод скасовано', 'info')
    return redirect(url_for('cart_view'))


@app.route('/cart/checkout', methods=['POST'])
def cart_checkout():
    """Оформлення замовлення з кошика"""
    cart = session.get('cart', {})
    if not cart:
        flash('Кошик порожній', 'error')
        return redirect(url_for('cart_view'))
    
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    if not name or not email:
        flash("Введіть ім'я та email", 'error')
        return redirect(url_for('cart_view'))
    
    db = get_db()
    
    # Find or create customer
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
    
    # Підрахунок суми і знижки
    total = 0.0
    discount = 0.0
    promo_code = session.get('promo_code')
    
    # Рахуємо загальну суму товарів
    for pid, qty in cart.items():
        cur = db.execute('SELECT * FROM products WHERE id = ?', (int(pid),))
        prod = cur.fetchone()
        if prod:
            total += prod['price'] * qty
    
    # Якщо є промокод — рахуємо знижку
    if promo_code:
        cur = db.execute('SELECT discount_percent FROM promo_codes WHERE code = ? AND active = 1', (promo_code,))
        promo_row = cur.fetchone()
        if promo_row:
            discount = total * (promo_row['discount_percent'] / 100.0)
    
    # Create order з промокодом і знижкою
    cur = db.execute('INSERT INTO orders (customer_id,status,created_at,promo_code,discount_amount) VALUES (?,?,?,?,?)',
                     (customer_id, 'new', datetime.utcnow().isoformat(), promo_code, discount))
    db.commit()
    order_id = cur.lastrowid
    
    # Add order items
    for pid, qty in cart.items():
        cur = db.execute('SELECT * FROM products WHERE id = ?', (int(pid),))
        prod = cur.fetchone()
        if prod:
            db.execute('INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (?,?,?,?)',
                       (order_id, int(pid), qty, prod['price']))
            # Reduce stock
            new_stock = prod['stock'] - qty
            if new_stock < 0:
                new_stock = 0
            db.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, int(pid)))
    
    db.commit()
    
    # Clear cart and promo code
    session.pop('cart', None)
    session.pop('promo_code', None)
    flash('Замовлення успішно оформлено! Дякуємо!', 'success')
    return redirect(url_for('home'))


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


# === ADMIN ROUTES ===
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == '123':  # Простий пароль
            session['admin_logged_in'] = True
            flash('Вхід в адмін-панель успішний', 'success')
            return redirect(url_for('admin_index'))
        else:
            flash('Невірний пароль', 'error')
            return redirect(url_for('admin_login'))
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Вихід з адмін-панелі', 'success')
    return redirect(url_for('home'))


@app.route('/admin')
@admin_required
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/feedback')
@admin_required
def admin_feedback():
    db = get_db()
    cur = db.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    feedbacks = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/feedback.html', feedbacks=feedbacks)


@app.route('/admin/feedback/delete/<int:fb_id>', methods=['POST'])
@admin_required
def admin_feedback_delete(fb_id):
    db = get_db()
    db.execute('DELETE FROM feedback WHERE id = ?', (fb_id,))
    db.commit()
    flash('Відгук видалено', 'success')
    return redirect(url_for('admin_feedback'))


@app.route('/admin/products')
@admin_required
def admin_products():
    db = get_db()
    cur = db.execute('SELECT * FROM products')
    products = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/products.html', products=products)


@app.route('/admin/products/new', methods=['POST'])
@admin_required
def admin_products_new():
    """Створити новий товар з форми в адмінці."""
    name = request.form.get('name')
    price = request.form.get('price')
    stock = request.form.get('stock')
    category = request.form.get('category')
    description = request.form.get('description')

    if not name or not price:
        flash('Назва і ціна обов\'язкові', 'error')
        return redirect(url_for('admin_products'))

    try:
        price_val = float(price)
        stock_val = int(stock or 0)
    except ValueError:
        flash('Невірний формат ціни або кількості', 'error')
        return redirect(url_for('admin_products'))

    db = get_db()
    db.execute('INSERT INTO products (name, description, price, stock, category) VALUES (?,?,?,?,?)',
               (name, description, price_val, stock_val, category))
    db.commit()
    flash('Товар додано', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_products_delete(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    flash('Товар видалено', 'success')
    return redirect(url_for('admin_products'))


@app.route('/admin/promo')
@admin_required
def admin_promo():
    """Адмін: список промокодів"""
    db = get_db()
    cur = db.execute('SELECT * FROM promo_codes ORDER BY created_at DESC')
    promos = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/promo.html', promos=promos)


@app.route('/admin/promo/new', methods=['POST'])
@admin_required
def admin_promo_new():
    """Створити новий промокод"""
    code = request.form.get('code', '').strip().upper()
    discount = request.form.get('discount')
    
    if not code or not discount:
        flash('Код і відсоток знижки обов\'язкові', 'error')
        return redirect(url_for('admin_promo'))
    
    try:
        discount_val = float(discount)
        if discount_val <= 0 or discount_val > 100:
            raise ValueError
    except ValueError:
        flash('Знижка має бути від 0 до 100%', 'error')
        return redirect(url_for('admin_promo'))
    
    db = get_db()
    # Перевірка унікальності
    existing = db.execute('SELECT * FROM promo_codes WHERE code = ?', (code,)).fetchone()
    if existing:
        flash('Промокод з таким кодом вже існує', 'error')
        return redirect(url_for('admin_promo'))
    
    db.execute('INSERT INTO promo_codes (code, discount_percent, active, created_at) VALUES (?,?,?,?)',
               (code, discount_val, 1, datetime.utcnow().isoformat()))
    db.commit()
    flash(f'Промокод "{code}" створено', 'success')
    return redirect(url_for('admin_promo'))


@app.route('/admin/promo/toggle/<int:promo_id>', methods=['POST'])
@admin_required
def admin_promo_toggle(promo_id):
    """Змінити статус активності промокоду"""
    db = get_db()
    promo = db.execute('SELECT * FROM promo_codes WHERE id = ?', (promo_id,)).fetchone()
    if promo:
        new_active = 0 if promo['active'] else 1
        db.execute('UPDATE promo_codes SET active = ? WHERE id = ?', (new_active, promo_id))
        db.commit()
        status = 'активовано' if new_active else 'деактивовано'
        flash(f'Промокод {status}', 'success')
    return redirect(url_for('admin_promo'))


@app.route('/admin/promo/delete/<int:promo_id>', methods=['POST'])
@admin_required
def admin_promo_delete(promo_id):
    """Видалити промокод"""
    db = get_db()
    db.execute('DELETE FROM promo_codes WHERE id = ?', (promo_id,))
    db.commit()
    flash('Промокод видалено', 'success')
    return redirect(url_for('admin_promo'))


@app.route('/admin/orders')
@admin_required
def admin_orders():
    db = get_db()
    cur = db.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = []
    for o in cur.fetchall():
        order = dict(o)
        # get customer
        customer_obj = {'name': 'Невідомий', 'email': '', 'phone': ''}
        if order.get('customer_id'):
            c = db.execute('SELECT * FROM customers WHERE id = ?', (order['customer_id'],)).fetchone()
            if c:
                customer_obj = dict(c)
        order['customer'] = customer_obj
        items_cur = db.execute('SELECT oi.*, p.name FROM order_items oi LEFT JOIN products p ON oi.product_id=p.id WHERE oi.order_id = ?', (order['id'],))
        order['items'] = [dict(i) for i in items_cur.fetchall()]
        orders.append(SimpleNamespace(**order))
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/orders/update_status/<int:order_id>', methods=['POST'])
@admin_required
def admin_orders_update_status(order_id):
    new_status = request.form.get('status')
    # normalize and validate
    status = (new_status or '').strip().lower()
    allowed = {'new','processing','shipped','completed','cancelled'}
    if status not in allowed:
        flash('Некоректний статус замовлення', 'error')
        return redirect(url_for('admin_orders'))

    db = get_db()
    cur = db.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    db.commit()
    if cur.rowcount == 0:
        flash('Замовлення не знайдено', 'error')
    else:
        flash('Статус замовлення оновлено', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/admin/customers')
@admin_required
def admin_customers():
    db = get_db()
    cur = db.execute('SELECT * FROM customers')
    customers = [row_to_obj(r) for r in cur.fetchall()]
    return render_template('admin/customers.html', customers=customers)


@app.route('/admin/customers/delete/<int:customer_id>', methods=['POST'])
@admin_required
def admin_customers_delete(customer_id):
    db = get_db()
    db.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    db.commit()
    flash('Клієнт видалений', 'success')
    return redirect(url_for('admin_customers'))


if __name__ == '__main__':
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    try:
        port = int(os.environ.get('FLASK_RUN_PORT', '5000'))
    except ValueError:
        port = 5000
    app.run(debug=True, host=host, port=port)
