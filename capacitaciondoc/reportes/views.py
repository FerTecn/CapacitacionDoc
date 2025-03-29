import locale
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from .models import ConstanciaDocente, ConstanciaInstructor
from usuarios.models import CustomUser
from encuesta.models import Encuesta
from eventos.models import Calificacion, Evento, Inscripcion
from catalogos.models import Autoridad, Docente, Instructor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image
import os
from django.conf import settings

# Registra las fuentes Montserrat
montserrat_regular_path = os.path.join(settings.BASE_DIR, "static/fonts/Montserrat-Regular.ttf")
montserrat_bold_path = os.path.join(settings.BASE_DIR, "static/fonts/Montserrat-Bold.ttf")

pdfmetrics.registerFont(TTFont('Montserrat', montserrat_regular_path))
pdfmetrics.registerFont(TTFont('Montserrat-Bold', montserrat_bold_path))

def generar_constancia_pdf(request, evento_id, user_id):
    
    locale.setlocale(locale.LC_TIME, 'spanish')

    user = CustomUser.objects.get(id=user_id)

    evento = get_object_or_404(Evento, id=evento_id)
    curso = evento.curso
    
    constancia = None
    
    if user.rol == "Docente":
        constancia = ConstanciaDocente.objects.filter(curso=evento, docente=user.docente).first()
        print(constancia)
    elif user.rol == "Instructor":
        constancia = ConstanciaInstructor.objects.filter(curso=evento, instructor=user.instructor).first()

    if request.user.rol == "Instructor" and curso.instructor.user.id != request.user.id:
        messages.warning(request, 'No tienes permiso para ver esta constancia.')
        return redirect('home')
    
    inscrito = Inscripcion.objects.filter(evento=evento, usuario=user).exists()
    if request.user.rol == "Docente" and request.user.id != user_id and not inscrito:
        messages.warning(request, 'No tienes permiso para ver esta constancia.')
        return redirect('home')
    
    if not constancia:
        messages.warning(request, "Constancia no encontrada.")
        return redirect('home')
    
    datos = {
        "nombre_receptor": user.first_name,
        "apellidos_receptor": f'{user.last_name_paterno} {user.last_name_materno}',
        "nombre_curso": constancia.curso.curso.nombre,
        "fecha_inicio": constancia.curso.fechaInicio.strftime("%d de %B de %Y"),
        "fecha_fin": constancia.curso.fechaFin.strftime("%d de %B de %Y"),
        "duracion": f"{constancia.curso.curso.horas} horas",
        "fecha_emision": constancia.fecha.strftime("%d de %B de %Y"),
        "firmante": constancia.director.get_full_name(),
        "cargo_firmante": constancia.director.get_puesto(),
        "ruta_fondo": '',
        "ruta_logo": os.path.join(settings.MEDIA_ROOT, f'formatos/constancia/{evento.fechaInicio.year}', 'header.png'),
        "ruta_firma": os.path.join(settings.MEDIA_ROOT, f'autoridades/{constancia.director.puesto.cargo_masculino}/{constancia.director.get_full_name()}', 'firma.png'),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="constancia_{evento_id}.pdf"'
    c = canvas.Canvas(response, pagesize=letter)
    ancho, alto = letter

    if not os.path.exists(datos["ruta_logo"]):
        print(f"Error: No se encontró la imagen {datos['ruta_logo']}")

    # Fondo del certificado
    if os.path.exists(datos["ruta_fondo"]):
        fondo = datos["ruta_fondo"]
        c.drawImage(fondo, 0, 0, width=ancho, height=alto, mask='auto')
    
    # Logotipo
    if os.path.exists(datos["ruta_logo"]):
        logo = datos["ruta_logo"]
        logo_ancho_original = 924
        logo_alto_original = 126
        escala = (ancho - 100) / logo_ancho_original
        logo_ancho = logo_ancho_original * escala
        logo_alto = logo_alto_original * escala
        c.drawImage(logo, (ancho - logo_ancho) / 2, alto - logo_alto - 50, width=logo_ancho, height=logo_alto, mask='auto')

    # Encabezado y texto con contraste
    c.setFont("Montserrat-Bold", 18)
    c.setFillColorRGB(51/255, 51/255, 51/255)  # Color negro para el texto
    c.drawCentredString(ancho / 2, alto - 180, "EL TECNOLÓGICO NACIONAL DE MÉXICO")
    c.setFont("Montserrat-Bold", 14)
    c.drawCentredString(ancho / 2, alto - 200, "A TRAVÉS DEL INSTITUTO TECNOLÓGICO DE APIZACO")
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 245, "OTORGA EL PRESENTE")
    c.setFont("Montserrat-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 300, "RECONOCIMIENTO")
    c.setFont("Montserrat", 24)
    c.drawCentredString(ancho / 2, alto - 345, "A")
    c.setFont("Montserrat-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 390, f"{datos['nombre_receptor'].upper()}")
    c.setFont("Montserrat-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 420, f"{datos['apellidos_receptor'].upper()}")
    c.setFont("Montserrat", 14)
    if user.rol== "Instructor":
        c.drawCentredString(ancho / 2, alto - 460, f"POR IMPARTIR EL CURSO")
    elif user.rol== "Docente":
        c.drawCentredString(ancho / 2, alto - 460, f"POR ACREDITAR EL CURSO")
    c.setFont("Montserrat-Bold", 13)
    c.drawCentredString(ancho / 2, alto - 480, datos["nombre_curso"].upper())
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 500, f"REALIZADO DEL {datos['fecha_inicio'].upper()} AL {datos['fecha_fin'].upper()}")
    c.drawCentredString(ancho / 2, alto - 520, f"CON DURACIÓN DE {datos['duracion'].upper()}")

    # Firma
    if os.path.exists(datos["ruta_firma"]):
        firma = datos["ruta_firma"]
        firma_ancho = 200
        firma_alto = 100
        c.drawImage(firma, (ancho - firma_ancho) / 2, alto - 650, width=firma_ancho, height=firma_alto, mask='auto')

    # Datos de emisión
    c.setFont("Montserrat", 9)
    c.drawCentredString(ancho / 2, alto - 550, f"AV. INSTITUTO TECNOLÓGICO NO. 418, AHUASHUATEPEC, TZOMPANTEPEC, TLAX., {datos['fecha_emision'].upper()}")

    # Espacio para la firma del responsable
    c.setFont("Montserrat", 12)
    c.drawCentredString(ancho / 2, alto - 650, "__________________________________")
    c.setFont("Montserrat-Bold", 13)
    c.drawCentredString(ancho / 2, alto - 670, datos["firmante"].upper())
    c.setFont("Montserrat-Bold", 13)
    c.drawCentredString(ancho / 2, alto - 690, datos["cargo_firmante"].upper())

    # Guardar el PDF
    c.showPage()
    c.save()
    return response

def listacursos(request):
    user = request.user
    cursos = []

    if user.rol == "Instructor":
        eventos = Evento.objects.filter(curso__instructor=user.instructor).order_by('curso__nombre')

    elif user.rol == "Docente":
        inscripciones = Inscripcion.objects.filter(usuario=user).order_by('evento__curso__nombre')
        eventos = [inscripcion.evento for inscripcion in inscripciones]
        
    else:
        eventos = Evento.objects.all().order_by('curso__nombre')

    for evento in eventos:
            curso_info = {
                'nombre': evento.curso.nombre,
                'fecha_inicio': evento.fechaInicio,
                'fecha_fin': evento.fechaFin,
                'horas': evento.curso.horas,
                'evento_id': evento.id,
            }
            if user.rol != "Instructor":  # Solo agregar el instructor si rol es instructor
                curso_info['instructor'] = evento.curso.instructor

            cursos.append(curso_info)

    return render(request, 'lista_cursos.html', {'cursos': cursos, 'user': user})

def listaconstancias(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    docentes_inscritos = Inscripcion.objects.filter(evento=evento).select_related('usuario')
    docentes = []
    for docente in docentes_inscritos:
        if docente.usuario.rol == "Docente":
            encuesta_realizada = Encuesta.objects.filter(inscripcion__usuario=docente.usuario, inscripcion__evento=evento).exists()
            calificacion = Calificacion.objects.filter(inscripcion__evento=evento, inscripcion__usuario=docente.usuario).first()
            if calificacion:
                aprobado = calificacion.calificacion.aprobatoria
            else:
                calificacion = None
                aprobado = False
            
            docentes.append({
                'docente': docente.usuario,
                'encuesta_realizada': encuesta_realizada,
                'calificacion': calificacion,
                'aprobado': aprobado,
            })
    
    instructor = evento.curso.instructor if evento.curso and evento.curso.instructor else None

    return render(request, 'lista_constancias.html', {
        'evento': evento,
        'docentes': docentes,
        'instructor': instructor,
        })

def estatusconstancia(request, evento_id, user_id):
    if request.user.id != user_id and request.user.rol == "Docente":
        messages.warning(request, "No puedes generar constancias de otros docentes.")
        return redirect('lista_cursos')
    
    evento = get_object_or_404(Evento, id=evento_id)
    user = get_object_or_404(CustomUser, id=user_id)

    if user.rol != "Docente":
        messages.warning(request, "El usuario no es un docente.")
        return redirect('lista_constancias', evento_id=evento.id)

    inscripcion = Inscripcion.objects.filter(evento=evento, usuario=user).first()
    if not inscripcion:
        messages.warning(request, "El usuario no está inscrito en el evento.")
        return redirect('lista_constancias', evento_id=evento.id)
    
    encuesta_realizada = Encuesta.objects.filter(inscripcion__usuario=user, inscripcion__evento=evento).exists()
    if encuesta_realizada:
        message_encuesta = 'Encuesta de satisfacción <b class="text-success">realizada satisfactoriamente</b>.'
    else:
        message_encuesta = 'El docente debe realizar la encuesta de satisfacción para poder generar la constancia.'

    calificacion = Calificacion.objects.filter(inscripcion__evento=evento, inscripcion__usuario=user).first()
    if calificacion:
        aprobado = calificacion.calificacion.aprobatoria
        if aprobado:
            message_calificacion = f'Calificación obtenida: <b class="text-success">{calificacion.calificacion}</b>'
        else:
            message_calificacion = f'<b class="text-danger">Calificación reprobatoria: {calificacion.calificacion}.</b> Lamentamos que no hayas aprobado el curso.'
    else:
        aprobado = None
        message_calificacion = f"<b>Sin calificación.</b> <br>Una vez el docente culmine el curso satisfactoriamente, obtendrá una calificación asignada por el instructor {evento.curso.instructor.user.get_user_full_name()}."

    return render(request, 'generar_constancia.html', {
        'evento': evento, 
        'user': user, 
        'encuesta_realizada': encuesta_realizada, 
        'calificacion': calificacion,
        'aprobado': aprobado,
        'message_encuesta': message_encuesta,
        'message_calificacion': message_calificacion,
    })

def generarconstanciadocente(request, evento_id, user_id):
    if request.user.rol == "Docente" and request.user.id != user_id:
        messages.warning(request, "No puedes generar constancias de otros docentes.")
        return redirect('estatus_constancia_docente', evento_id=evento_id, user_id=user_id)
    
    docente = get_object_or_404(Docente, user_id=user_id)
    evento = get_object_or_404(Evento, id=evento_id)
    # Verificar si ya existe constancia
    constancia_existente = ConstanciaDocente.objects.filter(
        curso=evento,
        docente=docente
    ).first()

    if constancia_existente:
        return redirect('descargar_constancia', evento_id=evento.id, user_id=docente.user.id)

    director = get_object_or_404(Autoridad, puesto__cargo_masculino='Director', estatus = True)

    inscrito = Inscripcion.objects.filter(evento__id=evento_id, usuario=docente.user).exists()
    if not inscrito:
        messages.warning(request, "No estas inscrito en el evento.")
        return redirect('estatus_constancia_docente', evento_id=evento.id, user_id=docente.user.id)
    
    encuesta = Encuesta.objects.filter(inscripcion__evento=evento, inscripcion__usuario=docente.user).first()
    if not encuesta:
        messages.warning(request, "El docente debe realizar la encuesta de satisfacción para poder generar la constancia.")
        return redirect('estatus_constancia_docente', evento_id=evento.id, user_id=docente.user.id)
        
    calificacion = Calificacion.objects.filter(inscripcion__evento=evento, inscripcion__usuario=docente.user).first()
    if not calificacion or not calificacion.calificacion.aprobatoria:
        messages.warning(request, "El docente debe aprobar el curso para poder generar la constancia.")
        return redirect('estatus_constancia_docente', evento_id=evento.id, user_id=docente.user.id)
    

    try:
        constancia = ConstanciaDocente.objects.create(
            curso=evento,
            docente=docente,
            defaults={
                'calificacion': calificacion,
                'encuesta': encuesta,
                'fecha': evento.fechaFin,
                'director': director
            }
        )
        return redirect('descargar_constancia', evento_id=evento.id, user_id=docente.user.id)
    except ValidationError as e:
        messages.warning(request, str(e))
        return redirect('estatus_constancia_docente', evento_id=evento.id, user_id=docente.user.id)
    
def generarconstanciainstructor(request, evento_id, user_id):
    evento = get_object_or_404(Evento, id=evento_id)
    instructor = get_object_or_404(Instructor, user_id=user_id)

    constancia_existente = ConstanciaInstructor.objects.filter(
        curso=evento,
        instructor=instructor
    ).first()

    if constancia_existente:
        return redirect('descargar_constancia', evento_id=evento.id, user_id=user_id)
    
    director = get_object_or_404(Autoridad, puesto__cargo_masculino='Director', estatus = True)

    # Comprobar que el instructor corresponde al evento del curso
    if evento.curso.instructor.user.id == user_id:

        try:
            constancia = ConstanciaInstructor.objects.create(
                curso=evento,
                instructor=instructor,
                fecha=evento.fechaFin,
                director=director
            )
            return redirect('descargar_constancia', evento_id=evento.id, user_id=user_id)
        except ValidationError as e:
            messages.warning(request, str(e))
            if request.user.rol == "Instructor":
                return redirect('lista_cursos')
            elif request.user.rol != Docente and request.user.rol != "Instructor":
                return redirect('lista_constancias', evento_id=evento.id)
    else:
        messages.warning(request, "El instructor no corresponde al evento del curso.")
        if request.user.rol == "Instructor":
            return redirect('lista_cursos')
        elif request.user.rol != "Docente" and request.user.rol != "Instructor": 
            return redirect('lista_constancias', evento_id=evento.id)
