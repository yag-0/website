import os
from app import init_db, app, DB_PATH

# Цей скрипт запускає функцію init_db в контексті програми
# і створює файл бази даних 'site.db', якщо він ще не існує.

print(f"Спроба ініціалізувати базу даних за шляхом: {DB_PATH}")

# Створюємо контекст програми Flask для коректної роботи get_db() всередині init_db()
with app.app_context():
    init_db()
    
print("База даних 'site.db' успішно ініціалізована (або вже існувала).")
print("Тепер ви можете запустити додаток: python app.py")
