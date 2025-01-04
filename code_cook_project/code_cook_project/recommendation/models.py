from django.db import models
from recipes.models import Recipes

class RecipeSimilarity(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='base_recipe')
    similar_recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE, related_name='similar_recipe')
    similarity_score = models.FloatField()

    def __str__(self):
        return f"{self.recipe.title} -> {self.similar_recipe.title} ({self.similarity_score})"
