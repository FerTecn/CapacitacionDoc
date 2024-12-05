from django import forms
from .models import GradoAcademico, Lugar, Sede, Instructor, Docente,Departamento,Dirigido,Genero,PerfilCurso,Periodo

class AñadirGradoAcForm(forms.ModelForm):
    class Meta:
        model= GradoAcademico
        fields = ['clave', 'grado']

class ActualizarGradoAcForm(forms.ModelForm):
    class Meta:
        model= GradoAcademico
        fields = ['clave', 'grado']
        
#LUGAR
class AñadirLugarForm(forms.ModelForm):
    class Meta:
        model= Lugar
        fields = ['clave', 'nombreEdificio', 'ubicacion']

class ActualizarLugarForm(forms.ModelForm):
    class Meta:
        model= Lugar
        fields = ['clave', 'nombreEdificio', 'ubicacion']

#SEDES
class AñadirSedeForm(forms.ModelForm):
    class Meta:
        model= Sede
        fields = ['clave', 'sede']

class ActualizarSedeForm(forms.ModelForm):
    class Meta:
        model= Sede
        fields = ['clave', 'sede']
    
#INSTRUCTORES
class AñadirInstructorForm(forms.ModelForm):
    class Meta:
        model= Instructor
        fields = ['clave', 'nombre', 'apPaterno', 'apMaterno', 
                  'fechaNac', 'CURP', 'RFC', 'telefono', 'email', 
                  'institucion', 'grado', 'cedulaProf', 'puesto', 
                  'empresa', 'curso', 'nombreEmpresa', 'duracionHoras', 'fechaParticipacion']

class ActualizarInstructorForm(forms.ModelForm):
    class Meta:
        model= Instructor
        fields = ['clave', 'nombre', 'apPaterno', 'apMaterno', 
                  'fechaNac', 'CURP', 'RFC', 'telefono', 'email', 
                  'institucion', 'grado', 'cedulaProf', 'puesto', 
                  'empresa', 'curso', 'nombreEmpresa', 'duracionHoras', 'fechaParticipacion']
        
#DOCENTES
class AñadirDocenteForm(forms.ModelForm):
    class Meta:
        model= Docente
        fields = ['clave', 'nombre', 'apPaterno', 'apMaterno', 'genero',
                  'CURP', 'RFC', 'telefono', 'email', 'departamento']

class ActualizarDocenteForm(forms.ModelForm):
    class Meta:
        model= Docente
        fields = ['clave', 'nombre', 'apPaterno', 'apMaterno', 'genero',
                  'CURP', 'RFC', 'telefono', 'email', 'departamento']

#DEPARTAMENTOS
class AñadirDepartamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = ['clave', 'departamento']

class ActualizarDepartamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = ['clave', 'departamento']
      
#DIRIGIDO
class AñadirDirigidoForm(forms.ModelForm):
    class Meta:
        model= Dirigido
        fields = ['clave', 'dirigido']

class ActualizarDirigidoForm(forms.ModelForm):
    class Meta:
        model= Dirigido
        fields = ['clave', 'dirigido']

#GÉNERO
class AñadirGéneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields = ['clave', 'genero']

class ActualizarGéneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields = ['clave', 'genero']

#PERFIL DE CURSO
class AñadirPerfilcursoForm(forms.ModelForm):
    class Meta:
        model= PerfilCurso
        fields = ['clave', 'perfilCurso']

class ActualizarPerfilcursoForm(forms.ModelForm):
    class Meta:
        model= PerfilCurso
        fields = ['clave', 'perfilCurso']

#PERIODO
class AñadirPeriodoForm(forms.ModelForm):
    class Meta:
        model= Periodo
        fields = ['clave', 'inicioPeriodo','finPeriodo' ]

class ActualizarPeriodoForm(forms.ModelForm):
    class Meta:
        model= Periodo
        fields = ['clave', 'inicioPeriodo','finPeriodo']