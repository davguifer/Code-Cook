from django.shortcuts import render
from .models import Receta
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

# Vista de la página principal
def home(request):
    return render(request, 'base.html')


# Extracción de datos con BeautifulSoup
BASE_URL = "https://www.moulinex.es/recetas/lista"
def cargar_datos(request):
    """Scrapea todas las recetas de la página y las guarda en la base de datos."""
    recetas_guardadas = 0
    errores = []

    try:
        # Obtener la página principal
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Seleccionar el ul con la clase c__items
        lista_recetas = soup.find("ul", class_="c__items")
        print(lista_recetas)
        print("###")
        print(lista_recetas.find_all("li"))
        print("###")
        print(lista_recetas.find_all("a", class_="is-full-area ng-star-inserted"))
        if lista_recetas:
            # Encontrar todos los <a> dentro del <ul>
            enlaces = lista_recetas.find_all("a", class_="is-full-area")
            for enlace in enlaces:
                href = enlace.get("href")
                titulo = enlace.find("span", class_="is-visually-hidden").text.strip() if enlace.find("span", class_="is-visually-hidden") else "Sin título"
                print(f"Enlace: {href}, Título: {titulo}")

        if lista_recetas:
            recetas = lista_recetas.find_all("li", class_="c__item")
            for receta in recetas:
                try:
                    # Extraer enlace a la receta
                    enlace = receta.find("a", class_="is-full-area")
                    if enlace:
                        url_receta = f"https://www.moulinex.es{enlace['href']}"
                        
                        # Acceder al detalle de la receta
                        response_receta = requests.get(url_receta)
                        response_receta.raise_for_status()
                        soup_receta = BeautifulSoup(response_receta.text, 'html.parser')

                        # Extraer detalles de la receta
                        titulo = soup_receta.find("h1", class_="c__title").text.strip()
                        ingredientes = "\n".join([
                            ing.text.strip() for ing in soup_receta.find_all("p", class_="is-body-s is-medium")
                        ])
                        tiempo_total = soup_receta.find("span", class_="c__duration brand-h3").text.strip()

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
                except Exception as receta_error:
                    errores.append(f"Error procesando una receta: {receta_error}")
        else:
            errores.append("No se encontró la lista de recetas.")

    except Exception as e:
        errores.append(str(e))

    return JsonResponse({
        'mensaje': f"Se han guardado {recetas_guardadas} recetas.",
        'errores': errores
    })