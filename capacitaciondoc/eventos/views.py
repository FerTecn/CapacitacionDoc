from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Evento, Inscripcion
from catalogos.models import Lugar, Instructor, GradoAcademico, Periodo

# Create your views here.
def eventolista(request):
    eventos = Evento.objects.all()
    return render(request, 'eventolista.html', {'eventos': eventos})

def eventover(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  
    return render(request, 'eventover.html', {'evento': evento})

#CREACION DEL EVENTO
def crearevento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    lugares = Lugar.objects.all()
    instructores = Instructor.objects.all()

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
        # Actualizar el lugar si es enviado en el formulario
        lugar_id = request.POST.get('lugar')
        lugar = get_object_or_404(Lugar, id=lugar_id)
        evento.lugar = lugar

        # Si se seleccionó un nuevo instructor, actualizarlo
        nuevo_instructor_id = request.POST.get('nuevo_instructor')
        if nuevo_instructor_id:
            nuevo_instructor = get_object_or_404(Instructor, id=nuevo_instructor_id)
            evento.curso.instructor = nuevo_instructor
            evento.curso.save()
            
        # Actualizar las horas 
        horas_nuevas = request.POST.get('horas')
        if horas_nuevas and horas_nuevas.isdigit() and int(horas_nuevas) > 0:
            evento.curso.horas = int(horas_nuevas)
            evento.curso.save()

        evento.save()
        
        # Crear la inscripción para este evento
        Inscripcion.objects.create(evento=evento)

        # Redirigir a la lista de inscripciones
        return redirect(reverse('eventolista'))
        
    # Renderizar el formulario si no es una solicitud POST
    return render(request, 'crearevento.html', {
        'evento': evento,
        'lugares': lugares,
        'instructores': instructores,
        'lugar_seleccionado': lugar_seleccionado,
    })

def añadirlugar(request):
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

    return render(request, 'añadirlugar.html')

def cambiarinstructor(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    instructores = Instructor.objects.all()  # Obtener todos los instructores disponibles

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
def inscripcionlista(request):
    inscripciones = Inscripcion.objects.all()  # Obtener todas las inscripciones
    eventos = []

    for inscripcion in inscripciones:
        evento = inscripcion.evento  # Obtener el evento asociado a cada inscripción
        eventos.append({
            'id': evento.id,  # Agrega el ID del evento aquí
            'nombre': evento.curso.nombre,
            'periodo': evento.curso.periodo,
            'horas': evento.curso.horas,
            'instructor': evento.curso.instructor,
            'lugar': evento.lugar,
            'aceptado': inscripcion.aceptado, #Estado para que cambien los botones
        })

    return render(request, 'inscripcionlista.html', {'eventos': eventos})

def vercurso(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    return render(request, 'vercurso.html', {'evento': evento})

def aceptarinscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    inscripcion.aceptado = True
    inscripcion.save()
    return redirect('inscripcionlista')  

def invalidarinscripcion(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    inscripcion.aceptado = False
    inscripcion.save()
    return redirect('inscripcionlista')  