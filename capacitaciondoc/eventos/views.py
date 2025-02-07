from datetime import datetime, timedelta
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from plancapacitacion.models import RegistroCurso

from django.core.files.storage import FileSystemStorage #Para archivos y directorios


from .forms import EventoForm, EvidenciaForm
from .models import Asistencia, Calificacion, Evento, Evidencia, Inscripcion
from catalogos.models import Docente, Lugar, Instructor, GradoAcademico, Periodo

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
            if not Evidencia.objects.filter(evento=evento).exists():
                Evidencia.objects.create(evento=evento)

            evento.save()

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
    inscripciones.delete()
    # Elimina la evidencia que el instructor carga
    evidencias = Evidencia.objects.filter(evento=evento)
    evidencias.delete()
    messages.success(request, "Se deshizo el evento.")

    # Limpiar los campos de lugar y fechas del evento
    evento.lugar = None
    evento.fechaInicio = None
    evento.fechaFin = None
    evento.horaInicio = None
    evento.horaFin = None
    evento.save()

    messages.info(request, "Puedes crear el evento nuevamente.")

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
    usuario = request.user
    # Verificar si el usuario es docente o instructor
    es_docente = Docente.objects.filter(user=usuario).exists()
    es_instructor = Instructor.objects.filter(user=usuario).exists()

    # Filtrar eventos que tienen lugar, fecha y hora definidos
    eventos_disponibles = Evento.objects.filter(
        lugar__isnull=False, fechaInicio__isnull=False, fechaFin__isnull=False
    ).order_by('curso__nombre')

    eventos_inscritos = []
    eventos_instructor = []

    if es_docente:
        # Obtener eventos donde el usuario está inscrito
        inscripciones_usuario = Inscripcion.objects.filter(usuario=usuario).order_by('evento__curso__nombre')
        eventos_inscritos = [inscripcion.evento for inscripcion in inscripciones_usuario]

        # Filtrar eventos en los que aún no está inscrito
        eventos_disponibles = eventos_disponibles.exclude(id__in=[evento.id for evento in eventos_inscritos])

    elif es_instructor:
        # Filtrar eventos donde el usuario es instructor
        eventos_instructor = eventos_disponibles.filter(curso__instructor__user=usuario)

    return render(request, 'inscripcionlista.html', {
        'es_docente': es_docente,
        'es_instructor': es_instructor,
        'eventos_inscritos': eventos_inscritos,
        'eventos_instructor': eventos_instructor,
        'eventos_disponibles': eventos_disponibles,
    })

