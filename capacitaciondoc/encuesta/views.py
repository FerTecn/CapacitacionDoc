from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from collections import defaultdict

from eventos.models import Inscripcion, Evento
from catalogos.models import Docente
from plancapacitacion.models import RegistroCurso
from .models import Encuesta
from django.contrib import messages

# Create your views here.
@login_required(login_url='signin')
@permission_required('encuesta.view_encuesta', raise_exception=True)
def listarcursos4encuesta(request):
    if request.user.rol == "Docente":
        # Filtra las inscripciones del usuario docente autenticado
        inscripciones = Inscripcion.objects.filter(usuario=request.user)
        cursos = []
        for inscripcion in inscripciones:
            encuesta_hecha = Encuesta.objects.filter(inscripcion=inscripcion).exists()
            cursos.append({
                'curso': inscripcion.evento.curso,
                'evento': inscripcion.evento,
                'encuesta_hecha': encuesta_hecha,
            })
    else:
        # Muestra todos los cursos
        eventos = Evento.objects.all()
        cursos = []

        for evento in eventos:
            cursos.append({
                'curso': evento.curso,
                'evento': evento,
                })
    return render(request, 'cursosparaencuesta.html', {'cursos': cursos})

@login_required(login_url='signin')
@permission_required('encuesta.add_encuesta', raise_exception=True)
def encuesta(request, curso_id):
    # Obtener el curso especifico
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    inscripcion = get_object_or_404(Inscripcion, evento__curso=curso, usuario=request.user)

    if Encuesta.objects.filter(inscripcion=inscripcion).exists():
        messages.warning(request, 'Ya realizaste esta encuesta')
        return redirect('encuesta')
    
    if request.method == 'POST':
        # Verificar si el docente estuvo inscrito en el curso
        inscripcion_valida = Inscripcion.objects.filter(
            usuario=request.user,
            evento__curso=curso,
            aceptado=True,
        ).exists()

        if not inscripcion_valida:
            print('invalido')
            return redirect('encuesta')
        
        encuesta = Encuesta(
            inscripcion = inscripcion,
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
    return render(request, 'encuesta.html', {'inscripcion': inscripcion})

def gracias(request):
    return render(request, 'gracias.html')