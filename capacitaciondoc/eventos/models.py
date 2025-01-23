from django.db import models
from catalogos.models import Lugar, Instructor
from plancapacitacion.models import RegistroCurso


# Create your models here.
class Evento(models.Model):
    curso= models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True)
    instructor=models.ForeignKey(Instructor,on_delete=models.SET_NULL, null=True, blank=True )
    lugar=models.ForeignKey(Lugar,on_delete=models.SET_NULL, null=True )
    fecha = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.curso} - {self.fecha}"
    class Meta:
        verbose_name_plural = 'Eventos'

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    aceptado = models.BooleanField(default=False)  # Campo para rastrear estado de aceptación

    def __str__(self):
        return f"{self.evento}"
    
    class Meta:
        verbose_name_plural = 'Inscripcion'
    
class asistencia(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    #Docentes
    
    def __str__(self):
        return f"{self.evento}"

    class Meta:
        verbose_name_plural = 'Asistencia'
class oficioComision(models.Model):
    clave = models.CharField(max_length=10)
    fecha=models.CharField(max_length=40)
    nombre=models.CharField(max_length=40)
    lugar=models.CharField(max_length=40)
    horas=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.fecha} {self.nombre} {self.lugar} {self.horas} "
    
    class Meta:
        verbose_name_plural = 'Oficios de comisión'

    class Meta:
        verbose_name_plural = 'Inscripciones'
class calificacion(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
    periodo=models.CharField(max_length=40)
    lugar=models.CharField(max_length=40)
    horas=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.nombre} {self.periodo} {self.lugar} {self.horas} "
    
    class Meta:
        verbose_name_plural = 'Calificaciones'
