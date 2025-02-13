import locale
from django.db import models

from usuarios.models import CustomUser

# Create your models here.
class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    clave = models.CharField(max_length=10)
    fechaNac=models.DateField(null=True)
    RFC = models.CharField(max_length=13, null=True)
    telefono=models.CharField(max_length=10, null=True)    
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name_paterno} {self.user.last_name_materno}"
    
    class Meta:
        verbose_name_plural = 'Instructores'

class FormacionAcademica(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='formaciones_academicas')
    institucion = models.CharField(max_length=40)
    grado = models.ForeignKey('GradoAcademico', on_delete=models.SET_NULL, null=True, verbose_name="Grado Académico")

    cedulaProf = models.CharField(max_length=8, null=True)

    def __str__(self):
        return f"{self.institucion} - {self.cedulaProf}"
    
class ExperienciaLaboral(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='experiencias_laborales')
    puesto = models.CharField(max_length=40)
    empresa = models.CharField(max_length=60)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"
    
class ExperienciaDocente(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='experiencias_docentes')
    materia = models.CharField(max_length=40)
    periodo = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.materia} - {self.periodo}"

class ParticipacionInstructor(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='participaciones_instructor')
    curso = models.CharField(max_length=40)
    nombreEmpresa = models.CharField(max_length=40)
    duracionHoras = models.IntegerField()
    periodoInicio = models.DateField(null=True)
    periodoFin = models.DateField(null=True)

    def __str__(self):
        return f"{self.curso} en {self.nombreEmpresa}"

class GradoAcademico(models.Model):
    grado = models.CharField(max_length=40) 

    def __str__(self):
        return self.grado
    
    class Meta:
        verbose_name_plural = 'Grado académico'

class Lugar(models.Model):
    #clave = models.CharField(max_length=10)
    nombreEdificio = models.CharField(max_length=40)
    ubicacion = models.CharField(max_length=40)
 
    def __str__(self):
        return f"{self.nombreEdificio} {self.ubicacion}"  
    
    class Meta:
        verbose_name_plural = 'Lugares'
    
class Sede(models.Model):
    clave=models.CharField(max_length=10)
    sede = models.CharField(max_length=100) 
    
    def __str__(self):
        return self.sede
    
    class Meta:
        verbose_name_plural = 'Sedes'
    
class Docente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    clave = models.CharField(max_length=10)
    fechaNac=models.DateField(null=True)
    genero = models.ForeignKey('Genero', on_delete=models.SET_NULL, null=True, verbose_name="Género")
    RFC=models.CharField(max_length=13, null= True)
    telefono=models.CharField(max_length=10, null=True)
    departamento = models.ForeignKey('Departamento', on_delete=models.SET_NULL, null=True, verbose_name="Departamento")
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name_paterno} {self.user.last_name_materno} {self.departamento}"
    
    class Meta:
        verbose_name_plural = 'Docentes'

class Genero(models.Model):
    genero=models.CharField(max_length=20)

    def __str__(self):
        return self.genero
    
    class Meta:
        verbose_name_plural = 'Genero'

class Departamento(models.Model):
    nomenclatura = models.CharField(max_length=10, null=True)
    numerodepartamento=models.CharField(max_length=54, null=True)
    departamento=models.CharField(max_length=40)
    nombreJefe=models.CharField(max_length=54, null=True)
    apParternoJefe=models.CharField(max_length=40, null=True)
    apMaternoJefe=models.CharField(max_length=40, null=True)
    telefono=models.CharField(max_length=40, null=True)
    email=models.CharField(max_length=60, null=True)
    paginaWeb=models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.departamento
    
    class Meta:
        verbose_name_plural = 'Departamentos'

class Periodo(models.Model):
    clave=models.TextField(max_length=50)
    inicioPeriodo=models.DateField()
    finPeriodo=models.DateField()


    def save(self, *args, **kwargs):
        # Establecer temporalmente el idioma a español
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Configuración para sistemas Linux/MacOS
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

        # Generar clave con el formato "Mes Año - Mes Año"
        self.clave = f"{self.inicioPeriodo.strftime('%B %Y').capitalize()} - {self.finPeriodo.strftime('%B %Y').capitalize()}"

        # Restaurar el idioma al predeterminado del sistema
        locale.setlocale(locale.LC_TIME, '')
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return f"{self.clave}"
    
    class Meta:
        verbose_name_plural = 'Periodos'
    
class Dirigido(models.Model):
    #clave = models.CharField(max_length=10)
    dirigido=models.CharField(max_length=20)

    def __str__(self):
        return self.dirigido
    
    class Meta:
        verbose_name_plural = 'Dirigido a'
    
class PerfilCurso(models.Model):
    #clave = models.CharField(max_length=10)
    perfilCurso=models.CharField(max_length=40)
    
    def __str__(self):
        return self.perfilCurso
    
    class Meta:
        verbose_name_plural = 'Perfiles de Curso'

class Director(models.Model):
    nombre=models.CharField(max_length=40)
    apPaterno=models.CharField(max_length=40)
    apMaterno=models.CharField(max_length=40)
    puesto=models.CharField(max_length=40)
    estatus=models.BooleanField()

class ValorCalificacion(models.Model):
    valorCalificacion =  models.CharField(max_length=40)

    def __str__(self):
        return self.valorCalificacion
    
    class Meta:
        verbose_name_plural = 'Valores de Calificación'
        verbose_name = 'Valor de Calificación'