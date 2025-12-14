#!/usr/bin/env python3
"""
Скрипт підготовки Flask Market до розгортання
Перевіряє конфігурацію, безпеку та залежності
"""

import os
import sys
import subprocess
from pathlib import Path

class DeploymentChecklist:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0
        
    def check(self, name, passed, message=""):
        if passed:
            print(f"✓ {name}")
            self.checks_passed += 1
        else:
            print(f"✗ {name}")
            if message:
                print(f"  └─ {message}")
            self.checks_failed += 1
    
    def warn(self, name, message=""):
        print(f"⚠ {name}")
        if message:
            print(f"  └─ {message}")
        self.warnings += 1
    
    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"Результати перевірки:")
        print(f"{'='*60}")
        print(f"✓ Пройдено: {self.checks_passed}")
        print(f"✗ Не пройдено: {self.checks_failed}")
        print(f"⚠ Попередження: {self.warnings}")
        print(f"{'='*60}\n")
        
        if self.checks_failed == 0:
            print("✓ Все готово до розгортання!")
            return True
        else:
            print("✗ Виправте помилки перед розгортанням")
            return False

def main():
    checklist = DeploymentChecklist()
    base_dir = Path(__file__).parent
    
    print("🚀 Перевірка готовності Flask Market до розгортання\n")
    
    # === 1. ПЕРЕВІРКА ФАЙЛІВ ===
    print("📁 Перевірка файлів конфігурації...")
    checklist.check("app.py існує", (base_dir / "app.py").exists())
    checklist.check("models.py існує", (base_dir / "models.py").exists())
    checklist.check("api.py існує", (base_dir / "api.py").exists())
    checklist.check(".gitignore існує", (base_dir / ".gitignore").exists())
    checklist.check(".env.example існує", (base_dir / ".env.example").exists())
    checklist.check("requirements.txt існує", (base_dir / "requirements.txt").exists())
    checklist.check("Dockerfile існує", (base_dir / "Dockerfile").exists())
    checklist.check("docker-compose.yml існує", (base_dir / "docker-compose.yml").exists())
    checklist.check("config.py існує", (base_dir / "config.py").exists())
    
    # === 2. ПЕРЕВІРКА БЕЗПЕКИ ===
    print("\n🔒 Перевірка безпеки...")
    
    # Перевірити що .env не в git
    gitignore_path = base_dir / ".gitignore"
    if gitignore_path.exists():
        gitignore_content = gitignore_path.read_text()
        checklist.check(".env в .gitignore", ".env" in gitignore_content, 
                       "Переконайтесь що конфіденційні файли не попадають у репозиторій")
    
    # Перевірити SECRET_KEY в .env.example
    env_example = base_dir / ".env.example"
    if env_example.exists():
        env_content = env_example.read_text()
        checklist.warn("Розділ SECRET_KEY в .env.example", 
                      "Переконайтесь що в продакшені використовується сильний SECRET_KEY")
    
    # === 3. ПЕРЕВІРКА КОДА ===
    print("\n📝 Перевірка коду...")
    
    try:
        import py_compile
        py_compile.compile(str(base_dir / "app.py"), doraise=True)
        checklist.check("app.py синтаксис", True)
    except py_compile.PyCompileError as e:
        checklist.check("app.py синтаксис", False, str(e))
    
    try:
        py_compile.compile(str(base_dir / "models.py"), doraise=True)
        checklist.check("models.py синтаксис", True)
    except py_compile.PyCompileError as e:
        checklist.check("models.py синтаксис", False, str(e))
    
    try:
        py_compile.compile(str(base_dir / "api.py"), doraise=True)
        checklist.check("api.py синтаксис", True)
    except py_compile.PyCompileError as e:
        checklist.check("api.py синтаксис", False, str(e))
    
    # === 4. ПЕРЕВІРКА ЗАЛЕЖНОСТЕЙ ===
    print("\n📦 Перевірка залежностей...")
    
    requirements_path = base_dir / "requirements.txt"
    if requirements_path.exists():
        requirements = requirements_path.read_text().strip().split('\n')
        essential_packages = ['Flask', 'flask-cors', 'flasgger']
        for package in essential_packages:
            found = any(package.lower() in req.lower() for req in requirements if req.strip())
            checklist.check(f"{package} в requirements.txt", found)
    
    # === 5. ПЕРЕВІРКА DOCKER ===
    print("\n🐳 Перевірка Docker конфігурації...")
    
    dockerfile = base_dir / "Dockerfile"
    if dockerfile.exists():
        content = dockerfile.read_text()
        checklist.check("FROM statement в Dockerfile", "FROM" in content)
        checklist.check("HEALTHCHECK в Dockerfile", "HEALTHCHECK" in content)
        checklist.check("EXPOSE в Dockerfile", "EXPOSE" in content)
        checklist.warn("Non-root user в Dockerfile", 
                      "Переконайтесь що запускаєте контейнер від непривілейованого користувача")
    
    docker_compose = base_dir / "docker-compose.yml"
    if docker_compose.exists():
        content = docker_compose.read_text()
        checklist.check("services в docker-compose", "services:" in content)
        checklist.check("healthcheck в docker-compose", "healthcheck:" in content)
        checklist.check("restart policy в docker-compose", "restart:" in content)
    
    # === 6. ПЕРЕВІРКА ЛОГУВАННЯ ===
    print("\n📋 Перевірка логування...")
    checklist.warn("Налаштування логування", 
                  "Переконайтесь що логи писаються в файл для production")
    
    # === 7. ПЕРЕВІРКА БД ===
    print("\n💾 Перевірка бази даних...")
    site_db = base_dir / "site.db"
    checklist.warn("База даних ініціалізована", 
                  f"БД знаходиться за: {site_db}")
    
    # === РЕЗУЛЬТАТИ ===
    success = checklist.print_summary()
    
    # === РЕКОМЕНДАЦІЇ ===
    print("📋 Рекомендації перед розгортанням:")
    print("  1. Змініть SECRET_KEY на складний випадковий рядок")
    print("  2. Змініть ADMIN_PASSWORD на сильний пароль")
    print("  3. Налаштуйте SSL сертифікати (HTTPS)")
    print("  4. Налаштуйте резервне копіювання БД")
    print("  5. Додайте моніторинг (Sentry, Prometheus)")
    print("  6. Налаштуйте логування в файл")
    print("  7. Переведіть на PostgreSQL замість SQLite для production")
    print("  8. Налаштуйте rate limiting для API")
    print("  9. Включіть CORS тільки для дозволених domains")
    print(" 10. Тестуйте запуск в контейнері перед production\n")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
