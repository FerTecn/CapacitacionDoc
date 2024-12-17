from django.db import models
from catalogos.models import Instructor
from catalogos.models import Periodo
from catalogos.models import Sede
from catalogos.models import Dirigido
from catalogos.models import PerfilCurso
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class registroCurso(models.Model):
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
        if not validarCurso.objects.filter(curso=self).exists():
            validarCurso.objects.create(curso=self)
    
    class Meta:
        verbose_name_plural = 'Registro de cursos'
    
class validarCurso(models.Model):
    curso= models.ForeignKey(registroCurso, on_delete=models.CASCADE)

    def __str__(self):
        return f"Curso: {self.curso.nombre} "
    
    class Meta:
        verbose_name_plural = 'Validación de cursos'
      
class fichaTecnica(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
    instructor=models.CharField(max_length=40)
    justificacion=models.CharField(max_length=200)
    objetivo=models.CharField(max_length=200)
    descripcion=models.CharField(max_length=200)
    horas=models.CharField(max_length=40)
    contenido=models.CharField(max_length=200)
    competencias=models.CharField(max_length=200)
    departamento=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.nombre} {self.instructor} {self.horas} {self.departamento}"
    
    class Meta:
        verbose_name_plural = 'Ficha técnica'