from django.shortcuts import render, get_object_or_404
from .models import RecipeSimilarity
from recipes.models import Recipes
from django.shortcuts import redirect
from django.contrib import messages
from .utils import calculate_recipe_similarities


def recipe_recommendations(request, recipe_id):

    recipe = get_object_or_404(Recipes, id=recipe_id)
    recipe.ingredients_list = recipe.ingredients.split(",") if recipe.ingredients else []
    recommendations = RecipeSimilarity.objects.filter(recipe=recipe).order_by('-similarity_score')[:5]

    for rec in recommendations:
        rec.similar_recipe.ingredients_list = rec.similar_recipe.ingredients.split(",") if rec.similar_recipe.ingredients else []

    return render(request, 'recipe_recommendations.html', {
        'recipe': recipe,
        'recommendations': recommendations,
    })



def confirm_load_recommendation(request):
    if request.method == "POST":
        if 'confirm' in request.POST: 
            try:
                if not Recipes.objects.exists(): 
                    messages.error(request, "No recipes found in the database. Cannot calculate recommendations.")
                    return redirect('home')  
                else:
                    load_recipe_similarities()
                    messages.success(request, "Recipe similarities successfully calculated!")
            except Exception as e:
                messages.error(request, f"An error occurred while processing recipes: {str(e)}")
            return redirect('home')
        elif 'cancel' in request.POST:  
            return redirect('home')

    return render(request, "confirm_load_recommendations.html")


def load_recipe_similarities():
    recipes_processed = 0
    errors = []
    try:
        recipes_processed = calculate_recipe_similarities()
    except Exception as e:
        errors.append(str(e))

    return recipes_processed, errors
