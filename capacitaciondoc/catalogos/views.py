from datetime import datetime
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Frame, PageTemplate, BaseDocTemplate, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

from .models import (
    ValorCalificacion,
    ExperienciaDocente, 
    ExperienciaLaboral, 
    FormacionAcademica, 
    ParticipacionInstructor)
from .models import (
    Docente, Instructor,
    GradoAcademico, Lugar, Sede, Departamento,
    Dirigido, Genero, PerfilCurso ,Periodo, Director)

from .forms import GradoAcForm, LugarForm, SedeForm, DirectorForm, ValorCalificacionForm
from .forms import (
    AgregarDocenteForm, ActualizarDocenteForm, 
    DepartamentoForm, DirigidoForm, GeneroForm, PerfilcursoForm, PeriodoForm)
from .forms import (
    AñadirInstructorForm, ActualizarInstructorForm, FormacionAcademicaForm,
    ExperienciaLaboralForm, ExperienciaDocenteForm,
    ParticipacionInstructorForm
)
# Create your views here.

#GRADO ACADEMICO
@login_required(login_url='signin')
@permission_required('catalogos.view_gradoacademico', raise_exception=True)
def gradolista(request):
    gradoac = GradoAcademico.objects.all()
    return render(request, 'gradolista.html', {'gradoac': gradoac})

@login_required(login_url='signin')
@permission_required('catalogos.add_gradoacademico', raise_exception=True)
def gradocrear(request):
    if request.method == 'POST':
        form = GradoAcForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grado creado correctamente.")
            return redirect('gradolista') 
    else:
        form = GradoAcForm()

    return render(request, 'gradocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_gradoacademico', raise_exception=True)
