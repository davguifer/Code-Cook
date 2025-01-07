from whoosh.query import NumericRange, And, Or, Term
import shutil
from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import MultifieldParser, OrGroup
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from recipes.models import Recipes
import os
from whoosh.qparser import QueryParser
import re

def load_index(request):
    if request.method == "POST":
        try:
            if not Recipes.objects.exists():
                messages.error(request, "No recipes found in the database. Cannot generate the search index.")
                return redirect('home') 
            else:
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


'''SEARCH RECIPES BY TITLE'''
def search_recipes_by_title(request): 
    results_list = []

    if request.method == "GET" and "titulo" in request.GET:
        query = request.GET.get("titulo", "").strip().lower()
        index_dir = os.path.join(os.path.dirname(__file__), 'index')

        try:
            ix = open_dir(index_dir)
            with ix.searcher() as searcher:
                parser = QueryParser("title", schema=ix.schema) 
                search_query = parser.parse(f'*{query}*')
                results = searcher.search(search_query)

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
            print(f"Error while searching for recipes: {e}")

    
    return render(request, "search_recipes_by_title.html", {"results": results_list})



'''SEARCH RECIPES BY TIME'''
def search_recipes_by_time(request):
    return render(request, "search_recipes_by_time.html")


'''SEARCH RECIPES BY COOKING TIME'''
def search_recipes_by_cooking_time(request):
    results_list = []
    error_message = None

    if request.method == "GET" and "cook_time" in request.GET and "filter_cook" in request.GET:
        try:
            cook_time_str = request.GET.get("cook_time", "0").strip()
            filter_cook = request.GET.get("filter_cook", "").strip()

            if not cook_time_str.isdigit():
                raise ValueError("Cooking time must be a valid integer.")
            cook_time = int(cook_time_str)

            if filter_cook not in ["lt", "gt", "eq"]:
                raise ValueError("The comparison filter is invalid. Use: lt, gt, or eq.")

            index_dir = os.path.join(os.path.dirname(__file__), 'index')
            if not os.path.exists(index_dir):
                raise Exception(f"Index not found in {index_dir}")

            ix = open_dir(index_dir)

            with ix.searcher() as searcher:
                if filter_cook == "gt":
                    query = NumericRange("cook_time", cook_time + 1, None)
                elif filter_cook == "lt":
                    query = NumericRange("cook_time", None, cook_time - 1)
                elif filter_cook == "eq":
                    query = NumericRange("cook_time", cook_time, cook_time)

                results = searcher.search(query, limit=None)

                for result in results:
                    results_list.append({
                        "title": result.get("title", "Unknown Title"),
                        "servings": result.get("servings", "N/A"),
                        "prep_time": result.get("prep_time", "N/A"),
                        "cook_time": result.get("cook_time", "N/A"),
                        "total_time": result.get("total_time", "N/A"),
                        "difficulty": result.get("difficulty", "N/A"),
                        "rating": result.get("rating", "N/A"),
                        "num_reviews": result.get("num_reviews", "N/A"),
                        "ingredients_list": result.get("ingredients", "").split(","),
                    })

            return render(request, "search_recipes_by_time.html", {
                "recipes": results_list,
                "filter_time": cook_time,
                "comparator": filter_cook
            })

        except ValueError as ve:
            print(f"Value error: {ve}")
            error_message = str(ve)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or "No such file or directory" in str(e):
                print("Error: Index not found. Please load the index and try again.")
                error_message = "The index is missing. Please load the index to proceed."
            else:
                print(f"General error: {e}")
                error_message = f"An error occurred: {str(e)}"

    else:
        print("No valid search was submitted")

    return render(request, "search_recipes_by_time.html", {
        "recipes": results_list,
        "error": error_message
    })


