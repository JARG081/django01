# example/views.py
from datetime import datetime
import hashlib
from django.conf import settings
from supabase import create_client
from django.http import HttpResponse, HttpResponseRedirect

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def index(request):
    # Redirige directamente al login
    return HttpResponseRedirect('/login/')

def login(request):
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .container { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 350px; }
            h2 { margin-bottom: 20px; }
            input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }
            button { width: 100%; padding: 10px; background: #007bff; color: #fff; border: none; border-radius: 4px; font-size: 1em; }
            button:hover { background: #0056b3; }
            .register-link { display: block; margin-top: 15px; text-align: center; color: #007bff; text-decoration: none; }
            .register-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Ingresar</h2>
            <form method="post">
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

        # Hash de la contraseña
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()

        # Insertar usuario en Supabase
        data = {"nick": nick, "pass": hashed_pass}
        response = supabase.table("Users").insert(data).execute()

        # Redirige al login tras registro exitoso
        if response.status_code == 201:
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponse("<h2>Error al registrar usuario</h2><a href='/register/'>Intentar de nuevo</a>")

    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Registro</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .container { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 350px; }
            h2 { margin-bottom: 20px; }
            input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }
            button { width: 100%; padding: 10px; background: #28a745; color: #fff; border: none; border-radius: 4px; font-size: 1em; }
            button:hover { background: #218838; }
            .login-link { display: block; margin-top: 15px; text-align: center; color: #007bff; text-decoration: none; }
            .login-link:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Registro</h2>
            <form method="post">
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