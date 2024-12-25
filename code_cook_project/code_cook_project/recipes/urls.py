from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_recetas, name='lista_recetas'),
    #path('receta/<int:pk>/', views.detalle_receta, name='detalle_receta'),
    #path('recomendaciones/<int:pk>/', views.recomendaciones, name='recomendaciones'),
]
