from django.db import models
from catalogos.models import Instructor
from catalogos.models import Periodo
from catalogos.models import Sede
from catalogos.models import Dirigido
from catalogos.models import PerfilCurso
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class RegistroCurso(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
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
    # clave = models.CharField(max_length=10)
    # nombre=models.CharField(max_length=40)
    curso = models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True, blank=True)
    # instructor=models.CharField(max_length=40)
    introduccion=models.TextField()
    justificacion=models.TextField()
    servicio = models.CharField(
        max_length=20,
        choices=[
            ('Curso', 'Curso'), 
            ('Taller', 'Taller'), 
        ],
    )
    elementosDidacticos = models.CharField(max_length=200)
    competencias = models.CharField(max_length=200)
    fuentes = models.TextField()
    
    def __str__(self):
        return f"Ficha de {self.curso.nombre} {self.curso.instructor} {self.servicio}"
    
    class Meta:
        verbose_name_plural = 'Fichas técnicas'

class ContenidoTematico(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, verbose_name=("Ficha Técnica"), on_delete=models.CASCADE, null=True, blank=True, related_name="contenidos_tematicos")
    tema = models.CharField(max_length=200)
    tiempo = models.IntegerField()
    actividades = models.TextField()

class CriterioEvaluacion(models.Model):
    fichaTecnica = models.ForeignKey(FichaTecnica, verbose_name=("Ficha Técnica"), on_delete=models.CASCADE, null=True, blank=True, related_name="criterios_evaluacion")
    criterio = models.CharField(max_length=200)
    valor = models.IntegerField()
    instrumento = models.CharField(max_length=200)