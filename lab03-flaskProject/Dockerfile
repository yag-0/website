# Single-stage build on slim (musllinux wheels avoid rpds issues)
FROM python:3.11-slim

WORKDIR /app

# Install system deps for healthcheck + Python deps
RUN apt-get update \
  && apt-get install -y --no-install-recommends wget \
  && rm -rf /var/lib/apt/lists/*

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create data dir for SQLite
RUN mkdir -p /app/data && chmod 755 /app/data

# Copy app code
COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_PATH=/app/data/database.db

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