@login_required(login_url='signin')
@permission_required('eventos.view_evento', raise_exception=True)
def vercurso(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscritos = Inscripcion.objects.filter(evento=evento).select_related('usuario__docente')

    return render(request, 'vercurso.html', {'evento': evento, 'inscritos': inscritos})

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
@permission_required('eventos.view_asistencia', raise_exception=True)
def listacursosasistencia(request):
    # Filtrar eventos que tienen lugar, fecha y hora definidos
    eventos = Evento.objects.filter(
        lugar__isnull=False, fechaInicio__isnull=False, fechaFin__isnull=False
    ).order_by('curso__nombre')

    if request.user.rol == 'Instructor':
        # Filtrar eventos donde el usuario es instructor
        eventos = eventos.filter(curso__instructor__user=request.user)

    return render(request, 'listacursosasistencia.html', {
        'eventos': eventos,
    })

@login_required(login_url='signin')
@permission_required('eventos.view_calificacion', raise_exception=True)
def listacursoscalificacion(request):
    # Filtrar eventos que tienen lugar, fecha y hora definidos
    eventos = Evento.objects.filter(
        lugar__isnull=False, fechaInicio__isnull=False, fechaFin__isnull=False
    ).order_by('curso__nombre')

    if request.user.rol == 'Instructor':
        # Filtrar eventos donde el usuario es instructor
        eventos = eventos.filter(curso__instructor__user=request.user)

    return render(request, 'listacursoscalificacion.html', {
        'eventos': eventos,
    })

@login_required(login_url='signin')
@permission_required('eventos.view_asistencia', raise_exception=True)
def detalle_curso_asistencia(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscritos = Inscripcion.objects.filter(evento=evento).select_related('usuario__docente')
    return render(request, 'detallecursoasistencia.html', {'evento': evento, 'inscritos': inscritos})

@login_required(login_url='signin')
@permission_required('eventos.view_calificacion', raise_exception=True)
def detalle_curso_calificacion(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscritos = Inscripcion.objects.filter(evento=evento).select_related('usuario__docente')
    return render(request, 'detallecursocalificacion.html', {'evento': evento, 'inscritos': inscritos})

@login_required(login_url='signin')
@permission_required('eventos.change_evidencia', raise_exception=True)
def evidencia(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    evidencia = Evidencia.objects.filter(evento=evento).first()

    if request.method == 'POST':
        form = EvidenciaForm(request.POST, request.FILES, instance=evidencia)
        if evidencia.archivo_evidencia:
            fs = FileSystemStorage()
            fs.delete(evidencia.archivo_evidencia.name)
            
        if form.is_valid():
            form.save()
            return redirect('detalle_curso_calificacion', evento_id=evento.id)
    else:
        
        form = EvidenciaForm(instance=evidencia)
    return render(request, 'evidencia.html', {'evento':evento, 'evidencia':evidencia, 'form': form})

def generar_dias_semana(evento):
    dias_semana = []
    fecha_actual = evento.fechaInicio
    while fecha_actual <= evento.fechaFin:
        if fecha_actual.weekday() < 5:  # 0=Lunes, 4=Viernes
            dias_semana.append(fecha_actual)
        fecha_actual += timedelta(days=1)
    return dias_semana

@login_required(login_url='signin')
@permission_required('eventos.add_asistencia', raise_exception=True)
def tomar_asistencia(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = Inscripcion.objects.filter(evento=evento).select_related('usuario__docente')
    dias_semana = generar_dias_semana(evento)  # Lista de fechas (Lunes a Viernes)

    # Preprocesar asistencias para cada inscripción y día
    asistencias_por_inscripcion = []
    for inscripcion in inscripciones:
        asistencias = {}
        for fecha in dias_semana:
            asistencia = inscripcion.asistencia_set.filter(fecha=fecha).first()
            asistencias[fecha] = asistencia.asistio if asistencia else False
        asistencias_por_inscripcion.append({
            'inscripcion': inscripcion,
            'asistencias': asistencias
        })

    if request.method == 'POST':
        for inscripcion in inscripciones:
            for fecha in dias_semana:
                asistio = request.POST.get(f'asistencia_{inscripcion.id}_{fecha}', False)
                Asistencia.objects.update_or_create(
                    inscripcion=inscripcion,
                    fecha=fecha,
                    defaults={'asistio': bool(asistio)}
                )
        messages.success(request, "Asistencias guardadas correctamente.")
        return redirect('tomar-asistencia', evento_id=evento.id)

    return render(request, 'asistencia.html', {
        'evento': evento,
        'asistencias_por_inscripcion': asistencias_por_inscripcion,
        'dias_semana': dias_semana,
    })

@login_required(login_url='signin')
@permission_required('eventos.add_calificacion', raise_exception=True)
def asignar_calificacion(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    inscripciones = Inscripcion.objects.filter(evento=evento, aceptado=True)  # Solo docentes aceptados
    evidencia = Evidencia.objects.filter(evento=evento, evidencia=True).exists()  # Verifica si hay evidencia
    
    if not evidencia:
        messages.warning(request, "No puedes asignar calificación si no has cargado tu evidencia del curso.")
        return redirect('detalle_curso_calificacion', evento_id=evento.id)  # Redirigir a la página de detalle del evento
    
    if request.method == 'POST':
        for inscripcion in inscripciones:
            calificacion_value = request.POST.get(f'calificacion_{inscripcion.id}')
            comentario_value = request.POST.get(f'comentario_{inscripcion.id}')
            
            if calificacion_value:  # Solo crear calificación si se ingresó un valor
                Calificacion.objects.update_or_create(
                    inscripcion=inscripcion,
                    defaults={
                        'calificacion': calificacion_value,
                        'comentario': comentario_value,
                    }
                )
        return redirect('detalle_curso_calificacion', evento_id=evento.id)  # Redirigir a la página de detalle del evento

    return render(request, 'calificacion.html', {
        'evento': evento,
        'inscripciones': inscripciones,
    })