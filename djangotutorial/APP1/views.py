from django.http import HttpResponse


def index(request):
    return HttpResponse("<h1>Bienvenido al gestor de clases</h1>")