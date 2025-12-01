# example/views.py
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
import hashlib
import os
import json
from pathlib import Path
from typing import List


SUPABASE_SERVICE_ROL_KEY = os.getenv("SUPABASE_SERVICE_ROL_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")

def get_supabase():
    # Importar dentro de la función para que un fallo no rompa el arranque
    try:
        from supabase import create_client
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        # NO levantar excepción aquí; devolvemos None y la vista muestra un mensaje
        print("Error inicializando Supabase:", e)
        return None

def index(request):
    return render(request, 'impostor.html')

def waiting_view(request):
    return render(request, 'waiting.html')

def item2_view(request):
    return render(request, 'item.html', {'title': 'Item2'})

def item3_view(request):
    return render(request, 'item.html', {'title': 'Item3'})

def item4_view(request):
    return render(request, 'item.html', {'title': 'Item4'})

@ensure_csrf_cookie
@require_http_methods(["GET","POST"])
@csrf_protect
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

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

    if not getattr(response, "data", None):
        return HttpResponse("<h2>Usuario no encontrado</h2><a href='/login/'>Intentar de nuevo</a>")

    user = response.data[0]
    if user.get("pass") != hashed_pass:
        return HttpResponse("<h2>Contraseña incorrecta</h2><a href='/login/'>Intentar de nuevo</a>")

    return HttpResponse(f"<h2>Bienvenido, {username}</h2>")

@ensure_csrf_cookie
@require_http_methods(["GET","POST"])
@csrf_protect
def register_view(request):
    if request.method == "GET":
        return render(request, "register.html")

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

# --- Endpoints de diagnóstico que NO dependen de Supabase ---
@never_cache
def ping(request):
    payload = {
        "ok": True,
        "path": request.path,
        "method": request.method,
    }
    if request.GET:
        payload["query_params"] = dict(request.GET)
    if request.body:
        try:
            payload["body"] = request.body.decode("utf-8")
        except Exception:
            payload["body"] = str(request.body)
    return JsonResponse(payload)

@never_cache
def env_check(request):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    masked_key = (key[:6] + "..." + key[-4:]) if key and len(key) > 10 else None
    payload = {
        "SUPABASE_URL_set": bool(url),
        "SUPABASE_KEY_set": bool(key),
        "SUPABASE_KEY_masked": masked_key,
    }
    # Útiles para ver encabezados que Vercel pasa a tu función
    payload["headers"] = {k: v for k, v in request.headers.items()}
    if request.GET:
        payload["query_params"] = dict(request.GET)
    return JsonResponse(payload)

# ----------------------------
# Lobby JSON-based endpoints
# ----------------------------

LOBBY_FILE = Path(settings.BASE_DIR) / "lobby.json"

def _read_lobby() -> List[str]:
    try:
        if not LOBBY_FILE.exists():
            return []
        with LOBBY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [str(x) for x in data]
            return []
    except Exception:
        return []

def _write_lobby(users: List[str]) -> None:
    tmp = LOBBY_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(sorted(set(users)), f, ensure_ascii=False)
    tmp.replace(LOBBY_FILE)

@csrf_exempt
@require_http_methods(["POST"])
def lobby_join(request):
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        body = {}
    username = (body.get("username") or "").strip()
    if not username:
        return JsonResponse({"ok": False, "error": "username requerido"}, status=400)

    users = _read_lobby()
    if username not in users:
        users.append(username)
        _write_lobby(users)
    return JsonResponse({"ok": True, "users": users})

@csrf_exempt
@require_http_methods(["POST"])
def lobby_leave(request):
    try:
        body = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        body = {}
    username = (body.get("username") or "").strip()
    if not username:
        return JsonResponse({"ok": False, "error": "username requerido"}, status=400)

    users = [u for u in _read_lobby() if u != username]
    _write_lobby(users)
    return JsonResponse({"ok": True, "users": users})

@never_cache
@require_http_methods(["GET"])
def lobby_users(request):
    return JsonResponse({"ok": True, "users": _read_lobby()})
