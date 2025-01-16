from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GradoAcademico, Lugar, Sede, Instructor, Docente,Departamento,Dirigido,Genero,PerfilCurso,Periodo, Director
from .forms import AñadirGradoAcForm, ActualizarGradoAcForm, AñadirLugarForm, ActualizarLugarForm, AñadirSedeForm, ActualizarSedeForm, ActualizarDirectorForm, AgregarDirectorForm
from .forms import AñadirInstructorForm, ActualizarInstructorForm, AñadirDocenteForm, ActualizarDocenteForm, AñadirDepartamentoForm, ActualizarDepartamentoForm,AñadirDirigidoForm,ActualizarDirigidoForm,AñadirGéneroForm,ActualizarGéneroForm,ActualizarPerfilcursoForm,AñadirPerfilcursoForm,ActualizarPeriodoForm,AñadirPeriodoForm

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
    instructores = Instructor.objects.all()
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
def instructorver(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructorver.html', {'instructor': instructor})

@login_required(login_url='signin')
def instructoractualizar(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        form = ActualizarInstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('instructorlista') 
    else:
        form = ActualizarInstructorForm(instance=instructor)
    return render(request, 'instructoractualizar.html', {'form': form, 'instructor': instructor})

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
    docentes = Docente.objects.all()
    return render(request, 'docentelista.html', {'docentes': docentes})

@login_required(login_url='signin')
def docenteañadir(request):
    if request.method == 'POST':
        form = AñadirDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docentelista') 
    else:
        form = AñadirDocenteForm()

    return render(request, 'docenteañadir.html', {'form': form})

@login_required(login_url='signin')
def docentever(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    return render(request, 'docentever.html', {'docente': docente})

@login_required(login_url='signin')
def docenteactualizar(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        form = ActualizarDocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            return redirect('docentelista') 
    else:
        form = ActualizarDocenteForm(instance=docente)
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