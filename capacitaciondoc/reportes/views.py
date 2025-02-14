from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from eventos.models import Evento
from catalogos.models import Instructor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings

def generar_constancia(request, evento_id):
    user = request.user
    # Obtener el evento específico
    evento = get_object_or_404(Evento, id=evento_id)
    curso = evento.curso
    instructor = evento.instructor

    # Configurar los datos necesarios para la constancia
    datos = {
        "nombre_curso": curso.nombre,
        "fecha_inicio": evento.fechaInicio.strftime("%d de %B de %Y"),
        "fecha_fin": evento.fechaFin.strftime("%d de %B de %Y"),
        "horas": curso.horas,
        "nombre_instructor": f"{user.first_name} {user.last_name_paterno}",
        "ruta_fondo": os.path.join(settings.MEDIA_ROOT, 'fondos', 'fondo_constancia.jpg'),
        "ruta_logo": os.path.join(settings.MEDIA_ROOT, 'logos', 'logo_tecnm.png'),
        "ruta_firma": os.path.join(settings.MEDIA_ROOT, 'firmas', 'firma_director.png'),
        "ruta_sello": os.path.join(settings.MEDIA_ROOT, 'sellos', 'sello_tecnm.png'),
    }

    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="constancia_{evento_id}.pdf"'

    # Crear el canvas de ReportLab
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Agregar el fondo (si existe)
    if datos["ruta_fondo"] and os.path.exists(datos["ruta_fondo"]):
        fondo = ImageReader(datos["ruta_fondo"])
        p.drawImage(fondo, 0, 0, width=width, height=height)

    # Agregar el logo (si existe)
    if datos["ruta_logo"] and os.path.exists(datos["ruta_logo"]):
        logo = ImageReader(datos["ruta_logo"])
        p.drawImage(logo, 50, height - 150, width=100, height=100)

    # Agregar la firma (si existe)
    if datos["ruta_firma"] and os.path.exists(datos["ruta_firma"]):
        firma = ImageReader(datos["ruta_firma"])
        p.drawImage(firma, width - 150, 50, width=100, height=50)

    # Agregar el sello (si existe)
    if datos["ruta_sello"] and os.path.exists(datos["ruta_sello"]):
        sello = ImageReader(datos["ruta_sello"])
        p.drawImage(sello, width - 150, 150, width=100, height=100)

    # Agregar texto
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 200, f"Constancia de participación en el curso: {datos['nombre_curso']}")
    p.drawString(100, height - 220, f"Impartido por: {datos['nombre_instructor']}")
    p.drawString(100, height - 240, f"Fecha de inicio: {datos['fecha_inicio']}")
    p.drawString(100, height - 260, f"Fecha de término: {datos['fecha_fin']}")
    p.drawString(100, height - 280, f"Duración: {datos['horas']} horas")

    # Finalizar el PDF
    p.showPage()
    p.save()

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