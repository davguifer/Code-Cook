from django.urls import path
from . import views
from recipes.whoosh_config.whoosh_config import load_index

urlpatterns = [
    path('', views.home, name='home'),
    path('load-data', views.confirm_load_data, name='confirm_load_data'),
    path('load-index', load_index, name='load_index'),
    path('recipes', views.recipes_list, name='recipes_list'),

]
