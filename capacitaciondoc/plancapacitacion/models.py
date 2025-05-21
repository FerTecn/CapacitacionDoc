from django.db import models
from catalogos.models import Autoridad, Carrera, Departamento, Instructor
from catalogos.models import Periodo
from catalogos.models import Sede
from catalogos.models import Dirigido
from catalogos.models import PerfilCurso

from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class RegistroCurso(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=100)
    objetivo=models.TextField(max_length=200)
    periodo=models.ForeignKey(Periodo, on_delete=models.CASCADE)
    sede=models.ForeignKey(Sede, on_delete=models.CASCADE)
    horas=models.IntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    dirigido=models.ForeignKey(Dirigido, on_delete=models.CASCADE)
    perfilCurso=models.ForeignKey(PerfilCurso, on_delete=models.CASCADE)
    aceptado=models.BooleanField (default=False)
    
    def __str__(self):
        return f"{self.nombre} {self.periodo} {self.horas} {self.instructor} {self.aceptado}"
    
    def save(self, *args, **kwargs):
        # Llama al método original de guardado
        super().save(*args, **kwargs)
        # Asegúrate de que el curso no esté ya en validarCurso
        if not ValidarCurso.objects.filter(curso=self).exists():
            ValidarCurso.objects.create(curso=self)
        if not FichaTecnica.objects.filter(curso=self).exists():
            FichaTecnica.objects.create(curso=self)
    
    class Meta:
        verbose_name_plural = 'Registro de cursos'
        db_table = 'plancapacitacion_registrocurso'
    
class ValidarCurso(models.Model):
    curso= models.ForeignKey(RegistroCurso, on_delete=models.CASCADE)

    def __str__(self):
        return f"Curso: {self.curso.nombre} "
    
    class Meta:
        verbose_name_plural = 'Validación de cursos'

class FichaTecnica(models.Model):
    curso = models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True, blank=True)
    introduccion=models.TextField()
    justificacion=models.TextField()
    servicio = models.CharField(
        max_length=20,
        choices=[
            ('Curso', 'Curso'), 
            ('Taller', 'Taller'), 
        ],
    )
    elementosDidacticos = models.TextField()
    competencias = models.TextField()
    fuentes = models.TextField()
    jefeDesarrolloAcademico = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Ficha de {self.curso.nombre} {self.curso.instructor} {self.servicio}"
    
    class Meta:
        verbose_name_plural = 'Fichas técnicas'

class ContenidoTematico(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, verbose_name=("Ficha Técnica"), on_delete=models.CASCADE, null=True, blank=True, related_name="contenidos_tematicos")
    tema = models.CharField(max_length=200)
    tiempo = models.IntegerField()
    actividades = models.TextField()

    class Meta:
        verbose_name_plural="Contenidos Temáticos"

class CriterioEvaluacion(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, verbose_name=("Ficha Técnica"), on_delete=models.CASCADE, null=True, blank=True, related_name="criterios_evaluacion")
    criterio = models.CharField(max_length=200)
    valor = models.IntegerField()
    instrumento = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural="Criterios de Evaluación"

# Deteccionnecesidades
class DeteccionNecesidades(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(auto_now_add=True)
    jefeDepAcademico = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True, related_name="jefeDepAcademico")
    presidenteAcademia = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True, related_name="presidenteAcademia")

class AsignaturaDeteccionNecesidades(models.Model):
    deteccionNecesidades = models.ForeignKey(DeteccionNecesidades, on_delete=models.SET_NULL, null=True)
    asignatura = models.CharField(max_length=200)
    contenido = models.TextField()
    noProfesores = models.IntegerField()
    periodoInicio = models.DateField()
    periodoFin = models.DateField()
    instructores = models.ManyToManyField(Instructor)

# ConcentradoDiagnostico
class ConcentradoDiagnostico(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    fecha_realizacion = models.DateField(auto_now_add=True)
    jefeDepAcademico = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True, related_name="jefe_dep_academico")
    presidenteAcademia = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True, related_name="presidente_academia")

class ActividadAsignatura(models.Model):
    diagnostico = models.ForeignKey(ConcentradoDiagnostico, on_delete=models.SET_NULL, null=True)
    actividad = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200, choices=[
        ('Taller', 'Taller'),
        ('Curso', 'Curso'),
        ('Conferencia', 'Conferencia'),
    ])
    noProfesores = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    fecha_realizacion = models.DateField()

    
    def mes_anio(self):
        """Formato MM/AAAA para la fecha"""
        return self.fecha_realizacion.strftime("%B de %Y")

    def __str__(self):
        return f"{self.nombre_actividad} ({self.get_tipo_display()})"

class ActividadModulosEspecialidad(models.Model):
    diagnostico = models.ForeignKey(ConcentradoDiagnostico, on_delete=models.SET_NULL, null=True)
    actividad = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200, choices=[
        ('Taller', 'Taller'),
        ('Curso', 'Curso'),
        ('Conferencia', 'Conferencia'),
    ])
    carreras = models.ManyToManyField(Carrera, verbose_name="Carreras atendidas")
    noProfesores = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    fechaRealizacion = models.DateField()

    def carreras_lista(self):
        """Devuelve string con nombres de carreras"""
        return ", ".join(c.carrera for c in self.carreras.all())

    def mes_anio(self):
        return self.fechaRealizacion.strftime("%B de %Y")

    def __str__(self):
        return f"{self.actividad} ({self.carreras_lista})"