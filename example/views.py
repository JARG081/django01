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
        <title>Modulo de Ingles Pre-Icfes 2025</title>
        <style>
           
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #f0f2f5; /* Un gris claro para el fondo */
                color: #333;
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }

           
            .container {
                background-color: #ffffff;
                padding: 40px;
                border-radius: 10px; 
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); 
                max-width: 800px;
                width: 100%;
                text-align: center; 
                box-sizing: border-box;
            }

           
            h1 {
                color: #1c2b4d;
                font-size: 2.5em;
                margin-top: 0;
                margin-bottom: 10px;
            }

            
            h2 {
                color: #555;
                font-size: 1.5em;
                font-weight: 400; 
                margin-bottom: 30px;
            }

            
            p {
                font-size: 1.1em;
                line-height: 1.6; 
                margin-bottom: 30px;
            }

            
            .repo-link {
                display: inline-block;
                background-color: #007bff;
                color: #ffffff;
                padding: 15px 30px;
                font-size: 1.2em;
                font-weight: bold;
                text-decoration: none; 
                border-radius: 5px; /* Bordes redondeados */
                transition: background-color 0.3s ease, transform 0.2s ease; 
            }

            
            .repo-link:hover {
                background-color: #0056b3;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>

        <div class="container">
            <h1>Módulo de Inglés Pre-Icfes 2025</h1>
            <h2>Repositorio de Documentación</h2>
            <p>
                Toda la documentación estará en el siguiente enlace en una carpeta de Google Drive.
            </p>
            
            <a href="https://drive.google.com/drive/folders/1Qhx7mElU_EdPfO3gKjrwLs2bPt4-qRc3?usp=sharing" class="repo-link">Repositorio</a>
            <p>
                Ingrese a los Minutos.
            </p>
             <h2>CAMBIO TESTEO</h2>
            <a href="/minutos/" class="repo-link">Página Minutos</a>
            <p>
                Ingrese al Timer.
            </p>
            
            <a href="/timer/" class="repo-link">Página Timer</a>
            <p>
                Ver ejemplo de otra vista:
            </p>
            
            <a href="/ejemplo/" class="repo-link">Ver Ejemplo</a>
        </div>

    </body>
    </html>
    '''
    return HttpResponse(html)

def timer(request):
    return HttpResponse("Esta es la página del temporizador.")

def minutos(request):
    return HttpResponse("Esta es la página de minutos.")

def ejemplo(request):
    return HttpResponse("Esta es la página de ejemplo.")