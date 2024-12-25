from django.db import models

class Receta(models.Model):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    autor = models.CharField(max_length=255, blank=True, null=True)
    visitas = models.FloatField(default=0, blank=True, null=True)
    porciones = models.IntegerField(blank=True, null=True)
    tiempo_preparacion = models.CharField(max_length=50, blank=True, null=True)
    tiempo_coccion = models.CharField(max_length=50, blank=True, null=True)
    dificultad = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    introduccion = models.TextField(blank=True, null=True)
    ingredientes = models.TextField(blank=True, null=True)
    instrucciones = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo
