from flask import Blueprint, jsonify, request
from flasgger import swag_from
from models import (
    get_db_connection,
    get_products,
    get_orders,
    get_order_details,
    add_order,
    update_order_status,
    delete_order
)

api_bp = Blueprint('api', __name__)

# Products endpoints
@api_bp.route('/api/products', methods=['GET'])
def get_all_products():
    """
    Отримати всі продукти
    ---
    tags:
      - Products
    responses:
      200:
        description: Список всіх продуктів
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Ноутбук"
              price:
                type: number
                format: float
                example: 25000.50
              image:
                type: string
                example: "laptop.jpg"
      500:
        description: Помилка сервера
    """
    try:
        products = get_products()
        return jsonify([dict(product) for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Orders endpoints
@api_bp.route('/api/orders', methods=['GET'])
def get_all_orders():
    """
    Отримати всі замовлення
    ---
    tags:
      - Orders
    responses:
      200:
        description: Список всіх замовлень
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              customer_name:
                type: string
                example: "Іван Петренко"
              customer_email:
                type: string
                example: "user@example.com"
              status:
                type: string
                example: "new"
              created_at:
                type: string
                example: "2024-01-15 14:30:00"
              promo_code:
                type: string
                example: "1234"
              discount_amount:
                type: number
                format: float
                example: 250.50
      500:
        description: Помилка сервера
    """
    try:
        orders = get_orders()
        return jsonify([dict(order) for order in orders]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Отримати деталі замовлення
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID замовлення
    responses:
      200:
        description: Деталі замовлення
        schema:
          type: object
          properties:
            order:
              type: object
              properties:
                id:
                  type: integer
                customer_name:
                  type: string
                customer_email:
                  type: string
                phone:
                  type: string
                status:
                  type: string
                created_at:
                  type: string
                promo_code:
                  type: string
                discount_amount:
                  type: number
            items:
              type: array
              items:
                type: object
                properties:
                  product_name:
                    type: string
                  quantity:
                    type: integer
                  price:
                    type: number
      404:
        description: Замовлення не знайдено
      500:
        description: Помилка сервера
    """
    try:
        order, items = get_order_details(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify({
            'order': dict(order),
            'items': [dict(item) for item in items]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders', methods=['POST'])
def create_order():
    """
    Створити нове замовлення
    ---
    tags:
      - Orders
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - customer_name
            - customer_email
            - customer_phone
            - cart
          properties:
            customer_name:
              type: string
              example: "Іван Петренко"
            customer_email:
              type: string
              example: "user@example.com"
            customer_phone:
              type: string
              example: "+380501234567"
            promo_code:
              type: string
              example: "1234"
            cart:
              type: object
              example: {
                "1": {
                  "id": 1,
                  "name": "Ноутбук",
                  "price": 25000.50,
                  "quantity": 1
                }
              }
    responses:
      201:
        description: Замовлення успішно створено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order created successfully"
            order_id:
              type: integer
              example: 42
      400:
        description: Відсутні обов'язкові поля
      500:
        description: Помилка сервера
    """
    try:
        data = request.get_json()
        required_fields = ['customer_name', 'customer_email', 'customer_phone', 'cart']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields: customer_name, customer_email, customer_phone, cart'}), 400
        
        order_id = add_order(
            data['customer_name'],
            data['customer_email'],
            data['customer_phone'],
            data['cart'],
            data.get('promo_code')
        )
        return jsonify({'message': 'Order created successfully', 'order_id': order_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Оновити статус замовлення
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID замовлення
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              example: "processing"
              enum: ["new", "processing", "shipped", "completed", "cancelled"]
    responses:
      200:
        description: Замовлення успішно оновлено
      400:
        description: Некоректний або відсутній статус
      404:
        description: Замовлення не знайдено
      500:
        description: Помилка сервера
    """
    try:
        data = request.get_json()
        required_fields = ['status']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required field: status'}), 400

        status = str(data['status']).strip().lower()
        allowed = {'new','processing','shipped','completed','cancelled'}
        if status not in allowed:
            return jsonify({'error': f"Invalid status. Allowed: {sorted(list(allowed))}"}), 400

        updated = update_order_status(order_id, status)
        if not updated:
            return jsonify({'error': 'Order not found'}), 404
        return jsonify({'message': 'Order updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/orders/<int:order_id>', methods=['DELETE'])
def remove_order(order_id):
    """
    Видалити замовлення
    ---
    tags:
      - Orders
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID замовлення для видалення
    responses:
      200:
        description: Замовлення успішно видалено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Order deleted successfully"
      500:
        description: Помилка сервера
    """
    try:
        delete_order(order_id)
        return jsonify({'message': 'Order deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Feedback endpoints
@api_bp.route('/api/feedback', methods=['GET'])
def get_all_feedback():
    """
    Отримати всі відгуки
    ---
    tags:
      - Feedback
    responses:
      200:
        description: Список всіх відгуків
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Іван Петренко"
              email:
                type: string
                example: "ivan@example.com"
              message:
                type: string
                example: "Дуже задоволений покупкою!"
      500:
        description: Помилка сервера
    """
    try:
        conn = get_db_connection()
        feedback = conn.execute('SELECT * FROM feedback').fetchall()
        conn.close()
        return jsonify([dict(f) for f in feedback]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/feedback', methods=['POST'])
def create_feedback():
    """
    Створити новий відгук
    ---
    tags:
      - Feedback
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - message
          properties:
            name:
              type: string
              example: "Іван Петренко"
            email:
              type: string
              example: "ivan@example.com"
            message:
              type: string
              example: "Дуже задоволений покупкою!"
    responses:
      201:
        description: Відгук успішно створено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Feedback submitted successfully"
      400:
        description: Не всі обов'язкові поля заповнені
      500:
        description: Помилка сервера
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['name', 'email', 'message']):
            return jsonify({'error': 'All fields are required'}), 400
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)',
            (data['name'], data['email'], data['message'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Feedback submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """
    Видалити відгук
    ---
    tags:
      - Feedback
    parameters:
      - name: feedback_id
        in: path
        type: integer
        required: true
        description: ID відгуку для видалення
    responses:
      200:
        description: Відгук успішно видалено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Feedback deleted successfully"
            deleted_id:
              type: integer
              example: 1
      404:
        description: Відгук не знайдено
      500:
        description: Помилка сервера
    """
    try:
        conn = get_db_connection()
        # Перевіряємо чи існує відгук
        feedback = conn.execute('SELECT * FROM feedback WHERE id = ?', (feedback_id,)).fetchone()
        
        if not feedback:
            return jsonify({'error': 'Feedback not found'}), 404
            
        conn.execute('DELETE FROM feedback WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Feedback deleted successfully',
            'deleted_id': feedback_id
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
