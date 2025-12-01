# Impostor Lobby - Django

Aplicación de lobby simple con **Django + HTML/CSS/JS vanilla puro**. Sin frameworks frontend (no Angular, no React, no TypeScript).

Los usuarios pueden unirse a una sala de espera, ver otros usuarios conectados en tiempo real, y salir del lobby.

## How it Works

Our Django application, `example` is configured as an installed application in `api/settings.py`:

```python
# api/settings.py
INSTALLED_APPS = [
    # ...
    'example',
]
```

We allow "\*.vercel.app" subdomains in `ALLOWED_HOSTS`, in addition to 127.0.0.1:

```python
# api/settings.py
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app']
```

The `wsgi` module must use a public variable named `app` to expose the WSGI application:

```python
# api/wsgi.py
app = get_wsgi_application()
```

The corresponding `WSGI_APPLICATION` setting is configured to use the `app` variable from the `api.wsgi` module:

```python
# api/settings.py
WSGI_APPLICATION = 'api.wsgi.app'
```

There is a single view which renders the current time in `example/views.py`:

```python
# example/views.py
from datetime import datetime

from django.http import HttpResponse


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)
```

This view is exposed a URL through `example/urls.py`:

```python
# example/urls.py
from django.urls import path

from example.views import index


urlpatterns = [
    path('', index),
]
```

Finally, it's made accessible to the Django server inside `api/urls.py`:

```python
# api/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('example.urls')),
]
```

This example uses the Web Server Gateway Interface (WSGI) with Django to enable handling requests on Vercel with Serverless Functions.

## Estructura del Proyecto

- **Navegación**: 4 items en el navbar (Impostor, Item2, Item3, Item4)
- **Página Impostor** (`/`): Formulario para ingresar nombre de usuario y unirse al lobby
- **Sala de Espera** (`/waiting`): 
  - Contador regresivo de 60 a 0 segundos
  - Lista de usuarios conectados (actualización cada 2 segundos)
  - Botón para salir del lobby
- **Persistencia**: Los usuarios se guardan en `lobby.json` en el root del proyecto

## APIs JSON

- `POST /api/lobby/join` - Unirse al lobby
  ```json
  { "username": "tu_nick" }
  ```
- `POST /api/lobby/leave` - Salir del lobby
  ```json
  { "username": "tu_nick" }
  ```
- `GET /api/lobby/users` - Listar usuarios en el lobby

## Ejecutar Localmente

1. Crear y activar entorno virtual:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

3. Ejecutar servidor de desarrollo:
```powershell
python manage.py runserver
```

4. Abrir navegador en `http://localhost:8000`

## Deploy en Vercel

El proyecto está configurado para desplegar en Vercel:

```bash
vercel
```

**Nota importante**: En Vercel, el filesystem es efímero. El archivo `lobby.json` se resetea entre despliegues y no se comparte entre instancias. Para persistencia real en producción, considera usar Supabase u otra base de datos.
