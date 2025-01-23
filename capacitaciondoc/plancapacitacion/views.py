from django.shortcuts import render, render, get_object_or_404, redirect
from .models import registroCurso, validarCurso
from .forms import CursoForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from eventos.models import Evento

# Create your views here.
def registrocursolista(request):
    cursos = registroCurso.objects.all()
    return render(request, 'registrocursolista.html', {'cursos': cursos})

def registrocursover(request, curso_id):
    curso = get_object_or_404(registroCurso, id=curso_id)
    return render(request, 'registrocursover.html', {'curso': curso})

def registrocursoactualizar(request, curso_id):
    curso = get_object_or_404(registroCurso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('registrocursolista')  #Regresa a la lista de los cursos
    else:
        form = CursoForm(instance=curso)
    return render(request, 'registrocursoactualizar.html', {'form': form, 'curso': curso})

def registrocursoeliminar(request, curso_id):
    curso = get_object_or_404(registroCurso, id=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('registrocursolista')  
    return render(request, 'registrocursoeliminar.html', {'curso': curso})

def registrocursocrear(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrocursolista') 
    else:
        form = CursoForm()

    return render(request, 'registrocursocrear.html', {'form': form})

#VALIDACION DE CURSOS
def validarcursolista(request):
    validarcurso = validarCurso.objects.select_related('curso', 'curso__periodo', 'curso__instructor').all()
    return render(request, 'validarcursolista.html', {
        'validarcurso': validarcurso,
    })

def validarver(request, validar_id):
    validar = get_object_or_404(validarCurso, id=validar_id)
    curso = validar.curso  # El curso asociado al registro de validación
    return render(request, 'validarver.html', {'curso': curso})

def aceptar_curso(request, curso_id):
    curso = get_object_or_404(registroCurso, id=curso_id)
    
    # Verificar si ya existe un evento asociado a este curso
    if not Evento.objects.filter(curso=curso).exists():
        curso.aceptado = True
        curso.save()
        Evento.objects.create(curso=curso)
    
    # Redirigir de vuelta a la lista de cursos
    return HttpResponseRedirect(reverse('validarcursolista'))

def invalidar_curso(request, curso_id):
    curso = get_object_or_404(registroCurso, id=curso_id)
    
    # Cambiar el estado del curso a rechazado
    curso.aceptado = False
    curso.save()
    
    # Eliminar el evento
    Evento.objects.filter(curso=curso).delete()

    return HttpResponseRedirect(reverse('validarcursolista'))
