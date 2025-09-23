"""
WSGI config for api project.
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
application = get_wsgi_application()
It exposes the WSGI callable as a module-level variable named ``app``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# Vercel expects either 'app' or 'handler' as the entry point
application = get_wsgi_application()
app = application  # For Vercel compatibility
handler = application  # Alternative for Vercel compatibility
