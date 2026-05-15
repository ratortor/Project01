from django.db import models

# Create your models here.
class Curso(models.Model):           
      nombre = models.CharField(max_length=100)                                
      grado = models.CharField(max_length=20)  

      def _str_(self):                  
          return f"{self.nombre} ({self.grado})"