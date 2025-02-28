import locale
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
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
    print(user)
    
    evento = get_object_or_404(Evento, id=evento_id)
    curso = evento.curso

    # Obtiene la autoridad que contenga cargo director
    # Dado que director es el mismo id para directora, obtenemos a través de cargo en masculino
    autoridad = get_object_or_404(Autoridad, puesto__cargo_masculino="Director", estatus=True)

    # Para obtener el cargo según el género, llamamos la funcion get_puesto() que
    # devuelve el puesto de la autoridad según su género
    cargo = autoridad.get_puesto()
    
    datos = {
        "nombre_receptor": user.first_name,
        "apellidos_receptor": f'{user.last_name_paterno} {user.last_name_materno}',
        "nombre_curso": curso.nombre.upper(),
        "fecha_inicio": evento.fechaInicio.strftime("%d de %B de %Y"),
        "fecha_fin": evento.fechaFin.strftime("%d de %B de %Y"),
        "duracion": f"{curso.horas} horas",
        "fecha_emision": evento.fechaFin.strftime("%d de %B de %Y"),
        "firmante": autoridad.get_full_name(),
        "cargo_firmante": cargo,
        "ruta_fondo": '',
        "ruta_logo": os.path.join(settings.MEDIA_ROOT, f'formatos/constancia/{evento.fechaInicio.year}', 'header.png'),
        "ruta_firma": os.path.join(settings.MEDIA_ROOT, f'autoridades/{autoridad.puesto.cargo_masculino}/{autoridad.get_full_name()}', 'firma.png'),
    }
    print(evento.fechaInicio.year)

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
        c.drawCentredString(ancho / 2, alto - 460, f"Por impartir el curso:")
    elif user.rol== "Docente":
        c.drawCentredString(ancho / 2, alto - 460, f"Por acreditar el curso:")
    c.setFont("Montserrat-Bold", 13)
    c.drawCentredString(ancho / 2, alto - 480, datos["nombre_curso"])
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 500, f"Realizado del {datos['fecha_inicio']} al {datos['fecha_fin']}")
    c.drawCentredString(ancho / 2, alto - 520, f"Con duración de {datos['duracion']}")

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
            if user.rol != "Docente":  # Solo agregar el instructor si NO es docente
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
def generar_constancia(request, evento_id, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    evento = get_object_or_404(Evento, id=evento_id)

    if user.rol == "Instructor":
        return redirect('descargar_constancia', evento_id=evento.id, user_id=user.id)
    elif user.rol == "Docente":
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
    print(encuesta_realizada)
    return render(request, 'generar_constancia.html', {
        'evento': evento, 
        'user': user, 
        'encuesta_realizada': encuesta_realizada, 
        'calificacion': calificacion,
        'aprobado': aprobado,
        'message_encuesta': message_encuesta,
        'message_calificacion': message_calificacion,
    })