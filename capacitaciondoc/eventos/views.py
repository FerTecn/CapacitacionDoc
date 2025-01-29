from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from plancapacitacion.models import RegistroCurso

from .forms import EventoForm
from .models import Evento, Inscripcion
from catalogos.models import Lugar, Instructor, GradoAcademico, Periodo

# Create your views here.
@login_required(login_url='signin')
@permission_required('eventos.view_evento', raise_exception=True)
def eventolista(request):
    eventos = Evento.objects.all()
    return render(request, 'eventolista.html', {'eventos': eventos})

@login_required(login_url='signin')
@permission_required('eventos.view_evento', raise_exception=True)
def eventover(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  
    return render(request, 'eventover.html', {'evento': evento})

#CREACION DEL EVENTO
@login_required(login_url='signin')
@permission_required('eventos.change_evento', raise_exception=True)
def crearevento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    lugares = Lugar.objects.all()
    instructores = Instructor.objects.all()
    error = None

    # Guardar el ID del evento en la sesión para redirección
    request.session['evento_id'] = evento_id
    
    # Verificar si hay un lugar recién creado
    nuevo_lugar_id = request.session.pop('nuevo_lugar_id', None)
    lugar_seleccionado = None
    if nuevo_lugar_id:
        lugar_seleccionado = get_object_or_404(Lugar, id=nuevo_lugar_id)
        evento.lugar = lugar_seleccionado
        evento.save()

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            # Guardar el evento
            evento = form.save(commit=False)
            
            # Actualizar el instructor si es necesario
            nuevo_instructor_id = request.POST.get('nuevo_instructor')
            if nuevo_instructor_id:
                nuevo_instructor = get_object_or_404(Instructor, id=nuevo_instructor_id)
                evento.curso.instructor = nuevo_instructor
                evento.curso.save()
            
            # Actualizar las horas del curso
            horas_nuevas = request.POST.get('horas')
            if horas_nuevas and horas_nuevas.isdigit() and int(horas_nuevas) > 0:
                evento.curso.horas = int(horas_nuevas)
                evento.curso.save()

            # Actualizar el lugar si es enviado en el formulario
            lugar_id = request.POST.get('lugar')
            lugar = get_object_or_404(Lugar, id=lugar_id)
            evento.lugar = lugar

            evento.save()

            # Crear el curso listo para inscripcion para este evento
            Inscripcion.objects.get_or_create(evento=evento)

            return redirect(reverse('eventolista'))
        else:
            error = "Por favor corrija los errores en el formulario."
    else:
        form = EventoForm(instance=evento)

    # Renderizar el formulario si no es una solicitud POST
    return render(request, 'crearevento.html', {
        'form': form,
        'evento': evento,
        'lugares': lugares,
        'instructores': instructores,
        'lugar_seleccionado': lugar_seleccionado,
        'error': error,
    })

@login_required(login_url='signin')
@permission_required('eventos.change_evento', raise_exception=True)
def eventodeshacer(request, evento_id):
    # Obtener el evento
    evento = get_object_or_404(Evento, id=evento_id)

    # Eliminar las inscripciones asociadas al evento
    inscripciones = Inscripcion.objects.filter(evento=evento)
    if inscripciones.exists():
        inscripciones.delete()
        messages.success(request, "Las inscripciones asociadas al evento han sido eliminadas.")

        # Limpiar los campos de lugar y fechas del evento
        evento.lugar = None
        evento.fechaInicio = None
        evento.fechaFin = None
        evento.horaInicio = None
        evento.horaFin = None
        evento.save()

        messages.info(request, "Los campos de lugar y fecha del evento han sido limpiados.")
    else:
        messages.info(request, "No hay inscripciones asociadas a este evento.")

    # Redirigir a la lista de eventos
    return redirect(reverse('eventolista'))

def lugarcrearnuevo(request):
    if request.method == 'POST':
        nombre_edificio = request.POST.get('nombreEdificio')
        ubicacion = request.POST.get('ubicacion')
        
        if nombre_edificio and ubicacion:
            # Crear el nuevo lugar
            nuevo_lugar = Lugar.objects.create(
                nombreEdificio=nombre_edificio,
                ubicacion=ubicacion
            )

            # Guardar el ID del nuevo lugar en la sesión
            request.session['nuevo_lugar_id'] = nuevo_lugar.id
            
            # Redirigir a la página de crear evento con el lugar seleccionado
            return redirect('crearevento', evento_id=request.session.get('evento_id'))

    return render(request, 'lugarcrearnuevo.html')

def cambiarinstructor(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    instructores = Instructor.objects.all()  # Obtener todos los instructores disponibles

    # Obtener el instructor actual asociado al curso
    instructor_actual = evento.curso.instructor

    if request.method == 'POST':
        nuevo_instructor_id = request.POST.get('nuevo_instructor')
        if nuevo_instructor_id:
            nuevo_instructor = get_object_or_404(Instructor, id=nuevo_instructor_id)
            evento.curso.instructor = nuevo_instructor
            evento.curso.save()  # Guardar el cambio en el instructor
            return redirect('crearevento', evento_id=evento.id)  # Redirigir de nuevo a la página del evento

    return render(request, 'cambiarinstructor.html', {
        'evento': evento,
        'instructores': instructores,
        'instructor_actual': instructor_actual,
    })
    
def añadirinstructor(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    instructores = Instructor.objects.all()  
    grados = GradoAcademico.objects.all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        clave = request.POST.get('clave')
        nombre = request.POST.get('nombre')
        apPaterno = request.POST.get('apPaterno')
        apMaterno = request.POST.get('apMaterno')
        fechaNac = request.POST.get('fechaNac')  
        CURP = request.POST.get('CURP')  
        RFC = request.POST.get('RFC') 
        telefono = request.POST.get('telefono')  
        email = request.POST.get('email')  
        
        # Formación académica
        institucion = request.POST.get('institucion')  
        grado_id = request.POST.get('grado')
        cedulaProf = request.POST.get('cedulaProf')  

        # Experiencia laboral
        puesto = request.POST.get('puesto')  
        empresa = request.POST.get('empresa')  

        # Experiencia docente
        materia = request.POST.get('materia')  
        periodo = request.POST.get('periodo')  

        # Participación como instructor
        curso = request.POST.get('curso') 
        nombreEmpresa = request.POST.get('nombreEmpresa')  
        duracionHoras = request.POST.get('duracionHoras')  
        fechaParticipacion = request.POST.get('fechaParticipacion')  

        # Obtener el grado académico relacionado
        grado = None
        if grado_id:
            grado = GradoAcademico.objects.get(id=grado_id)
            
        # Crear el nuevo instructor
        nuevo_instructor = Instructor.objects.create(
            clave=clave,
            nombre=nombre,
            apPaterno=apPaterno,
            apMaterno=apMaterno,
            fechaNac=fechaNac,
            CURP=CURP,
            RFC=RFC,
            telefono=telefono,
            email=email,
            institucion=institucion,
            grado=grado,
            cedulaProf=cedulaProf,
            puesto=puesto,
            empresa=empresa,
            materia=materia,
            periodo=periodo,
            curso=curso,
            nombreEmpresa=nombreEmpresa,
            duracionHoras=duracionHoras,
            fechaParticipacion=fechaParticipacion,
        )

        # Asignar el nuevo instructor al evento
        evento.curso.instructor = nuevo_instructor
        evento.curso.save()

        return redirect('crearevento', evento_id=evento.id)  
    
    return render(request, 'añadirinstructor.html', {
        'evento': evento,
        'grados': grados,
    })
    
#INSCRIPCION
@login_required(login_url='signin')
@permission_required('eventos.view_evento', raise_exception=True)
def inscripcionlista(request):
    # Filtrar eventos que tienen lugar, fecha y hora definidos
    eventos_disponibles = Evento.objects.filter(
        lugar__isnull=False, fechaInicio__isnull=False, fechaFin__isnull=False
    )

    # Verificar en qué eventos está inscrito el usuario actual
    inscripciones_usuario = Inscripcion.objects.filter(usuario=request.user)
    eventos_inscritos = [inscripcion.evento for inscripcion in inscripciones_usuario]

    # Dividir eventos en dos listas
    eventos_inscritos = [inscripcion.evento for inscripcion in inscripciones_usuario]
    eventos_disponibles = eventos_disponibles.exclude(id__in=[evento.id for evento in eventos_inscritos])

    return render(request, 'inscripcionlista.html', {
        'eventos_disponibles': eventos_disponibles,
        'eventos_inscritos': eventos_inscritos,
    })
    # inscripciones = Inscripcion.objects.all()  # Obtener todas las inscripciones
    # eventos = []

    # for inscripcion in inscripciones:
    #     evento = inscripcion.evento  # Obtener el evento asociado a cada inscripción
    #     eventos.append({
    #         'id': evento.id,  # Agrega el ID del evento aquí
    #         'nombre': evento.curso.nombre,
    #         'periodo': evento.curso.periodo,
    #         'horas': evento.curso.horas,
    #         'instructor': evento.curso.instructor,
    #         'lugar': evento.lugar,
    #         'aceptado': inscripcion.aceptado, #Estado para que cambien los botones
    #     })

    return render(request, 'inscripcionlista.html', {'eventos': eventos})

@login_required(login_url='signin')
@permission_required('eventos.view_evento', raise_exception=True)
def vercurso(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'vercurso.html', {'evento': evento})

@login_required(login_url='signin')
@permission_required('eventos.change_inscripcion', raise_exception=True)
def aceptarinscripcion(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    # Verificar si el usuario ya está inscrito
    print(evento.id, request.user.id)

    if not Inscripcion.objects.filter(evento=evento, usuario=request.user).exists():
        Inscripcion.objects.create(evento=evento, usuario=request.user, aceptado=True)
        messages.success(request, f"Te has inscrito exitosamente al curso '{evento.curso.nombre}'.")
    else:
        messages.info(request, f"Ya estás inscrito en el curso '{evento.curso.nombre}'.")

    return redirect('inscripcionlista')

@login_required(login_url='signin')
@permission_required('eventos.change_inscripcion', raise_exception=True)
def invalidarinscripcion(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    # Verificar si el usuario está inscrito
    inscripcion = Inscripcion.objects.filter(evento=evento, usuario=request.user).first()
    if inscripcion:
        inscripcion.delete()
        messages.success(request, f"Tu inscripción al curso '{evento.curso.nombre}' ha sido invalidada.")
    else:
        messages.warning(request, "No tienes una inscripción para este evento.")
    return redirect('inscripcionlista')

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_registrocurso', raise_exception=True)
def miscursosinstructor(request):
    if request.user.rol == 'Instructor':
        # Obtener el instructor a partir del usuario autenticado
        instructor = get_object_or_404(Instructor, user=request.user)

        # Obtener los cursos asignados al instructor actual
        cursos_asignados = RegistroCurso.objects.filter(instructor=instructor)

        # Obtener los eventos relacionados con esos cursos
        eventos_asignados = Evento.objects.filter(curso__in=cursos_asignados)

        # Obtener los docentes inscritos en esos eventos
        eventos_con_docentes = []
        for evento in eventos_asignados:
            docentes_inscritos = Inscripcion.objects.filter(evento=evento)
            eventos_con_docentes.append({
                'evento': evento,
                'docentes': docentes_inscritos
            })

        return render(request, 'miscursos.html', {
            'eventos_con_docentes': eventos_con_docentes,
        })
    else:
        return redirect ('home')