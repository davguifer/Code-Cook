from django.shortcuts import render
from .models import Recipes
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

# Vista de la página principal
def home(request):
    return render(request, 'base.html')

# URL base de las recetas
BASE_URL = "https://www.bbcgoodfood.com/search"

def load_data(request):
    """Scrapea todas las recetas de la página y los usuarios y guarda los datos en la base de datos correspondiente."""
    recetas_guardadas = 0
    errores = []

    try:
        # Obtener la página principal
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscamos cada contenedor div de cada receta
        category_heading = soup.find("div", class_="layout-md-rail__primary")
        if category_heading:
            category_container = category_heading.find_all("div", class_="search-result--list")
            #print(category_container)
            for receta in category_container:
                enlace_receta = receta.find("a", class_="link d-block")
                if enlace_receta:
                    url_receta = f"https://www.bbcgoodfood.com{enlace_receta['href']}"
                    #print(url_receta)
                    # Acceder al detalle de la receta
                    response_receta = requests.get(url_receta)
                    response_receta.raise_for_status()
                    soup_receta = BeautifulSoup(response_receta.text, 'html.parser')

                    # Extraer detalles de la receta
                    titulo = soup_receta.find("h1", class_="heading-1").text.strip()
                    servings = soup_receta.find("li", class_="mt-sm list-item").findAll("div")[-1].string.strip()
                    aux_prep_time = soup_receta.find("li", class_ = "body-copy-small list-item").findAll("span")[-1].string.strip().split()
                    if aux_prep_time[1] == "hr" or aux_prep_time[1] == "hrs" and len(aux_prep_time) == 2:
                        aux_prep_time[0] == aux_prep_time[0]*60
                    elif len(aux_prep_time) == 4 and aux_prep_time[1] == "hr" or aux_prep_time[1] == "hrs":
                        aux_prep_time[0] == aux_prep_time[0]*60 + aux_prep_time[3]
                    else:
                        aux_prep_time[0] == aux_prep_time[0]
                    
                    prep_time = aux_prep_time[0]
                    
                
                    


                    
                    
                    '''
                    Receta.objects.create(
                        titulo=titulo,
                        ingredientes=ingredientes,
                        accesorios="",  # No se identificaron accesorios en las imágenes
                        tiempo_total=int(tiempo_total.split()[0]),
                        tiempo_preparacion=0,  # Ajustar si existe en la estructura
                        tiempo_de_coccion=0,  # Ajustar si existe en la estructura
                        tiempo_de_resposo=0,  # Ajustar si existe en la estructura
                        num_personas=0,  # Ajustar si existe en la estructura
                    )
                    
                    recetas_guardadas += 1
                    '''
                    
    except Exception as e:
        errores.append(str(e))

    return JsonResponse({
        'mensaje': f"Se han guardado {recetas_guardadas} recetas.",
        'errores': errores
    })