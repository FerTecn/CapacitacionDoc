from django.db import models

# Create your models here.
class Instructor(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
    apPaterno=models.CharField(max_length=40)
    apMaterno=models.CharField(max_length=40)
    fechaNac=models.DateField(null=True, blank=True)
    CURP = models.CharField(max_length=18, null=True)
    RFC = models.CharField(max_length=13, null=True)
    telefono=models.CharField(max_length=10, null=True)
    email=models.CharField(max_length=50, null=True)

    #Formación academica
    institucion=models.CharField(max_length=40, null=True, blank=True)
    grado = models.ForeignKey('GradoAcademico', on_delete=models.CASCADE, null=True)
    cedulaProf=models.CharField(max_length=8, null=True)
    
    #Experiencia laboral
    puesto=models.CharField(max_length=40, null=True, blank=True)
    empresa=models.CharField(max_length=40, null=True, blank=True)
    
    #Experiencia docente
    materia=models.CharField(max_length=40, null=True, blank=True)
    periodo=models.CharField(max_length=40, null=True, blank=True)
    
    #Participacion como instructor
    curso=models.CharField(max_length=40, null=True, blank=True)
    nombreEmpresa=models.CharField(max_length=40, null=True, blank=True)
    duracionHoras=models.IntegerField(max_length=40, null=True, blank=True)
    fechaParticipacion=models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apPaterno} {self.apMaterno} {self.grado}"
    
    class Meta:
        verbose_name_plural = 'Instructores'
        
class GradoAcademico(models.Model):
    clave = models.CharField(max_length=10)
    grado = models.CharField(max_length=40) 
 
    def __str__(self):
        return self.grado
    
    class Meta:
        verbose_name_plural = 'Grado académico'

class Lugar(models.Model):
    clave = models.CharField(max_length=10)
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
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
    apPaterno=models.CharField(max_length=40)
    apMaterno=models.CharField(max_length=40)
    fechaNac=models.DateField(null=True, blank=True)
    genero = models.ForeignKey('Genero', on_delete=models.CASCADE) 
    CURP=models.CharField(max_length=18)
    RFC=models.CharField(max_length=13)
    telefono=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)
        
    def __str__(self):
        return f"{self.nombre} {self.apPaterno} {self.apMaterno} {self.departamento}"
    
    class Meta:
        verbose_name_plural = 'Docentes'
    
class Genero(models.Model):
    clave = models.CharField(max_length=10)
    genero=models.CharField(max_length=20)

    def __str__(self):
        return self.genero
    
    class Meta:
        verbose_name_plural = 'Genero'

class Departamento(models.Model):
    clave = models.CharField(max_length=10)
    departamento=models.CharField(max_length=40)

    def __str__(self):
        return self.departamento
    
    class Meta:
        verbose_name_plural = 'Departamentos'

class Periodo(models.Model):
    clave=models.CharField(max_length=50)
    inicioPeriodo=models.DateField()
    finPeriodo=models.DateField()
    
    def __str__(self):
        return f"{self.inicioPeriodo} {self.finPeriodo}"
    
    class Meta:
        verbose_name_plural = 'Periodos'
    
class Dirigido(models.Model):
    clave = models.CharField(max_length=10)
    dirigido=models.CharField(max_length=20)

    def __str__(self):
        return self.dirigido
    
    class Meta:
        verbose_name_plural = 'Dirigido a'
    
class PerfilCurso(models.Model):
    clave = models.CharField(max_length=10)
    perfilCurso=models.CharField(max_length=40)
    
    def __str__(self):
        return self.perfilCurso
    
    class Meta:
        verbose_name_plural = 'Perfiles de Curso'