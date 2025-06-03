import locale
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
import os
from django.conf import settings

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from catalogos.forms import AñadirInstructorForm
from catalogos.models import Instructor
from usuarios.models import CustomUser

from io import BytesIO
from .utils import draw_table

from .models import (
    CargoAutoridad,
    FormatoConstancia,
    FormatoDepartamento,
    ValorCalificacion,
    ExperienciaDocente, 
    ExperienciaLaboral, 
    FormacionAcademica, 
    ParticipacionInstructor, 
    Carrera)
from .models import (
    Docente, Instructor,
    GradoAcademico, Lugar, Sede, Departamento,
    Dirigido, Genero, PerfilCurso ,Periodo, Autoridad)

from .forms import CargoAutoridadForm, FormatoConstanciaForm, FormatoConstanciaUpdateForm, FormatoDepartamentoForm, FormatoDepartamentoUpdateForm, GradoAcForm, LugarForm, SedeForm, AutoridadForm, ValorCalificacionForm
from .forms import (
    AgregarDocenteForm, ActualizarDocenteForm, 
    DepartamentoForm, DirigidoForm, GeneroForm, PerfilcursoForm, PeriodoForm)
from .forms import (
    AñadirInstructorForm, ActualizarInstructorForm, FormacionAcademicaForm,
    ExperienciaLaboralForm, ExperienciaDocenteForm,
    ParticipacionInstructorForm, CarreraForm
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
def instructorlista(request):
    if request.user.rol == 'Instructor':
        try:
            instructor = Instructor.objects.get(user=request.user)
        except Instructor.DoesNotExist:
            return HttpResponseForbidden("No tienes un perfil de instructor asociado.")

        # Solo ese instructor se ve a sí mismo
        return render(request, 'instructorlista.html', {'instructores': [instructor]})

    # Para los demás (jefes, etc.)
    if not request.user.has_perm('catalogos.view_instructor'):
        return HttpResponseForbidden("No tienes permiso para ver la lista de instructores.")

    instructores = Instructor.objects.select_related('user')
    return render(request, 'instructorlista.html', {'instructores': instructores})


@login_required(login_url='signin')
@permission_required('catalogos.add_instructor', raise_exception=True)
def instructorcrear(request):
    if request.method == 'POST':
        form = AñadirInstructorForm(request.POST)
        if form.is_valid():
            # Crear el usuario con los campos básicos
            curp = form.cleaned_data['curp']
            user = CustomUser.objects.create_user(
                username=curp,
                curp=curp,
                first_name=form.cleaned_data['first_name'],
                last_name_paterno=form.cleaned_data['last_name_paterno'],
                last_name_materno=form.cleaned_data['last_name_materno'],
                password='Temporal123.',
                rol='Instructor',
            )

            # Crear el instructor con clave temporal y otros campos en null o vacíos
            Instructor.objects.create(
                user=user,
                clave=None,  
                fechaNac=None,
                RFC=None,
                telefono=None
            )

            return redirect('instructorlista')
    else:
        form = AñadirInstructorForm()

    return render(request, 'instructorcrear.html', {'form': form})


@login_required(login_url='signin')
#@permission_required('catalogos.view_instructor', raise_exception=True)
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

@login_required(login_url='signin')
#@permission_required('catalogos.view_instructor', raise_exception=True)
def generar_cv_pdf(request, instructor_id=None):
    locale.setlocale(locale.LC_TIME, 'spanish')  # Establecer la localización para formatear la fecha a español
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
        ("Nombre", instructor.user.get_user_full_name()),
        ("Fecha de nacimiento", instructor.fechaNac.strftime('%d de %B de %Y')),
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
    story.append(draw_table(data1, [200, 150, 150], styles))

    # Tabla Experiencias laborales
    story.append(Paragraph("<b>3. Experiencia Laboral</b>", styles['Heading2']))
    data2 = [["No.", "Puesto", "Empresa", "Permanencia"]]
    for index, exp in enumerate(instructor.experiencias_laborales.all(), start=1):
        data2.append([
            index, 
            exp.puesto, 
            exp.empresa, 
            f"{exp.fecha_inicio.strftime('%d de %B de %Y')} - <br/> {exp.fecha_fin.strftime('%d de %B de %Y')}"
        ])
    story.append(draw_table(data2, [50, 150, 150, 150], styles))

    # Tabla Experiencias Docencias
    story.append(Paragraph("<b>4. Experiencia en Docencia</b>", styles['Heading2']))
    data3 = [["No.", "Materia", "Periodo"]]
    for index, exp in enumerate(instructor.experiencias_docentes.all(), start=1):
        data3.append([index, exp.materia, exp.periodo])
    story.append(draw_table(data3, [50, 300, 150], styles))
    

    # Tabla Participaicones como instructor
    story.append(Paragraph("<b>5. Participaciones como Instructor</b>", styles['Heading2']))
    data4 = [["No.", "Curso", "Empresa", "Horas", "Fecha"]]
    for index, part in enumerate(instructor.participaciones_instructor.all(), start=1):
        data4.append([
            index, 
            part.curso, 
            part.nombreEmpresa, 
            part.duracionHoras, 
            f"{part.periodoInicio.strftime('%d de %B de %Y')} -<br/> {part.periodoFin.strftime('%d de %B de %Y')}"])
    story.append(draw_table(data4, [40, 170, 120, 50, 130], styles))

    doc.build(story)
    
    buffer.seek(0)
    filename = f"CV_{instructor.user.get_user_full_name().replace(' ', '_')}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response

@login_required(login_url='signin')
#@permission_required('catalogos.change_instructor', raise_exception=True)
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

#Autoridad
@login_required(login_url='signin')
@permission_required('catalogos.view_autoridad', raise_exception=True)
def autoridadlista(request):
    autoridades = Autoridad.objects.all()
    return render(request, 'autoridadlista.html', {'autoridades': autoridades})

@login_required(login_url='signin')
@permission_required('catalogos.add_autoridad', raise_exception=True)
def autoridadcrear(request):
    if request.method == 'POST':
        form = AutoridadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Autoridad creada correctamente.")
            return redirect('autoridadlista') 
    else:
        form = AutoridadForm()

    return render(request, 'autoridadagregar.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_autoridad', raise_exception=True)
def autoridadver(request, autoridad_id):
    autoridad= get_object_or_404(Autoridad, id=autoridad_id)
    form = AutoridadForm(instance=autoridad)
    return render(request, 'autoridadver.html', {'autoridad': autoridad, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_autoridad', raise_exception=True)
def autoridadactualizar(request, autoridad_id):
    autoridad= get_object_or_404(Autoridad, id=autoridad_id)
    if request.method == 'POST':
        form = AutoridadForm(request.POST, request.FILES, instance=autoridad)
        if form.is_valid():
            form.save()
            messages.success(request, "Autoridad actualizada correctamente.")
            return redirect('autoridadlista')
    else:
        form = AutoridadForm(instance=autoridad)
    return render(request, 'autoridadactualizar.html', {'form': form, 'autoridad': autoridad})

# @login_required(login_url='signin')
# @permission_required('catalogos.delete_autoridad', raise_exception=True)
# def autoridadeliminar(request, autoridad_id):
#     autoridad = get_object_or_404(Autoridad, id=autoridad_id)
#     if request.method == 'POST':
#         autoridad.delete()
#         return redirect('autoridadlista')  
#     return render(request, 'autoridadeliminar.html', {'autoridad': autoridad})

@login_required(login_url='signin')
@permission_required('catalogos.view_cargoautoridad', raise_exception=True)
def cargoautoridadlista(request):
    cargos = CargoAutoridad.objects.all()
    return render(request, 'cargoautoridadlista.html', {'cargos': cargos})

@login_required(login_url='signin')
@permission_required('catalogos.add_cargoautoridad', raise_exception=True)
def cargoautoridadcrear(request):
    if request.method == 'POST':
        form = CargoAutoridadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo de autoridad creado correctamente.")
            return redirect('cargoautoridadlista') 
    else:
        form = CargoAutoridadForm()

    return render(request, 'cargoautoridadagregar.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_cargoautoridad', raise_exception=True)
def cargoautoridadver(request, cargo_id):
    cargo= get_object_or_404(CargoAutoridad, id=cargo_id)
    form = CargoAutoridadForm(instance=cargo)
    return render(request, 'cargoautoridadver.html', {'cargo': cargo, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_cargoautoridad', raise_exception=True)
def cargoautoridadactualizar(request, cargo_id):
    cargo= get_object_or_404(CargoAutoridad, id=cargo_id)
    if request.method == 'POST':
        form = CargoAutoridadForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, "Cargo de autoridad actualizado correctamente.")
            return redirect('cargoautoridadlista')
    else:
        form = CargoAutoridadForm(instance=cargo)
    return render(request, 'cargoautoridadactualizar.html', {'form': form, 'cargo': cargo})

@login_required(login_url='signin')
@permission_required('catalogos.delete_cargoautoridad', raise_exception=True)
def cargoautoridadeliminar(request, cargo_id):
    cargo = get_object_or_404(CargoAutoridad, id=cargo_id)
    if request.method == 'POST':
        cargo.delete()
        return redirect('cargoautoridadlista')  
    return render(request, 'cargoautoridadeliminar.html', {'cargo': cargo})

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

@login_required(login_url='signin')
@permission_required('catalogos.view_formatodepartamento', raise_exception=True)
def formatoslista(request):
    formatosdepartamentos = FormatoDepartamento.objects.all().order_by('departamento', '-year')
    formatosconstancias = FormatoConstancia.objects.all().order_by('-year')

    return render(request, 'formatoslista.html', {
        'formatosdepartamentos': formatosdepartamentos, 
        'formatosconstancias': formatosconstancias
        })

@login_required(login_url='signin')
@permission_required('catalogos.add_formatodepartamento', raise_exception=True)
def formatodepartamentocrear(request):
    if request.method == 'POST':
        form = FormatoDepartamentoForm(request.POST, request.FILES)
        if form.is_valid():
            departamento = form.cleaned_data.get('departamento')
            year = form.cleaned_data.get('year')

            # Verificar si ya existe un formato con el mismo departamento y año
            if FormatoDepartamento.objects.filter(departamento=departamento, year=year).exists():
                messages.warning(request, "Ya existe un formato para este departamento y año.")
                return render(request, 'formatodepartamentocrear.html', {'form': form})
            
            form.save()
            messages.success(request, f"Formato de { form.instance.departamento }-{form.instance.year} creado correctamente.")
            return redirect('formatoslista') 
    else:
        form = FormatoDepartamentoForm()

    return render(request, 'formatodepartamentocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_formatodepartamento', raise_exception=True)
def formatodepartamentover(request, formato_id):
    formato = get_object_or_404(FormatoDepartamento, id=formato_id)
    form = FormatoDepartamentoForm(instance=formato)
    return render(request, 'formatodepartamentover.html', {'formato': formato, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_formatodepartamento', raise_exception=True)
def formatodepartamentoactualizar(request, formato_id):
    formato = get_object_or_404(FormatoDepartamento, id=formato_id)
    if request.method == 'POST':
        form = FormatoDepartamentoUpdateForm(request.POST, request.FILES, instance=formato)

        if form.is_valid():
            form.save()
            messages.success(request, "Formato actualizado correctamente.")
            return redirect('formatoslista')
        else:
            print(form.errors)
    else:
        form = FormatoDepartamentoForm(instance=formato)
    return render(request, 'formatodepartamentoactualizar.html', {'form': form, 'formato': formato})

@login_required(login_url='signin')
@permission_required('catalogos.delete_formatodepartamento', raise_exception=True)
def eliminar_imagen_departamento(request, tipo_imagen, formato_id):
    formato = get_object_or_404(FormatoDepartamento, id=formato_id)

    if tipo_imagen == 'header':
        formato.header.delete(save=False)
        formato.header = None
        mensaje = "Header eliminado correctamente."
    elif tipo_imagen == 'footer':
        formato.footer.delete(save=False)
        formato.footer = None
        mensaje = "Footer eliminado correctamente."
    else:
        messages.error(request, "Tipo de imagen no válido.")
        return redirect('formatoslista')

    formato.save()
    messages.success(request, mensaje)
    return redirect('formatodepartamentoactualizar', formato_id=formato.id)

@login_required(login_url='signin')
@permission_required('catalogos.add_formatoconstancia', raise_exception=True)
def formatoconstanciacrear(request):
    if request.method == 'POST':
        form = FormatoConstanciaForm(request.POST, request.FILES)
        if form.is_valid():
            year = form.cleaned_data.get('year')

            # Verificar si ya existe un formato con el mismo departamento y año
            if FormatoConstancia.objects.filter(year=year).exists():
                messages.warning(request, "Ya existe un formato para este año.")
                return render(request, 'formatoconstanciacrear.html', {'form': form})
            
            form.save()
            messages.success(request, "Formato creado correctamente.")
            return redirect('formatoslista') 
    else:
        form = FormatoConstanciaForm()

    return render(request, 'formatoconstanciacrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_formatoconstancia', raise_exception=True)
def formatoconstanciaver(request, formato_id):
    formato = get_object_or_404(FormatoConstancia, id=formato_id)
    form = FormatoConstanciaForm(instance=formato)
    return render(request, 'formatoconstanciaver.html', {'formato': formato, 'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.change_formatoconstancia', raise_exception=True)
def formatoconstanciaactualizar(request, formato_id):
    formato = get_object_or_404(FormatoConstancia, id=formato_id)
    if request.method == 'POST':
        form = FormatoConstanciaUpdateForm(request.POST, request.FILES, instance=formato)

        if form.is_valid():
            form.save()
            messages.success(request, "Formato actualizado correctamente.")
            return redirect('formatoslista')
        else:
            print(form.errors)
    else:
        form = FormatoConstanciaForm(instance=formato)
    return render(request, 'formatoconstanciaactualizar.html', {'form': form, 'formato': formato, 'año': formato.year,})

@login_required(login_url='signin')
@permission_required('catalogos.delete_formatoconstancia', raise_exception=True)
def eliminar_imagen_constancia(request, tipo_imagen, año):
    formato = get_object_or_404(FormatoConstancia, year=año)

    if tipo_imagen == 'header':
        formato.header.delete()
        formato.header = None
        mensaje = "Header eliminado correctamente."
    elif tipo_imagen == 'footer':
        formato.footer.delete()
        formato.footer = None
        mensaje = "Footer eliminado correctamente."
    elif tipo_imagen == 'fondo':
        formato.fondo.delete()
        formato.fondo = None
        mensaje = "Fondo eliminado correctamente."
    elif tipo_imagen == 'margend':
        formato.margend.delete()
        formato.margend = None
        mensaje = "Margen derecho eliminado correctamente."
    else:
        messages.error(request, "Tipo de imagen no válido.")
        return redirect('formatoslista')

    formato.save()
    messages.success(request, mensaje)

    # 🔁 Redirige correctamente con el formato_id
    return redirect('formatoconstanciaactualizar', formato_id=formato.id)

#CARRERAS
@login_required(login_url='signin')
@permission_required('catalogos.view_carrera', raise_exception=True)
def carreralista(request):
    carreras = Carrera.objects.all()
    return render(request, 'carreralista.html', {'carreras': carreras})

@login_required(login_url='signin')
@permission_required('catalogos.add_carrera', raise_exception=True)
def carreracrear(request):
    if request.method == 'POST':
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrera creada correctamente.")
            return redirect('carreralista') 
    else:
        form = CarreraForm()

    return render(request, 'carreracrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('catalogos.view_carrera', raise_exception=True)
def carreraver(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    return render(request, 'carreraver.html', {'carrera': carrera})

@login_required(login_url='signin')
@permission_required('catalogos.change_carrera', raise_exception=True)
def carreraactualizar(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    if request.method == 'POST':
        form = CarreraForm(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            messages.success(request, "Carrera actualizado correctamente.")
            return redirect('carreralista') 
    else:
        form = CarreraForm(instance=carrera)
    return render(request, 'carreraactualizar.html', {'form': form, 'carrera': carrera})

@login_required(login_url='signin')
@permission_required('catalogos.delete_carrera', raise_exception=True)
def carreraeliminar(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    if request.method == 'POST':
        carrera.delete()
        messages.success(request, f"Carrera {carrera} eliminado correctamente.")
        return redirect('carreralista')  
    return render(request, 'carreraeliminar.html', {'carrera': carrera})