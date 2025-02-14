from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from eventos.models import Evento
from catalogos.models import Instructor
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

def procesar_imagen_png(ruta_imagen):
    """Convierte un PNG con transparencia a un formato compatible con ReportLab."""
    img = Image.open(ruta_imagen)
    if img.mode in ("RGBA", "LA"):
        fondo = Image.new("RGBA", img.size, (255, 255, 255, 0))
        fondo.paste(img, mask=img.split()[3])
        return ImageReader(fondo)
    return ImageReader(img)

def generar_constancia(request, evento_id):
    user = request.user
    evento = get_object_or_404(Evento, id=evento_id)
    curso = evento.curso
    
    datos = {
        "nombre_receptor": f"{user.first_name} {user.last_name}",
        "nombre_curso": curso.nombre.upper(),
        "fecha_inicio": evento.fechaInicio.strftime("%d de %B de %Y"),
        "fecha_fin": evento.fechaFin.strftime("%d de %B de %Y"),
        "duracion": f"{curso.horas} horas",
        "fecha_emision": evento.fechaFin.strftime("%d de %B de %Y"),
        "firmante": "Yesica Imelda Saavedra Benítez",  # Cambia según el firmante real
        "cargo_firmante": "Directora",  # Cambia según el cargo real
        "ruta_fondo": os.path.join(settings.MEDIA_ROOT, 'fondos', 'fondo_constancia.jpg'),
        "ruta_logo": os.path.join(settings.MEDIA_ROOT, 'logos', 'logo_tecnm.png'),
        "ruta_firma": os.path.join(settings.MEDIA_ROOT, 'firmas', 'firma_director.png'),
        "ruta_sello": os.path.join(settings.MEDIA_ROOT, 'sellos', 'sello_tecnm.png'),
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="constancia_{evento_id}.pdf"'
    c = canvas.Canvas(response, pagesize=letter)
    ancho, alto = letter

    # Fondo del certificado
    if os.path.exists(datos["ruta_fondo"]):
        fondo = procesar_imagen_png(datos["ruta_fondo"])
        c.drawImage(fondo, 0, 0, width=ancho, height=alto)
    
    # Logotipo
    if os.path.exists(datos["ruta_logo"]):
        logo = procesar_imagen_png(datos["ruta_logo"])
        logo_ancho_original = 924
        logo_alto_original = 126
        escala = (ancho - 100) / logo_ancho_original
        logo_ancho = logo_ancho_original * escala
        logo_alto = logo_alto_original * escala
        c.drawImage(logo, (ancho - logo_ancho) / 2, alto - logo_alto - 50, width=logo_ancho, height=logo_alto)

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
    c.drawCentredString(ancho / 2, alto - 420, f"{datos['nombre_receptor'].split()[-1].upper()}")
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 460, f"Por impartir el curso:")
    c.setFont("Montserrat-Bold", 13)
    c.drawCentredString(ancho / 2, alto - 480, datos["nombre_curso"])
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 500, f"Realizado del {datos['fecha_inicio']} al {datos['fecha_fin']}")
    c.drawCentredString(ancho / 2, alto - 520, f"Con duración de {datos['duracion']}")

    # Firma
    if os.path.exists(datos["ruta_firma"]):
        firma = procesar_imagen_png(datos["ruta_firma"])
        firma_ancho = 200
        firma_alto = 100
        c.drawImage(firma, (ancho - firma_ancho) / 2, alto - 650, width=firma_ancho, height=firma_alto)

    # Sello
    if os.path.exists(datos["ruta_sello"]):
        sello = procesar_imagen_png(datos["ruta_sello"])
        sello_ancho = 180
        sello_alto = 130
        c.drawImage(sello, ancho - sello_ancho - 10, alto - 680, width=sello_ancho, height=sello_alto)

    # Datos de emisión
    c.setFont("Montserrat", 9)
    c.drawCentredString(ancho / 2, alto - 550, f"AV. INSTITUTO TECNOLÓGICO NO. 418, AHUASHUATEPEC, TZOMPANTEPEC, TLAX., {datos['fecha_emision']}")

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