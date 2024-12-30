from django.urls import path
from . import views
from recipes.whoosh_config.whoosh_config import load_index, search_recipes_by_title, search_recipes_by_time, search_recipes_by_cooking_time, search_recipes_by_prep_time, search_recipes_by_total_time

urlpatterns = [
    path('', views.home, name='home'),
    path('load-data', views.confirm_load_data, name='confirm_load_data'),
    path('load-index', load_index, name='load_index'),
    path('recipes', views.recipes_list, name='recipes_list'),
    path('search/search-by-title', search_recipes_by_title, name='search_recipes_by_title'),
    path('search/search-by-time', search_recipes_by_time, name='search_recipes_by_time'),
    path('search/search-by-prep-time', search_recipes_by_prep_time, name='search_recipes_by_prep_time'),
    path('search/search-by-cook-time', search_recipes_by_cooking_time, name='search_recipes_by_cooking_time'),
    path('search/search-by-total-time', search_recipes_by_total_time, name='search_recipes_by_total_time'),

]
