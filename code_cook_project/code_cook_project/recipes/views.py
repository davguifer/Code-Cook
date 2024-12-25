from django.shortcuts import render
from .models import Receta

# Create your views here.
def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'recetas_list.html', {'recetas': recetas})
