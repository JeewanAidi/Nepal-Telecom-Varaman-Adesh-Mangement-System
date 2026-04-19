"""
Django settings for ntc_travel project.
Nepal Telecom Travel Order Management System

Environment-aware settings:
  - Local development: SQLite (no .env needed)
  - Production (Render): PostgreSQL via DATABASE_URL env variable
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────────────
# On Render, set SECRET_KEY in environment variables.
# Locally, it falls back to the insecure default.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-ntc-mahendranagar-travel-management-2024-secret-key'
)

# DEBUG: True locally, False on Render (set DEBUG=False in Render env vars)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allow localhost + Render domain
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    '127.0.0.1,localhost'
).split(',')

# Always allow Render's internal domains
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ─────────────────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel_management',
]

# ─────────────────────────────────────────────────────────
# MIDDLEWARE — WhiteNoise must be right after SecurityMiddleware
# ─────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← Render static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ntc_travel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'travel_management' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ntc_travel.wsgi.application'

# ─────────────────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────────────────
# If DATABASE_URL is set (Render provides this automatically for PostgreSQL),
# use PostgreSQL. Otherwise fall back to local SQLite for development.
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: Render PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,        # Keep connections alive for 10 minutes
            conn_health_checks=True,
        )
    }
else:
    # Local development: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─────────────────────────────────────────────────────────
# PASSWORD VALIDATORS
# ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────────────────
# LOCALISATION
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────
# STATIC FILES — WhiteNoise serves them on Render
# ─────────────────────────────────────────────────────────
STATIC_URL = '/static/'

# Folder where your app's static files live (CSS, JS, images)
STATICFILES_DIRS = [
    BASE_DIR / 'travel_management' / 'static',
]

# Folder where `collectstatic` gathers everything for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compression + caching for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────────────────
# MEDIA FILES
# ─────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────────────────
# AUTH REDIRECTS
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# ─────────────────────────────────────────────────────────
# SECURITY HEADERS (enforced in production only)
# ─────────────────────────────────────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
