# Лабораторна робота №5: Розробка RESTful API.  

## Інформація про проєкт
- **Назва проєкту:** Інтернет магазин електронніки
- **Автори:** Кучерук Максим Сергійович


## Опис проєкту
REST API для інтернет-магазину електроніки. Надає можливість керувати товарами, замовленнями та відгуками клієнтів через HTTP-запити. API підтримує створення замовлень з промокодами, автоматичний розрахунок знижок, управління статусами замовлень та збір відгуків від клієнтів.

## Технології
- Python 3.11
- Flask 3.1.2
- SQLite3 (вбудована БД)
- Flasgger 0.9.7.1 (Swagger документація)
- JSON (формат обміну даними)

## Endpoints API

### 1. Отримати всі продукти
- **URL:** `/api/products`
- **Метод:** `GET`
- **Опис:** Повертає список усіх доступних товарів у магазині
- **Параметри:** Відсутні
- **Приклад відповіді:**
```json
[
  {
    "id": 1,
    "name": "Ноутбук ASUS",
    "description": "Потужний ноутбук для роботи",
    "price": 25000.00,
    "stock": 15,
    "category": "Ноутбуки"
  }
]
```
- **Коди відповідей:** 200 OK, 500 Internal Server Error
- **Скріншот з Postman (або Swagger):**
![скріншот з postman](lab-reports/lab5/1.png)

### 2. Отримати всі замовлення
- **URL:** `/api/orders`
- **Метод:** `GET`
- **Опис:** Повертає список усіх замовлень з інформацією про клієнтів
- **Параметри:** Відсутні
- **Приклад відповіді:**
```json
[
  {
    "id": 1,
    "customer_id": 1,
    "customer_name": "Іван Петренко",
    "customer_email": "ivan@example.com",
    "status": "new",
    "created_at": "2024-11-16T10:30:00",
    "promo_code": "1234",
    "discount_amount": 2500.00
  }
]
```
- **Коди відповідей:** 200 OK, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/2.png)

### 3. Отримати деталі замовлення
- **URL:** `/api/orders/{order_id}`
- **Метод:** `GET`
- **Опис:** Повертає повну інформацію про конкретне замовлення, включаючи товари
- **Параметри:** `order_id` (integer, обов'язковий) - ID замовлення
- **Приклад відповіді:**
```json
{
  "order": {
    "id": 2,
    "customer_name": "Іван Петренко",
    "customer_email": "ivan@example.com",
    "phone": "+380501234567",
    "status": "processing",
    "created_at": "2024-11-16T10:40:00",
    "promo_code": "1234",
    "discount_amount": 5000.00
  },
  "items": [
    {
      "id": 1,
      "order_id": 2,
      "product_id": 1,
      "product_name": "Ноутбук ASUS",
      "quantity": 2,
      "price": 25000.00
    }
  ]
}
```
- **Коди відповідей:** 200 OK, 404 Not Found, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/3.png)

### 4. Створити нове замовлення
- **URL:** `/api/orders`
- **Метод:** `POST`
- **Опис:** Створює нове замовлення з автоматичним розрахунком знижки при використанні промокоду
- **Заголовки:** `Content-Type: application/json`
- **Приклад запиту:**
```json
{
  "customer_name": "Іван Петренко",
  "customer_email": "ivan@example.com",
  "customer_phone": "+380501234567",
  "promo_code": "1234",
  "cart": {
    "1": {
      "id": 1,
      "name": "Ноутбук ASUS",
      "price": 25000.00,
      "quantity": 2
    }
  }
}
```
- **Приклад відповіді:**
```json
{
  "message": "Order created successfully",
  "order_id": 2
}
```
- **Коди відповідей:** 201 Created, 400 Bad Request, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/4.png)

### 5. Оновити статус замовлення
- **URL:** `/api/orders/{order_id}`
- **Метод:** `PUT`
- **Опис:** Змінює статус існуючого замовлення
- **Параметри:** `order_id` (integer, обов'язковий) - ID замовлення
- **Заголовки:** `Content-Type: application/json`
- **Приклад запиту:**
```json
{
  "status": "processing"
}
```
- **Дозволені статуси:** `new`, `processing`, `shipped`, `completed`, `cancelled`
- **Приклад відповіді:**
```json
{
  "message": "Order updated successfully"
}
```
- **Коди відповідей:** 200 OK, 400 Bad Request, 404 Not Found, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/5.png)

