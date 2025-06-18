from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from collections import defaultdict

from eventos.models import Inscripcion, Evento
from catalogos.models import Docente
from plancapacitacion.models import RegistroCurso
from .models import Encuesta
from .forms import EncuestaForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.timezone import now

# Create your views here.
@login_required(login_url='signin')
@permission_required('encuesta.view_encuesta', raise_exception=True)
def listarcursos4encuesta(request):
    if request.user.rol == "Docente":
        # Filtra las inscripciones del usuario docente autenticado
        inscripciones = Inscripcion.objects.filter(usuario=request.user, aceptado=True).order_by('evento__curso__nombre')
        cursos = []
        for inscripcion in inscripciones:
            curso = inscripcion.evento
            encuesta_hecha = Encuesta.objects.filter(inscripcion=inscripcion).exists()

            # Verificar si el curso ya ha comenzado
            curso_comenzado = curso.fechaInicio <= now().date()
            curso_finalizado = curso.fechaFin < now().date()
            print(curso)
            print(curso_comenzado)
            print(curso_finalizado)

            cursos.append({
                'curso': inscripcion.evento.curso,
                'evento': inscripcion.evento,
                'encuesta_hecha': encuesta_hecha,
                'curso_comenzado': curso_comenzado,
                'curso_finalizado': curso_finalizado,
            })
    else:
        # Muestra todos los cursos que están activos y tienen un evento
        eventos = Evento.objects.all().order_by('curso__nombre')
        cursos = []

        for evento in eventos:
            # Verificar si el curso ya ha comenzado
            curso_comenzado = evento.fechaInicio <= now().date()
            curso_finalizado = evento.fechaFin < now().date()

            cursos.append({
                'curso': evento.curso,
                'evento': evento,
                'curso_comenzado': curso_comenzado,
                'curso_finalizado': curso_finalizado,
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
        
        form = EncuestaForm(request.POST)
        if form.is_valid():
            try:
                form.instance.inscripcion = inscripcion
                form.save()
                return redirect('gracias')  # Redirige a una página de agradecimiento
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect('encuesta')
    else:
        form = EncuestaForm()

    return render(request, 'encuesta.html', {'inscripcion': inscripcion, 'form': form})

def gracias(request):
    return render(request, 'gracias.html')

def resultados(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    inscripciones = Inscripcion.objects.filter(evento__curso=curso, aceptado=True)
    encuestas = Encuesta.objects.filter(inscripcion__in=inscripciones)

    resultados = {}
    comentarios = []
    for field in Encuesta._meta.fields:
        if field.name.startswith(('instructor', 'curso', 'material', 'insfraestructura')):
            opciones = []
            for opcion_valor in range(1, 6): #itera del 1 al 5
                conteo = encuestas.filter(**{field.name: opcion_valor}).count()
                opciones.append({'opcion': opcion_valor, 'count': conteo})
            resultados[field.name] = opciones
        if field.name == "comentarios":
            comentarios = encuestas.values("comentarios")

    return render(request, 'resultados.html', {
        'resultados': resultados, 
        'curso': curso, 
        'inscripciones': inscripciones, 
        'encuestas': encuestas,
        'comentarios': comentarios,
    })