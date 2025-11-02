import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'site.db')

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL DEFAULT 0.0, stock INTEGER DEFAULT 0, category TEXT)')
    cur.execute('SELECT COUNT(1) FROM products')
    if cur.fetchone()[0] == 0:
        samples = [
            ('Навушники X1', 'Бездротові навушники', 999.0, 10, 'Аудіо'),
            ('Миша M300', 'Оптична миша', 249.5, 25, 'Периферія'),
            ('Клавіатура K100', 'Механічна клавіатура', 1299.0, 5, 'Периферія'),
        ]
        cur.executemany('INSERT INTO products (name,description,price,stock,category) VALUES (?,?,?,?,?)', samples)
        conn.commit()
        print('Seeded products.')
    else:
        print('Products already exist, skipping.')
    conn.close()


if __name__ == '__main__':
    seed()
