# api/settings.py
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-...'
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.vercel.app']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://minutosepsm.vercel.app',  # producción (https obligatorio)
]

# --- Cookies seguros: en dev (DEBUG=True) deben ir en False para permitir HTTP ---
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Django debe confiar en los headers del proxy para detectar HTTPS/host
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Si tu front y back están en el MISMO origen, Lax es lo ideal.
# Si vas a enviar cookies cross-site (front en *.vercel.app y API en otro dominio),
# usa None **solo si** SIEMPRE servirás por HTTPS:
CSRF_COOKIE_SAMESITE = 'Lax'    # o 'None' si front/backend son dominios distintos + HTTPS
SESSION_COOKIE_SAMESITE = 'Lax' # o 'None' si necesitas cross-site con HTTPS

# Si no usas django-cors-headers, quita esta línea para evitar falsas expectativas
# CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'example',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # CSRF activo
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]
WSGI_APPLICATION = 'api.wsgi.application'

DATABASES = {}  # (Tu config real)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # usamos service_role en backend

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Faltan SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY en Vercel → Settings → Environment Variables"
    )
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("Supabase ENV incompleta: SUPABASE_URL or SUPABASE_*_KEY not set. Views will degrade gracefully.")
    
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": { "console": { "class": "logging.StreamHandler" } },
    "root": { "handlers": ["console"], "level": "INFO" },
}
