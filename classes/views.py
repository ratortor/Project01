    from django.shortcuts import render  
  def index(request):    
    print("correct")
    context = {
        'message': 'Bienvenido al gestor de clases',
    }              
      return render(request, 'classes/index.html', context)  
