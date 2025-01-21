from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ExperienciaDocente, ExperienciaLaboral, FormacionAcademica, GradoAcademico, Lugar, ParticipacionInstructor, Sede, Instructor, Docente,Departamento,Dirigido,Genero,PerfilCurso,Periodo, Director
from .forms import AñadirGradoAcForm, ActualizarGradoAcForm, AñadirLugarForm, ActualizarLugarForm, AñadirSedeForm, ActualizarSedeForm, ActualizarDirectorForm, AgregarDirectorForm
from .forms import AñadirInstructorForm, AgregarDocenteForm, ActualizarDocenteForm, AñadirDepartamentoForm, ActualizarDepartamentoForm,AñadirDirigidoForm,ActualizarDirigidoForm,AñadirGéneroForm,ActualizarGéneroForm,ActualizarPerfilcursoForm,AñadirPerfilcursoForm,ActualizarPeriodoForm,AñadirPeriodoForm
from .forms import (
    ActualizarInstructorForm, FormacionAcademicaForm,
    ExperienciaLaboralForm, ExperienciaDocenteForm,
    ParticipacionInstructorForm
)
# Create your views here.

#GRADO ACADEMICO
@login_required(login_url='signin')
def gradolista(request):
    gradoac = GradoAcademico.objects.all()
    return render(request, 'gradolista.html', {'gradoac': gradoac})

def gradoañadir(request):
    if request.method == 'POST':
        form = AñadirGradoAcForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gradolista') 
    else:
        form = AñadirGradoAcForm()

    return render(request, 'gradoañadir.html', {'form': form})

