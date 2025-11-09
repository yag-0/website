import os
import sqlite3

# Видаляємо стару базу даних
db_path = 'site.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f'Стара база даних {db_path} видалена')

# Запускаємо додаток для створення нової бази
print('Нова база даних буде створена при першому запиті до додатку')
print('Запустіть: python app.py')
