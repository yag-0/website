# Multi-stage build для мінімальної величини образу
FROM python:3.11-slim as builder

WORKDIR /tmp
# Copy entire build context; handle both repo-root and subfolder contexts
COPY . /tmp/context
# Create a virtual environment, detect requirements.txt path, install deps, and stage app source
RUN python -m venv /opt/venv \
  && /opt/venv/bin/pip install --upgrade pip \
  && REQ="/tmp/context/requirements.txt" \
  && if [ ! -f "$REQ" ]; then REQ="/tmp/context/lab03-flaskProject/requirements.txt"; fi \
  && /opt/venv/bin/pip install --no-cache-dir -r "$REQ" \
  && mkdir -p /opt/appsrc \
  && if [ -d "/tmp/context/lab03-flaskProject" ]; then cp -a /tmp/context/lab03-flaskProject/. /opt/appsrc/; else cp -a /tmp/context/. /opt/appsrc/; fi

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

# Copy Python virtualenv та підготовлене джерело застосунку з builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/appsrc /app



# Create data directory for SQLite
RUN mkdir -p /app/data && chmod 755 /app/data

# Set environment
ENV PATH=/opt/venv/bin:$PATH \
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
