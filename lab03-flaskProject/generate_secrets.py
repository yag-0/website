#!/usr/bin/env python3
"""
Генератор безпечних ключів для production конфігурації
"""

import secrets
import string
from pathlib import Path

def generate_secret_key(length=32):
    """Генерує криптографічно безпечний SECRET_KEY"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_password(length=16):
    """Генерує криптографічно безпечний пароль"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    print("🔐 Генератор безпечних ключів для Flask Market\n")
    
    # Генерація SECRET_KEY
    secret_key = generate_secret_key(48)
    print(f"Новий SECRET_KEY (48 символів):")
    print(f"  {secret_key}\n")
    
    # Генерація ADMIN_PASSWORD
    admin_password = generate_password(16)
    print(f"Новий ADMIN_PASSWORD (16 символів):")
    print(f"  {admin_password}\n")
    
    # Пропозиція оновити .env
    print("💡 Оновіть .env файл на сервері:")
    print(f"  SECRET_KEY={secret_key}")
    print(f"  ADMIN_PASSWORD={admin_password}\n")
    
    # Порада безпеки
    print("⚠️  БЕЗПЕКА:")
    print("  ✓ Ніколи не комітьте .env в репозиторій")
    print("  ✓ Користуйтеся环境 змінними на хостингу")
    print("  ✓ Регулярно оновлюйте ключі")
    print("  ✓ Не ділитися SECRET_KEY з кимось\n")
    
    # Пропозиція зберегти
    response = input("Зберегти ключі в .env.production? (y/n): ").lower()
    if response == 'y':
        base_dir = Path(__file__).parent
        env_prod = base_dir / ".env.production"
        content = f"""# Production Environment Variables
# ⚠️  НЕ комітьте цей файл у репозиторій!

# Flask Application
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY={secret_key}

# Database
DATABASE_PATH=/app/data/database.db

# Admin Panel
ADMIN_PASSWORD={admin_password}

# CORS (змініть на ваш домен)
CORS_ORIGINS=https://yourdomain.com

# Server
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
"""
        env_prod.write_text(content)
        print(f"\n✓ Файл .env.production створено")
        print(f"  Потім скопіюйте його на сервер та перейменуйте на .env")
    else:
        print("\n✓ Ключі не збережені")

if __name__ == "__main__":
    main()
