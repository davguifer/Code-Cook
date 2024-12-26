from django.db import models

class Receta(models.Model):
    titulo = models.CharField(max_length=255)
    ingredientes = models.TextField()
    accesorios = models.TextField()
    tiempo_total = models.IntegerField()
    tiempo_preparacion = models.IntegerField()
    tiempo_de_coccion = models.IntegerField()
    tiempo_de_resposo = models.IntegerField()
    num_personas = models.IntegerField()

    def __str__(self):
        return self.titulo
