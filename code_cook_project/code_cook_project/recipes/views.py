from django.shortcuts import render
from .models import Recipes
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def home(request):
    return render(request, 'base.html')

BASE_URL = "https://www.bbcgoodfood.com/search?page=1"

# This function will be used to load the data from the BBC Good Food website
def load_data(request):
    recetas_guardadas = 0
    errores = []
    page = 1 
    cont = 0 

    try:
        while page <= 20:  
            paginated_url = f"https://www.bbcgoodfood.com/search?page={page}"
            response = requests.get(paginated_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Search for each div container of each recipe
            category_heading = soup.find("div", class_="layout-md-rail__primary")
            if not category_heading:
                break  

            category_container = category_heading.find_all("div", class_="search-result--list")
            if not category_container:
                break 
            
            for recipes in category_container:
                link_receta = recipes.find("a", class_="link d-block")
                if link_receta:
                    url_receta = f"https://www.bbcgoodfood.com{link_receta['href']}"
                    # Access the recipe detail
                    response_receta = requests.get(url_receta)
                    response_receta.raise_for_status()
                    soup_receta = BeautifulSoup(response_receta.text, 'html.parser')

                    # Extract the recipe details

                    '''Title'''
                    title = soup_receta.find("h1", class_="heading-1").text.strip()

                    '''Servings'''
                    div_elements = soup_receta.findAll("div", class_="icon-with-text__children")
                    servings = "Unknown"

                    for div in div_elements:
                        if "Serves" in div.text.strip(): 
                            servings_text = div.text.strip()
                            numbers = " ".join([word for word in servings_text.split() if word.isdigit() or "-" in word])
                            servings = f"Serves {numbers}"
                            break
                    

                    '''Times(in minutes)'''
                    container = soup_receta.find("div", class_="icon-with-text__children").findAll("li", class_="body-copy-small list-item")
                    
                    
                    prep_time = 0 
                    cook_time = 0

                    if len(container) == 2:
                        if "Prep" in container[0].text:
                            prep_time = convert_to_minutes(container[0].find("time").text)
                            cook_time = convert_to_minutes(container[1].find("time").text)
                        elif "Cook" in container[0].text:
                            cook_time = convert_to_minutes(container[0].find("time").text)
                    elif len(container) == 1:
                        if "Prep" in container[0].text:
                            prep_time = convert_to_minutes(container[0].find("time").text)
                        elif "Cook" in container[0].text:
                            cook_time = convert_to_minutes(container[0].find("time").text)
                    
                    total_time = prep_time + cook_time

                    '''Ingredients'''
                    aux_ingredients = []
                    ingredients_sections = soup_receta.find_all("ul", class_="ingredients-list list")

                    for section in ingredients_sections:
                        li_elements = section.find_all("li")
                        for li in li_elements:
                            all_text = []
                            if li.contents:
                                for content in li.contents:
                                    if content.name == "a":
                                        all_text.append(content.get_text(strip=True))
                                    elif isinstance(content, str):
                                        all_text.append(content.strip())

                            if not all_text and li.find("a", class_="link--styled"):
                                all_text.append(li.find("a", class_="link--styled").get_text(strip=True))
                            ingredient = " ".join(all_text).strip()
                            aux_ingredients.append(ingredient)
                            

                    ingredients = ", ".join(aux_ingredients)


                    '''Difficulty'''
                    div_elements = soup_receta.findAll("div", class_="icon-with-text__children")
                    difficulty = "Unknown"

                    for div in div_elements:
                        text = div.text.strip()
                        if "Easy" in text or "More effort" in text or "A challenge" in text:
                            difficulty = text
                            break


                    print(f"Title: {title}")
                    print(f"Prep time: {prep_time}")
                    print(f"Cook time: {cook_time}")
                    print(f"Total time: {total_time}")
                    print(f"Sergins: {servings}")
                    print(f"Ingredients: {ingredients}")
                    print(f"Difficulty: {difficulty}")
                    print("--------------------")
                            
            page += 1
            print(f"Page: {page}")

    except Exception as e:
        errores.append(str(e))

    return JsonResponse({
        'mensaje': f"Se han guardado {recetas_guardadas} recetas.",
        'errores': errores
    })

def convert_to_minutes(time_str):
    time_parts = time_str.replace("and", "").split() 
    total_minutes = 0
    
    for i in range(0, len(time_parts), 2):
        value = int(time_parts[i])  
        unit = time_parts[i + 1].lower()  
        
        if "hr" in unit:  # "hr" o "hrs"
            total_minutes += value * 60
        elif "min" in unit:  # "min" o "mins"
            total_minutes += value
    
    return total_minutes

