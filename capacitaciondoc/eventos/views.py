from datetime import datetime, timedelta
import locale
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse

from django.core.files.storage import FileSystemStorage #Para archivos y directorios


from .forms import DepartamentoForm, EventoForm, EvidenciaForm, OficioComisionForm
from .models import Asistencia, Calificacion, Evento, Evidencia, Inscripcion, OficioComision
from catalogos.models import Departamento, Docente, Lugar, Instructor, GradoAcademico, ValorCalificacion

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import BaseDocTemplate, PageTemplate, Paragraph, Table, TableStyle, Spacer, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from io import BytesIO
import os
import re

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

        if 'guardar' in request.POST:  # Si se presionó el botón "Guardar"
            if form.is_valid():
                nueva_evidencia = request.FILES.get('archivo_evidencia', None)

                # Si hay una nueva evidencia, eliminar la anterior (si existe)
                if nueva_evidencia:
                    if evidencia and evidencia.archivo_evidencia:
                        fs = FileSystemStorage()
                        fs.delete(evidencia.archivo_evidencia.name)
                elif evidencia and not nueva_evidencia:
                    # Si no hay nueva evidencia, mantener la existente
                    form.instance.archivo_evidencia = evidencia.archivo_evidencia

                # Guardar el formulario
                evidencia = form.save(commit=False)
                evidencia.evento = evento
                evidencia.save()

                messages.success(request, "Evidencia guardada exitosamente.")
                return redirect('detalle_curso_calificacion', evento_id=evento.id)

        elif 'borrar' in request.POST:  # Si se presionó el botón "Borrar"
            if evidencia and evidencia.archivo_evidencia:
                fs = FileSystemStorage()
                fs.delete(evidencia.archivo_evidencia.name)
                evidencia.delete()
                messages.success(request, "Evidencia borrada exitosamente.")
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
    valores_calificacion = ValorCalificacion.objects.all()  # Obtiene todas las opciones de calificación
    
    if not evidencia:
        messages.warning(request, "No puedes asignar calificación si no has cargado tu evidencia del curso.")
        return redirect('detalle_curso_calificacion', evento_id=evento.id)  # Redirigir a la página de detalle del evento
    
    if request.method == 'POST':
        todas_seleccionadas = True  # Bandera para controlar si todas las calificaciones están seleccionadas

        for inscripcion in inscripciones:
            calificacion_value = request.POST.get(f'calificacion_{inscripcion.id}')
            
            if not calificacion_value:  # Si no se seleccionó calificación, marca como no seleccionada
                todas_seleccionadas = False
                messages.warning(request, f'Por favor, seleccione una calificación para {inscripcion.usuario.first_name} {inscripcion.usuario.last_name_paterno}.')

            else:
                calificacion_obj = ValorCalificacion.objects.get(id=calificacion_value)
                Calificacion.objects.update_or_create(
                    inscripcion=inscripcion,
                    defaults={'calificacion': calificacion_obj}
                )

        if todas_seleccionadas:
            messages.success(request, "Calificaciones asignadas correctamente.")
            return redirect('detalle_curso_calificacion', evento_id=evento.id)  # Redirigir a la página de detalle del evento

        # Si no todas las calificaciones fueron seleccionadas, no redirigir
        return render(request, 'calificacion.html', {
            'evento': evento,
            'inscripciones': inscripciones,
            'valores_calificacion': valores_calificacion,
        })
    
    return render(request, 'calificacion.html', {
        'evento': evento,
        'inscripciones': inscripciones,
        'valores_calificacion': valores_calificacion,  # Pasar las opciones de calificación a la plantilla
    })

@login_required(login_url='signin')
@permission_required('eventos.view_oficiocomision', raise_exception=True)
def oficioslista(request):
    departamentos = Departamento.objects.all()
    docentes = None
    departamento_seleccionado = None
    oficios = OficioComision.objects.all()

    # Obtener el ID del departamento de la URL
    departamento_id = request.GET.get('departamento_id')

    # Si hay un departamento_id en la URL, pre-seleccionar ese departamento
    if departamento_id:
        departamento_seleccionado = Departamento.objects.get(id=departamento_id)

    # Crear un diccionario para mapear cada docente con su oficio
    oficios_dict = {oficio.docente.id: oficio for oficio in oficios}

    # Combinar request.GET con el valor inicial
    form_data = request.GET.copy()
    if departamento_seleccionado:
        form_data['departamento'] = departamento_seleccionado.id

    # Pasar el form_data al formulario
    form = DepartamentoForm(form_data or None, initial={'departamento': departamento_seleccionado})
    if form.is_valid():
        departamento_seleccionado = form.cleaned_data["departamento"]
        docentes = Docente.objects.filter(departamento=departamento_seleccionado)

    return render(request, "oficioslista.html", {
        "departamentos": departamentos, 
        "docentes": docentes, 
        'departamento_seleccionado':departamento_seleccionado,
        'oficios': oficios,
        'oficios_dict': oficios_dict,
        'form': form
        })

