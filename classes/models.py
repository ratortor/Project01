from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.grado})"

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre


