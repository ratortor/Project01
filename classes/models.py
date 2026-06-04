from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.grado})"
