from django.db import models


<<<<<<< HEAD
      def __str__(self):                  
          return f"{self.nombre} ({self.grado})"
=======
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.grado})"
>>>>>>> d3b0cff3351878684c21df801688cc3416a0b663
