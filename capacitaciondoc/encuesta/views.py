from django.shortcuts import render, redirect, get_object_or_404

from eventos.models import Inscripcion, Evento
from catalogos.models import Docente
from plancapacitacion.models import RegistroCurso
from .models import Encuesta
from django.contrib import messages

# Create your views here.
def listarcursos4encueta(request):
    # Filtra las inscripciones del usuario docente autenticado
    inscripciones = Inscripcion.objects.filter(usuario=request.user)
    cursos = []
    for inscripcion in inscripciones:
        evento = inscripcion.evento
        curso = evento.curso

        # Verificar si ya tiene una encuesta existente relacionada
        encuesta_hecha = Encuesta.objects.filter(docente=request.user, curso= curso).exists()

        cursos.append({
            'evento': evento,
            'curso': curso,
            'encuesta_hecha': encuesta_hecha,
        })
    return render(request, 'cursosparaencuesta.html', {'cursos': cursos})

    
def encuesta(request, curso_id):
    # Obtener el evento especifico
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    evento = get_object_or_404(Evento, curso=curso)

    if Encuesta.objects.filter(docente=request.user, curso=curso).exists():
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
            docente = request.user, curso = curso,
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
    return render(request, 'encuesta.html', {'evento': evento})

def gracias(request):
    return render(request, 'gracias.html')