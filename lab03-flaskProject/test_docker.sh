#!/bin/bash
# Скрипт для тестування Flask Market в Docker контейнері
# Використання: bash test_docker.sh

set -e

echo "🐳 Тестування Flask Market в Docker"
echo "===================================="

# Перевірка Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker не встановлено"
    exit 1
fi

echo "✓ Docker знайдено"

# Перевірка docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "✗ docker-compose не встановлено"
    exit 1
fi

echo "✓ docker-compose знайдено"

# Зупинення старих контейнерів
echo ""
echo "Очищення старих контейнерів..."
docker-compose down -v 2>/dev/null || true

# Збірка образу
echo ""
echo "Збирання Docker образу..."
docker-compose build --no-cache

# Запуск контейнера
echo ""
echo "Запуск контейнера..."
docker-compose up -d

# Очікування запуску
echo ""
echo "Очікування запуску контейнера..."
sleep 5

# Перевірка health check
echo ""
echo "Перевірка health status..."
for i in {1..10}; do
    if docker-compose exec -T web wget --no-verbose --tries=1 --spider http://localhost:5000/health 2>/dev/null; then
        echo "✓ Health check пройшов"
        break
    fi
    echo "⏳ Спроба $i/10..."
    sleep 2
done

# Перевірка API
echo ""
echo "Тестування API endpoints..."

echo "  GET /api/products"
docker-compose exec -T web curl -s http://localhost:5000/api/products | head -c 100
echo "..."

echo ""
echo "  GET /api/feedback"
docker-compose exec -T web curl -s http://localhost:5000/api/feedback | head -c 100
echo "..."

# Перевірка логів
echo ""
echo "Останні логи контейнера:"
docker-compose logs --tail=20

echo ""
echo "✓ Тестування завершено успішно!"
echo ""
echo "Для зупинення контейнера: docker-compose down"
echo "Для перегляду логів: docker-compose logs -f"
