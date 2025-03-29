from django.shortcuts import render, render, get_object_or_404, redirect
from catalogos.models import Autoridad
from .models import FichaTecnica, RegistroCurso, ValidarCurso
from .forms import ContenidoTematicoFormSet, CriterioEvaluacionFormSet, CursoForm, FichaTecnicaForm
from .utils import cell_text_processor, text_processor, draw_table
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from eventos.models import Evento
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
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