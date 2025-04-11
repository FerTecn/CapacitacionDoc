from django.conf import settings
from django.shortcuts import render, render, get_object_or_404, redirect
from catalogos.models import Autoridad, Carrera, Departamento, Instructor
from .models import ActividadAsignatura, ActividadModulosEspecialidad, AsignaturaDeteccionNecesidades, ConcentradoDiagnostico, DeteccionNecesidades, FichaTecnica, RegistroCurso, ValidarCurso
from .forms import ActividadAsignaturaFormSet, ActividadModulosEspecialidadFormSet, AsignaturaDeteccionNecesidadesForm, AsignaturaDeteccionNecesidadesFormSet, ContenidoTematicoFormSet, CriterioEvaluacionFormSet, CursoForm, FichaTecnicaForm
from .utils import cell_text_processor, draw_table_diagnosticos, draw_table_firma, text_processor, draw_table
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from eventos.models import Evento
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, Frame, Image, SimpleDocTemplate, PageTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os
import locale
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

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_fichatecnica', raise_exception=True)
def cursosfichas(request):
    if request.user.rol == "Instructor":
        cursos = RegistroCurso.objects.filter(instructor__user=request.user)
    else:
        cursos = RegistroCurso.objects.all()
    return render(request, 'cursosfichas.html', {'cursos': cursos})

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_fichatecnica', raise_exception=True)
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

