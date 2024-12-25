from django.shortcuts import render
from .models import Receta
from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

# Vista de la página principal
def home(request):
    return render(request, 'base.html')


# Extracción de datos con BeautifulSoup
BASE_URL = "https://www.mundorecetas.com/recetas-pc/"


from django.shortcuts import render
from django.http import JsonResponse
from .models import Receta
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.mundorecetas.com/recetas-pc/"


def cargar_datos(request):
    """Scrapea todas las recetas de la página y las guarda en la base de datos."""
    recetas_guardadas = 0
    errores = []

    try:
        # Obtener la página principal
        response = requests.get(BASE_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer categorías
        tabla_categorias = soup.find("table", {"border": "0"})
        celdas_categorias = tabla_categorias.find_all("td", {"align": "center", "valign": "top"})

        for celda in celdas_categorias:
            enlace_categoria = celda.find("a", href=True)
            if enlace_categoria:
                nombre_categoria = enlace_categoria.text.strip()
                url_categoria = BASE_URL + enlace_categoria['href']
                # Navegar a la categoría
                response_categoria = requests.get(url_categoria)
                response_categoria.raise_for_status()
                soup_categoria = BeautifulSoup(response_categoria.text, 'html.parser')

                # Extraer recetas de la categoría
                celdas_recetas = soup_categoria.find_all("td", class_="row1")
                for celda_receta in celdas_recetas:
                    enlace_receta = celda_receta.find("a", href=True)
                    if enlace_receta:
                        url_receta = BASE_URL + enlace_receta['href']

                        # Acceder a los detalles de la receta
                        response_receta = requests.get(url_receta)
                        response_receta.raise_for_status()
                        soup_receta = BeautifulSoup(response_receta.text, 'html.parser')
                        
                        print(soup_receta.find("h1", class_="entry_title").text.strip() if soup_receta.find("h1", class_="entry_title") else "Sin título")
                        print(soup_receta.find("b").string if soup_receta.find("b").string else "Desconocido")
                        print(int(soup_receta.find(text=lambda t: "Visitas:" in t).split(":")[-1].strip().replace(".", "")) if "Visitas:" in soup_receta.text else 0)

                        # Extraer detalles de la receta
                        detalles_receta = {
                            "titulo": soup_receta.find("h1", class_="entry_title").text.strip() if soup_receta.find("h1", class_="entry_title") else "Sin título",
                            "autor": soup_receta.find("b").string if soup_receta.find("b").string else "Desconocido",
                            "visitas": int(soup_receta.find(text=lambda t: "Visitas:" in t).split(":")[-1].strip().replace(".", "")) if "Visitas:" in soup_receta.text else 0,
                            "porciones": soup_receta.find("span", class_="yield").text.strip() if soup_receta.find("span", class_="yield") else None,
                            "tiempo_preparacion": soup_receta.find("span", class_="preptime").text.strip() if soup_receta.find("span", class_="preptime") else None,
                            "tiempo_coccion": soup_receta.find("span", class_="cooktime").text.strip() if soup_receta.find("span", class_="cooktime") else None,
                            "dificultad": soup_receta.find("span", class_="duration").text.strip() if soup_receta.find("span", class_="duration") else None,
                            "categoria": nombre_categoria,
                            "introduccion": soup_receta.find("h2", text="Introducción:").find_next("p").text.strip() if soup_receta.find("h2", text="Introducción:") else None,
                            "ingredientes": "\n".join([ing.text.strip() for ing in soup_receta.find_all("span", class_="ingredient")]),
                            "instrucciones": soup_receta.find("h2", text="Instrucciones:").find_next("p").text.strip() if soup_receta.find("h2", text="Instrucciones:") else None,
                            "url": url_receta,
                        }

                        # Guardar en la base de datos
                        Receta.objects.create(**detalles_receta)
                        recetas_guardadas += 1

    except Exception as e:
        errores.append(str(e))

    return JsonResponse({
        'mensaje': f"Se han guardado {recetas_guardadas} recetas.",
        'errores': errores
    })

