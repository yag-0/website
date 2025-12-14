#!/usr/bin/env python3
"""
Скрипт для міграції та управління базою даних
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / 'site.db'

def backup_database():
    """Створити резервну копію БД"""
    if not DB_PATH.exists():
        print("❌ База даних не існує")
        return False
    
    backup_path = DB_PATH.parent / f'site_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
    try:
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        print(f"✓ Резервна копія створена: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Помилка при створенні резервної копії: {e}")
        return False

def init_database():
    """Ініціалізувати БД"""
    from models import initialize_db
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        initialize_db(conn)
        conn.close()
        print("✓ База даних ініціалізована")
        return True
    except Exception as e:
        print(f"❌ Помилка при ініціалізації БД: {e}")
        return False

def check_database():
    """Перевірити цілісність БД"""
    if not DB_PATH.exists():
        print("❌ База даних не існує")
        return False
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Отримати список таблиць
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = cursor.fetchall()
        
        print("✓ База даних цілісна")
        print(f"\nТаблиці ({len(tables)}):")
        
        for (table,) in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} рядків")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def migrate_to_postgresql():
    """Вказівка на міграцію на PostgreSQL"""
    print("""
    📋 Міграція на PostgreSQL
    
    1. Встановіть PostgreSQL на сервері:
       sudo apt-get install postgresql postgresql-contrib
    
    2. Встановіть PyPI пакети:
       pip install psycopg2-binary
    
    3. Експортуйте дані з SQLite:
       sqlite3 site.db .dump > database.sql
    
    4. Імпортуйте в PostgreSQL:
       createdb flaskmarket
       psql flaskmarket < database.sql
    
    5. Оновіть DATABASE_URL в .env:
       DATABASE_URL=postgresql://user:password@localhost:5432/flaskmarket
    
    6. Оновіть models.py для використання SQLAlchemy або psycopg2
    
    Детальніше: https://docs.sqlalchemy.org/
    """)

def vacuum_database():
    """Оптимізувати БД"""
    if not DB_PATH.exists():
        print("❌ База даних не існує")
        return False
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute('VACUUM')
        conn.execute('ANALYZE')
        conn.close()
        print("✓ База даних оптимізована")
        return True
    except Exception as e:
        print(f"❌ Помилка: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("""
    🗄️  Управління базою даних Flask Market
    
    Використання: python manage_db.py <команда>
    
    Команди:
      init        - Ініціалізувати БД
      backup      - Створити резервну копію
      check       - Перевірити цілісність БД
      vacuum      - Оптимізувати БД
      migrate-pg  - Вказівка на міграцію на PostgreSQL
    """)
        return 1
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        return 0 if init_database() else 1
    elif command == 'backup':
        return 0 if backup_database() else 1
    elif command == 'check':
        return 0 if check_database() else 1
    elif command == 'vacuum':
        return 0 if vacuum_database() else 1
    elif command == 'migrate-pg':
        migrate_to_postgresql()
        return 0
    else:
        print(f"❌ Невідома команда: {command}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