@login_required(login_url='signin')
@permission_required('plancapacitacion.add_fichatecnica', raise_exception=True)
def fichatecnicacrear(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    autoridad = get_object_or_404(Autoridad, puesto__cargo_masculino='Jefe de Desarrollo Académico', estatus=True)
    ficha, created = FichaTecnica.objects.get_or_create(curso=curso, jefeDesarrolloAcademico=autoridad)

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

@login_required(login_url='signin')
@permission_required('plancapacitacion.view_fichatecnica', raise_exception=True)
def fichatecnicapdf(request, curso_id):
    curso = get_object_or_404(RegistroCurso, id=curso_id)
    ficha = get_object_or_404(FichaTecnica, curso=curso)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle("Normal", parent=styles["Normal"], leading=14, alignment=TA_JUSTIFY)
    style_center = ParagraphStyle("Center",  parent=style_normal,  alignment=TA_CENTER)
    style_bold = ParagraphStyle("Bold",  parent=style_normal,  fontName="Helvetica-Bold")

    # Lista para almacenar contenido
    Story = []

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

    data = [
        ['1) Introducción', ficha.introduccion],
        ['2) Justificación', ficha.justificacion],
        ['3) Objetivo', ficha.curso.objetivo],
        ['4) Descripción del Servicio', ''],
        ['a) Tipo de servicio', ficha.servicio],
        ['b) Duración en horas del curso', f'{ficha.curso.horas} horas'],
        ['c) Contenido Temático del Curso', ''],
        ['d) Elementos didácticos', ficha.elementosDidacticos],
        ['e) Criterios de evaluación', ''],
        ['5) Competencias a desarrollar', ficha.competencias],
        ['6) Fuentes de información', ficha.fuentes]
    ]
    
    # Introduccion, Justificacion y Objetivo
    for label, value in data[:3]:
        Story.append(Paragraph(f"{label}:", style_bold))
        Story.append(Paragraph(text_processor(value), style_normal))
        Story.append(Spacer(1, 12))
    
    # Descripción del servicio (a, b, c)
    for label, value in data[3:7]:
        Story.append(Paragraph(f"<b>{label}:</b> {text_processor(value)}", style_normal))

    # c) Contenido Temático del Curso (Tabla)
    data_table = [["Temas/Subtemas", "Tiempo Programado\n(Horas)", "Actividades de Aprendizaje"]]
    for contenido in ficha.contenidos_tematicos.all():
        data_table.append([contenido.tema, contenido.tiempo, contenido.actividades])
    Story.append(draw_table(data_table, [200, 100, 170], style_normal))
    Story.append(Spacer(1, 12))

    # **4) --> Continuación de descripción del servicio**
    for label, value in data[7:9]:
        Story.append(Paragraph(f"<b>{label}:</b> {text_processor(value)}", style_normal))

    # **e) Criterios de evaluación (Tabla)**
    data_table = [["No", "Criterio", "Valor", "Instrumento de Evaluación"]]
    for index, criterio in enumerate(ficha.criterios_evaluacion.all(), start=1):
        data_table.append([index, criterio.criterio, criterio.valor, criterio.instrumento])
    Story.append(draw_table(data_table, [30, 180, 60, 200], style_normal))
    Story.append(Spacer(1, 12))

    # Competencias
    for label, value in data[9:10]:
        Story.append(Paragraph(f"{label}:", style_bold))
        Story.append(Paragraph(text_processor(value), style_normal))
        Story.append(Spacer(1, 12))

    # Funetes de informacion
    for label, value in data[10:]:
        Story.append(Paragraph(f"{label}:", style_bold))
        Story.append(Paragraph(cell_text_processor(value), style_normal))
        Story.append(Spacer(1, 12))

    # **Firmas y Sello (agregados al final)**
    Story.append(Spacer(1, 100))
    data_table = [
        [ficha.curso.instructor, "", f"{ficha.jefeDesarrolloAcademico.get_full_name()}"],
        ["Nombre y Firma del Facilitador", "Sello", f"Nombre y Firma {'de la' if ficha.jefeDesarrolloAcademico.genero.genero == 'Femenino' else 'del'}\n {ficha.jefeDesarrolloAcademico.get_puesto()}"],
    ]
    table = Table(data_table, [200, 100, 200])
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

def diagnosticonecesidadesdepartamentoslista(request):
    departamentos = Departamento.objects.all()
    return render(request, 'diagnosticodepartamentoslista.html', {'departamentos': departamentos})

def diagnosticonecesidadescrear(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    jefeDepAcademico = Autoridad.objects.filter(puesto__cargo_masculino = "Jefe de Departamento Académico", estatus = True).first()
    presidenteAcademia = Autoridad.objects.filter(puesto__cargo_masculino = "Presidente de Academia", estatus = True).first()
    instructores = Instructor.objects.all()

    if request.method == 'POST':
        diagnostico, created = DeteccionNecesidades.objects.get_or_create(departamento=departamento, jefeDepAcademico=jefeDepAcademico, presidenteAcademia=presidenteAcademia)
        form_set = AsignaturaDeteccionNecesidadesFormSet(request.POST, instance=diagnostico, prefix='diagnosticonecesidades')
        if form_set.is_valid():
            form_set.save()
            messages.success(request, "Datos de la diagnostico de necesidades actualizados correctamente.")
            return redirect('diagnosticodepartamentoslista')

        else:
            print(form_set.errors)

    else:
        form_set = AsignaturaDeteccionNecesidadesFormSet(prefix='diagnosticonecesidades')

    return render(request, 'diagnosticonecesidadescrear.html', {
        'form_set': form_set, 
        'departamento': departamento, 
        'jefeDepAcademico': jefeDepAcademico, 
        'presidenteAcademia': presidenteAcademia,
        'instructores': instructores
        })

def diagnosticonecesidadesactualizar(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    diagnostico = DeteccionNecesidades.objects.filter(departamento=departamento).first()
    instructores = Instructor.objects.all()

    if request.method == 'POST':
        form_set = AsignaturaDeteccionNecesidadesFormSet(request.POST, instance=diagnostico, prefix='diagnosticonecesidades')
        if form_set.is_valid():
            form_set.save()
            messages.success(request, "Datos de la diagnostico de necesidades actualizados correctamente.")
            return redirect('diagnosticodepartamentoslista')

    else:
        form_set = AsignaturaDeteccionNecesidadesFormSet(instance=diagnostico, prefix='diagnosticonecesidades')

    return render(request, 'diagnosticonecesidadesactualizar.html', {'form_set': form_set, 'diagnostico': diagnostico, 'instructores': instructores})

def concentradonecesidadescrear(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    jefeDepAcademico = Autoridad.objects.filter(puesto__cargo_masculino = "Jefe de Departamento Académico", estatus = True).first()
    presidenteAcademia = Autoridad.objects.filter(puesto__cargo_masculino = "Presidente de Academia", estatus = True).first()
    carreras = Carrera.objects.all()
    
    if request.method == 'POST':
        concentrado, created = ConcentradoDiagnostico.objects.get_or_create(departamento=departamento, jefeDepAcademico=jefeDepAcademico, presidenteAcademia=presidenteAcademia)
        asignatura_formset = ActividadAsignaturaFormSet(request.POST, instance=concentrado, prefix='actividadasignatura')
        modulos_esp_formset = ActividadModulosEspecialidadFormSet(request.POST, instance=concentrado, prefix='actividadmodulosesp')
        if asignatura_formset.is_valid() and modulos_esp_formset.is_valid():
            asignatura_formset.save()
            modulos_esp_formset.save()
            messages.success(request, "Datos del concentrado de necesidades actualizados correctamente.")
            return redirect('diagnosticodepartamentoslista')
        else:
            print(f'{asignatura_formset.errors} asignatura')
            print(f'{modulos_esp_formset.errors} modulos')
    else:
        asignatura_formset = ActividadAsignaturaFormSet(prefix='actividadasignatura')
        modulos_esp_formset = ActividadModulosEspecialidadFormSet(prefix='actividadmodulosesp')
    return render(request, 'concentradonecesidadescrear.html', {
        'departamento': departamento,
        'jefeDepAcademico': jefeDepAcademico,
        'presidenteAcademia': presidenteAcademia,
        'asignatura_formset': asignatura_formset,
        'modulos_esp_formset': modulos_esp_formset,
        'carreras': carreras,
        })

def concentradonecesidadesactualizar(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    concentrado = ConcentradoDiagnostico.objects.filter(departamento=departamento).first()
    carreras = Carrera.objects.all()

    if request.method == 'POST':
        asignatura_formset = ActividadAsignaturaFormSet(request.POST, instance=concentrado, prefix='actividadasignatura')
        modulos_esp_formset = ActividadModulosEspecialidadFormSet(request.POST, instance=concentrado, prefix='actividadmodulosesp')
        if asignatura_formset.is_valid() and modulos_esp_formset.is_valid():
            asignatura_formset.save()
            modulos_esp_formset.save()
            messages.success(request, "Datos del concentrado de necesidades actualizados correctamente.")
            return redirect('diagnosticodepartamentoslista')
    else:
        asignatura_formset = ActividadAsignaturaFormSet(instance=concentrado, prefix='actividadasignatura')
        modulos_esp_formset = ActividadModulosEspecialidadFormSet(instance=concentrado, prefix='actividadmodulosesp')
    return render(request, 'concentradonecesidadesactualizar.html', {
        'concentrado': concentrado,
        'carreras': carreras,
        'asignatura_formset': asignatura_formset,
        'modulos_esp_formset': modulos_esp_formset,
        })

def pdfdiagnostico(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    diagnostico = DeteccionNecesidades.objects.filter(departamento=departamento_id).first()
    asignaturas = diagnostico.asignaturadeteccionnecesidades_set.all()

    concentrado = ConcentradoDiagnostico.objects.filter(departamento=departamento).first()
    actividades_asignatura = concentrado.actividadasignatura_set.all()
    actividades_modulos_esp = concentrado.actividadmodulosespecialidad_set.all()
    
    

    locale.setlocale(locale.LC_TIME, 'spanish')
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer, pagesize=letter,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    font_path_regular = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Montserrat-Regular.ttf')
    font_path_bold = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Montserrat-Bold.ttf')

    if os.path.exists(font_path_regular):
        pdfmetrics.registerFont(TTFont('Montserrat-Regular', font_path_regular))

    if os.path.exists(font_path_bold):
        pdfmetrics.registerFont(TTFont('Montserrat-Bold', font_path_bold))
    
    pdfmetrics.registerFontFamily(
        'Montserrat-Regular',
        normal='Montserrat-Regular',
        bold='Montserrat-Bold'
    )
    
    styles = getSampleStyleSheet()

    style_normal = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Regular', 
        allowHtml=True,
        fontSize=8,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    )

    style_normal_center = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Regular', 
        fontSize=8,
        spaceAfter=8,
        alignment=TA_CENTER,
    )

    style_normal_left = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Regular', 
        fontSize=8,
        spaceAfter=8,
    )
    
    style_bold = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Bold', 
        fontSize=8,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
    )

    style_bold_center = ParagraphStyle(
        'MontserratNormal',
        parent=styles['Normal'],
        fontName='Montserrat-Bold', 
        fontSize=8,
        spaceAfter=8,
        alignment=TA_CENTER,
    )

    # Lista para almacenar contenido
    Story = []

    def header(canvas, doc):
        page_number = f"Página: {canvas.getPageNumber()}"
        
        # Celdas con contenido dinámico
        documento = Paragraph("Nombre del documento: Formato para el diagnóstico de Necesidades de Formación y Actualización Docente y Profesional", style_bold)
        revision = Paragraph("Revisión: 0", style_bold)
        referencia = Paragraph("Referencia: ITAPI-AD-PO-003-02", style_bold)
        codigo = Paragraph("Código: ITAPI-AD-PO-003-02", style_bold)
        pagina = Paragraph(page_number, style_bold)
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_docs.png')

        if os.path.exists(logo_path):
            logo = Image(logo_path, width=3.6 * cm, height=2*cm)
        else:
            logo = "Imagen no existe"

        encabezado = [
            [logo, documento, codigo],
            ['', '', revision],
            ['', referencia, pagina],
        ]

        tabla_encabezado = Table(encabezado, colWidths=[100, 280, 120])
        tabla_encabezado.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, 0), "CENTER"),
            ("ALIGN", (1, 0), (1, 1), "CENTER"),
            ("ALIGN", (2, 0), (2, 2), "RIGHT"),
            ("SPAN", (0, 0), (0, 2)),
            ("SPAN", (1, 0), (1, 1)),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        # Dibuja el encabezado
        tabla_encabezado.wrapOn(canvas, doc.width, doc.topMargin)
        tabla_encabezado.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - tabla_encabezado._height)

    def pie_pagina(canvas, doc):
        footer_path = os.path.join(settings.BASE_DIR, 'static/img/logo_sidebar_ita.png')
        if os.path.exists(footer_path):
            img_width = 3.7 * cm  # Ajusta esto al tamaño real que deseas
            img_height = 2 * cm

            # Posición: esquina inferior derecha
            x = doc.pagesize[0] - doc.rightMargin - img_width
            y = doc.bottomMargin - 0.5 * cm  

            canvas.drawImage(footer_path, x, y, width=img_width, height=img_height, preserveAspectRatio=True, mask='auto')
        else:
            canvas.drawString(2 * cm, 2 * cm, "Pie de página no encontrado")

    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 3 * cm, id='normal')

    # Crear una plantilla de página con encabezado y pie de página
    plantilla = PageTemplate(id='plantilla', frames=frame, onPage=header, onPageEnd=pie_pagina)
    doc.addPageTemplates([plantilla])

    titulo = Paragraph("INSTITUTO TÉCNICO DE APIZACO", style_bold_center)
    subtitulo = Paragraph("Departamento de Desarrollo Académico", style_bold_center)

    Story.append(titulo)
    Story.append(Spacer(1, -10))
    Story.append(subtitulo)

    

    documento = Paragraph("DIAGNÓSTICO DE NECIDADES DE FORMACIÓN Y ACTUALIZACIÓN DOCENTE Y PROFESIONAL", style_bold_center)
    Story.append(documento)

    Story.append(Spacer(1, 12))

    Story.append(Paragraph(f"<b>Departamento:</b> {departamento.departamento}", style_normal))
    Story.append(Spacer(1, -8))
    Story.append(Paragraph(f"<b>Fecha de realización del diagnóstico:</b> {diagnostico.fecha.strftime('%d de %B del %Y')}", style_normal))
    Story.append(Spacer(1, 12))

    firma_jefe = [
        [Paragraph(request.user.get_user_full_name(), style_normal_center),''],
        [Paragraph('Jefe(a) del Departamento Académico', style_bold), Paragraph('Firma', style_bold_center)],
    ]

    firma_presidente = [
        [Paragraph(request.user.get_user_full_name(), style_normal_center),''],
        [Paragraph('Presidente de Academia', style_bold), Paragraph('Firma', style_bold_center)],
    ]
    
    Story.append(draw_table_firma(firma_jefe, [doc.width / 2, doc.width / 2]))
    Story.append(Spacer(1, 12))
    Story.append(draw_table_firma(firma_presidente, [doc.width / 2, doc.width / 2]))

    Story.append(Spacer(1, 20))

    text = Paragraph("a)  PRIORIZAR LAS ASIGNATURAS EN LAS QUE REQUIERA LA FORMACIÓN O ACTUALIZACIÓN DE LOS Y LAS PROFESOR(AS) EN LOS MÓDULOS DE ESPECIALIDAD, AVALADOS POR LA ACADEMIA.", style_bold)
    Story.append(text)

    table = [
        ["Asignaturas en las que se requiere", "Contenidos Temáticos", "No. Profesores", "Periodo", "Facilitadores(as)"],
    ]

    for data in asignaturas:
        instructores = ", ".join([str(instructor) for instructor in data.instructores.all()])
        table.append([data.asignatura, data.contenido, str(data.noProfesores), f'{data.periodoInicio.strftime("%d de %B del %Y")} - {data.periodoFin.strftime("%d de %B del %Y")}', instructores])

    Story.append(draw_table_diagnosticos(table, [100, 140, 60, 100, 100], style_bold_center, style_normal_left))
    # Agregar salto de página si es necesario
    Story.append(PageBreak())

    titulo2 = "INSTITUTO TÉCNICO DE APIZACO"
    subtitulo2 = "Departamento de Desarrollo Académico"
    Story.append(Paragraph(titulo2, style_bold_center))
    Story.append(Spacer(1, -10))
    Story.append(Paragraph(subtitulo2, style_bold_center))

    documento2 = "CONCENTRADO DEL DIAGNÓSTICO DE NECESIDADES DE FORMACIÓN Y ACTUALIZACIÓN DOCENTE Y PROFESIONAL"
    Story.append(Paragraph(documento2, style_bold_center))

    Story.append(Spacer(1, 12))

    Story.append(Paragraph(f"<b>Departamento:</b> {departamento.departamento}", style_normal))
    Story.append(Spacer(1, -8))
    Story.append(Paragraph(f"<b>Fecha de realización del diagnóstico:</b> {diagnostico.fecha.strftime('%d de %B del %Y')}", style_normal))
    Story.append(Spacer(1, 12))

    firma_jefe2 = [
        [Paragraph(request.user.get_user_full_name(), style_normal_center),''],
        [Paragraph('Jefe(a) del Departamento Académico', style_bold), Paragraph('Firma', style_bold_center)],
    ]

    firma_presidente2 = [
        [Paragraph(request.user.get_user_full_name(), style_normal_center),''],
        [Paragraph('Presidente de Academia', style_bold), Paragraph('Firma', style_bold_center)],
    ]
    
    Story.append(draw_table_firma(firma_jefe2, [doc.width / 2, doc.width / 2]))
    Story.append(Spacer(1, 12))
    Story.append(draw_table_firma(firma_presidente2, [doc.width / 2, doc.width / 2]))

    Story.append(Spacer(1, 20))

    Story.append(Paragraph("a)	ACTIVIDADES O EVENTOS  QUE SE LLEVARÁN A CABO PARA LA FORMACIÓN Y ACTUALIZACIÓN DOCENTE (CONTENIDOS TEMÁTICOS DE LAS ASIGNATURAS)", style_bold))

    table2 = [
        ["Actividad o evento", "Tipo", "No. Profesores", "Fecha en la que se realizará la actividad"],
    ]

    for actividad in actividades_asignatura:
        table2.append([actividad.actividad, actividad.tipo, str(actividad.noProfesores), actividad.mes_anio()])
    
    Story.append(draw_table_diagnosticos(table2, [200, 100, 100, 100], style_bold_center, style_normal_left))
    Story.append(Spacer(1, 20))

    Story.append(Paragraph("b)	ACTIVIDADES O EVENTOS QUE SE LLEVARÁN A CABO PARA LA FORMACIÓN Y ACTUALIZACIÓN PROFESIONAL (MÓDULOS DE ESPECIALIDAD)", style_bold))

    table3 = [
        ["Actividad o evento", "Tipo", "Carrera(s) atendida(s)", "No. Profesores", "Fecha en la que se realizará la actividad"],
    ]

    for actividad in actividades_modulos_esp:
        carreras = "\n ".join([str(carrera) for carrera in actividad.carreras.all()])
        table3.append([actividad.actividad, actividad.tipo, carreras, str(actividad.noProfesores), actividad.mes_anio()])
    
    
    Story.append(draw_table_diagnosticos(table3, [120, 80, 120, 80, 100], style_bold_center, style_normal_left))
    Story.append(Spacer(1, 20))


    # Generar PDF
    doc.build(Story)

    buffer.seek(0)
    filename = f"Hola.pdf"
    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response