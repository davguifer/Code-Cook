from django.db import models

# Create your models here.
class Receta(models.Model):
    titulo = models.CharField(max_length=255)
    ingredientes = models.TextField()
    instrucciones = models.TextField()
    tiempo_preparacion = models.IntegerField()
    dificultad = models.CharField(max_length=50)