def gradover(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    return render(request, 'gradover.html', {'grado': grado})

@login_required(login_url='signin')
@permission_required('catalogos.change_gradoacademico', raise_exception=True)
def gradoactualizar(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    if request.method == 'POST':
        form = GradoAcForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            messages.success(request, "Grado actualizado correctamente.")
            return redirect('gradolista') 
    else:
        form = GradoAcForm(instance=grado)
    return render(request, 'gradoactualizar.html', {'form': form, 'grado': grado})

@login_required(login_url='signin')
@permission_required('catalogos.delete_gradoacademico', raise_exception=True)
def gradoeliminar(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    if request.method == 'POST':
        grado.delete()
        messages.success(request, f"Grado {grado} eliminado correctamente.")
        return redirect('gradolista')  
    return render(request, 'gradoeliminar.html', {'grado': grado})

 #LUGARES

@login_required(login_url='signin')
@permission_required('catalogos.view_lugar', raise_exception=True)
def lugarlista(request):
    Lugares = Lugar.objects.all()
    return render(request, 'lugarlista.html', {'Lugares': Lugares})

@login_required(login_url='signin')
@permission_required('catalogos.add_lugar', raise_exception=True)
def lugarcrear(request):
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lugar creado correctamente.")
            return redirect('lugarlista') 
    else:
        form = LugarForm()

    return render(request, 'lugarcrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_lugar', raise_exception=True)
def lugarver(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    return render(request, 'lugarver.html', {'lugar': lugar})

@login_required(login_url='signin')
@permission_required('catalogos.change_lugar', raise_exception=True)
def lugaractualizar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    if request.method == 'POST':
        form = LugarForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            messages.success(request, "Lugar actualizado correctamente.")
            return redirect('lugarlista') 
    else:
        form = LugarForm(instance=lugar)
    return render(request, 'lugaractualizar.html', {'form': form, 'lugar': lugar})

@login_required(login_url='signin')
@permission_required('catalogos.delete_lugar', raise_exception=True)
def lugareliminar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    if request.method == 'POST':
        lugar.delete()
        messages.success(request, f"Lugar {lugar} eliminado correctamente.")
        return redirect('lugarlista')  
    return render(request, 'lugareliminar.html', {'lugar': lugar})

#SEDES
@login_required(login_url='signin')
@permission_required('catalogos.view_sede', raise_exception=True)
def sedelista(request):
    sedes = Sede.objects.all()
    return render(request, 'sedelista.html', {'sedes': sedes})

@login_required(login_url='signin')
@permission_required('catalogos.add_sede', raise_exception=True)
def sedecrear(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sede creada correctamente.")
            return redirect('sedelista') 
    else:
        form = SedeForm()

    return render(request, 'sedecrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_sede', raise_exception=True)
def sedever(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    return render(request, 'sedever.html', {'sede': sede})

@login_required(login_url='signin')
@permission_required('catalogos.change_sede', raise_exception=True)
def sedeactualizar(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    if request.method == 'POST':
        form = SedeForm(request.POST, instance=sede)
        if form.is_valid():
            form.save()
            messages.success(request, "Sede actualizada correctamente.")
            return redirect('sedelista') 
    else:
        form = SedeForm(instance=sede)
    return render(request, 'sedeactualizar.html', {'form': form, 'sede': sede})

@login_required(login_url='signin')
@permission_required('catalogos.delete_sede', raise_exception=True)
def sedeeliminar(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    if request.method == 'POST':
        sede.delete()
        messages.success(request, f"Sede {sede} eliminada correctamente.")
        return redirect('sedelista')  
    return render(request, 'sedeeliminar.html', {'sede': sede})

#INSTRUCTORES
@login_required(login_url='signin')
@permission_required('catalogos.view_instructor', raise_exception=True)
def instructorlista(request):
    if request.user.rol == 'Instructor': #Si eres Instructor, ves tu registro
        try:
            instructores = Instructor.objects.filter(user=request.user).select_related('user')
        except Instructor.DoesNotExist:
            return HttpResponseForbidden("No tienes un perfil de instructor asociado.")
    else:
        instructores = Instructor.objects.select_related('user')
    
    return render(request, 'instructorlista.html', {'instructores': instructores})

@login_required(login_url='signin')
@permission_required('catalogos.add_instructor', raise_exception=True)
def instructorcrear(request):
    if request.method == 'POST':
        form = AñadirInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructorlista') 
    else:
        form = AñadirInstructorForm()

    return render(request, 'instructorcrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_instructor', raise_exception=True)
def instructorver(request, instructor_id=None):
    if request.user.rol == 'Instructor':
        # Verificar si el registro que intenta acceder es suyo
        instructor = get_object_or_404(Instructor, user=request.user)
    elif request.user.rol == 'Instructor' and instructor.id != instructor_id:
        return HttpResponseForbidden("No tienes permiso para ver este registro.")
    else:
        # Si es otro rol, puede editar cualquier registro si tienes el permiso
        if instructor_id is None:
            return HttpResponseForbidden("No se especificó un instructor para editar.")
        instructor = get_object_or_404(Instructor, id=instructor_id)
    

    # Obtener las relaciones relacionadas con el instructor
    formaciones = instructor.formaciones_academicas.all()  # Formación académica
    experiencias_laborales = instructor.experiencias_laborales.all()  # Experiencia laboral
    experiencias_docentes = instructor.experiencias_docentes.all()  # Experiencia docente
    participaciones = instructor.participaciones_instructor.all()  # Participaciones como instructor

    # Renderizar el template con los datos necesarios
    return render(request, 'instructorver.html', {
        'instructor': instructor,
        'formaciones': formaciones,
        'experiencias_laborales': experiencias_laborales,
        'experiencias_docentes': experiencias_docentes,
        'participaciones': participaciones,
    })

def format_date(fecha_str):
    meses = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    
    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
    mes = meses[fecha_obj.strftime("%B")]
    return fecha_obj.strftime(f"%d-{mes}-%Y")

def calc_row_height(contenido, ancho_columna, style):
    paragraph = Paragraph(contenido, style)
    w, h = paragraph.wrap(ancho_columna, 800)  # Ajusta la altura según el contenido
    return h + 6

def draw_table(data, col_widths, styles):
    processed_data = []
    alturas_filas = []
    
    for fila in data:
        processed_row = []
        altura_maxima = 0
        
        for i, celda in enumerate(fila):
            contenido = str(celda)
            paragraph = Paragraph(contenido, styles['Normal'])
            w, h = paragraph.wrap(col_widths[i], 800)
            processed_row.append(paragraph)
            altura_maxima = max(altura_maxima, h + 6)
        
        processed_data.append(processed_row)
        alturas_filas.append(altura_maxima)
    
    table = Table(processed_data, colWidths=col_widths, rowHeights=alturas_filas)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("VALIGN", (0, 1), (-1, -1), "TOP"),
    ]))
    return table

def generar_cv_pdf(request, instructor_id=None):
    if request.user.rol == 'Instructor':
        # Verificar si el registro que intenta acceder es suyo
        instructor = get_object_or_404(Instructor, user=request.user)
    elif request.user.rol == 'Instructor' and instructor.id != instructor_id:
        return HttpResponseForbidden("No tienes permiso para ver este registro.")
    else:
        # Si es otro rol, puede editar cualquier registro si tienes el permiso
        if instructor_id is None:
            return HttpResponseForbidden("No se especificó un instructor para editar.")
        instructor = get_object_or_404(Instructor, id=instructor_id)
    if not instructor.fechaNac or not instructor.RFC or not instructor.telefono or not instructor.clave:
        messages.warning(request, "Completa tus datos personales antes de generar el CV.")
        return redirect('instructorver', instructor_id=instructor.id)
    
    # Tamaño carta (8.5 x 11 pulgadas)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>CURRICULUM VITAE DEL INSTRUCTOR</b>", styles['Title']))
    story.append(Paragraph("M00-SC-029-A01", styles['Title']))
    
    story.append(Paragraph("<b>1. Datos Personales</b>", styles['Heading2']))
    datos = [
        ("Nombre", f"{instructor.user.last_name_paterno} {instructor.user.last_name_materno} {instructor.user.first_name}"),
        ("Fecha de nacimiento", format_date(f"{instructor.fechaNac}")),
        ("CURP", instructor.user.curp),
        ("RFC", instructor.RFC),
        ("Teléfono", instructor.telefono),
        ("Correo Electrónico", instructor.user.email)
    ]
    for label, value in datos:
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>{label}:</b> {value}", styles['Normal']))

    # **Formaciones académicas**
    story.append(Paragraph("<b>2. Formación Académica</b>", styles['Heading2']))
    data1 = [["Institución", "Titulación", "Cédula Profesional"]]
    for formacion in instructor.formaciones_academicas.all():
        data1.append([formacion.institucion, formacion.grado, formacion.cedulaProf])
    story.append(draw_table(data1, [200, 150, 100], styles))

    # Tabla Experiencias laborales
    story.append(Paragraph("<b>3. Experiencia Laboral</b>", styles['Heading2']))
    data2 = [["No.", "Puesto", "Empresa", "Permanencia"]]
    for index, exp in enumerate(instructor.experiencias_laborales.all(), start=1):
        data2.append([index, exp.puesto, exp.empresa, f"{format_date(str(exp.fecha_inicio))} - {format_date(str(exp.fecha_fin))}"])
    story.append(draw_table(data2, [40, 150, 150, 110], styles))

    # Tabla Experiencias Docencias
    story.append(Paragraph("<b>4. Experiencia en Docencia</b>", styles['Heading2']))
    data3 = [["No.", "Materia", "Periodo"]]
    for index, exp in enumerate(instructor.experiencias_docentes.all(), start=1):
        data3.append([index, exp.materia, exp.periodo])
    story.append(draw_table(data3, [40, 260, 150], styles))
    

    # Tabla Participaicones como instructor
    story.append(Paragraph("<b>5. Participaciones como Instructor</b>", styles['Heading2']))
    data4 = [["No.", "Curso", "Empresa", "Horas", "Fecha"]]
    for index, part in enumerate(instructor.participaciones_instructor.all(), start=1):
        data4.append([index, part.curso, part.nombreEmpresa, part.duracionHoras, f"{format_date(str(part.periodoInicio))} - {format_date(str(part.periodoFin))}"])
    story.append(draw_table(data4, [40, 150, 110, 50, 100], styles))

    doc.build(story)
    
    buffer.seek(0)
    filename = f"CV_{instructor.user.last_name_paterno}_{instructor.user.last_name_materno}_{instructor.user.first_name}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@login_required(login_url='signin')
@permission_required('catalogos.change_instructor', raise_exception=True)
def instructoractualizar(request, instructor_id=None):
    if request.user.rol == 'Instructor':
        # Si es un instructor, solo puede editar su propio registro
        instructor = get_object_or_404(Instructor, user=request.user)
    else:
        # Si es otro rol, puede editar cualquier registro si tienes el permiso
        if instructor_id is None:
            return HttpResponseForbidden("No se especificó un instructor para editar.")
        instructor = get_object_or_404(Instructor, id=instructor_id)

    if request.method == 'POST':
        form = ActualizarInstructorForm(request.POST, instance=instructor, user_instance=instructor.user)
        formacion_form = FormacionAcademicaForm()
        experiencia_laboral_form = ExperienciaLaboralForm()
        experiencia_docente_form = ExperienciaDocenteForm()
        participacion_form = ParticipacionInstructorForm()

        if 'instructor' in request.POST:
            # Actualizar datos del instructor
            form = ActualizarInstructorForm(request.POST, instance=instructor, user_instance=instructor.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Datos del instructor actualizados correctamente.", extra_tags="datos-personales")
                return redirect('instructoractualizar', instructor_id=instructor.id)
            else:
                messages.error(request, "Corrige los errores en el formulario.")

        elif 'formacion_academica' in request.POST:
            # Agregar una formación académica
            formacion_form = FormacionAcademicaForm(request.POST)
            if formacion_form.is_valid():
                nueva_formacion = formacion_form.save(commit=False)
                nueva_formacion.instructor = instructor
                nueva_formacion.save()
                messages.success(request, "Formación académica agregada correctamente.", extra_tags="formacion-academica")
                return redirect(f'{request.path}#formacion-academica')
            else:
                messages.warning(request, "Corrige los errores en el formulario.")
                return redirect(f'{request.path}#formacion-academica')

        elif 'experiencia_laboral' in request.POST:
            # Agregar una experiencia laboral
            experiencia_laboral_form = ExperienciaLaboralForm(request.POST)
            if experiencia_laboral_form.is_valid():
                nueva_experiencia = experiencia_laboral_form.save(commit=False)
                nueva_experiencia.instructor = instructor
                nueva_experiencia.save()
                messages.success(request, "Experiencia laboral agregada correctamente.", extra_tags="experiencia-laboral")
                return redirect(f'{request.path}#experiencia-laboral')
            else:
                return redirect(f'{request.path}#experiencia-laboral')

        elif 'experiencia_docente' in request.POST:
            # Agregar una experiencia docente
            experiencia_docente_form = ExperienciaDocenteForm(request.POST)
            if experiencia_docente_form.is_valid():
                nueva_experiencia_docente = experiencia_docente_form.save(commit=False)
                nueva_experiencia_docente.instructor = instructor
                nueva_experiencia_docente.save()
                messages.success(request, "Experiencia docente agregada correctamente.", extra_tags="experiencia-docente")
                return redirect(f'{request.path}#experiencia-docente')
            else:
                return redirect(f'{request.path}#experiencia-docente')

        elif 'participacion_instructor' in request.POST:
            # Agregar una participación como instructor
            participacion_form = ParticipacionInstructorForm(request.POST)
            if participacion_form.is_valid():
                nueva_participacion = participacion_form.save(commit=False)
                nueva_participacion.instructor = instructor
                nueva_participacion.save()
                messages.success(request, "Participación como instructor agregada correctamente.", extra_tags="participacion-instructor")
                return redirect(f'{request.path}#participacion-instructor')
            else:
                return redirect(f'{request.path}#participacion-instructor')

    else:
        # Formularios iniciales para GET
        form = ActualizarInstructorForm(instance=instructor, user_instance=instructor.user)
        formacion_form = FormacionAcademicaForm()
        experiencia_laboral_form = ExperienciaLaboralForm()
        experiencia_docente_form = ExperienciaDocenteForm()
        participacion_form = ParticipacionInstructorForm()
    
    # Manejar la eliminación
    if 'delete_formacion' in request.GET:
        formacion_id = request.GET.get('delete_formacion')
        formacion = get_object_or_404(FormacionAcademica, id=formacion_id)
        formacion.delete()
        messages.success(request, "Formación académica eliminada correctamente.", extra_tags="formacion-academica")
        return redirect(f'{request.path}#formacion-academica')

    if 'delete_experiencia' in request.GET:
        experiencia_id = request.GET.get('delete_experiencia')
        experiencia = get_object_or_404(ExperienciaLaboral, id=experiencia_id)
        experiencia.delete()
        messages.success(request, "Experiencia laboral eliminada correctamente.", extra_tags="experiencia-laboral")
        return redirect(f'{request.path}#experiencia-laboral')

    if 'delete_experiencia_docente' in request.GET:
        experiencia_docente_id = request.GET.get('delete_experiencia_docente')
        experiencia_docente = get_object_or_404(ExperienciaDocente, id=experiencia_docente_id)
        experiencia_docente.delete()
        messages.success(request, "Experiencia docente eliminada correctamente.", extra_tags="experiencia-docente")
        return redirect(f'{request.path}#experiencia-docente')

    if 'delete_participacion' in request.GET:
        participacion_id = request.GET.get('delete_participacion')
        participacion = get_object_or_404(ParticipacionInstructor, id=participacion_id)
        participacion.delete()
        messages.success(request, "Participación como instructor eliminada correctamente.", extra_tags="participacion-instructor")
        return redirect(f'{request.path}#participacion-instructor')
    
    # Obtener datos relacionados para mostrar en las tablas
    formaciones = instructor.formaciones_academicas.all()
    experiencias_laborales = instructor.experiencias_laborales.all()
    experiencias_docentes = instructor.experiencias_docentes.all()
    participaciones = instructor.participaciones_instructor.all()

    return render(request, 'instructoractualizar.html', {
        'form': form,
        'formacion_form': formacion_form,
        'experiencia_laboral_form': experiencia_laboral_form,
        'experiencia_docente_form': experiencia_docente_form,
        'participacion_form': participacion_form,
        'instructor': instructor,
        'formaciones': formaciones,
        'experiencias_laborales': experiencias_laborales,
        'experiencias_docentes': experiencias_docentes,
        'participaciones': participaciones,
    })

@login_required(login_url='signin')
@permission_required('catalogos.delete_instructor', raise_exception=True)
def instructoreliminar(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructorlista')  
    return render(request, 'instructoreliminar.html', {'instructor': instructor})

#DOCENTES
@login_required(login_url='signin')
@permission_required('catalogos.view_docente', raise_exception=True)
def docentelista(request):
    if request.user.rol == 'Docente':  #Si eres docente solo modificas tu registro
        try:
            docentes = Docente.objects.filter(user=request.user).select_related('user')
        except Docente.DoesNotExist:
            return HttpResponseForbidden("No tienes un perfil de docente asociado.")
    else: #Si eres otro rol con permisos de ver puedes ver todos los docentes de la BD
        docentes = Docente.objects.select_related('user')
    
    return render(request, 'docentelista.html', {'docentes': docentes})

@login_required(login_url='signin')
@permission_required('catalogos.add_docente', raise_exception=True)
def docentecrear(request):
    if request.method == 'POST':
        form = AgregarDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docentelista') 
    else:
        form = AgregarDocenteForm()

    return render(request, 'docentecrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_docente', raise_exception=True)
def docentever(request, docente_id=None):
    if request.user.rol == 'Docente':
        # Verificar si el registro que intenta acceder es suyo
        docente = get_object_or_404(Docente, user=request.user)
    elif request.user.rol == 'Docente' and docente.id != docente_id:
        return HttpResponseForbidden("No tienes permiso para ver este registro.")
    else:
        # Si el usuario tiene otro rol con permisos, puede acceder al registro del instructor indicado
        if docente_id is None:
            return HttpResponseForbidden("No se especificó un docente para editar.")
        docente = get_object_or_404(Docente, id=docente_id)
            
    # Renderizar el template con el docente
    return render(request, 'docentever.html', {'docente': docente})

@login_required(login_url='signin')
@permission_required('catalogos.change_docente', raise_exception=True)
def docenteactualizar(request, docente_id=None):
    if request.user.rol == 'Docente':
        # Si es un docente, solo puede editar su propio registro
        docente = get_object_or_404(Docente, user=request.user)
    else:
        # Si es otro rol puede editar cualquier registro si tienes el permiso
        if docente_id is None:
            return HttpResponseForbidden("No se especificó un docente para editar.")
        docente = get_object_or_404(Docente, id=docente_id)

    if request.method == 'POST':
        form = ActualizarDocenteForm(request.POST, instance=docente, user_instance=docente.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos actualizados correctamente.")
            return redirect('docentelista') 
    else:
        form = ActualizarDocenteForm(instance=docente,  user_instance=docente.user)
    return render(request, 'docenteactualizar.html', {'form': form, 'docente': docente})

@login_required(login_url='signin')
@permission_required('catalogos.delete_docente', raise_exception=True)
def docenteeliminar(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.delete()
        messages.success(request, "Registro eliminado correctamente.")
        return redirect('docentelista')  
    return render(request, 'docenteeliminar.html', {'docente': docente})

#DEPARTAMENTOS
@login_required(login_url='signin')
@permission_required('catalogos.view_departamento', raise_exception=True)
def departamentolista(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentolista.html', {'departamentos': departamentos})

@login_required(login_url='signin')
@permission_required('catalogos.add_departamento', raise_exception=True)
def departamentocrear(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Departamento creado correctamente.")
            return redirect('departamentolista') 
    else:
        form = DepartamentoForm()

    return render(request, 'departamentocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_departamento', raise_exception=True)
def departamentover(request, departamento_id):
    departamento= get_object_or_404(Departamento, id=departamento_id)
    form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentover.html', {'departamento': departamento, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_departamento', raise_exception=True)
def departamentoactualizar(request, departamento_id):
    departamento= get_object_or_404(Departamento, id=departamento_id)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del departamento actualizados correctamente.")
            return redirect('departamentolista') 
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'departamentoactualizar.html', {'form': form, 'departamento': departamento})

@login_required(login_url='signin')
@permission_required('catalogos.delete_departamento', raise_exception=True)
def departamentoeliminar(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    if request.method == 'POST':
        departamento.delete()
        messages.success(request, f"Departamento {departamento} eliminado correctamente.")
        return redirect('departamentolista')  
    return render(request, 'departamentoeliminar.html', {'departamento': departamento})

#DIRIGIDO
@login_required(login_url='signin')
@permission_required('catalogos.view_dirigido', raise_exception=True)
def dirigidolista(request):
    dirigidos = Dirigido.objects.all()
    return render(request, 'dirigidolista.html', {'dirigidos': dirigidos})

@login_required(login_url='signin')
@permission_required('catalogos.add_dirigido', raise_exception=True)
def dirigidocrear(request):
    if request.method == 'POST':
        form = DirigidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dirigido creado correctamente.")
            return redirect('dirigidolista') 
    else:
        form = DirigidoForm()

    return render(request, 'dirigidocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_dirigido', raise_exception=True)
def dirigidover(request, dirigido_id):
    dirigido= get_object_or_404(Dirigido, id=dirigido_id)
    form = DirigidoForm(instance=dirigido)
    return render(request, 'dirigidover.html', {'dirigido': dirigido, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_dirigido', raise_exception=True)
def dirigidoactualizar(request, dirigido_id):
    dirigido= get_object_or_404(Dirigido, id=dirigido_id)
    if request.method == 'POST':
        form = DirigidoForm(request.POST, instance=dirigido)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del dirigido actualizados correctamente.")
            return redirect('dirigidolista') 
    else:
        form = DirigidoForm(instance=dirigido)
    return render(request, 'dirigidoactualizar.html', {'form': form, 'dirigido': dirigido})

@login_required(login_url='signin')
@permission_required('catalogos.delete_dirigido', raise_exception=True)
def dirigidoeliminar(request, dirigido_id):
    dirigido = get_object_or_404(Dirigido, id=dirigido_id)
    if request.method == 'POST':
        dirigido.delete()
        messages.success(request, f"Dirigido {dirigido} eliminado correctamente.")
        return redirect('dirigidolista')  
    return render(request, 'dirigidoeliminar.html', {'dirigido': dirigido})

#GÉNERO
@login_required(login_url='signin')
@permission_required('catalogos.view_genero', raise_exception=True)
def generolista(request):
    generos = Genero.objects.all()
    return render(request, 'generolista.html', {'generos': generos})

@login_required(login_url='signin')
@permission_required('catalogos.add_genero', raise_exception=True)
def generocrear(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Genero creado correctamente.")
            return redirect('generolista') 
    else:
        form = GeneroForm()

    return render(request, 'generocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_genero', raise_exception=True)
def generover(request, genero_id):
    genero= get_object_or_404(Genero, id=genero_id)
    return render(request, 'generover.html', {'genero': genero})

@login_required(login_url='signin')
@permission_required('catalogos.change_genero', raise_exception=True)
def generoactualizar(request, genero_id):
    genero= get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del genero actualizados correctamente.")
            return redirect('generolista') 
    else:
        form = GeneroForm(instance=genero)
    return render(request, 'generoactualizar.html', {'form': form, 'genero': genero})

@login_required(login_url='signin')
@permission_required('catalogos.delete_genero', raise_exception=True)
def generoeliminar(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        genero.delete()
        messages.success(request, f"Genero {genero} eliminado correctamente.")
        return redirect('generolista')  
    return render(request, 'generoeliminar.html', {'genero': genero})

#PERFIL DE CURSO
@login_required(login_url='signin')
@permission_required('catalogos.view_perfilcurso', raise_exception=True)
def perfilcursolista(request):
    perfilcursos = PerfilCurso.objects.all()
    return render(request, 'perfilcursolista.html', {'perfilcursos': perfilcursos})

@login_required(login_url='signin')
@permission_required('catalogos.add_perfilcurso', raise_exception=True)
def perfilcursocrear(request):
    if request.method == 'POST':
        form = PerfilcursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil de curso creado correctamente.")
            return redirect('perfilcursolista') 
    else:
        form = PerfilcursoForm()

    return render(request, 'perfilcursocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_perfilcurso', raise_exception=True)
def perfilcursover(request, perfilCurso_id):
    perfilCurso= get_object_or_404(PerfilCurso, id=perfilCurso_id)
    return render(request, 'perfilcursover.html', {'perfilCurso': perfilCurso})

@login_required(login_url='signin')
@permission_required('catalogos.change_perfilcurso', raise_exception=True)
def perfilcursoactualizar(request, perfilCurso_id):
    perfilCurso= get_object_or_404(PerfilCurso, id=perfilCurso_id)
    if request.method == 'POST':
        form = PerfilcursoForm(request.POST, instance=perfilCurso)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del perfil de curso actualizados correctamente.")
            return redirect('perfilcursolista') 
    else:
        form = PerfilcursoForm(instance=perfilCurso)
    return render(request, 'perfilcursoactualizar.html', {'form': form, 'perfilCurso': perfilCurso})

@login_required(login_url='signin')
@permission_required('catalogos.delete_perfilcurso', raise_exception=True)
def perfilcursoeliminar(request, perfilCurso_id):
    perfilCurso = get_object_or_404(PerfilCurso, id=perfilCurso_id)
    if request.method == 'POST':
        perfilCurso.delete()
        messages.success(request, f"Perfil de curso {perfilCurso} eliminado correctamente.")
        return redirect('perfilcursolista')  
    return render(request, 'perfilcursoeliminar.html', {'perfilCurso': perfilCurso})

#PERIODO
@login_required(login_url='signin')
@permission_required('catalogos.view_periodo', raise_exception=True)
def periodolista(request):
    periodos = Periodo.objects.all()
    return render(request, 'periodolista.html', {'periodos': periodos})

@login_required(login_url='signin')
@permission_required('catalogos.add_periodo', raise_exception=True)
def periodocrear(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Periodo creado correctamente.")
            return redirect('periodolista')
    else:
        form = PeriodoForm()

    return render(request, 'periodocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_periodo', raise_exception=True)
def periodover(request, periodo_id):
    periodo= get_object_or_404(Periodo, id=periodo_id)
    return render(request, 'periodover.html', {'periodo': periodo})

@login_required(login_url='signin')
@permission_required('catalogos.change_periodo', raise_exception=True)
def periodoactualizar(request, periodo_id):
    periodo= get_object_or_404(Periodo, id=periodo_id)
    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del periodo actualizados correctamente.")
            return redirect('periodolista') 
    else:
        form = PeriodoForm(instance=periodo)
    return render(request, 'periodoactualizar.html', {'form': form, 'periodo': periodo})

@login_required(login_url='signin')
@permission_required('catalogos.delete_periodo', raise_exception=True)
def periodoeliminar(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    if request.method == 'POST':
        periodo.delete()
        messages.success(request, f"Periodo {periodo} eliminado correctamente.")
        return redirect('periodolista')  
    return render(request, 'periodoeliminar.html', {'periodo': periodo})

#Director
@login_required(login_url='signin')
@permission_required('catalogos.view_director', raise_exception=True)
def directorlista(request):
    directores = Director.objects.all()
    return render(request, 'directorlista.html', {'directores': directores})

@login_required(login_url='signin')
@permission_required('catalogos.add_director', raise_exception=True)
def directorcrear(request):
    if request.method == 'POST':
        form = DirectorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Autoridad creada correctamente.")
            return redirect('directorlista') 
    else:
        form = DirectorForm()

    return render(request, 'directoragregar.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_director', raise_exception=True)
def directorver(request, director_id):
    director= get_object_or_404(Director, id=director_id)
    form = DirectorForm(instance=director)
    return render(request, 'directorver.html', {'director': director, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_director', raise_exception=True)
def directoractualizar(request, director_id):
    director= get_object_or_404(Director, id=director_id)
    if request.method == 'POST':
        form = DirectorForm(request.POST, instance=director)
        if form.is_valid():
            form.save()
            messages.success(request, "Autoridad actualizada correctamente.")
            return redirect('directorlista')
    else:
        form = DirectorForm(instance=director)
    return render(request, 'directoractualizar.html', {'form': form, 'director': director})

# @login_required(login_url='signin')
# @permission_required('catalogos.delete_director', raise_exception=True)
# def directoreliminar(request, director_id):
#     director = get_object_or_404(Director, id=director_id)
#     if request.method == 'POST':
#         director.delete()
#         return redirect('directorlista')  
#     return render(request, 'directoreliminar.html', {'director': director})

@login_required(login_url='signin')
@permission_required('catalogos.view_valorcalificacion', raise_exception=True)
def valorcalificacionlista(request):
    valores = ValorCalificacion.objects.all()
    return render(request, 'valorcalificacionlista.html', {'valores': valores})

@login_required(login_url='signin')
@permission_required('catalogos.add_valorcalificacion', raise_exception=True)
def valorcalificacioncrear(request):
    if request.method == 'POST':
        form = ValorCalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Valor de calificación creado correctamente.")
            return redirect('valorcalificacionlista') 
    else:
        form = ValorCalificacionForm()

    return render(request, 'valorcalificacionagregar.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_valorcalificacion', raise_exception=True)
def valorcalificacionactualizar(request, valor_id):
    valor = get_object_or_404(ValorCalificacion, id=valor_id)
    if request.method == 'POST':
        form = ValorCalificacionForm(request.POST, instance=valor)
        if form.is_valid():
            form.save()
            messages.success(request, "Valor de calificación actualizado correctamente.")
            return redirect('valorcalificacionlista')
    else:
        form = ValorCalificacionForm(instance=valor)
    return render(request, 'valorcalificacionactualizar.html', {'form': form, 'valor': valor})

@login_required(login_url='signin')
@permission_required('catalogos.delete_valorcalificacion', raise_exception=True)
def valorcalificacioneliminar(request, valor_id):
    valor = get_object_or_404(ValorCalificacion, id=valor_id)
    if request.method == 'POST':
        valor.delete()
        messages.success(request, f"Valor de calificación {valor} eliminado correctamente.")
        return redirect('valorcalificacionlista')  
    return render(request, 'valorcalificacioneliminar.html', {'valor': valor})