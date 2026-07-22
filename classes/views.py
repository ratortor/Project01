from django.shortcuts import render 

from .models import Curso

from django.shortcuts import render, get_object_or_404

def index(request):    
        
    return render(request, 'classes/index.html')  

def lista_cursos(request):

    cursos = Curso.objects.all()

    context = {
        'cursos': cursos
    }
    
    return render(request, 'classes/lista_cursos.html', context)

def detalle_curso(request, pk):
    
    curso = get_object_or_404(Curso, pk=pk)
    
    
    estudiantes = curso.estudiante_set.all()  
    
    return render(request, 'classes/detalle_curso.html', {
        'curso': curso,
        'estudiantes': estudiantes,
    })