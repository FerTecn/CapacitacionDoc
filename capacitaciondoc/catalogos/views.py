from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from .models import GradoAcademico, Lugar, Sede, Instructor, Docente,Departamento,Dirigido,Genero,PerfilCurso,Periodo
from .forms import AñadirGradoAcForm, ActualizarGradoAcForm, AñadirLugarForm, ActualizarLugarForm, AñadirSedeForm, ActualizarSedeForm
from .forms import AñadirInstructorForm, ActualizarInstructorForm, AñadirDocenteForm, ActualizarDocenteForm, AñadirDepartamentoForm, ActualizarDepartamentoForm,AñadirDirigidoForm,ActualizarDirigidoForm,AñadirGéneroForm,ActualizarGéneroForm,ActualizarPerfilcursoForm,AñadirPerfilcursoForm,ActualizarPeriodoForm,AñadirPeriodoForm

# Create your views here.

#GRADO ACADEMICO
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

def gradover(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    return render(request, 'gradover.html', {'grado': grado})

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

def gradoeliminar(request, grado_id):
    grado = get_object_or_404(GradoAcademico, id=grado_id)
    if request.method == 'POST':
        grado.delete()
        return redirect('gradolista')  
    return render(request, 'gradoeliminar.html', {'grado': grado})

 #LUGARES
def lugarlista(request):
    Lugares = Lugar.objects.all()
    return render(request, 'lugarlista.html', {'Lugares': Lugares})

def lugarañadir(request):
    if request.method == 'POST':
        form = AñadirLugarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lugarlista') 
    else:
        form = AñadirLugarForm()

    return render(request, 'lugarañadir.html', {'form': form})

def lugarver(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    return render(request, 'lugarver.html', {'lugar': lugar})

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

def lugareliminar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    if request.method == 'POST':
        lugar.delete()
        return redirect('lugarlista')  
    return render(request, 'lugareliminar.html', {'lugar': lugar})

#SEDES
def sedelista(request):
    sedes = Sede.objects.all()
    return render(request, 'sedelista.html', {'sedes': sedes})

def sedeañadir(request):
    if request.method == 'POST':
        form = AñadirSedeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sedelista') 
    else:
        form = AñadirSedeForm()

    return render(request, 'sedeañadir.html', {'form': form})

def sedever(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    return render(request, 'sedever.html', {'sede': sede})

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

def sedeeliminar(request, sede_id):
    sede = get_object_or_404(Sede, id=sede_id)
    if request.method == 'POST':
        sede.delete()
        return redirect('sedelista')  
    return render(request, 'sedeeliminar.html', {'sede': sede})

#INSTRUCTORES
def instructorlista(request):
    instructores = Instructor.objects.all()
    return render(request, 'instructorlista.html', {'instructores': instructores})

def instructorañadir(request):
    if request.method == 'POST':
        form = AñadirInstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructorlista') 
    else:
        form = AñadirInstructorForm()

    return render(request, 'instructorañadir.html', {'form': form})

def instructorver(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    return render(request, 'instructorver.html', {'instructor': instructor})

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

def instructoreliminar(request, instructor_id):
    instructor = get_object_or_404(Instructor, id=instructor_id)
    if request.method == 'POST':
        instructor.delete()
        return redirect('instructorlista')  
    return render(request, 'instructoreliminar.html', {'instructor': instructor})

#DOCENTES
def docentelista(request):
    docentes = Docente.objects.all()
    return render(request, 'docentelista.html', {'docentes': docentes})

def docenteañadir(request):
    if request.method == 'POST':
        form = AñadirDocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('docentelista') 
    else:
        form = AñadirDocenteForm()

    return render(request, 'docenteañadir.html', {'form': form})

def docentever(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    return render(request, 'docentever.html', {'docente': docente})

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

def docenteeliminar(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id)
    if request.method == 'POST':
        docente.delete()
        return redirect('docentelista')  
    return render(request, 'docenteeliminar.html', {'docente': docente})

#DEPARTAMENTOS
def departamentolista(request):
    departamentos = Departamento.objects.all()
    return render(request, 'departamentolista.html', {'departamentos': departamentos})

def departamentoañadir(request):
    if request.method == 'POST':
        form = AñadirDepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departamentolista') 
    else:
        form = AñadirDepartamentoForm()

    return render(request, 'departamentoañadir.html', {'form': form})

def departamentover(request, departamento_id):
    departamento= get_object_or_404(Departamento, id=departamento_id)
    return render(request, 'departamentover.html', {'departamento': departamento})


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

def departamentoeliminar(request, departamento_id):
    departamento = get_object_or_404(Departamento, id=departamento_id)
    if request.method == 'POST':
        departamento.delete()
        return redirect('departamentolista')  
    return render(request, 'departamentoeliminar.html', {'departamento': departamento})


#DIRIGIDO
def dirigidolista(request):
    dirigidos = Dirigido.objects.all()
    return render(request, 'dirigidolista.html', {'dirigidos': dirigidos})

def dirigidoañadir(request):
    if request.method == 'POST':
        form = AñadirDirigidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dirigidolista') 
    else:
        form = AñadirDirigidoForm()

    return render(request, 'dirigidoañadir.html', {'form': form})

def dirigidover(request, dirigido_id):
    dirigido= get_object_or_404(Dirigido, id=dirigido_id)
    return render(request, 'dirigidover.html', {'dirigido': dirigido})


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


def dirigidoeliminar(request, dirigido_id):
    dirigido = get_object_or_404(Dirigido, id=dirigido_id)
    if request.method == 'POST':
        dirigido.delete()
        return redirect('dirigidolista')  
    return render(request, 'dirigidoeliminar.html', {'dirigido': dirigido})


#GÉNERO
def génerolista(request):
    generos = Genero.objects.all()
    return render(request, 'génerolista.html', {'generos': generos})

def géneroañadir(request):
    if request.method == 'POST':
        form = AñadirGéneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('génerolista') 
    else:
        form = AñadirGéneroForm()

    return render(request, 'géneroañadir.html', {'form': form})

def génerover(request, genero_id):
    genero= get_object_or_404(Genero, id=genero_id)
    return render(request, 'génerover.html', {'genero': genero})


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


def géneroeliminar(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        genero.delete()
        return redirect('génerolista')  
    return render(request, 'géneroeliminar.html', {'genero': genero})




#PERFIL DE CURSO
def perfilcursolista(request):
    perfilcursos = PerfilCurso.objects.all()
    return render(request, 'perfilcursolista.html', {'perfilcursos': perfilcursos})

def perfilcursoañadir(request):
    if request.method == 'POST':
        form = AñadirPerfilcursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('perfilcursolista') 
    else:
        form = AñadirPerfilcursoForm()

    return render(request, 'perfilcursoañadir.html', {'form': form})

def perfilcursover(request, perfilCurso_id):
    perfilCurso= get_object_or_404(PerfilCurso, id=perfilCurso_id)
    return render(request, 'perfilcursover.html', {'perfilCurso': perfilCurso})


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


def perfilcursoeliminar(request, perfilCurso_id):
    perfilCurso = get_object_or_404(PerfilCurso, id=perfilCurso_id)
    if request.method == 'POST':
        perfilCurso.delete()
        return redirect('perfilcursolista')  
    return render(request, 'perfilcursoeliminar.html', {'perfilCurso': perfilCurso})


#PERIODO
def periodolista(request):
    periodos = Periodo.objects.all()
    return render(request, 'periodolista.html', {'periodos': periodos})

def periodoañadir(request):
    if request.method == 'POST':
        form = AñadirPeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('periodolista') 
    else:
        form = AñadirPeriodoForm()

    return render(request, 'periodoañadir.html', {'form': form})

def periodover(request, periodo_id):
    periodo= get_object_or_404(Periodo, id=periodo_id)
    return render(request, 'periodover.html', {'periodo': periodo})


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


def periodoeliminar(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    if request.method == 'POST':
        periodo.delete()
        return redirect('periodolista')  
    return render(request, 'periodoeliminar.html', {'periodo': periodo})