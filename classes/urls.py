from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/<int:pk>/', views.detalle_curso, name='detalle_curso'),
]