'''SEARCH RECIPES BY PREP TIME'''
def search_recipes_by_prep_time(request):
    results_list = []
    error_message = None

    if request.method == "GET" and "prep_time" in request.GET and "filter_prep" in request.GET:
        try:
            prep_time_str = request.GET.get("prep_time", "0").strip()
            filter_prep = request.GET.get("filter_prep", "").strip()

            if not prep_time_str.isdigit():
                raise ValueError("Preparation time must be a valid integer.")
            prep_time = int(prep_time_str)

            if filter_prep not in ["lt", "gt", "eq"]:
                raise ValueError("The comparison filter is invalid. Use: lt, gt, or eq.")

            index_dir = os.path.join(os.path.dirname(__file__), 'index')
            if not os.path.exists(index_dir):
                raise Exception(f"Index not found in {index_dir}")

            ix = open_dir(index_dir)

            with ix.searcher() as searcher:
                if filter_prep == "gt":
                    query = NumericRange("prep_time", prep_time + 1, None)
                elif filter_prep == "lt":
                    query = NumericRange("prep_time", None, prep_time - 1)
                elif filter_prep == "eq":
                    query = NumericRange("prep_time", prep_time, prep_time)

                results = searcher.search(query, limit=None)

                for result in results:
                    results_list.append({
                        "title": result.get("title", "Unknown Title"),
                        "servings": result.get("servings", "N/A"),
                        "prep_time": result.get("prep_time", "N/A"),
                        "cook_time": result.get("cook_time", "N/A"),
                        "total_time": result.get("total_time", "N/A"),
                        "difficulty": result.get("difficulty", "N/A"),
                        "rating": result.get("rating", "N/A"),
                        "num_reviews": result.get("num_reviews", "N/A"),
                        "ingredients_list": result.get("ingredients", "").split(","),
                    })

            return render(request, "s.html", {
                "recipes": results_list,
                "filter_time": prep_time,
                "comparator": filter_prep
            })

        except ValueError as ve:
            print(f"Value error: {ve}")
            error_message = str(ve)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or "No such file or directory" in str(e):
                print("Error: Index not found. Please load the index and try again.")
                error_message = "The index is missing. Please load the index to proceed."
            else:
                print(f"General error: {e}")
                error_message = f"An error occurred: {str(e)}"

    else:
        print("No valid search was submitted")

    return render(request, "search_recipes_by_time.html", {
        "recipes": results_list,
        "error": error_message
    })


'''SEARCH RECIPES BY TOTAL TIME'''
def search_recipes_by_total_time(request):
    results_list = []
    error_message = None

    if request.method == "GET" and "total_time" in request.GET and "filter_total" in request.GET:
        try:
            total_time_str = request.GET.get("total_time", "0").strip()
            filter_total = request.GET.get("filter_total", "").strip()

            if not total_time_str.isdigit():
                raise ValueError("Total time must be a valid integer.")
            total_time = int(total_time_str)

            if filter_total not in ["lt", "gt", "eq"]:
                raise ValueError("The comparison filter is invalid. Use: lt, gt, or eq.")

            index_dir = os.path.join(os.path.dirname(__file__), 'index')
            if not os.path.exists(index_dir):
                raise Exception(f"Index not found in {index_dir}")

            ix = open_dir(index_dir)

            with ix.searcher() as searcher:
                if filter_total == "gt":
                    query = NumericRange("total_time", total_time + 1, None)
                elif filter_total == "lt":
                    query = NumericRange("total_time", None, total_time - 1)
                elif filter_total == "eq":
                    query = NumericRange("total_time", total_time, total_time)

                results = searcher.search(query, limit=None)

                for result in results:
                    results_list.append({
                        "title": result.get("title", "Unknown Title"),
                        "servings": result.get("servings", "N/A"),
                        "prep_time": result.get("prep_time", "N/A"),
                        "cook_time": result.get("cook_time", "N/A"),
                        "total_time": result.get("total_time", "N/A"),
                        "difficulty": result.get("difficulty", "N/A"),
                        "rating": result.get("rating", "N/A"),
                        "num_reviews": result.get("num_reviews", "N/A"),
                        "ingredients_list": result.get("ingredients", "").split(","),
                    })

            return render(request, "search_recipes_by_time.html", {
                "recipes": results_list,
                "filter_time": total_time,
                "comparator": filter_total
            })

        except ValueError as ve:
            print(f"Value error: {ve}")
            error_message = str(ve)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or "No such file or directory" in str(e):
                print("Error: Index not found. Please load the index and try again.")
                error_message = "The index is missing. Please load the index to proceed."
            else:
                print(f"General error: {e}")
                error_message = f"An error occurred: {str(e)}"

    else:
        print("No valid search was submitted")

    return render(request, "search_recipes_by_time.html", {
        "recipes": results_list,
        "error": error_message
    })



