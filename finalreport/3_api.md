# API Документація

## Зміст
1. [Загальна інформація](#загальна-інформація)
2. [Базовий URL](#базовий-url)
3. [Аутентифікація](#аутентифікація)
4. [Endpoints](#endpoints)
   - [Products](#products)
   - [Orders](#orders)
   - [Feedback](#feedback)
5. [Коди помилок](#коди-помилок)
6. [Приклади використання](#приклади-використання)

---

## Загальна інформація

**API Version:** 1.0  
**Format:** JSON  
**Charset:** UTF-8  
**CORS:** Enabled (всі origins)  
**Documentation:** Swagger UI доступний за адресою `/apidocs`

### Технології
- Flask REST API
- Flasgger (Swagger/OpenAPI 2.0)
- SQLite backend

---

## Базовий URL

```
Development: http://localhost:5000
Production:  https://your-domain.com
```

Всі endpoints починаються з `/api/`

---

## Аутентифікація

**Поточна версія:** Аутентифікація не потрібна (public API)

Для production рекомендується додати:
- API Key в заголовках
- JWT tokens
- Rate limiting

---

## Endpoints

### Products

#### GET /api/products
Отримати список всіх продуктів

**Request:**
```http
GET /api/products HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Ноутбук ASUS TUF Gaming",
    "description": "Потужний ігровий ноутбук з RTX 4060",
    "price": 25999.99,
    "stock": 15,
    "category": "Ноутбуки",
    "image_url": "/static/images/laptop1.jpg",
    "created_at": "2024-01-15 10:30:00"
  },
  {
    "id": 2,
    "name": "Клавіатура Razer BlackWidow",
    "description": "Механічна клавіатура з RGB підсвіткою",
    "price": 3499.00,
    "stock": 42,
    "category": "Периферія",
    "image_url": "/static/images/keyboard.jpg",
    "created_at": "2024-01-16 14:20:00"
  }
]
```

**Response (500 Error):**
```json
{
  "error": "Database connection error"
}
```

**cURL приклад:**
```bash
curl -X GET http://localhost:5000/api/products
```

**JavaScript приклад:**
```javascript
fetch('http://localhost:5000/api/products')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

**Python приклад:**
```python
import requests

response = requests.get('http://localhost:5000/api/products')
products = response.json()
print(products)
```

---

### Orders

#### GET /api/orders
Отримати список всіх замовлень

**Request:**
```http
GET /api/orders HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "customer_name": "Іван Петренко",
    "customer_email": "ivan@example.com",
    "customer_phone": "+380501234567",
    "status": "new",
    "total_amount": 25999.99,
    "promo_code": "WINTER25",
    "discount_amount": 6499.99,
    "created_at": "2024-01-20 15:45:00"
  },
  {
    "id": 2,
    "customer_name": "Олена Сидоренко",
    "customer_email": "olena@example.com",
    "customer_phone": "+380672345678",
    "status": "processing",
    "total_amount": 7998.00,
    "promo_code": null,
    "discount_amount": 0.0,
    "created_at": "2024-01-21 10:15:00"
  }
]
```

**cURL приклад:**
```bash
curl -X GET http://localhost:5000/api/orders
```

---

#### GET /api/orders/{order_id}
Отримати деталі конкретного замовлення з позиціями товарів

**Parameters:**
- `order_id` (path, required) - ID замовлення

**Request:**
```http
GET /api/orders/1 HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "order": {
    "id": 1,
    "customer_name": "Іван Петренко",
    "customer_email": "ivan@example.com",
    "customer_phone": "+380501234567",
    "status": "new",
    "total_amount": 25999.99,
    "promo_code": "WINTER25",
    "discount_amount": 6499.99,
    "created_at": "2024-01-20 15:45:00"
  },
  "items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "product_name": "Ноутбук ASUS TUF Gaming",
      "quantity": 1,
      "price_at_time": 25999.99,
      "subtotal": 25999.99
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 5,
      "product_name": "Миша Logitech G502",
      "quantity": 2,
      "price_at_time": 1499.00,
      "subtotal": 2998.00
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "error": "Order not found"
}
```

**cURL приклад:**
```bash
curl -X GET http://localhost:5000/api/orders/1
```

**Python приклад:**
```python
import requests

order_id = 1
response = requests.get(f'http://localhost:5000/api/orders/{order_id}')

if response.status_code == 200:
    order_data = response.json()
    print(f"Order #{order_data['order']['id']}")
    print(f"Customer: {order_data['order']['customer_name']}")
    print(f"Items: {len(order_data['items'])}")
elif response.status_code == 404:
    print("Order not found")
```

---

#### POST /api/orders
Створити нове замовлення

**Request Body:**
```json
{
  "customer_name": "Іван Петренко",
  "customer_email": "ivan@example.com",
  "customer_phone": "+380501234567",
  "promo_code": "WINTER25",
  "cart": {
    "1": {
      "id": 1,
      "name": "Ноутбук ASUS TUF Gaming",
      "price": 25999.99,
      "quantity": 1
    },
    "5": {
      "id": 5,
      "name": "Миша Logitech G502",
      "price": 1499.00,
      "quantity": 2
    }
  }
}
```

**Required fields:**
- `customer_name` (string) - Ім'я покупця
- `customer_email` (string) - Email покупця
- `customer_phone` (string) - Телефон покупця
- `cart` (object) - Кошик з товарами

**Optional fields:**
- `promo_code` (string) - Промокод для знижки

**Response (201 Created):**
```json
{
  "message": "Order created successfully",
  "order_id": 42
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Missing required fields: customer_name, customer_email, customer_phone, cart"
}
```

**cURL приклад:**
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Іван Петренко",
    "customer_email": "ivan@example.com",
    "customer_phone": "+380501234567",
    "cart": {
      "1": {
        "id": 1,
        "name": "Ноутбук",
        "price": 25999.99,
        "quantity": 1
      }
    }
  }'
```

**JavaScript приклад:**
```javascript
const orderData = {
  customer_name: 'Іван Петренко',
  customer_email: 'ivan@example.com',
  customer_phone: '+380501234567',
  promo_code: 'WINTER25',
  cart: {
    '1': {
      id: 1,
      name: 'Ноутбук ASUS',
      price: 25999.99,
      quantity: 1
    }
  }
};

fetch('http://localhost:5000/api/orders', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(orderData)
})
.then(response => response.json())
.then(data => {
  console.log('Order created:', data.order_id);
})
.catch(error => console.error('Error:', error));
```

**Python приклад:**
```python
import requests

order_data = {
    'customer_name': 'Іван Петренко',
    'customer_email': 'ivan@example.com',
    'customer_phone': '+380501234567',
    'promo_code': 'WINTER25',
    'cart': {
        '1': {
            'id': 1,
            'name': 'Ноутбук ASUS',
            'price': 25999.99,
            'quantity': 1
        },
        '5': {
            'id': 5,
            'name': 'Миша Logitech',
            'price': 1499.00,
            'quantity': 2
        }
    }
}

response = requests.post(
    'http://localhost:5000/api/orders',
    json=order_data
)

if response.status_code == 201:
    result = response.json()
    print(f"Order created with ID: {result['order_id']}")
else:
    print(f"Error: {response.json()['error']}")
```

---

#### PUT /api/orders/{order_id}
Оновити статус замовлення

**Parameters:**
- `order_id` (path, required) - ID замовлення

**Request Body:**
```json
{
  "status": "processing"
}
```

**Allowed statuses:**
- `new` - Нове замовлення
- `processing` - В обробці
- `shipped` - Відправлено
- `completed` - Виконано
- `cancelled` - Скасовано

**Response (200 OK):**
```json
{
  "message": "Order updated successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid status. Allowed: ['cancelled', 'completed', 'new', 'processing', 'shipped']"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Order not found"
}
```

**cURL приклад:**
```bash
curl -X PUT http://localhost:5000/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "processing"}'
```

**Python приклад:**
```python
import requests

order_id = 1
response = requests.put(
    f'http://localhost:5000/api/orders/{order_id}',
    json={'status': 'completed'}
)

if response.status_code == 200:
    print("Order status updated")
elif response.status_code == 404:
    print("Order not found")
elif response.status_code == 400:
    print(f"Invalid status: {response.json()['error']}")
```

---

#### DELETE /api/orders/{order_id}
Видалити замовлення

**Parameters:**
- `order_id` (path, required) - ID замовлення

**Request:**
```http
DELETE /api/orders/1 HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "message": "Order deleted successfully"
}
```

**cURL приклад:**
```bash
curl -X DELETE http://localhost:5000/api/orders/1
```

**Python приклад:**
```python
import requests

order_id = 1
response = requests.delete(f'http://localhost:5000/api/orders/{order_id}')

if response.status_code == 200:
    print("Order deleted successfully")
```

---

### Feedback

#### GET /api/feedback
Отримати всі відгуки

**Request:**
```http
GET /api/feedback HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Іван Петренко",
    "email": "ivan@example.com",
    "message": "Дуже задоволений покупкою! Швидка доставка.",
    "created_at": "2024-01-20 16:30:00"
  },
  {
    "id": 2,
    "name": "Олена Сидоренко",
    "email": "olena@example.com",
    "message": "Відмінний магазин, рекомендую!",
    "created_at": "2024-01-21 09:15:00"
  }
]
```

**cURL приклад:**
```bash
curl -X GET http://localhost:5000/api/feedback
```

---

#### POST /api/feedback
Створити новий відгук

**Request Body:**
```json
{
  "name": "Іван Петренко",
  "email": "ivan@example.com",
  "message": "Дуже задоволений покупкою! Швидка доставка."
}
```

**Required fields:**
- `name` (string) - Ім'я автора
- `email` (string) - Email автора
- `message` (string) - Текст відгуку

**Response (201 Created):**
```json
{
  "message": "Feedback submitted successfully"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "All fields are required"
}
```

**cURL приклад:**
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Іван Петренко",
    "email": "ivan@example.com",
    "message": "Чудовий магазин!"
  }'
```

**JavaScript приклад:**
```javascript
const feedbackData = {
  name: 'Іван Петренко',
  email: 'ivan@example.com',
  message: 'Дуже задоволений покупкою!'
};

fetch('http://localhost:5000/api/feedback', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(feedbackData)
})
.then(response => response.json())
.then(data => console.log(data.message))
.catch(error => console.error('Error:', error));
```

---

#### DELETE /api/feedback/{feedback_id}
Видалити відгук

**Parameters:**
- `feedback_id` (path, required) - ID відгуку

**Request:**
```http
DELETE /api/feedback/1 HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "message": "Feedback deleted successfully",
  "deleted_id": 1
}
```

**Response (404 Not Found):**
```json
{
  "error": "Feedback not found"
}
```

**cURL приклад:**
```bash
curl -X DELETE http://localhost:5000/api/feedback/1
```

---

## Коди помилок

### HTTP Status Codes

| Код | Значення              | Опис                                      |
|-----|-----------------------|-------------------------------------------|
| 200 | OK                    | Запит успішно виконано                    |
| 201 | Created               | Ресурс успішно створено                   |
| 400 | Bad Request           | Некоректний запит або відсутні параметри  |
| 404 | Not Found             | Ресурс не знайдено                        |
| 500 | Internal Server Error | Внутрішня помилка сервера                 |

### Error Response Format

Всі помилки повертаються у форматі:
```json
{
  "error": "Опис помилки"
}
```

**Приклади:**
```json
{
  "error": "Missing required fields: customer_name, customer_email, customer_phone, cart"
}
```

```json
{
  "error": "Order not found"
}
```

```json
{
  "error": "Database connection error"
}
```

---

## Приклади використання

### Повний цикл замовлення (Python)

```python
import requests

BASE_URL = 'http://localhost:5000/api'

# 1. Отримуємо список товарів
response = requests.get(f'{BASE_URL}/products')
products = response.json()
print(f"Доступно {len(products)} товарів")

# 2. Вибираємо товари і додаємо в кошик
cart = {}
for product in products[:2]:  # Візьмемо перші 2 товари
    cart[str(product['id'])] = {
        'id': product['id'],
        'name': product['name'],
        'price': product['price'],
        'quantity': 1
    }

# 3. Створюємо замовлення
order_data = {
    'customer_name': 'Тестовий Користувач',
    'customer_email': 'test@example.com',
    'customer_phone': '+380501234567',
    'promo_code': 'WINTER25',
    'cart': cart
}

response = requests.post(f'{BASE_URL}/orders', json=order_data)
if response.status_code == 201:
    order_id = response.json()['order_id']
    print(f"Замовлення створено: #{order_id}")
    
    # 4. Перевіряємо деталі замовлення
    response = requests.get(f'{BASE_URL}/orders/{order_id}')
    order_details = response.json()
    print(f"Загальна сума: {order_details['order']['total_amount']} грн")
    print(f"Кількість позицій: {len(order_details['items'])}")
    
    # 5. Оновлюємо статус
    response = requests.put(
        f'{BASE_URL}/orders/{order_id}',
        json={'status': 'processing'}
    )
    print("Статус оновлено на 'processing'")

# 6. Залишаємо відгук
feedback_data = {
    'name': 'Тестовий Користувач',
    'email': 'test@example.com',
    'message': 'Чудовий сервіс!'
}
response = requests.post(f'{BASE_URL}/feedback', json=feedback_data)
print("Відгук відправлено")
```

### Frontend інтеграція (JavaScript/React)

```javascript
// API service module
class FlaskMarketAPI {
  constructor(baseURL = 'http://localhost:5000/api') {
    this.baseURL = baseURL;
  }

  async fetchProducts() {
    const response = await fetch(`${this.baseURL}/products`);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  }

  async createOrder(orderData) {
    const response = await fetch(`${this.baseURL}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    });
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error);
    }
    return response.json();
  }

  async getOrderDetails(orderId) {
    const response = await fetch(`${this.baseURL}/orders/${orderId}`);
    if (!response.ok) throw new Error('Order not found');
    return response.json();
  }

  async submitFeedback(feedbackData) {
    const response = await fetch(`${this.baseURL}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feedbackData)
    });
    if (!response.ok) throw new Error('Failed to submit feedback');
    return response.json();
  }
}

// Використання
const api = new FlaskMarketAPI();

// Отримання товарів
api.fetchProducts()
  .then(products => {
    console.log('Products:', products);
  })
  .catch(error => console.error(error));

// Створення замовлення
const order = {
  customer_name: 'Іван Петренко',
  customer_email: 'ivan@example.com',
  customer_phone: '+380501234567',
  cart: { /* ... */ }
};

api.createOrder(order)
  .then(result => {
    console.log('Order created:', result.order_id);
  })
  .catch(error => alert(error.message));
```

### Mobile App (Flutter/Dart)

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class FlaskMarketAPI {
  final String baseUrl = 'http://localhost:5000/api';

  Future<List<dynamic>> getProducts() async {
    final response = await http.get(Uri.parse('$baseUrl/products'));
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load products');
    }
  }

  Future<Map<String, dynamic>> createOrder(Map<String, dynamic> orderData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/orders'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(orderData),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      final error = json.decode(response.body);
      throw Exception(error['error']);
    }
  }
}

// Використання
final api = FlaskMarketAPI();

// Отримати товари
final products = await api.getProducts();
print('Loaded ${products.length} products');

// Створити замовлення
final orderData = {
  'customer_name': 'Іван Петренко',
  'customer_email': 'ivan@example.com',
  'customer_phone': '+380501234567',
  'cart': { /* ... */ }
};

try {
  final result = await api.createOrder(orderData);
  print('Order created: ${result['order_id']}');
} catch (e) {
  print('Error: $e');
}
```

---

## Rate Limiting (Рекомендовано для production)

```python
# Додати в app.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@api_bp.route('/api/orders', methods=['POST'])
@limiter.limit("10 per minute")
def create_order():
    # ...
```

---

## Swagger/OpenAPI Документація

Інтерактивна документація доступна за адресою:

```
http://localhost:5000/apidocs
```

Тут можна:
- Переглянути всі endpoints
- Тестувати API запити
- Переглянути схеми даних
- Завантажити OpenAPI специфікацію

---

## Висновок

Flask Market API надає простий та зрозумілий інтерфейс для роботи з каталогом товарів, замовленнями та відгуками. RESTful архітектура дозволяє легко інтегрувати API з будь-якими клієнтськими застосунками.

**Основні переваги:**
- ✅ RESTful дизайн
- ✅ JSON формат
- ✅ Swagger документація
- ✅ CORS підтримка
- ✅ Прості та зрозумілі endpoints

**Для production:**
- Додати API аутентифікацію (JWT)
- Впровадити rate limiting
- Додати пагінацію для великих списків
- Впровадити кешування
- Додати versioning (напр. `/api/v1/products`)
