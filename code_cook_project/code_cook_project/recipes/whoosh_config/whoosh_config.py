import shutil
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import MultifieldParser, OrGroup
from django.shortcuts import render
from recipes.models import Recipes
import os
from django.shortcuts import redirect


def load_index(request):
    if request.method == "POST":
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

        return redirect("home")
    return render(request, "confirm_load_index.html")


'''
def buscar_recetas(request):
    if request.method == "GET":
        query = request.GET.get("query", "")
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        ix = open_dir(index_dir)
        results_list = []

        with ix.searcher() as searcher:
            parser = MultifieldParser(["title", "synopsis"], schema=ix.schema, group=OrGroup)
            search_query = parser.parse(query)
            results = searcher.search(search_query)

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
    return render(request, "buscar_recetas.html")
'''

