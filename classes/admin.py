from django.contrib import admin
from .models import Curso, Estudiante

class EstudianteInline(admin.TabularInline):
    model = Estudiante
    extra = 1  # Número de formularios vacíos listos para agregar nuevos estudiantes

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'nombre', 'grado')
    
    search_fields = ('nombre', 'grado')
    
    inlines = [EstudianteInline]

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'nombre', 'curso')
    
    search_fields = ('nombre', 'curso__nombre')