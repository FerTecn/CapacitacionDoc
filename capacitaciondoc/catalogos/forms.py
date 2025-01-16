from django import forms
from .models import GradoAcademico, Lugar, Sede, Instructor, Docente,Departamento,Dirigido,Genero,PerfilCurso,Periodo, Director

#GRADO ACADEMICO
class AñadirGradoAcForm(forms.ModelForm):
    class Meta:
        model= GradoAcademico
        fields = '__all__'
        labels={ 'grado': 'Grado académico',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })

class ActualizarGradoAcForm(forms.ModelForm):
    class Meta:
        model=GradoAcademico
        fields = '__all__'
        labels={ 'grado': 'Grado académico',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
#LUGAR
class AñadirLugarForm(forms.ModelForm):
    class Meta:
        model= Lugar
        fields = '__all__'
        labels={'nombreEdificio': 'Nombre del edificio'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})  
              
class ActualizarLugarForm(forms.ModelForm):
    class Meta:
        model= Lugar
        fields = '__all__'
        labels={'nombreEdificio': 'Nombre del edificio'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})  

#SEDES
class AñadirSedeForm(forms.ModelForm):
    class Meta:
        model= Sede
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})  

class ActualizarSedeForm(forms.ModelForm):
    class Meta:
        model= Sede
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})  
    
#INSTRUCTORES
class AñadirInstructorForm(forms.ModelForm):
    class Meta:
        model= Instructor
        fields = '__all__'
        labels={'apPaterno': 'Apellido paterno',
                'apMaterno': 'Apellido materno',
                'fechaNac': 'Fecha de nacimiento',
                'telefono': 'Teléfono',
                'institucion': 'Institución académica',
                'grado': 'Grado académico',
                'cedulaProf': 'Cédula profesional',
                'curso': 'Nombre del curso',
                'nombreEmpresa': 'Nombre de la empresa y/o Institución',
                'duracionHoras': 'Duración de horas',}
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'fechaParticipacion': 'dd/mm/aa',
            'periodo': 'Ejemplo: Enero 2022 - Junio 2022',
            'fechaParticipacion':'Ejemplo: Enero 2022 - Junio 2022',}
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, ''), 
         })
        
        # Configurar fechaNac como campo de tipo date
        self.fields['fechaNac'].widget = forms.DateInput(
            attrs={
                'type': 'date', 
                'class': 'form-control',
            })

class ActualizarInstructorForm(forms.ModelForm):
    class Meta:
        model= Instructor
        fields = '__all__'
        labels={'apPaterno': 'Apellido paterno',
                'apMaterno': 'Apellido materno',
                'fechaNac': 'Fecha de nacimiento',
                'grado': 'Grado académico',
                'cedulaProf': 'Cedula profesional',
                'curso': 'Nombre del curso',
                'nombreEmpresa': 'Nombre de la empresa y/o Institución',
                'duracionHoras': 'Duración de horas',
                'fechaParticipacion': 'Fecha que participo en el curso',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            
            'fechaParticipacion': 'dd/mm/aa',
            'periodo': 'Ejemplo: Enero 2022 - Junio 2022',
            'fechaParticipacion':'Ejemplo: Enero 2022 - Junio 2022',}
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, ''), 
         })
            
        self.fields['fechaNac'].widget = forms.DateInput(
            format='%Y-%m-%d', 
            attrs={
                'type': 'date',
                'class': 'form-control',
            })
            
#DOCENTES
class AñadirDocenteForm(forms.ModelForm):
    class Meta:
        model= Docente
        fields = '__all__'
        labels={'apPaterno': 'Apellido paterno',
                'apMaterno': 'Apellido materno',
                'fechaNac': 'Fecha de nacimiento',
                'genero': 'Género',
                'departamento': 'Departamento',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'fechaNac': 'dd/mm/aa',}
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, ''), 
         }) 
        
        self.fields['fechaNac'].widget = forms.DateInput(
            attrs={
                'type': 'date', 
                'class': 'form-control',
            })

class ActualizarDocenteForm(forms.ModelForm):
    class Meta:
        model= Docente
        fields = '__all__'
        labels={'apPaterno': 'Apellido paterno',
                'apMaterno': 'Apellido materno',
                'fechaNac':'Fecha de nacimiento',
                'genero': 'Género',
                'departamento': 'Departamento',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        self.fields['fechaNac'].widget = forms.DateInput(
            format='%Y-%m-%d', 
            attrs={
                'type': 'date',
                'class': 'form-control',
            })
            
#DEPARTAMENTOS
class AñadirDepartamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

class ActualizarDepartamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#DIRIGIDO
class AñadirDirigidoForm(forms.ModelForm):
    class Meta:
        model= Dirigido
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

class ActualizarDirigidoForm(forms.ModelForm):
    class Meta:
        model= Dirigido
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#GÉNERO
class AñadirGéneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

class ActualizarGéneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#PERFIL DE CURSO
class AñadirPerfilcursoForm(forms.ModelForm):
    class Meta:
        model= PerfilCurso
        fields = '__all__'
        labels={'perfilCurso': 'Perfil del curso'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

class ActualizarPerfilcursoForm(forms.ModelForm):
    class Meta:
        model= PerfilCurso
        fields = '__all__'
        labels={'perfilCurso': 'Perfil del curso'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#PERIODO
class AñadirPeriodoForm(forms.ModelForm):
    class Meta:
        model= Periodo
        fields = '__all__'
        labels={'inicioPeriodo': 'Inicio de periodo', 
                'finPeriodo': 'Fin de periodo',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'clave':'Ejemplo: mm/aa - mm/aa',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, '')  
            })
        
        self.fields['inicioPeriodo'].widget = forms.DateInput(
            attrs={
                'type': 'date',  
                'class': 'form-control',
            })
        
        self.fields['finPeriodo'].widget = forms.DateInput(
            attrs={
                'type': 'date',  
                'class': 'form-control',
            })

class ActualizarPeriodoForm(forms.ModelForm):
    class Meta:
        model= Periodo
        fields = '__all__'
        labels={'inicioPeriodo': 'Inicio de periodo', 
                'finPeriodo': 'Fin de periodo',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'clave': 'Ejemplo: mm/aa - mm/aa',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field, '')  
            })
        
        # Configurar inicioPeriodo como un campo de tipo date
        self.fields['inicioPeriodo'].widget = forms.DateInput(
            format='%Y-%m-%d',  # Asegúrate de usar un formato compatible con HTML5
            attrs={
                'type': 'date',
                'class': 'form-control',
            })

        # Configurar finPeriodo como un campo de tipo date
        self.fields['finPeriodo'].widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
                'class': 'form-control',
            })

#DIRECTOR
class AgregarDirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class ActualizarDirectorForm(forms.ModelForm):
    class Meta:
        model= Director
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 