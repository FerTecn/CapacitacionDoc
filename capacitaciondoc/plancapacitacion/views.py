from django.shortcuts import render, render, get_object_or_404, redirect
from .models import RegistroCurso, ValidarCurso
from .forms import CursoForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from eventos.models import Evento
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required(login_url='signin')
@permission_required('plancapacitacion.view_registrocurso', raise_exception=True)
def registrocursolista(request):
    cursos = RegistroCurso.objects.all()
    return render(request, 'registrocursolista.html', {'cursos': cursos})

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_registrocurso', raise_exception=True)
def registrocursover(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    return render(request, 'registrocursover.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_registrocurso', raise_exception=True)
def registrocursoactualizar(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('registrocursolista')  #Regresa a la lista de los cursos
    else:
        form = CursoForm(instance=curso)
    return render(request, 'registrocursoactualizar.html', {'form': form, 'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.delete_registrocurso', raise_exception=True)
def registrocursoeliminar(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('registrocursolista')  
    return render(request, 'registrocursoeliminar.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.add_registrocurso', raise_exception=True)
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
@login_required(login_url='signin')
@permission_required('plancapacitacion.view_validarcurso', raise_exception=True)
def validarcursolista(request):
    validarcurso = ValidarCurso.objects.select_related('curso', 'curso__periodo', 'curso__instructor').all()
    return render(request, 'validarcursolista.html', {
        'validarcurso': validarcurso,
    })

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_validarcurso', raise_exception=True)
def validarver(request, validar_id):
    validar = get_object_or_404(ValidarCurso, id=validar_id)
    curso = validar.curso  # El curso asociado al registro de validación
    return render(request, 'validarver.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_validarcurso', raise_exception=True)
def aceptar_curso(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    
    # Verificar si ya existe un evento asociado a este curso
    if not Evento.objects.filter(curso=curso).exists():
        curso.aceptado = True
        curso.save()
        Evento.objects.create(curso=curso)
    
    # Redirigir de vuelta a la lista de cursos
    return HttpResponseRedirect(reverse('validarcursolista'))

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_validarcurso', raise_exception=True)
def invalidar_curso(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    
    # Cambiar el estado del curso a rechazado
    curso.aceptado = False
    curso.save()
    
    # Eliminar el evento
    Evento.objects.filter(curso=curso).delete()

    return HttpResponseRedirect(reverse('validarcursolista'))
