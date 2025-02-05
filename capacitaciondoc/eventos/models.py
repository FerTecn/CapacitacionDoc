import os
from django.db import models
from django.conf import settings
from catalogos.models import Docente, Lugar, Instructor
from plancapacitacion.models import RegistroCurso


# Create your models here.
class Evento(models.Model):
    curso= models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True)
    instructor=models.ForeignKey(Instructor,on_delete=models.SET_NULL, null=True, blank=True )
    lugar=models.ForeignKey(Lugar,on_delete=models.SET_NULL, null=True )
    fechaInicio = models.DateField(null=True, blank=True)
    fechaFin = models.DateField(null=True, blank=True)
    horaInicio = models.TimeField(null=True, blank=True)  # Hora de inicio
    horaFin = models.TimeField(null=True, blank=True)  # Hora de fin
    
    
    def __str__(self):
        return f"{self.curso} - {self.fechaInicio} a {self.fechaFin}"
    class Meta:
        verbose_name_plural = 'Eventos'

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    aceptado = models.BooleanField(default=False)  # Campo para rastrear estado de aceptación
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Docente que se inscribe

    def __str__(self):
        return f"{self.evento}"
    
    class Meta:
        verbose_name_plural = 'Inscripcion'
        unique_together = ('evento', 'usuario')
    
class Asistencia(models.Model):
    inscripcion =models.ForeignKey(Inscripcion, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(null=True)
    asistio = models.BooleanField(default=False)
    
    def __str__(self):
        estado = "Presente" if self.asistio else "Ausente"
        return f"{self.inscripcion.usuario.first_name} {self.inscripcion.usuario.last_name_paterno} - {self.inscripcion.evento.curso.nombre} - {estado}"

    class Meta:
        verbose_name_plural = 'Asistencias'
        unique_together = ('inscripcion', 'fecha')
    #     db_table = 'eventos_asistencia'

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
# class calificacion(models.Model):
#     clave = models.CharField(max_length=10)
#     nombre=models.CharField(max_length=40)
#     periodo=models.CharField(max_length=40)
#     lugar=models.CharField(max_length=40)
#     horas=models.CharField(max_length=40)
    
#     def __str__(self):
#         return f"{self.nombre} {self.periodo} {self.lugar} {self.horas} "
    
#     class Meta:
#         verbose_name_plural = 'Calificaciones'


class Evidencia(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    evidencia = models.BooleanField(default=False)
    archivo_evidencia = models.ImageField(upload_to='evidencias/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Evidencias'


    def save(self, *args, **kwargs):
        """ Marcar `evidencia = True` si se sube un archivo """
        if self.archivo_evidencia:
            self.evidencia = True
        else:
            self.evidencia = False
        super().save(*args, **kwargs)