'''SEARCH RECIPES BY INGREDIENTS AND/OR TOTAL TIME'''
def search_recipes_by_ingredients_and_or_total_time(request):
    results_list = []
    error_message = None

    if request.method == "GET":
        ingredients_query = request.GET.get("ingredients", "").strip().lower()
        total_time_str = request.GET.get("total_time", "").strip()
        filter_total = request.GET.get("filter_total", "").strip()
        index_dir = os.path.join(os.path.dirname(__file__), 'index')

        try:
            ix = open_dir(index_dir)
            with ix.searcher() as searcher:
                combined_query = []

                if ingredients_query:
                    ingredients_list = [ingredient.strip() for ingredient in ingredients_query.split(",")]
                    processed_ingredients = []

                    for ingredient in ingredients_list:
                        cleaned_ingredient = re.sub(r'\b\d+\s*\w*\s*', '', ingredient).strip()
                        if cleaned_ingredient:
                            processed_ingredients.append(cleaned_ingredient)

                    ingredients_subqueries = []
                    for ingredient in processed_ingredients:
                        ingredient_parser = QueryParser("ingredients", schema=ix.schema)
                        ingredients_subqueries.append(ingredient_parser.parse(f'*{ingredient}*'))

                    if ingredients_subqueries:
                        combined_ingredients_query = ingredients_subqueries[0]
                        for subquery in ingredients_subqueries[1:]:
                            combined_ingredients_query &= subquery

                        combined_query.append(combined_ingredients_query)

                if total_time_str and filter_total:
                    if not total_time_str.isdigit():
                        raise ValueError("Total time must be a valid integer.")
                    total_time = int(total_time_str)

                    if filter_total not in ["lt", "gt", "eq"]:
                        raise ValueError("The comparison filter is invalid. Use: lt, gt, or eq.")

                    if filter_total == "gt":
                        time_subquery = NumericRange("total_time", total_time + 1, None)
                    elif filter_total == "lt":
                        time_subquery = NumericRange("total_time", None, total_time - 1)
                    elif filter_total == "eq":
                        time_subquery = NumericRange("total_time", total_time, total_time)

                    combined_query.append(time_subquery)

                if combined_query:
                    final_query = combined_query[0]
                    for subquery in combined_query[1:]:
                        final_query &= subquery

                    results = searcher.search(final_query, limit=None)

                    for result in results:
                        results_list.append({
                            "title": result.get("title", "Unknown Title"),
                            "servings": result.get("servings", "N/A"),
                            "prep_time": result.get("prep_time", "N/A"),
                            "cook_time": result.get("cook_time", "N/A"),
                            "total_time": result.get("total_time", "N/A"),
                            "difficulty": result.get("difficulty", "N/A"),
                            "rating": result.get("rating", "N/A"),
                            "num_reviews": result.get("num_reviews", "N/A"),
                            "ingredients_list": result.get("ingredients", "").split(","),
                        })

        except ValueError as ve:
            print(f"Value error: {ve}")
            error_message = str(ve)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or "No such file or directory" in str(e):
                print("Error: Index not found. Please load the index and try again.")
                error_message = "The index is missing. Please load the index to proceed."
            else:
                print(f"General error: {e}")
                error_message = f"An error occurred: {str(e)}"

    return render(request, "search_recipes_by_ingredients_and_or_total_time.html", {
        "recipes": results_list,
        "error": error_message,
    })

'''SEARCH RECIPES BY DIFFICULTY AND/OR RATING'''
def search_recipes_by_difficulty_and_or_rating(request):
    results_list = []
    error_message = None

    if request.method == "GET":
        difficulty_query = request.GET.get("difficulty", "").strip().lower()
        min_rating_str = request.GET.get("min_rating", "").strip()
        index_dir = os.path.join(os.path.dirname(__file__), 'index')

        try:
            if not os.path.exists(index_dir):
                raise Exception("Index not found. Please ensure the index is created.")

            ix = open_dir(index_dir)
            with ix.searcher() as searcher:
                combined_query = []

                if difficulty_query:
                    difficulty_parser = QueryParser("difficulty", schema=ix.schema)
                    difficulty_subquery = difficulty_parser.parse(f"{difficulty_query}")
                    combined_query.append(difficulty_subquery)

                if min_rating_str:
                    if not min_rating_str.replace(".", "").isdigit():
                        raise ValueError("Rating must be a valid number.")
                    min_rating = float(min_rating_str)
                    rating_subquery = NumericRange("rating", min_rating, None)
                    combined_query.append(rating_subquery)

                if combined_query:
                    final_query = combined_query[0]
                    for subquery in combined_query[1:]:
                        final_query = final_query & subquery

                    results = searcher.search(final_query, limit=None)

                    for result in results:
                        ingredients_list = result.get("ingredients", "").split(",") if result.get("ingredients") else []
                        results_list.append({
                            "title": result.get("title", "Unknown Title"),
                            "servings": result.get("servings", "N/A"),
                            "prep_time": result.get("prep_time", "N/A"),
                            "cook_time": result.get("cook_time", "N/A"),
                            "total_time": result.get("total_time", "N/A"),
                            "difficulty": result.get("difficulty", "N/A"),
                            "rating": result.get("rating", "N/A"),
                            "num_reviews": result.get("num_reviews", "N/A"),
                            "ingredients_list": ingredients_list,
                        })

        except ValueError as ve:
            print(f"Value error: {ve}")
            error_message = str(ve)
        except Exception as e:
            if isinstance(e, FileNotFoundError) or "No such file or directory" in str(e):
                print("Error: Index not found. Please load the index and try again.")
                error_message = "The index is missing. Please load the index to proceed."
            else:
                print(f"General error: {e}")
                error_message = f"An error occurred: {str(e)}"


    return render(request, "search_recipes_by_difficulty_and_or_rating.html", {
        "recipes": results_list,
        "error": error_message,
    })