@login_required(login_url='signin')
@permission_required('eventos.add_oficiocomision', raise_exception=True)
def oficiocrear(request, docente_id):
    departamento_id = request.GET.get('departamento_id')
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        form = OficioComisionForm(request.POST)
        if form.is_valid():
            oficio = form.save(commit=False)
            oficio.docente = docente
            oficio.nomenclatura = docente.departamento.nomenclatura
            oficio.save()
            messages.success(request, "Oficio creado correctamente.")
            # Redirigir a oficioslista con el departamento_id
            return HttpResponseRedirect(f"{reverse('oficioslista')}?departamento_id={departamento_id}")
    else:
        form = OficioComisionForm()
    
    return render(request, "oficiocrear.html", {'docente': docente, 'form': form, 'departamento_id': departamento_id})

@login_required(login_url='signin')
@permission_required('eventos.change_oficiocomision', raise_exception=True)
def oficioactualizar(request, oficio_id):
    departamento_id = request.GET.get('departamento_id')
    oficio = get_object_or_404(OficioComision, id=oficio_id)
    docente = oficio.docente
    if request.method == 'POST':
        form = OficioComisionForm(request.POST, instance=oficio)
        if form.is_valid():
            oficio = form.save(commit=False)
            oficio.nomenclatura = docente.departamento.nomenclatura
            oficio.save()
            messages.success(request, "Oficio actualizado correctamente.")
            return HttpResponseRedirect(f"{reverse('oficioslista')}?departamento_id={departamento_id}")
    else:
        form = OficioComisionForm(instance=oficio)
    
    return render(request, "oficioactualizar.html", {'oficio': oficio, 'form': form, 'docente': docente, 'departamento_id': departamento_id})

