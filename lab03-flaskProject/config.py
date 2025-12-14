# Production Configuration для Flask Market

import os
from datetime import timedelta

# === BASIC SETTINGS ===
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-CHANGE-THIS')
DEBUG = False
TESTING = False

# === SESSION SETTINGS ===
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_REFRESH_EACH_REQUEST = True

# === DATABASE SETTINGS ===
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'site.db')

# === LOGGING SETTINGS ===
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# === SECURITY SETTINGS ===
# CSRF Protection (якщо буде впровадний Flask-WTF)
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None
WTF_CSRF_SSL_STRICT = True

# === CORS SETTINGS ===
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'https://yourdomain.com').split(',')

# === RATE LIMITING ===
RATELIMIT_ENABLED = True
RATELIMIT_DEFAULT = "200 per day, 50 per hour"
RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')

# === CACHE SETTINGS ===
CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# === EMAIL SETTINGS (для сповіщень) ===
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@flaskmarket.com')

# === ADMIN SETTINGS ===
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'change-this-strong-password')

# === THIRD-PARTY SERVICES ===
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')

# === ADDITIONAL SETTINGS ===
JSON_SORT_KEYS = False
JSONIFY_PRETTYPRINT_REGULAR = False