'''TOP 3 RECIPES BY RATING'''
def search_top_recipes(request):
    results_list = []

    try:
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        if not os.path.exists(index_dir):
            raise Exception(f"Index not found in {index_dir}")
        
        ix = open_dir(index_dir)
        with ix.searcher() as searcher:
            top_reviews_query = searcher.search_page(
                QueryParser("num_reviews", ix.schema).parse("*"),
                1,
                sortedby="num_reviews",
                reverse=True,
                pagelen=10,
            )
            top_recipes = sorted(
                top_reviews_query,
                key=lambda r: r["rating"],
                reverse=True
            )[:3]  

            for result in top_recipes:
                ingredients_list = result.get("ingredients", "").split(",") if result.get("ingredients") else []
                results_list.append({
                    "title": result.get("title", "Unknown Title"),
                    "servings": result.get("servings", "N/A"),
                    "prep_time": result.get("prep_time", "N/A"),
                    "cook_time": result.get("cook_time", "N/A"),
                    "total_time": result.get("total_time", "N/A"),
                    "difficulty": result.get("difficulty", "N/A"),
                    "rating": result.get("rating", "N/A"),
                    "num_reviews": result.get("num_reviews", "N/A"),
                    "ingredients_list": ingredients_list,
                })

    except Exception as e:
        print(f"Error while searching top recipes: {e}")

    return render(request, "search_top_recipes.html", {"recipes": results_list})



'''QUICK RECIPES'''
def quick_recipes(request):
    results_list = []

    try:
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        if not os.path.exists(index_dir):
            raise Exception(f"Index not found in {index_dir}")
        
        ix = open_dir(index_dir)

        with ix.searcher() as searcher:
            query = NumericRange("total_time", None, 30)  
            results = searcher.search(query, limit=None)

            for result in results:
                results_list.append({
                    "title": result.get("title", "Unknown Title"),
                    "servings": result.get("servings", "N/A"),
                    "prep_time": result.get("prep_time", "N/A"),
                    "cook_time": result.get("cook_time", "N/A"),
                    "total_time": result.get("total_time", "N/A"),
                    "difficulty": result.get("difficulty", "N/A"),
                    "rating": result.get("rating", "N/A"),
                    "num_reviews": result.get("num_reviews", "N/A"),
                    "ingredients_list": result.get("ingredients", "").split(",") if result.get("ingredients") else [],
                })

    except Exception as e:
        print(f"Error while searching quick recipes: {e}")

    return render(request, "quick_recipes.html", {"recipes": results_list})


'''EASY RECIPES'''
def easy_recipes(request):
    results_list = []

    try:
        index_dir = os.path.join(os.path.dirname(__file__), 'index')
        if not os.path.exists(index_dir):
            raise Exception("Index not found. Please ensure the index is created.")

        ix = open_dir(index_dir)

        with ix.searcher() as searcher:
            query = QueryParser("difficulty", schema=ix.schema).parse("easy")
            results = searcher.search(query, limit=None)

            for result in results:
                ingredients_list = result.get("ingredients", "").split(",") if result.get("ingredients") else []
                results_list.append({
                    "title": result.get("title", "Unknown Title"),
                    "servings": result.get("servings", "N/A"),
                    "prep_time": result.get("prep_time", "N/A"),
                    "cook_time": result.get("cook_time", "N/A"),
                    "total_time": result.get("total_time", "N/A"),
                    "difficulty": result.get("difficulty", "N/A"),
                    "rating": result.get("rating", "N/A"),
                    "num_reviews": result.get("num_reviews", "N/A"),
                    "ingredients_list": ingredients_list, 
                })

    except Exception as e:
        print(f"Error while searching easy recipes: {e}")

    return render(request, "easy_recipes.html", {"recipes": results_list})

