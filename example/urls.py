# example/urls.py
from django.urls import path
from .views import index, login_view, register_view, ping, env_check

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('ping/', ping),
    path('env/', env_check),
]
