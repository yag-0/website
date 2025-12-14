# Multi-stage build для мінімальної величини образу
FROM python:3.11-slim as builder

WORKDIR /tmp
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

LABEL maintainer="Flask Market <info@flaskmarket.com>"
LABEL description="Flask Market - інтернет-магазин електроніки"

WORKDIR /app

# Install only wget для healthcheck
RUN apt-get update \
  && apt-get install -y --no-install-recommends wget \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy Python dependencies з builder stage
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data && chmod 755 /app/data

# Set environment
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    DATABASE_PATH=/app/data/database.db

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/health || exit 1

# Run application
CMD ["python", "app.py"]
