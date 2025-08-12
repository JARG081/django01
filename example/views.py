# example/views.py
from datetime import datetime
import hashlib
from django.conf import settings
from supabase import create_client
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token


# Función para inicializar el cliente de Supabase cuando se necesite
def get_supabase():
    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        print("Error inicializando Supabase:", e)
        return None


def index(request):
    return HttpResponseRedirect('/login/')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return HttpResponse("<h2>Faltan datos</h2><a href='/login/'>Intentar de nuevo</a>")

        hashed_pass = hashlib.sha256(password.encode()).hexdigest()

        supabase = get_supabase()
        if not supabase:
            return HttpResponse("<h2>Error al conectar con Supabase</h2>")

        try:
            response = supabase.table("Users").select("*").eq("nick", username).execute()
        except Exception as e:
            return HttpResponse(f"<h2>Error en la consulta: {e}</h2>")

        if not hasattr(response, "data") or not response.data:
            return HttpResponse("<h2>Usuario no encontrado</h2><a href='/login/'>Intentar de nuevo</a>")

        user = response.data[0]
        if user["pass"] != hashed_pass:
            return HttpResponse("<h2>Contraseña incorrecta</h2><a href='/login/'>Intentar de nuevo</a>")

        return HttpResponse(f"<h2>Bienvenido, {username}</h2>")

    csrf_token = get_token(request)
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
            .container {{ background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 350px; }}
            h2 {{ margin-bottom: 20px; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }}
            button {{ width: 100%; padding: 10px; background: #007bff; color: #fff; border: none; border-radius: 4px; font-size: 1em; }}
            button:hover {{ background: #0056b3; }}
            .register-link {{ display: block; margin-top: 15px; text-align: center; color: #007bff; text-decoration: none; }}
            .register-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Ingresar</h2>
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="text" name="username" placeholder="Usuario" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Ingresar</button>
            </form>
            <a href="/register/" class="register-link">¿No tienes cuenta? Regístrate</a>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)


def register(request):
    if request.method == "POST":
        nick = request.POST.get("username")
        password = request.POST.get("password")

        if not nick or not password:
            return HttpResponse("<h2>Faltan datos</h2><a href='/register/'>Intentar de nuevo</a>")

        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        data = {"nick": nick, "pass": hashed_pass}

        supabase = get_supabase()
        if not supabase:
            return HttpResponse("<h2>Error al conectar con Supabase</h2>")

        try:
            response = supabase.table("Users").insert(data).execute()
        except Exception as e:
            return HttpResponse(f"<h2>Error al registrar usuario: {e}</h2><a href='/register/'>Intentar de nuevo</a>")

        return HttpResponseRedirect('/login/')

    csrf_token = get_token(request)
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Registro</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
            .container {{ background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 350px; }}
            h2 {{ margin-bottom: 20px; }}
            input[type="text"], input[type="password"] {{ width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }}
            button {{ width: 100%; padding: 10px; background: #28a745; color: #fff; border: none; border-radius: 4px; font-size: 1em; }}
            button:hover {{ background: #218838; }}
            .login-link {{ display: block; margin-top: 15px; text-align: center; color: #007bff; text-decoration: none; }}
            .login-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Registro</h2>
            <form method="post">
                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                <input type="text" name="username" placeholder="Usuario" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Registrarse</button>
            </form>
            <a href="/login/" class="login-link">¿Ya tienes cuenta? Ingresa</a>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)
