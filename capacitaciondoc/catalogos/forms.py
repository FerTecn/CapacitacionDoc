from django import forms
from .models import (
    ExperienciaDocente, ExperienciaLaboral, FormacionAcademica, FormatoConstancia, FormatoDepartamento, 
    GradoAcademico, Lugar, ParticipacionInstructor, Sede, 
    Instructor, Docente, Autoridad,
    Departamento, Dirigido, Genero, PerfilCurso, Periodo, ValorCalificacion)

#GRADO ACADEMICO
class GradoAcForm(forms.ModelForm):
    class Meta:
        model=GradoAcademico
        fields = '__all__'
        labels={ 'grado': 'Grado académico',}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
#LUGAR
class LugarForm(forms.ModelForm):
    class Meta:
        model= Lugar
        fields = '__all__'
        labels={'nombreEdificio': 'Nombre del edificio'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})  

#SEDES
class SedeForm(forms.ModelForm):
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
    # Campos del modelo CustomUser
    first_name = forms.CharField(max_length=50, label="Nombre(s)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_paterno = forms.CharField(max_length=50, label="Apellido Paterno", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_materno = forms.CharField(max_length=50, label="Apellido Materno", widget=forms.TextInput(attrs={'class': 'form-control'}))
    curp = forms.CharField(max_length=18, label="CURP", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Instructor
        fields = ['clave', 'RFC', 'fechaNac', 'telefono']
        labels = {
            'clave': 'Clave',
            'RFC': 'RFC',
            'fechaNac': 'Fecha de nacimiento',
            'telefono': 'Teléfono',
        }
        widgets = {
            'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'RFC': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaNac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
        }


    def __init__(self, *args, **kwargs):
        # Obtenemos la instancia de CustomUser (pasada como argumento)
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            # Inicializamos los campos de CustomUser con los datos del usuario
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name_paterno'].initial = self.user_instance.last_name_paterno
            self.fields['last_name_materno'].initial = self.user_instance.last_name_materno
            self.fields['curp'].initial = self.user_instance.curp
            self.fields['email'].initial = self.user_instance.email

    def save(self, commit=True):
        # Guardar los cambios en el modelo Instructor
        instructor = super().save(commit=False)
        if self.user_instance:
            # Guardar los cambios en el modelo CustomUser
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name_paterno = self.cleaned_data['last_name_paterno']
            self.user_instance.last_name_materno = self.cleaned_data['last_name_materno']
            self.user_instance.curp = self.cleaned_data['curp']
            self.user_instance.email = self.cleaned_data['email']
            if commit:
                self.user_instance.save()
        if commit:
            instructor.save()
        return instructor

class FormacionAcademicaForm(forms.ModelForm):
    class Meta:
        model = FormacionAcademica
        fields = ['institucion', 'grado', 'cedulaProf']
        labels = {
            'institucion': 'Institución',
            'cedulaProf': 'Cédula Profesional',
        }
        widgets = {
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'grado': forms.Select(attrs={'class': 'form-control'}),
            'cedulaProf': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        institucion = cleaned_data.get('institucion')
        grado = cleaned_data.get('grado')
        cedulaProf = cleaned_data.get('cedulaProf')

        # Validar duplicados
        if FormacionAcademica.objects.filter(
            institucion=institucion,
            grado=grado,
            cedulaProf=cedulaProf
        ).exists():
            raise forms.ValidationError("Ya existe una formación académica con estos datos.")
        return cleaned_data
        
class ExperienciaLaboralForm(forms.ModelForm):
    class Meta:
        model = ExperienciaLaboral
        fields = ['puesto', 'empresa', 'fecha_inicio', 'fecha_fin']
        labels = {
            'puesto': 'Puesto laboral',
            'empresa': 'Nombre de la empresa',
            'fecha_inicio': 'Mes y año de incio',
            'fecha_fin': 'Mes y año de terminación'
        }
        widgets = {
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }
    

    def clean(self):
        cleaned_data = super().clean()
        puesto = cleaned_data.get('puesto')
        empresa = cleaned_data.get('empresa')
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')

        # Validar duplicados
        if ExperienciaLaboral.objects.filter(
            puesto=puesto,
            empresa=empresa,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        ).exists():
            raise forms.ValidationError("Ya existe esa experiencia laboral.")
        
        # Validar que la fecha de inicio sea anterior a la fecha de fin
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        
        return cleaned_data

class ExperienciaDocenteForm(forms.ModelForm):
    class Meta:
        model = ExperienciaDocente
        fields = ['materia', 'periodo']
        labels = {
            'materia': 'Materia',
            'periodo': 'Periodo en que impartió'
        }
        widgets = {
            'materia': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        materia = cleaned_data.get('materia')
        periodo = cleaned_data.get('periodo')

        # Validar duplicados
        if ExperienciaDocente.objects.filter(
            materia=materia,
            periodo=periodo
        ).exists():
            raise forms.ValidationError("Ya existe esa experiencia en docencia.")
        return cleaned_data

class ParticipacionInstructorForm(forms.ModelForm):
    class Meta:
        model = ParticipacionInstructor
        fields = ['curso', 'nombreEmpresa', 'duracionHoras', 'periodoInicio', 'periodoFin']
        labels = {
            'curso': 'Nombre del curso',
            'nombreEmpresa': 'Nombre de la Empresa / Institución',
            'duracionHoras': 'Duración de horas',
            'periodoInicio': 'Periodo en el que inició el curso',
            'periodoFin': 'Periodo en el que culminó el curso',
        }
        widgets = {
            'curso': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreEmpresa': forms.TextInput(attrs={'class': 'form-control'}),
            'duracionHoras': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodoInicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'periodoFin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean(self):
        cleaned_data = super().clean()
        curso = cleaned_data.get('curso')
        nombreEmpresa = cleaned_data.get('nombreEmpresa')
        duracionHoras = cleaned_data.get('duracionHoras')
        periodoInicio = cleaned_data.get('periodoInicio')
        periodoFin = cleaned_data.get('periodoFin')

        # Validar duplicados
        if ParticipacionInstructor.objects.filter(
            curso=curso,
            nombreEmpresa=nombreEmpresa,
            duracionHoras=duracionHoras,
            periodoInicio=periodoInicio,
            periodoFin=periodoFin,
        ).exists():
            raise forms.ValidationError("Ya existe esa esa participación.")
        return cleaned_data

#DOCENTES
class AgregarDocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['clave', 'fechaNac', 'genero', 'RFC', 'telefono', 'departamento']
        labels = {
            'clave': 'Clave',
            'fechaNac': 'Fecha de nacimiento',
            'genero': 'Género',
            'departamento': 'Departamento',
            }
        
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
            }, format='%Y-%m-%d' )

class ActualizarDocenteForm(forms.ModelForm):
    # Campos del modelo CustomUser
    first_name = forms.CharField(max_length=50, label="Nombre(s)", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_paterno = forms.CharField(max_length=50, label="Apellido Paterno", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_materno = forms.CharField(max_length=50, label="Apellido Materno", widget=forms.TextInput(attrs={'class': 'form-control'}))
    curp = forms.CharField(max_length=18, label="CURP", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Docente
        fields = ['clave','RFC', 'fechaNac', 'genero', 'departamento', 'telefono']
        labels = {
            'clave': 'Clave',
            'fechaNac': 'Fecha de nacimiento',
            'telefono': 'Teléfono',
        }
        widgets = {
            'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'RFC': forms.TextInput(attrs={'class': 'form-control'}),
            'fechaNac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        # Obtenemos la instancia de CustomUser (pasada como argumento)
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            # Inicializamos los campos de CustomUser con los datos del usuario
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name_paterno'].initial = self.user_instance.last_name_paterno
            self.fields['last_name_materno'].initial = self.user_instance.last_name_materno
            self.fields['curp'].initial = self.user_instance.curp
            self.fields['email'].initial = self.user_instance.email

    def save(self, commit=True):
        # Guardar los cambios en el modelo Docente
        docente = super().save(commit=False)
        if self.user_instance:
            # Guardar los cambios en el modelo CustomUser
            self.user_instance.first_name = self.cleaned_data['first_name']
            self.user_instance.last_name_paterno = self.cleaned_data['last_name_paterno']
            self.user_instance.last_name_materno = self.cleaned_data['last_name_materno']
            self.user_instance.curp = self.cleaned_data['curp']
            self.user_instance.email = self.cleaned_data['email']
            if commit:
                self.user_instance.save()
        if commit:
            docente.save()
            return docente 
            
#DEPARTAMENTOS
class DepartamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = '__all__'
        labels = {
            'nomenclatura': 'Nomenclatura',
            'numerodepartamento': 'Número de departamento',
            'departamento': 'Departamento',
            'nombreJefe': 'Nombre(s)',
            'apParternoJefe': 'Apellido Paterno',
            'apMaternoJefe': 'Apellido Materno',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico del departamento',
            'paginaWeb': 'Página Web',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#DIRIGIDO
class DirigidoForm(forms.ModelForm):
    class Meta:
        model= Dirigido
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#GÉNERO
class GeneroForm(forms.ModelForm):
    class Meta:
        model= Genero
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#PERFIL DE CURSO
class PerfilcursoForm(forms.ModelForm):
    class Meta:
        model= PerfilCurso
        fields = '__all__'
        labels={'perfilCurso': 'Perfil del curso'}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

#PERIODO
class PeriodoForm(forms.ModelForm):
    class Meta:
        model= Periodo
        fields = ['inicioPeriodo', 'finPeriodo']
        labels = {
            'inicioPeriodo': 'Inicio de Periodo',
            'finPeriodo': 'Fin de periodo'
        }
        widgets = {
            'inicioPeriodo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'finPeriodo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicioPeriodo')
        fin = cleaned_data.get('finPeriodo')

        # Validar que ambas fechas estén presentes
        if not inicio or not fin:
            raise forms.ValidationError("Debe proporcionar tanto la fecha de inicio como la fecha de fin.")

        # Validar que la fecha de fin no sea menor que la fecha de inicio
        if fin < inicio:
            raise forms.ValidationError("La fecha de fin no puede ser menor que la fecha de inicio.")

        return cleaned_data

#AUTORIDAD
class AutoridadForm(forms.ModelForm):
    class Meta:
        model = Autoridad
        fields = '__all__'
        labels = {
            'nombre': 'Nombre(s)',
            'apPaterno': 'Apellido Paterno',
            'apMaterno': 'Apellido Materno',
            'puesto': 'Cargo',
            'estatus': 'Estatus',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class ValorCalificacionForm(forms.ModelForm):
    class Meta:
        model = ValorCalificacion
        fields = '__all__'
        labels = {
            'valorCalificacion': 'Valor de Calificación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

class FormatoDepartamentoForm(forms.ModelForm):
    class Meta:
        model = FormatoDepartamento
        fields = '__all__'
        labels = {
            'header': 'Imagen de encabezado',
            'footer': 'Imagen de pie de página',
            'departamento': 'Departamento al que corresponde',
            'year': 'Año',
            'vigente': 'Formato vigente',
        }
        widgets = {
            'header': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'headerimg-input',  # ID para JavaScript
            }),
            'footer': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'footerimg-input',  # ID para JavaScript
            }),
            'departamento': forms.Select(attrs={'class': 'form-control',}),
            'year': forms.Select(attrs={'class': 'form-control',}),
        }

class FormatoDepartamentoUpdateForm(forms.ModelForm):
    class Meta:
        model = FormatoDepartamento
        exclude = ('departamento', 'year')
        labels = {
            'header': 'Imagen de encabezado',
            'footer': 'Imagen de pie de página',
            'departamento': 'Departamento al que corresponde',
            'year': 'Año',
            'vigente': 'Formato vigente',
        }
        widgets = {
            'header': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'headerimg-input',  # ID para JavaScript
            }),
            'footer': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'footerimg-input',  # ID para JavaScript
            }),
        }

class FormatoConstanciaForm(forms.ModelForm):
    class Meta:
        model = FormatoConstancia
        fields = '__all__'
        labels = {
            'header': 'Imagen de encabezado',
            'año': 'Año',
            'vigente': 'Formato vigente',
        }
        widgets = {
            'header': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'headerimg-input',  # ID para JavaScript
            }),
            'year': forms.Select(attrs={'class': 'form-control',}),
        }

class FormatoConstanciaUpdateForm(forms.ModelForm):
    class Meta:
        model = FormatoConstancia
        exclude = ('year',)
        labels = {
            'header': 'Imagen de encabezado',
            'año': 'Año',
            'vigente': 'Formato vigente',
        }
        widgets = {
            'header': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'headerimg-input',  # ID para JavaScript
            }),
        }