### 6. Видалити замовлення
- **URL:** `/api/orders/{order_id}`
- **Метод:** `DELETE`
- **Опис:** Видаляє замовлення та всі пов'язані з ним товари
- **Параметри:** `order_id` (integer, обов'язковий) - ID замовлення
- **Приклад відповіді:**
```json
{
  "message": "Order deleted successfully"
}
```
- **Коди відповідей:** 200 OK, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/6.png)

### 7. Отримати всі відгуки
- **URL:** `/api/feedback`
- **Метод:** `GET`
- **Опис:** Повертає список усіх відгуків клієнтів
- **Параметри:** Відсутні
- **Приклад відповіді:**
```json
[
  {
    "id": 1,
    "name": "Олена Іваненко",
    "email": "olena@example.com",
    "message": "Чудовий сервіс!",
    "created_at": "2024-11-16T11:00:00"
  }
]
```
- **Коди відповідей:** 200 OK, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/7.png)

### 8. Створити відгук
- **URL:** `/api/feedback`
- **Метод:** `POST`
- **Опис:** Додає новий відгук від клієнта
- **Заголовки:** `Content-Type: application/json`
- **Приклад запиту:**
```json
{
  "name": "Олена Іваненко",
  "email": "olena@example.com",
  "message": "Дуже задоволена покупкою! Швидка доставка."
}
```
- **Приклад відповіді:**
```json
{
  "message": "Feedback submitted successfully"
}
```
- **Коди відповідей:** 201 Created, 400 Bad Request, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/8.png)

### 9. Видалити відгук
- **URL:** `/api/feedback/{feedback_id}`
- **Метод:** `DELETE`
- **Опис:** Видаляє відгук за ID
- **Параметри:** `feedback_id` (integer, обов'язковий) - ID відгуку
- **Приклад відповіді:**
```json
{
  "message": "Feedback deleted successfully",
  "deleted_id": 1
}
```
- **Коди відповідей:** 200 OK, 404 Not Found, 500 Internal Server Error
![скріншот з postman](lab-reports/lab5/9.png)

## Результати тестування в Postman (або Swagger)

### Postman

### Тестовий сценарій 1: [Всі запити підряд]
- **Мета:** [активацвя всіх запитів підряд]
- **Результат:** ✅ Успішно 
- **Скріншот:**
![Тест 1](lab-reports/lab5/10.png)

## Обробка помилок
Список реалізованих кодів помилок:

### 200 OK
- **Коли виникає:** Успішне виконання GET, PUT, DELETE запитів
- **Приклад:** Отримання списку товарів, оновлення статусу замовлення

### 201 Created
- **Коли виникає:** Успішне створення нового ресурсу (POST запити)
- **Приклад:** Створення замовлення, додавання відгуку
- **Відповідь містить:** ID створеного ресурсу або повідомлення про успіх

### 400 Bad Request
- **Коли виникає:** 
  - Відсутні обов'язкові поля у запиті
  - Некоректний формат даних
  - Невалідне значення статусу замовлення (не з переліку дозволених)
- **Приклад відповіді:**
```json
{
  "error": "Missing required fields: customer_name, customer_email, customer_phone, cart"
}
```
або
```json
{
  "error": "Invalid status. Allowed: ['cancelled', 'completed', 'new', 'processing', 'shipped']"
}
```

### 404 Not Found
- **Коли виникає:**
  - Спроба отримати деталі неіснуючого замовлення
  - Оновлення статусу неіснуючого замовлення
  - Видалення неіснуючого відгуку
- **Приклад відповіді:**
```json
{
  "error": "Order not found"
}
```
або
```json
{
  "error": "Feedback not found"
}
```

### 500 Internal Server Error
- **Коли виникає:** Непередбачена помилка на сервері (помилка БД, виняток у коді)
- **Приклад відповіді:**
```json
{
  "error": "Database connection failed"
}
```
