# example/urls.py
from django.urls import path

from example import views  # Cambia el import para acceder a todas las vistas


urlpatterns = [
    path('', views.index),
    path('timer/', views.timer, name='timer'),
    path('minutos/', views.minutos, name='minutos'),
    path('ejemplo/', views.ejemplo, name='ejemplo'),  # Agrega la ruta de ejemplo
]