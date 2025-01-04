from django.urls import path
from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/recommendations/', views.recipe_recommendations, name='recipe_recommendations'),
    path('update-similarities/', views.update_recipe_similarities, name='update-similarities'),

]
