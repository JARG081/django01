# example/views.py
from datetime import datetime
import hashlib
from django.conf import settings
from supabase import create_client
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods

def get_supabase():
    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        print("Error inicializando Supabase:", e)
        return None

def index(request):
    return HttpResponseRedirect('/login/')

@ensure_csrf_cookie                 # Asegura set de cookie en GET
@require_http_methods(["GET","POST"])
@csrf_protect                       # Valida token en POST
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    # POST
    username = request.POST.get("username")
    password = request.POST.get("password")
    if not username or not password:
        return HttpResponse("<h2>Faltan datos</h2><a href='/login/'>Intentar de nuevo</a>")

    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    supabase = get_supabase()
    if not supabase:
        return HttpResponse("<h2>Error al conectar con Supabase</h2>")

    try:
        response = supabase.table("users").select("*").eq("nick", username).execute()
    except Exception as e:
        return HttpResponse(f"<h2>Error en la consulta: {e}</h2>")

    if not hasattr(response, "data") or not response.data:
        return HttpResponse("<h2>Usuario no encontrado</h2><a href='/login/'>Intentar de nuevo</a>")

    user = response.data[0]
    if user["pass"] != hashed_pass:
        return HttpResponse("<h2>Contraseña incorrecta</h2><a href='/login/'>Intentar de nuevo</a>")

    return HttpResponse(f"<h2>Bienvenido, {username}</h2>")

@ensure_csrf_cookie
@require_http_methods(["GET","POST"])
@csrf_protect
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

    # POST
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
        supabase.table("users").insert(data).execute()
    except Exception as e:
        return HttpResponse(f"<h2>Error al registrar usuario: {e}</h2><a href='/register/'>Intentar de nuevo</a>")

    return HttpResponseRedirect('/login/')
