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
            /* Estilos generales del cuerpo */
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

            /* Contenedor principal para centrar el contenido */
            .container {
                background-color: #ffffff; /* Fondo blanco para el contenido */
                padding: 40px;
                border-radius: 10px; /* Bordes redondeados */
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Sombra sutil para dar profundidad */
                max-width: 800px;
                width: 100%;
                text-align: center; /* Centrar todo el texto dentro del contenedor */
                box-sizing: border-box;
            }

            /* Estilo para el título principal */
            h1 {
                color: #1c2b4d; /* Un azul oscuro */
                font-size: 2.5em;
                margin-top: 0;
                margin-bottom: 10px;
            }

            /* Estilo para el subtítulo */
            h2 {
                color: #555; /* Un gris más oscuro */
                font-size: 1.5em;
                font-weight: 400; /* Más ligero que el título */
                margin-bottom: 30px;
            }

            /* Estilo para el párrafo de información */
            p {
                font-size: 1.1em;
                line-height: 1.6; /* Espaciado entre líneas para mejor legibilidad */
                margin-bottom: 30px;
            }

            /* Estilo para el enlace, haciéndolo parecer un botón */
            .repo-link {
                display: inline-block;
                background-color: #007bff; /* Color azul primario */
                color: #ffffff; /* Texto blanco */
                padding: 15px 30px;
                font-size: 1.2em;
                font-weight: bold;
                text-decoration: none; /* Quitar el subrayado del enlace */
                border-radius: 5px; /* Bordes redondeados */
                transition: background-color 0.3s ease, transform 0.2s ease; /* Transiciones suaves */
            }

            /* Efecto al pasar el cursor sobre el enlace */
            .repo-link:hover {
                background-color: #0056b3; /* Un azul más oscuro */
                transform: translateY(-2px); /* Eleva ligeramente el botón */
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
            
            <a href="#URL_PERSONALIZADA" class="repo-link">Repositorio</a>
        </div>

    </body>
    </html>
    '''
    return HttpResponse(html)