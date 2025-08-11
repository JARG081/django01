# example/views.py
from datetime import datetime

from django.http import HttpResponse

def index(request):
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #f0f2f5;
                color: #333;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .container {
                background-color: #fff;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                max-width: 400px;
                width: 100%;
                text-align: center;
            }
            .main-link {
                display: inline-block;
                background-color: #007bff;
                color: #fff;
                padding: 15px 30px;
                font-size: 1.2em;
                font-weight: bold;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s ease, transform 0.2s ease;
                margin-top: 20px;
            }
            .main-link:hover {
                background-color: #0056b3;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenido</h1>
            <p>Para continuar, ingrese a su cuenta.</p>
            <a href="/login/" class="main-link">Ingresar</a>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)

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
            input[type="text"], input[type="password"], input[type="email"] { width: 100%; padding: 10px; margin-bottom: 15px; border-radius: 4px; border: 1px solid #ccc; }
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
                <input type="email" name="email" placeholder="Correo electrónico" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Registrarse</button>
            </form>
            <a href="/login/" class="login-link">¿Ya tienes cuenta? Ingresa</a>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)