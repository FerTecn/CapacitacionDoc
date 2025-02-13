from django.shortcuts import render, render, get_object_or_404, redirect
from django.conf import settings
from datetime import datetime
from catalogos.models import Departamento, Director, Docente, Instructor
from .models import FichaTecnica, RegistroCurso, ValidarCurso
from .forms import ContenidoTematicoFormSet, CriterioEvaluacionFormSet, CursoForm, FichaTecnicaForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from eventos.models import Evento, Inscripcion
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


from io import BytesIO
import os
import re

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
    form = CursoForm(instance=curso)
    return render(request, 'registrocursover.html', {'curso': curso, 'form':form})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_registrocurso', raise_exception=True)
def registrocursoactualizar(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso actualizado correctamente.")
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
        messages.success(request, "Curso eliminado correctamente.")
        return redirect('registrocursolista')  
    return render(request, 'registrocursoeliminar.html', {'curso': curso})

@login_required(login_url='signin')
@permission_required('plancapacitacion.add_registrocurso', raise_exception=True)
def registrocursocrear(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Curso creado correctamente.")
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
    form = CursoForm(instance=curso)
    return render(request, 'validarver.html', {'curso': curso, 'form': form})

@login_required(login_url='signin')
@permission_required('plancapacitacion.change_validarcurso', raise_exception=True)
def aceptar_curso(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    
    # Verificar si ya existe un evento asociado a este curso
    if not Evento.objects.filter(curso=curso).exists():
        curso.aceptado = True
        curso.save()
        messages.success(request, "El curso se ha validado correctamente.")
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
    messages.success(request, "El curso ha sido invalidado.")
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

def fichatecnicacrear(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    ficha, created = FichaTecnica.objects.get_or_create(curso=curso)

    if request.method == 'POST':
        form = FichaTecnicaForm(request.POST, instance=ficha)
        contenido_tematico_formset = ContenidoTematicoFormSet(request.POST, instance=ficha, prefix='contenidos')
        criterio_evaluacion_formset = CriterioEvaluacionFormSet(request.POST, instance=ficha, prefix='criterios')
      

        if form.is_valid() and contenido_tematico_formset.is_valid() and criterio_evaluacion_formset.is_valid():
            ficha = form.save()

            contenido_tematico_formset.save()
            criterio_evaluacion_formset.save()

            messages.success(request, "Se guardó la información de la ficha técnica correctamente.")
            return redirect('fichatecnica')
        else:
            print(f'{form.errors} ')
            print(f'{contenido_tematico_formset.errors} contenido')
            print(f'{criterio_evaluacion_formset.errors} criterio')
            messages.warning(request, "Por favor, corregir los errores en el formulario.")
            
        
    else:
        form = FichaTecnicaForm(instance=ficha)
        contenido_tematico_formset = ContenidoTematicoFormSet(instance=ficha, prefix='contenidos')
        criterio_evaluacion_formset = CriterioEvaluacionFormSet(instance=ficha, prefix='criterios')


    # Renderizar el formulario si no es una solicitud POST
    return render(request, 'fichatecnicacrear.html', {
        'form': form, 
        'contenido_tematico_formset': contenido_tematico_formset, 
        'criterio_evaluacion_formset': criterio_evaluacion_formset,
        'curso': curso,
    })

def procesar_texto(texto):
    # Reemplazar saltos de línea (\n) por <br/>
    texto = texto.replace("\n", "<br/>")
    
    # Reemplazar dobles saltos de línea (\n\n) por un salto de párrafo <p></p>
    texto = re.sub(r'(\n\s*\n)', r'</p><p>', texto)
    
    # Asegurarnos de que el texto comience y termine dentro de <p> tags
    if not texto.startswith('<p>'):
        texto = '<p>' + texto
    if not texto.endswith('</p>'):
        texto = texto + '</p>'

    return texto
def fichatecnicapdf(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    ficha = get_object_or_404(FichaTecnica, curso=curso)
    jefe = get_object_or_404(Director, puesto="Jefe de Desarrollo Académico")

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
    Story.append(Paragraph(f"<b>Nombre del servicio:</b> {ficha.curso.nombre}", style_normal))
    Story.append(Paragraph(f"<b>Instructor(a):</b> {ficha.curso.instructor}", style_normal))
    Story.append(Spacer(1, 12))

    # **1) Introducción**
    Story.append(Paragraph(f"<b>1) Introducción:</b>", style_bold))
    Story.append(Paragraph(procesar_texto(ficha.introduccion), style_normal))
    Story.append(Spacer(1, 12))

    # **2) Justificación**
    Story.append(Paragraph(f"<b>2) Justificación:</b>", style_bold))
    Story.append(Paragraph(procesar_texto(ficha.justificacion), style_normal))
    Story.append(Spacer(1, 12))

    # **3) Objetivo**
    Story.append(Paragraph(f"<b>3) Objetivo:</b>", style_bold))
    Story.append(Paragraph(procesar_texto(ficha.curso.objetivo), style_normal))
    Story.append(Spacer(1, 12))

    # **4) Descripción del Servicio**
    Story.append(Paragraph(f"<b>4) Descripción del Servicio:</b>", style_bold))
    Story.append(Paragraph(f"<b>a. Tipo de Servicio:</b> {ficha.servicio}", style_normal))
    Story.append(Paragraph(f"<b>b. Duración en horas:</b> {ficha.curso.horas}", style_normal))

    # **Tabla de Contenido Temático**
    Story.append(Paragraph("<b>c. Contenido Temático del Curso:</b>", style_bold))
    
    data = [["Temas/Subtemas", "Tiempo Programado", "Actividades de Aprendizaje"]]
    for contenido in ficha.contenidos_tematicos.all():
        data.append([
            Paragraph(str(contenido.tema), style_normal),
            Paragraph(str(contenido.tiempo), style_normal),
            Paragraph(procesar_texto(contenido.actividades), style_normal)
        ])

    crear_tabla(data, [200, 100, 170])
    

    # **4) --> Continuación**
    Story.append(Paragraph(f"<b>d. Elementos didácticos:</b> {ficha.elementosDidacticos}", style_normal))
    Story.append(Paragraph(f"<b>e. Criterios de evaluación:</b>", style_normal))
    Story.append(Spacer(1, 12))

    # ** Tabla Criterios de evaluación
    data = [["No", "Criterio", "Valor", "Instrumento de Evaluación"]]
    for index, criterio in enumerate(ficha.criterios_evaluacion.all(), start=1):
        data.append([
            Paragraph(str(index), style_normal),
            Paragraph(str(criterio.criterio), style_normal), 
            Paragraph(str(criterio.valor), style_normal),
            Paragraph(str(criterio.instrumento), style_normal)
        ])
    
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
        [ficha.curso.instructor, "", f"{jefe.nombre} {jefe.apPaterno} {jefe.apMaterno}"],
        ["Nombre y Firma del Facilitador", "Sello", "Nombre y Firma del\n Jefe de Desarrollo Académico"],
    ]
    table = Table(data, [200, 100, 200])
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ('LINEBELOW', (0,0), (0,0), 1, colors.black),
        ('LINEBELOW', (2,0), (2,0), 1, colors.black),
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

def oficioslista(request):
    departamentos = Departamento.objects.all()
    docentes = None
    departamento_seleccionado = None
    if request.method == "GET" and "departamento_id" in request.GET:
        departamento_id = request.GET.get("departamento_id")
        departamento_seleccionado = get_object_or_404(Departamento, id=departamento_id)
        if departamento_id:
            docentes = Docente.objects.filter(departamento_id=departamento_id)

    return render(request, "oficioslista.html", {"departamentos": departamentos, "docentes": docentes, 'departamento_seleccionado':departamento_seleccionado})

def descargar_oficio(request, docente_id, departamento_id):
    docente = get_object_or_404(Docente, id=docente_id)
    inscripciones = Inscripcion.objects.filter(usuario=docente.user)
    departamento = get_object_or_404(Departamento, id=departamento_id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
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
        alignment=TA_JUSTIFY
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
    logo_path = os.path.join(settings.MEDIA_ROOT, 'docs', 'header.png')  # Ruta del logo
    logo = Image(logo_path, width=366.35, height=50)
    Story.append(logo)
    Story.append(Spacer(1, 50))

    # Encabezado alineado a la derecha
    fecha_actual = datetime.now().date()
    fecha_formateada = format_date(fecha_actual)

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
    oficio = Paragraph("Oficio No. MM-489/2025", style_right)
    asunto = Paragraph('Asunto: COMISIÓN',style_right)
    Story.append(oficio)
    Story.append(Spacer(1, 12))
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

    text = f"Con base en su desarrollo profesional en el desempeño de sus funciones y aunado a su alto sentido de responsabilidad, se le <b>COMISIONA</B> a participar en los siguientes <b>cursos y/o actividades intersemestrales</b>, durante el preiodo comprendido del fecha al decha:"
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
            Paragraph(f"{format_date(inscripcion.evento.fechaInicio)} al {format_date(inscripcion.evento.fechaFin)}", style_normal),
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

def format_date(fecha):
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    
    mes = meses[fecha.strftime("%B")]
    return fecha.strftime(f"%d-{mes}-%Y")