@login_required(login_url='signin')
@permission_required('eventos.view_oficiocomision', raise_exception=True)
def descargar_oficio(request, oficio_id):
    locale.setlocale(locale.LC_TIME, 'spanish')  # Establecer la localización para formatear la fecha a español en el pdf

    oficio = get_object_or_404(OficioComision, id=oficio_id)
    docente = oficio.docente
    inscripciones = Inscripcion.objects.filter(usuario=docente.user).order_by('evento__fechaInicio')
    departamento = docente.departamento

    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=letter,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1 * cm, bottomMargin=1 * cm)

    font_path_regular = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Montserrat-Regular.ttf')
    font_path_bold = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Montserrat-Bold.ttf')
    font_path_italic = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Montserrat-Italic.ttf')
    if os.path.exists(font_path_regular):
        pdfmetrics.registerFont(TTFont('Montserrat-Regular', font_path_regular))

    if os.path.exists(font_path_bold):
        pdfmetrics.registerFont(TTFont('Montserrat-Bold', font_path_bold))
    
    if os.path.exists(font_path_italic):
        pdfmetrics.registerFont(TTFont('Montserrat-Italic', font_path_italic))


    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Regular', 
        fontSize=10,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    )
    
    style_bold = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Bold', 
        fontSize=10,
        spaceAfter=8,
    )

    style_italic = ParagraphStyle(
        'MontserratItalic',
        parent=styles['Normal'],
        fontName='Montserrat-Italic', 
        fontSize=10,
        spaceAfter=8,
    )

    style_right = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Regular', 
        fontSize=10,
        spaceAfter=8,
        alignment=TA_RIGHT
    )

    # Definir el contenido del PDF
    Story = []

    # Agregar un encabezado con el logo
    def encabezado(canvas, doc):
        header_path = os.path.join(settings.MEDIA_ROOT, f'formatos/departamento/{departamento.departamento}/{oficio.fecha.year}', 'header.png')
        if os.path.exists(header_path):
            canvas.drawImage(header_path, 2 * cm, 25 * cm, width=17.5 * cm, height=50, preserveAspectRatio=True, mask='auto')
        else:
            canvas.drawString(2 * cm, 25 * cm, "Encabezado no encontrado")

    def pie_pagina(canvas, doc):
        footer_path = os.path.join(settings.MEDIA_ROOT, f'formatos/departamento/{departamento.departamento}/{oficio.fecha.year}', 'footer.png')
        if os.path.exists(footer_path):
            canvas.drawImage(footer_path, 1 * cm, 1 * cm, width= 19 * cm, height=100, preserveAspectRatio=True, mask='auto')
        else:
            canvas.drawString(2 * cm, 2 * cm, "Pie de página no encontrado")

    
    # Definir un marco para el contenido
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 2 * cm, id='normal')

    # Crear una plantilla de página con encabezado y pie de página
    plantilla = PageTemplate(id='plantilla', frames=frame, onPage=encabezado, onPageEnd=pie_pagina)
    doc.addPageTemplates([plantilla])

    # Encabezado alineado a la derecha
    fecha_formateada = oficio.fecha.strftime('%d/%B/%Y')

    encabezado_data = [
        ["Apizaco, Tlaxcala, ", f"{fecha_formateada}"],
        
    ]

    table = Table(encabezado_data, colWidths=[390, 100])
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -1), "Montserrat-Regular"),
        ("BACKGROUND", (1, 0), (1, 0), colors.black),  # FONDO NEGRO PARA LA FECHA
        ("TEXTCOLOR", (1, 0), (1, 0), colors.white),  # LETRAS BLANCAS EN LA FECHA
    ]))

    Story.append(table)
    Story.append(Spacer(1, 1))
    no_oficio = Paragraph(f"Oficio No. {oficio.nomenclatura}-{oficio.no_oficio}/{oficio.fecha.year}", style_right)
    asunto = Paragraph('Asunto: COMISIÓN',style_right)
    Story.append(no_oficio)
    Story.append(asunto)
    Story.append(Spacer(1, 12))
    

    presente = f'''
        {docente.user.first_name} {docente.user.last_name_paterno} {docente.user.last_name_materno}<br/>
        DOCENTE DEL DEPTO. DE {docente.departamento}<br/>
        PRESENTE
    '''.upper()
    destinatario = Paragraph(presente, style_bold)
    Story.append(destinatario)
    Story.append(Spacer(1,1))

    text = f'''
        Con base en su desarrollo profesional en el desempeño de sus funciones y aunado a su alto sentido de responsabilidad, 
        se le <b>COMISIONA</b> a participar en los siguientes <b>cursos y/o actividades intersemestrales</b>, 
        durante el preiodo comprendido del
        {inscripciones[0].evento.curso.periodo.inicioPeriodo} al {inscripciones[0].evento.curso.periodo.finPeriodo}:
    '''
    
    redaccion = Paragraph(text, style_normal)
    Story.append(redaccion)
    Story.append(Spacer(1,12))

    data = [
        [Paragraph('FECHA',style_bold), Paragraph('CURSO/ACTIVIDAD', style_bold), Paragraph('LUGAR', style_bold), Paragraph('HORARIO', style_bold)]
    ]
    for inscripcion in inscripciones:
        hora_inicio = inscripcion.evento.horaInicio.strftime("%H:%M") if inscripcion.evento.horaInicio else "N/A"
        hora_fin = inscripcion.evento.horaFin.strftime("%H:%M") if inscripcion.evento.horaFin else "N/A"
        data.append([
            Paragraph(f"{inscripcion.evento.fechaInicio.strftime('%d-%B-%Y')} al {inscripcion.evento.fechaFin.strftime('%d-%B-%Y')}", style_normal),
            Paragraph(inscripcion.evento.curso.nombre, style_normal), 
            Paragraph(f'{inscripcion.evento.lugar}', style_normal), 
            Paragraph(f'{hora_inicio} a {hora_fin} hrs.',style_normal),
        ])
    table = Table(data, [100, 200, 80, 110])
    table.setStyle(TableStyle([
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
    Story.append(table)
    Story.append(Spacer(1, 12))

    text = 'Sin otro particular por el momento y deséandole el mayor de los éxitos, me despido de usted.'
    despido = Paragraph(text, style_normal)
    Story.append(despido)
    Story.append(Spacer(1,12))

    att = Paragraph('ATENTAMENTE', style_bold)
    Story.append(att)
    Story.append(Spacer(1,-8))
    textend = f"Excelencia en Educación Tecnológica.<br/>Pensar para Servir, Servir para Triunfar."
    lema = Paragraph(textend, style_italic)
    Story.append(lema)
    Story.append(Spacer(1,60))

    
    jefe_dep = Paragraph(f'{departamento.nombreJefe} {departamento.apParternoJefe} {departamento.apMaternoJefe}'.upper(), style_bold)
    cargo = Paragraph(f'JEFE DEL DPTO. DE {departamento.departamento}'.upper(), style_bold)
    Story.append(jefe_dep)
    Story.append(Spacer(1,-6))
    Story.append(cargo)
    Story.append(Spacer(1,12))

    # Crear el documento PDF
    doc.build(Story)

    buffer.seek(0)
    filename = f"Oficio-Comision-{docente.user.first_name}.pdf"
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response