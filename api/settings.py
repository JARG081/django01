# api/settings.py

# -----------------------------------------------------------------------------
# Básicos
# -----------------------------------------------------------------------------
import os
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-...")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".vercel.app",  # cualquier subdominio de vercel
]

# Si has usado dos dominios parecidos, incluye ambos por seguridad:
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://minutosepsm.vercel.app",
    "https://minutosespm.vercel.app",
]
# Cargar variables de entorno desde .env
load_dotenv(BASE_DIR / ".env")

# -----------------------------------------------------------------------------
# Básicos
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-...")
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".vercel.app",  # cualquier subdominio de vercel
]

# Si has usado dos dominios parecidos, incluye ambos por seguridad:
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://minutosepsm.vercel.app",
    "https://minutosespm.vercel.app",
]

# -----------------------------------------------------------------------------
# Cookies / CSRF (seguras en prod)
# -----------------------------------------------------------------------------
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# Mismo dominio/origen => 'Lax'. Si tu front será otro dominio + HTTPS, usa 'None'.
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

# Detrás de proxy (Vercel) para detectar HTTPS y host correctos
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# -----------------------------------------------------------------------------
# Apps / Middleware
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "example",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Si tienes templates globales en /templates, mantenlo; APP_DIRS permite example/templates
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api.wsgi.application"

# -----------------------------------------------------------------------------
# DB / Internacionalización / Static
# -----------------------------------------------------------------------------
DATABASES = {}  # Usa tu config real cuando toque

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# Supabase (LEER SOLO DE ENV; no crashear si faltan para que /env y /ping funcionen)
# -----------------------------------------------------------------------------
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
# En backend preferimos service_role; si no hay, cae a anon
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning(
        "Supabase ENV incompleta: faltan SUPABASE_URL o SUPABASE_*_KEY. "
        "La app arranca, pero las vistas que usen Supabase pueden fallar."
    )

# -----------------------------------------------------------------------------
# Logging a consola (para ver tracebacks en Vercel → Functions / Logs)
# -----------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
