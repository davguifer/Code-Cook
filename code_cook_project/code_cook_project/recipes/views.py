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
                    # Acceder al detalle de la receta
                    response_receta = requests.get(url_receta)
                    response_receta.raise_for_status()
                    soup_receta = BeautifulSoup(response_receta.text, 'html.parser')

                    # Extraer detalles de la receta
                    titulo = soup_receta.find("h1", class_="heading-1").text.strip()
                    servings = soup_receta.find("li", class_="mt-sm list-item").findAll("div")[-1].string.strip()       
                    
                    container = soup_receta.find("div", class_="icon-with-text__children").findAll("li", class_="body-copy-small list-item")
                    if len(container) == 2:
                        prep_time = convert_to_minutes(container[0].find("time").text)
                        cook_time = convert_to_minutes(container[1].find("time").text)
                    else:
                        prep_time = convert_to_minutes(container[0].find("time").text)
                        cook_time = 0
                    
                    



                    
                                        
                    
                
                    


                    
                    
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

def convert_to_minutes(time_str):
    time_parts = time_str.split()
    total_minutes = 0
    
    for i in range(0, len(time_parts), 2):
        value = int(time_parts[i])
        unit = time_parts[i + 1].lower()
        
        if "hr" in unit:  # Puede ser "hr" o "hrs"
            total_minutes += value * 60
        elif "min" in unit:  # Puede ser "min" o "mins"
            total_minutes += value
    
    return total_minutes