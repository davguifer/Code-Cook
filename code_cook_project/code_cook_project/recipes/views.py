from django.shortcuts import render
from .models import Recipes
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup


def home(request):
    return render(request, 'base.html')

BASE_URL = "https://www.bbcgoodfood.com/search"

# This function will be used to load the data from the BBC Good Food website
def load_data(request):
    recetas_guardadas = 0
    errores = []
    cont = 0
    try:
        # Get the main page
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Search for each div container of each recipe
        category_heading = soup.find("div", class_="layout-md-rail__primary")
        if category_heading:
            category_container = category_heading.find_all("div", class_="search-result--list")   
            for recipes in category_container:
                link_receta = recipes.find("a", class_="link d-block")
                print(link_receta)
                if link_receta:
                    url_receta = f"https://www.bbcgoodfood.com{link_receta['href']}"
                    # Access the recipe detail
                    response_receta = requests.get(url_receta)
                    response_receta.raise_for_status()
                    soup_receta = BeautifulSoup(response_receta.text, 'html.parser')
                    # Extract the recipe details
                    title = soup_receta.find("h1", class_="heading-1").text.strip()
                    servings = soup_receta.find("li", class_="mt-sm list-item").findAll("div")[-1].string.strip()       
                    container = soup_receta.find("div", class_="icon-with-text__children").findAll("li", class_="body-copy-small list-item")

                    if len(container) == 2:
                        prep_time = convert_to_minutes(container[0].find("time").text)
                        cook_time = convert_to_minutes(container[1].find("time").text)
                    else:
                        prep_time = convert_to_minutes(container[0].find("time").text)
                        cook_time = 0

                    total_time = prep_time + cook_time

                    ingredients = []
                    ingredients_sections = soup_receta.find_all("ul", class_="ingredients-list list")
                    for section in ingredients_sections:
                        li_elements = section.find_all("li")
                        for li in li_elements:
                            ingredient = li.get_text(strip=True)
                            ingredients.append(ingredient)
                    
                    ingredients_text = ", ".join(ingredients)
                    
                    difficulty = soup_receta.findAll("li", class_="mt-sm mr-xl list-item")[1].text

                    '''
                    print(f"Title: {title}")
                    print(f"Servings: {servings}")
                    print(f"Prep Time: {prep_time} minutes")
                    print(f"Cook Time: {cook_time} minutes")
                    print(f"Total Time: {total_time} minutes")
                    print(f"Ingredients: {ingredients_text}")
                    print(f"Difficulty: {difficulty}")
                    cont += 1
                    print(cont)
                    print("-------------------------------------")
                    '''
                    
                    




                    
                                        
                    
                
                    


                    
                    
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