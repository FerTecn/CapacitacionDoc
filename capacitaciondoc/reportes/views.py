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

# Construye la ruta absoluta de las fuentes
montserrat_regular_path = os.path.join(settings.BASE_DIR, "static/fonts/Montserrat-Regular.ttf")
montserrat_bold_path = os.path.join(settings.BASE_DIR, "static/fonts/Montserrat-Bold.ttf")

print(os.path.exists(montserrat_regular_path))  # Debería imprimir True si la fuente está en la ubicación correcta

# Registra las fuentes con ReportLab
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
        "ruta_fondo": os.path.join(settings.MEDIA_ROOT, 'fondos', 'fondo_constancia.jpg'),
        "ruta_logo": os.path.join(settings.MEDIA_ROOT, 'logos', 'logo_tecnm.png'),
        "ruta_firma": os.path.join(settings.MEDIA_ROOT, 'firmas', 'firma_director.png'),
        "ruta_sello": os.path.join(settings.MEDIA_ROOT, 'sellos', 'sello_tecnm.png'),
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="constancia_{evento_id}.pdf"'
    c = canvas.Canvas(response, pagesize=letter)
    ancho, alto = letter
    
    if os.path.exists(datos["ruta_fondo"]):
        fondo = procesar_imagen_png(datos["ruta_fondo"])
        c.drawImage(fondo, 0, 0, width=ancho, height=alto)
    
    if os.path.exists(datos["ruta_logo"]):
        logo = procesar_imagen_png(datos["ruta_logo"])
        c.drawImage(logo, (ancho - 200) / 2, alto - 100, width=200, height=50)
    
    c.setFont("Montserrat-Bold", 24)
    c.drawCentredString(ancho / 2, alto - 200, "RECONOCIMIENTO")
    c.setFont("Montserrat-Bold", 18)
    c.drawCentredString(ancho / 2, alto - 250, datos["nombre_receptor"].upper())
    c.setFont("Montserrat", 14)
    c.drawCentredString(ancho / 2, alto - 300, f"Por participar en el curso: {datos['nombre_curso']}")
    c.drawCentredString(ancho / 2, alto - 320, f"Realizado del {datos['fecha_inicio']} al {datos['fecha_fin']}")
    c.drawCentredString(ancho / 2, alto - 340, f"Con duración de {datos['duracion']}")
    
    if os.path.exists(datos["ruta_firma"]):
        firma = procesar_imagen_png(datos["ruta_firma"])
        c.drawImage(firma, ancho / 2 - 50, 100, width=100, height=50)
    
    if os.path.exists(datos["ruta_sello"]):
        sello = procesar_imagen_png(datos["ruta_sello"])
        c.drawImage(sello, ancho - 180, 80, width=100, height=100)
    
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