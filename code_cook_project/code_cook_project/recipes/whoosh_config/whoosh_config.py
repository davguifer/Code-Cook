import shutil
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import MultifieldParser, OrGroup
from whoosh.query import Term, NumericRange
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from recipes.models import Recipes
import os
from whoosh.qparser import QueryParser


def load_index(request):
    if request.method == "POST":
        try:
            index_dir = os.path.join(os.path.dirname(__file__), 'index')

            schema = Schema(
                title=TEXT(stored=True, phrase=False),
                servings=TEXT(stored=True), 
                prep_time=NUMERIC(stored=True),
                cook_time=NUMERIC(stored=True),
                total_time=NUMERIC(stored=True),
                ingredients=TEXT(stored=True, phrase=False),
                difficulty=TEXT(stored=True, phrase=False),
                rating=NUMERIC(stored=True, decimal_places=2),
                num_reviews=NUMERIC(stored=True)
            )

            if os.path.exists(index_dir):
                shutil.rmtree(index_dir)
            os.mkdir(index_dir)

            ix = create_in(index_dir, schema=schema)
            writer = ix.writer()

            recipes = Recipes.objects.all()

            for recipe in recipes:
                writer.add_document(
                    title=recipe.title,
                    servings=recipe.servings,
                    prep_time=recipe.prep_time,
                    cook_time=recipe.cook_time,
                    total_time=recipe.total_time,
                    ingredients=recipe.ingredients,
                    difficulty=recipe.difficulty,
                    rating=recipe.rating,
                    num_reviews=recipe.num_reviews
                )
            writer.commit()

            messages.success(request, f"Index loaded successfully! {recipes.count()} recipes have been indexed.")

        except Exception as e:
            messages.error(request, f"An error occurred while loading the index: {str(e)}")

        return redirect("home")
    
    return render(request, "confirm_load_index.html")


def search_recipes_by_title(request): 
    results_list = []

    if request.method == "GET" and "titulo" in request.GET:
        query = request.GET.get("titulo", "").strip().lower()  # Convertir a minúsculas y eliminar espacios
        index_dir = os.path.join(os.path.dirname(__file__), 'index')

        try:
            ix = open_dir(index_dir)
            with ix.searcher() as searcher:
                # Crear consulta básica
                parser = QueryParser("title", schema=ix.schema)  # Usamos QueryParser para buscar solo en el título
                search_query = parser.parse(f'*{query}*')  # El asterisco (*) ayuda a buscar subtítulos que contengan palabras

                results = searcher.search(search_query)

                # Extraer datos de los resultados
                for result in results:
                    results_list.append({
                        "title": result["title"],
                        "servings": result.get("servings", "N/A"),
                        "prep_time": result.get("prep_time", "N/A"),
                        "cook_time": result.get("cook_time", "N/A"),
                        "total_time": result.get("total_time", "N/A"),
                        "ingredients": result.get("ingredients", "N/A"),
                        "difficulty": result.get("difficulty", "N/A"),
                        "rating": result.get("rating", "N/A"),
                        "num_reviews": result.get("num_reviews", "N/A"),
                    })

        except Exception as e:
            print(f"Error al buscar recetas: {e}")
    
    # Renderizar la plantilla con los resultados
    return render(request, "search_recipes_by_title.html", {"results": results_list})





def buscar_recetas_por_tiempo_coccion(request):
    if request.method == "GET":
        valor = int(request.GET.get("valor", 0))
        comparador = request.GET.get("comparador", "gte")  # Valores: gte, lte, eq
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        ix = open_dir(index_dir)
        results_list = []

        with ix.searcher() as searcher:
            if comparador == "gte":
                query = NumericRange("cook_time", valor, None)
            elif comparador == "lte":
                query = NumericRange("cook_time", None, valor)
            else:
                query = NumericRange("cook_time", valor, valor)

            results = searcher.search(query)

            for result in results:
                results_list.append({
                    "title": result["title"],
                    "servings": result["servings"],
                    "ingredients": result["ingredients"],
                    "prep_time": result["prep_time"],
                    "difficulty": result["difficulty"],
                    "url": result["url"]
                })

        return JsonResponse({"results": results_list})
    return render(request, "buscar_recetas_por_tiempo_coccion.html")

def buscar_recetas_por_ingrediente(request):
    if request.method == "GET":
        ingrediente = request.GET.get("ingrediente", "")
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        ix = open_dir(index_dir)
        results_list = []

        with ix.searcher() as searcher:
            query = Term("ingredients", ingrediente)
            results = searcher.search(query)

            for result in results:
                results_list.append({
                    "title": result["title"],
                    "servings": result["servings"],
                    "ingredients": result["ingredients"],
                    "prep_time": result["prep_time"],
                    "difficulty": result["difficulty"],
                    "url": result["url"]
                })

        return JsonResponse({"results": results_list})
    return render(request, "buscar_recetas_por_ingrediente.html")


