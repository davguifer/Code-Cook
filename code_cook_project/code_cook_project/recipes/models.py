from django.db import models

class Recipes(models.Model):
    title = models.CharField(max_length=255)
    servings = models.IntegerField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    details_post_cook_time = models.CharField(max_length=255)
    total_time = models.IntegerField()
    ingredients = models.TextField()
    dificulty = models.CharField(max_length=255)
    valoration = models.FloatField()


    def __str__(self):
        return self.title
