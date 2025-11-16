"""Тестування REST API endpoints"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_get_products():
    """Тест GET /api/products"""
    print("\n=== Тест: GET /api/products ===")
    response = requests.get(f"{BASE_URL}/api/products")
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_get_orders():
    """Тест GET /api/orders"""
    print("\n=== Тест: GET /api/orders ===")
    response = requests.get(f"{BASE_URL}/api/orders")
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_create_order():
    """Тест POST /api/orders"""
    print("\n=== Тест: POST /api/orders ===")
    order_data = {
        "customer_name": "Тестовий Користувач",
        "customer_email": "test@example.com",
        "customer_phone": "+380501111111",
        "promo_code": "1234",
        "cart": {
            "1": {
                "id": 1,
                "name": "Ноутбук",
                "price": 25000.00,
                "quantity": 2
            }
        }
    }
    response = requests.post(f"{BASE_URL}/api/orders", json=order_data)
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json().get('order_id')

def test_get_order_details(order_id):
    """Тест GET /api/orders/<id>"""
    print(f"\n=== Тест: GET /api/orders/{order_id} ===")
    response = requests.get(f"{BASE_URL}/api/orders/{order_id}")
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_update_order_status(order_id):
    """Тест PUT /api/orders/<id>"""
    print(f"\n=== Тест: PUT /api/orders/{order_id} ===")
    update_data = {"status": "processing"}
    response = requests.put(f"{BASE_URL}/api/orders/{order_id}", json=update_data)
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_get_feedback():
    """Тест GET /api/feedback"""
    print("\n=== Тест: GET /api/feedback ===")
    response = requests.get(f"{BASE_URL}/api/feedback")
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_create_feedback():
    """Тест POST /api/feedback"""
    print("\n=== Тест: POST /api/feedback ===")
    feedback_data = {
        "name": "Тестовий Відгук",
        "email": "feedback@example.com",
        "message": "Чудовий магазин! Рекомендую всім!"
    }
    response = requests.post(f"{BASE_URL}/api/feedback", json=feedback_data)
    print(f"Статус: {response.status_code}")
    print(f"Відповідь: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("Початок тестування API...")
    
    try:
        # 1. Продукти
        test_get_products()
        
        # 2. Замовлення
        test_get_orders()
        order_id = test_create_order()
        
        if order_id:
            test_get_order_details(order_id)
            test_update_order_status(order_id)
        
        # 3. Відгуки
        test_get_feedback()
        test_create_feedback()
        
        print("\n✅ Всі тести завершені!")
        
    except Exception as e:
        print(f"\n❌ Помилка: {e}")
