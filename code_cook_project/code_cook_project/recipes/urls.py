from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cargar-datos', views.cargar_datos, name='cargar_datos'),

]
