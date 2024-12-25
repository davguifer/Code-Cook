from django.contrib import admin
from .models import Receta

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'visitas')
