# example/urls.py
from django.urls import path
from .views import (
    index,
    waiting_view,
    item2_view,
    item3_view,
    item4_view,
    login_view,
    register_view,
    ping,
    env_check,
    lobby_join,
    lobby_leave,
    lobby_users,
)

urlpatterns = [
    # Páginas principales
    path('', index, name='index'),
    path('waiting', waiting_view, name='waiting'),
    path('item2', item2_view, name='item2'),
    path('item3', item3_view, name='item3'),
    path('item4', item4_view, name='item4'),
    # Login/Register (legacy)
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    # Diagnóstico
    path('ping/', ping),
    path('env/', env_check),
    # Lobby JSON-backed endpoints
    path('api/lobby/join', lobby_join),
    path('api/lobby/leave', lobby_leave),
    path('api/lobby/users', lobby_users),
]
