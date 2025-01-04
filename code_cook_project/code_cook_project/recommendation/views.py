from django.shortcuts import render, get_object_or_404
from .models import Recipes, RecipeSimilarity
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



def update_recipe_similarities(request):
    try:
        calculate_recipe_similarities()
        messages.success(request, "Recipe similarities successfully calculated.")
    except Exception as e:
        messages.error(request, f"An error occurred while calculating similarities: {str(e)}")
    return redirect('home')
