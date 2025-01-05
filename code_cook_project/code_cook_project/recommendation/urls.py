from django.urls import path
from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/recommendations/', views.recipe_recommendations, name='recipe_recommendations'),
    path('confirm-load-similarities/', views.confirm_load_recommendation, name='confirm-load-similarities'),

]
