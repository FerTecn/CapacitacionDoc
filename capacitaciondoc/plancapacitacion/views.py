from django.shortcuts import render, render, get_object_or_404, redirect

from catalogos.models import Instructor
from .models import FichaTecnica, RegistroCurso, ValidarCurso
from .forms import CursoForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from eventos.models import Evento
from django.contrib.auth.decorators import login_required, permission_required

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

from io import BytesIO

# Create your views here.
@login_required(login_url='signin')
@permission_required('plancapacitacion.view_registrocurso', raise_exception=True)
def registrocursolista(request):
    cursos = RegistroCurso.objects.all()
    return render(request, 'registrocursolista.html', {'cursos': cursos})

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_registrocurso', raise_exception=True)
def registrocursover(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    return render(request, 'registrocursover.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_registrocurso', raise_exception=True)
def registrocursoactualizar(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('registrocursolista')  #Regresa a la lista de los cursos
    else:
        form = CursoForm(instance=curso)
    return render(request, 'registrocursoactualizar.html', {'form': form, 'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.delete_registrocurso', raise_exception=True)
def registrocursoeliminar(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('registrocursolista')  
    return render(request, 'registrocursoeliminar.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.add_registrocurso', raise_exception=True)
def registrocursocrear(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrocursolista') 
    else:
        form = CursoForm()

    return render(request, 'registrocursocrear.html', {'form': form})

#VALIDACION DE CURSOS
@login_required(login_url='signin')
@permission_required('plancapacitacion.view_validarcurso', raise_exception=True)
def validarcursolista(request):
    validarcurso = ValidarCurso.objects.select_related('curso', 'curso__periodo', 'curso__instructor').all()
    return render(request, 'validarcursolista.html', {
        'validarcurso': validarcurso,
    })

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_validarcurso', raise_exception=True)
def validarver(request, validar_id):
    validar = get_object_or_404(ValidarCurso, id=validar_id)
    curso = validar.curso  # El curso asociado al registro de validación
    return render(request, 'validarver.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_validarcurso', raise_exception=True)
def aceptar_curso(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    
    # Verificar si ya existe un evento asociado a este curso
    if not Evento.objects.filter(curso=curso).exists():
        curso.aceptado = True
        curso.save()
        Evento.objects.create(curso=curso)
    
    # Redirigir de vuelta a la lista de cursos
    return HttpResponseRedirect(reverse('validarcursolista'))

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_validarcurso', raise_exception=True)
def invalidar_curso(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    
    # Cambiar el estado del curso a rechazado
    curso.aceptado = False
    curso.save()
    
    # Eliminar el evento
    Evento.objects.filter(curso=curso).delete()

    return HttpResponseRedirect(reverse('validarcursolista'))

def cursosfichas(request):
    if request.user.rol == "Instructor":
        cursos = RegistroCurso.objects.filter(instructor__user=request.user)
    else:
        cursos = RegistroCurso.objects.all()
    return render(request, 'cursosfichas.html', {'cursos': cursos})

def fichatecnicaver(request, curso_id):
    ficha = get_object_or_404(FichaTecnica, curso=curso_id)
    # Obtener las relaciones relacionadas con el curso
    contenidos_tematicos = ficha.contenidos_tematicos.all()
    criterios_evaluacion = ficha.criterios_evaluacion.all()

    # Renderizar el template con los datos necesarios
    return render(request, 'fichatecnicaver.html', {
        'ficha': ficha,
        'contenidos_tematicos': contenidos_tematicos,
        'criterios_evaluacion': criterios_evaluacion,
    })

def generarfichatecnica(request, ficha_id):
    ficha = get_object_or_404(FichaTecnica, id=ficha_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)

    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        leading=14,
        alignment=TA_JUSTIFY
    )
    style_center = ParagraphStyle(
        "Center", 
        parent=style_normal, 
        alignment=TA_CENTER
    )
    
    style_bold = ParagraphStyle(
        "Bold", 
        parent=style_normal, 
        fontName="Helvetica-Bold"
    )

    # Lista para almacenar contenido
    Story = []

    # Función para crear una tabla
    def crear_tabla(data, col_widths):
        table = Table(data, col_widths)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        
        Story.append(table)
        Story.append(Spacer(1, 12))

    # **Encabezado**
    encabezado = "FICHA TÉCNICA DEL SERVICIO DE ACTUALIZACIÓN PROFESIONAL<br/> Y FORMACIÓN DOCENTE"
    codigo = "M00-SC-029-A02"
    Story.append(Paragraph(f"<b>{encabezado}</b>", style_center))
    Story.append(Paragraph(f"<b>{codigo}</b>", style_center))
    Story.append(Spacer(1, 12))

    # **Datos generales**
    Story.append(Paragraph(f"<b>Instituto Tecnológico de Apizaco</b>", style_bold))
    Story.append(Paragraph(f"<b>Nombre del servicio:</b> {ficha.servicio}", style_normal))
    Story.append(Paragraph(f"<b>Instructor(a):</b> {ficha.curso.instructor}", style_normal))
    Story.append(Spacer(1, 12))

    # **1) Introducción**
    Story.append(Paragraph(f"<b>1) Introducción:</b>", style_bold))
    Story.append(Paragraph(ficha.introduccion, style_normal))
    Story.append(Spacer(1, 12))

    # **2) Justificación**
    Story.append(Paragraph(f"<b>2) Justificación:</b>", style_bold))
    Story.append(Paragraph(ficha.justificacion, style_normal))
    Story.append(Spacer(1, 12))

    # **3) Objetivo**
    Story.append(Paragraph(f"<b>3) Objetivo:</b>", style_bold))
    Story.append(Paragraph(ficha.curso.objetivo, style_normal))
    Story.append(Spacer(1, 12))

    # **4) Descripción del Servicio**
    Story.append(Paragraph(f"<b>4) Descripción del Servicio:</b>", style_bold))
    Story.append(Paragraph(f"<b>a. Tipo de Servicio:</b> {ficha.servicio}", style_normal))
    Story.append(Paragraph(f"<b>b. Duración en horas:</b> {ficha.curso.horas}", style_normal))

    # **Tabla de Contenido Temático**
    Story.append(Paragraph("<b>c. Contenido Temático del Curso:</b>", style_bold))
    
    data = [["Temas/Subtemas", "Tiempo Programado", "Actividades de Aprendizaje"]]
    for contenido in ficha.contenidos_tematicos.all():
        data.append([contenido.tema, contenido.tiempo, contenido.actividades])

    crear_tabla(data, [200, 100, 170])
    

    # **4) --> Continuación**
    Story.append(Paragraph(f"<b>d. Elementos didácticos:</b> {ficha.elementosDidacticos}", style_normal))
    Story.append(Paragraph(f"<b>e. Criterios de evaluación:</b>", style_normal))
    Story.append(Spacer(1, 12))

    # ** Tabla Criterios de evaluación
    data = [["No", "Criterio", "Valor", "Instrumento de Evaluación"]]
    for index, criterio in enumerate(ficha.criterios_evaluacion.all(), start=1):
        data.append([index, criterio.criterio, criterio.valor, criterio.instrumento])
    
    crear_tabla(data, [20, 200, 50, 200])

    # **5) Competencias a desarrollar**
    Story.append(Paragraph(f"<b>5) Competencias a desarrollar:</b>", style_bold))
    Story.append(Paragraph(f"{ficha.competencias}", style_normal))
    Story.append(Spacer(1, 12))

    # **6) Fuentes de infomación**
    Story.append(Paragraph(f"<b>6) Fuentes de información:</b>", style_bold))
    Story.append(Paragraph(f"{ficha.fuentes}", style_normal))

    # **Firmas y Sello (agregados al final)**
    Story.append(Spacer(1, 100))

    # Nuevas filas para las firmas y sello
    data = [
        ["Nombre y Firma del Facilitador", "Sello", "Nombre y Firma del\n Jefe de Desarrollo Académico"],
    ]
    table = Table(data, [200, 100, 200])
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
        
    Story.append(table)
    Story.append(Spacer(1, 12))


    # Agregar salto de página si es necesario
    Story.append(PageBreak())

    # Generar PDF
    doc.build(Story)

    buffer.seek(0)
    filename = f"Ficha_Técnica-{ficha.curso.nombre}.pdf"
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response