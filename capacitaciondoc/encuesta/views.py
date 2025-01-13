from django.shortcuts import render, redirect
from .models import Encuesta

# Create your views here.
def encuesta(request):
    if request.method == 'POST':
        encuesta = Encuesta(
            instructor1=request.POST['instructor1'],
            instructor2=request.POST['instructor2'],
            instructor3=request.POST['instructor3'],
            instructor4=request.POST['instructor4'],
            instructor5=request.POST['instructor5'],
            instructor6=request.POST['instructor6'],
            instructor7=request.POST['instructor7'],
            
            curso1=request.POST['curso1'],
            curso2=request.POST['curso2'],
            curso3=request.POST['curso3'],
            curso4=request.POST['curso4'],
            
            material1=request.POST['material1'],
            material2=request.POST['material2'],
            material3=request.POST['material3'],
            
            insfraestructura1=request.POST['insfraestructura1'],
            insfraestructura2=request.POST['insfraestructura2'],
            insfraestructura3=request.POST['insfraestructura3'],
            insfraestructura4=request.POST['insfraestructura4'],
            insfraestructura5=request.POST['insfraestructura5'],
            insfraestructura6=request.POST['insfraestructura6'],
            
            comentarios=request.POST.get('comentarios', '')
        )
        encuesta.save()
        return redirect('gracias')  # Redirige a una página de agradecimiento
    return render(request, 'encuesta.html')

def gracias(request):
    return render(request, 'gracias.html')