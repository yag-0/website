#!/usr/bin/env python3
"""
Локальний тест Flask Market аplication
Перевіряє основні функції без Docker
"""

import requests
import json
import time
from subprocess import Popen, PIPE
from pathlib import Path
import sys

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.process = None
    
    def test(self, name, func):
        """Запустити тест"""
        try:
            func()
            print(f"✓ {name}")
            self.passed += 1
        except Exception as e:
            print(f"✗ {name}")
            print(f"  └─ {str(e)}")
            self.failed += 1
    
    def print_summary(self):
        """Показати результати"""
        print(f"\n{'='*60}")
        print(f"Результати тестування:")
        print(f"{'='*60}")
        print(f"✓ Пройдено: {self.passed}")
        print(f"✗ Не пройдено: {self.failed}")
        print(f"{'='*60}\n")
        return self.failed == 0
    
    def start_server(self):
        """Запустити Flask сервер"""
        print("🚀 Запуск Flask сервера...")
        base_dir = Path(__file__).parent
        self.process = Popen(
            ["python", "app.py"],
            cwd=base_dir,
            stdout=PIPE,
            stderr=PIPE
        )
        time.sleep(3)  # Очікування запуску
        print("✓ Сервер запущено\n")
    
    def stop_server(self):
        """Зупинити Flask сервер"""
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✓ Сервер зупинено")

def main():
    runner = TestRunner()
    runner.start_server()
    
    try:
        print("🧪 Тестування Flask Market\n")
        
        # === Основні маршрути ===
        print("📄 Тестування маршрутів (Routes)...")
        runner.test("GET /", lambda: requests.get(f"{BASE_URL}/").raise_for_status())
        runner.test("GET /market", lambda: requests.get(f"{BASE_URL}/market").raise_for_status())
        runner.test("GET /cart", lambda: requests.get(f"{BASE_URL}/cart").raise_for_status())
        runner.test("GET /reviews", lambda: requests.get(f"{BASE_URL}/reviews").raise_for_status())
        runner.test("GET /about", lambda: requests.get(f"{BASE_URL}/about").raise_for_status())
        runner.test("GET /health", lambda: requests.get(f"{BASE_URL}/health").raise_for_status())
        
        # === API Products ===
        print("\n🛍️  Тестування API /api/products...")
        def test_products():
            response = requests.get(f"{API_URL}/products")
            response.raise_for_status()
            data = response.json()
            assert isinstance(data, list), "Products мають бути у форматі list"
        
        runner.test("GET /api/products", test_products)
        
        # === API Feedback ===
        print("\n💬 Тестування API /api/feedback...")
        def test_feedback_get():
            response = requests.get(f"{API_URL}/feedback")
            response.raise_for_status()
            data = response.json()
            assert isinstance(data, list), "Feedback мають бути у форматі list"
        
        runner.test("GET /api/feedback", test_feedback_get)
        
        def test_feedback_post():
            payload = {
                "name": "Test User",
                "email": "test@example.com",
                "message": "Test feedback"
            }
            response = requests.post(f"{API_URL}/feedback", json=payload)
            assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        runner.test("POST /api/feedback", test_feedback_post)
        
        # === API Orders ===
        print("\n📦 Тестування API /api/orders...")
        def test_orders_get():
            response = requests.get(f"{API_URL}/orders")
            response.raise_for_status()
            data = response.json()
            assert isinstance(data, list), "Orders мають бути у форматі list"
        
        runner.test("GET /api/orders", test_orders_get)
        
        # === Swagger/API Docs ===
        print("\n📚 Тестування API документації...")
        runner.test("GET /apidocs/", lambda: requests.get(f"{BASE_URL}/apidocs/").raise_for_status())
        runner.test("GET /apispec.json", lambda: requests.get(f"{BASE_URL}/apispec.json").raise_for_status())
        
        # === Performance ===
        print("\n⚡ Тестування продуктивності...")
        def test_response_time():
            import time
            start = time.time()
            requests.get(f"{API_URL}/products").raise_for_status()
            elapsed = time.time() - start
            assert elapsed < 1.0, f"Response time {elapsed}s > 1s (очікується < 1s)"
        
        runner.test("Response time < 1s", test_response_time)
        
        print("\n✓ Всі тести завершені")
        
    finally:
        runner.stop_server()
    
    success = runner.print_summary()
    
    if success:
        print("✅ Всі тести пройдені! Застосунок готовий до розгортання.")
        return 0
    else:
        print("❌ Деякі тести не пройшли. Перевірте помилки вище.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