@login_required(login_url='signin')
def gradover(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    return render(request, 'gradover.html', {'grado': grado})

@login_required(login_url='signin')
def gradoactualizar(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    if request.method == 'POST':
        form = ActualizarGradoAcForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            return redirect('gradolista') 
    else:
        form = ActualizarGradoAcForm(instance=grado)
    return render(request, 'gradoactualizar.html', {'form': form, 'grado': grado})

@login_required(login_url='signin')
def gradoeliminar(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    if request.method == 'POST':
        grado.delete()
        return redirect('gradolista')  
    return render(request, 'gradoeliminar.html', {'grado': grado})

 #LUGARES
@login_required(login_url='signin')
def lugarlista(request):
    Lugares = Lugar.objects.all()
    return render(request, 'lugarlista.html', {'Lugares': Lugares})

@login_required(login_url='signin')
def lugarañadir(request):
    if request.method == 'POST':
        form = AñadirLugarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lugarlista') 
    else:
        form = AñadirLugarForm()

    return render(request, 'lugarañadir.html', {'form': form})

@login_required(login_url='signin')
def lugarver(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    return render(request, 'lugarver.html', {'lugar': lugar})

@login_required(login_url='signin')
def lugaractualizar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    if request.method == 'POST':
        form = ActualizarLugarForm(request.POST, instance=lugar)
        if form.is_valid():
            form.save()
            return redirect('lugarlista') 
    else:
        form = ActualizarLugarForm(instance=lugar)
    return render(request, 'lugaractualizar.html', {'form': form, 'lugar': lugar})

@login_required(login_url='signin')
def lugareliminar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    if request.method == 'POST':
        lugar.delete()
        return redirect('lugarlista')  
    return render(request, 'lugareliminar.html', {'lugar': lugar})

#SEDES
@login_required(login_url='signin')
def sedelista(request):
    sedes = Sede.objects.all()
    return render(request, 'sedelista.html', {'sedes': sedes})

@login_required(login_url='signin')
def sedeañadir(request):
    if request.method == 'POST':
        form = AñadirSedeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sedelista') 
    else:
        form = AñadirSedeForm()

    return render(request, 'sedeañadir.html', {'form': form})

@login_required(login_url='signin')
def sedever(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    return render(request, 'sedever.html', {'sede': sede})

@login_required(login_url='signin')
def sedeactualizar(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    if request.method == 'POST':
        form = ActualizarSedeForm(request.POST, instance=sede)
        if form.is_valid():
            form.save()
            return redirect('sedelista') 
    else:
        form = ActualizarSedeForm(instance=sede)
    return render(request, 'sedeactualizar.html', {'form': form, 'sede': sede})

@login_required(login_url='signin')
def sedeeliminar(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    if request.method == 'POST':
        sede.delete()
        return redirect('sedelista')  
    return render(request, 'sedeeliminar.html', {'sede': sede})

#INSTRUCTORES
@login_required(login_url='signin')
@login_required(login_url='signin')
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
def instructorañadir(request):
    if request.method == 'POST':
        form = AñadirInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructorlista') 
    else:
        form = AñadirInstructorForm()

    return render(request, 'instructorañadir.html', {'form': form})

@login_required(login_url='signin')
def instructorver(request, instructor_id=None):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructorver.html', {'instructor': instructor})

@login_required(login_url='signin')
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
                print(form.errors)
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

        elif 'experiencia_laboral' in request.POST:
            # Agregar una experiencia laboral
            experiencia_laboral_form = ExperienciaLaboralForm(request.POST)
            if experiencia_laboral_form.is_valid():
                nueva_experiencia = experiencia_laboral_form.save(commit=False)
                nueva_experiencia.instructor = instructor
                nueva_experiencia.save()
                messages.success(request, "Experiencia laboral agregada correctamente.", extra_tags="experiencia-laboral")
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
def instructoreliminar(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructorlista')  
    return render(request, 'instructoreliminar.html', {'instructor': instructor})

#DOCENTES
@login_required(login_url='signin')
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
def docenteañadir(request):
    if request.method == 'POST':
        form = AgregarDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docentelista') 
    else:
        form = AgregarDocenteForm()

    return render(request, 'docenteañadir.html', {'form': form})

@login_required(login_url='signin')
def docentever(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    return render(request, 'docentever.html', {'docente': docente})

@login_required(login_url='signin')
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
            return redirect('docentelista') 
    else:
        form = ActualizarDocenteForm(instance=docente,  user_instance=docente.user)
    return render(request, 'docenteactualizar.html', {'form': form, 'docente': docente})

@login_required(login_url='signin')
def docenteeliminar(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.delete()
        return redirect('docentelista')  
    return render(request, 'docenteeliminar.html', {'docente': docente})

#DEPARTAMENTOS
@login_required(login_url='signin')
def departamentolista(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentolista.html', {'departamentos': departamentos})

@login_required(login_url='signin')
def departamentoañadir(request):
    if request.method == 'POST':
        form = AñadirDepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departamentolista') 
    else:
        form = AñadirDepartamentoForm()

    return render(request, 'departamentoañadir.html', {'form': form})


@login_required(login_url='signin')
def departamentover(request, departamento_id):
    departamento= get_object_or_404(Departamento, id=departamento_id)
    return render(request, 'departamentover.html', {'departamento': departamento})


@login_required(login_url='signin')
def departamentoactualizar(request, departamento_id):
    departamento= get_object_or_404(Departamento, id=departamento_id)
    if request.method == 'POST':
        form = ActualizarDepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('departamentolista') 
    else:
        form = ActualizarDepartamentoForm(instance=departamento)
    return render(request, 'departamentoactualizar.html', {'form': form, 'departamento': departamento})

@login_required(login_url='signin')
def departamentoeliminar(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    if request.method == 'POST':
        departamento.delete()
        return redirect('departamentolista')  
    return render(request, 'departamentoeliminar.html', {'departamento': departamento})


#DIRIGIDO
@login_required(login_url='signin')
def dirigidolista(request):
    dirigidos = Dirigido.objects.all()
    return render(request, 'dirigidolista.html', {'dirigidos': dirigidos})

@login_required(login_url='signin')
def dirigidoañadir(request):
    if request.method == 'POST':
        form = AñadirDirigidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dirigidolista') 
    else:
        form = AñadirDirigidoForm()

    return render(request, 'dirigidoañadir.html', {'form': form})

@login_required(login_url='signin')
def dirigidover(request, dirigido_id):
    dirigido= get_object_or_404(Dirigido, id=dirigido_id)
    return render(request, 'dirigidover.html', {'dirigido': dirigido})


@login_required(login_url='signin')
def dirigidoactualizar(request, dirigido_id):
    dirigido= get_object_or_404(Dirigido, id=dirigido_id)
    if request.method == 'POST':
        form = ActualizarDirigidoForm(request.POST, instance=dirigido)
        if form.is_valid():
            form.save()
            return redirect('dirigidolista') 
    else:
        form = ActualizarDirigidoForm(instance=dirigido)
    return render(request, 'dirigidoactualizar.html', {'form': form, 'dirigido': dirigido})


@login_required(login_url='signin')
def dirigidoeliminar(request, dirigido_id):
    dirigido = get_object_or_404(Dirigido, id=dirigido_id)
    if request.method == 'POST':
        dirigido.delete()
        return redirect('dirigidolista')  
    return render(request, 'dirigidoeliminar.html', {'dirigido': dirigido})


#GÉNERO
@login_required(login_url='signin')
def génerolista(request):
    generos = Genero.objects.all()
    return render(request, 'génerolista.html', {'generos': generos})

@login_required(login_url='signin')
def géneroañadir(request):
    if request.method == 'POST':
        form = AñadirGéneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('génerolista') 
    else:
        form = AñadirGéneroForm()

    return render(request, 'géneroañadir.html', {'form': form})

@login_required(login_url='signin')
def génerover(request, genero_id):
    genero= get_object_or_404(Genero, id=genero_id)
    return render(request, 'génerover.html', {'genero': genero})


@login_required(login_url='signin')
def géneroactualizar(request, genero_id):
    genero= get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        form = ActualizarGéneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return redirect('génerolista') 
    else:
        form = ActualizarGéneroForm(instance=genero)
    return render(request, 'géneroactualizar.html', {'form': form, 'genero': genero})


@login_required(login_url='signin')
def géneroeliminar(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        genero.delete()
        return redirect('génerolista')  
    return render(request, 'géneroeliminar.html', {'genero': genero})




#PERFIL DE CURSO
@login_required(login_url='signin')
def perfilcursolista(request):
    perfilcursos = PerfilCurso.objects.all()
    return render(request, 'perfilcursolista.html', {'perfilcursos': perfilcursos})

@login_required(login_url='signin')
def perfilcursoañadir(request):
    if request.method == 'POST':
        form = AñadirPerfilcursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfilcursolista') 
    else:
        form = AñadirPerfilcursoForm()

    return render(request, 'perfilcursoañadir.html', {'form': form})

@login_required(login_url='signin')
def perfilcursover(request, perfilCurso_id):
    perfilCurso= get_object_or_404(PerfilCurso, id=perfilCurso_id)
    return render(request, 'perfilcursover.html', {'perfilCurso': perfilCurso})


@login_required(login_url='signin')
def perfilcursoactualizar(request, perfilCurso_id):
    perfilCurso= get_object_or_404(PerfilCurso, id=perfilCurso_id)
    if request.method == 'POST':
        form = ActualizarPerfilcursoForm(request.POST, instance=perfilCurso)
        if form.is_valid():
            form.save()
            return redirect('perfilcursolista') 
    else:
        form = ActualizarPerfilcursoForm(instance=perfilCurso)
    return render(request, 'perfilcursoactualizar.html', {'form': form, 'perfilCurso': perfilCurso})


@login_required(login_url='signin')
def perfilcursoeliminar(request, perfilCurso_id):
    perfilCurso = get_object_or_404(PerfilCurso, id=perfilCurso_id)
    if request.method == 'POST':
        perfilCurso.delete()
        return redirect('perfilcursolista')  
    return render(request, 'perfilcursoeliminar.html', {'perfilCurso': perfilCurso})


#PERIODO
@login_required(login_url='signin')
def periodolista(request):
    periodos = Periodo.objects.all()
    return render(request, 'periodolista.html', {'periodos': periodos})

@login_required(login_url='signin')
def periodoañadir(request):
    if request.method == 'POST':
        form = AñadirPeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('periodolista') 
    else:
        form = AñadirPeriodoForm()

    return render(request, 'periodoañadir.html', {'form': form})

@login_required(login_url='signin')
def periodover(request, periodo_id):
    periodo= get_object_or_404(Periodo, id=periodo_id)
    return render(request, 'periodover.html', {'periodo': periodo})


@login_required(login_url='signin')
def periodoactualizar(request, periodo_id):
    periodo= get_object_or_404(Periodo, id=periodo_id)
    if request.method == 'POST':
        form = ActualizarPeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            return redirect('periodolista') 
    else:
        form = ActualizarPeriodoForm(instance=periodo)
    return render(request, 'periodoactualizar.html', {'form': form, 'periodo': periodo})


@login_required(login_url='signin')
def periodoeliminar(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    if request.method == 'POST':
        periodo.delete()
        return redirect('periodolista')  
    return render(request, 'periodoeliminar.html', {'periodo': periodo})

#Director
@login_required(login_url='signin')
def directorlista(request):
    directores = Director.objects.all()
    return render(request, 'directorlista.html', {'directores': directores})

@login_required(login_url='signin')
def directoragregar(request):
    if request.method == 'POST':
        form = AgregarDirectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('directorlista') 
    else:
        form = AgregarDirectorForm()

    return render(request, 'directoragregar.html', {'form': form})

@login_required(login_url='signin')
def directorver(request, director_id):
    director= get_object_or_404(Director, id=director_id)
    return render(request, 'directorver.html', {'director': director})


@login_required(login_url='signin')
def directoractualizar(request, director_id):
    director= get_object_or_404(Director, id=director_id)
    if request.method == 'POST':
        form = ActualizarPeriodoForm(request.POST, instance=director)
        if form.is_valid():
            form.save()
            return redirect('periodolista') 
    else:
        form = ActualizarDirectorForm(instance=director)
    return render(request, 'directoractualizar.html', {'form': form, 'director': director})


@login_required(login_url='signin')
def directoreliminar(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    if request.method == 'POST':
        director.delete()
        return redirect('directorlista')  
    return render(request, 'directoreliminar.html', {'director': director})