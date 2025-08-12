from datetime import datetime
import hashlib
from django.conf import settings
from supabase import create_client
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

# Función para conectar con Supabase
def get_supabase():
    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        print("Error inicializando Supabase:", e)
        return None

# Redirige a login por defecto
def index(request):
    return HttpResponseRedirect('/login/')

# LOGIN (con CSRF activado)
@csrf_protect
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

    return render(request, "login.html")

# REGISTRO (con CSRF activado)
@csrf_protect
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
            supabase.table("Users").insert(data).execute()
        except Exception as e:
            return HttpResponse(f"<h2>Error al registrar usuario: {e}</h2><a href='/register/'>Intentar de nuevo</a>")

        return HttpResponseRedirect('/login/')

    return render(request, "register.html")
