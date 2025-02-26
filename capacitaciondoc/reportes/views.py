import locale
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from eventos.models import Evento
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

def generar_constancia(request, evento_id):
    locale.setlocale(locale.LC_TIME, 'spanish')
    if request.user.rol == 'Instructor':
        user = request.user
    if request.user.rol == 'Docente':
        user = request.user
    
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
    if request.user.rol== "Instructor":
        c.drawCentredString(ancho / 2, alto - 460, f"Por impartir el curso:")
    elif request.user.rol== "Docente":
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

def lista_cursos(request):
    # Obtener el usuario actualmente logueado
    usuario_actual = request.user

    # Verificar si el usuario es un instructor
    if hasattr(usuario_actual, 'instructor'):
        # Obtener el instructor asociado al usuario
        instructor = usuario_actual.instructor

        # Obtener los eventos en los que el instructor está impartiendo cursos
        eventos = Evento.objects.filter() #instructor=instructor

        # Obtener las inscripciones relacionadas con esos eventos
        cursos_impartidos = []
        for evento in eventos:
            cursos_impartidos.append({
                'nombre': evento.curso.nombre,
                'fecha_inicio': evento.fechaInicio,
                'fecha_fin': evento.fechaFin,
                'horas': evento.curso.horas,
                'evento_id': evento.id,
            })

    else:
        # Si el usuario no es un instructor, no mostrar cursos
        cursos_impartidos = []

    return render(request, 'lista_cursos.html', {'cursos_impartidos': cursos_impartidos})