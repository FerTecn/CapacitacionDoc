import os
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from catalogos.models import Docente, Lugar, Instructor, ValorCalificacion
from plancapacitacion.models import RegistroCurso


# Create your models here.
class Evento(models.Model):
    curso= models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True)
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

class OficioComision(models.Model):
    no_oficio = models.CharField(max_length=40)
    nomenclatura = models.CharField(max_length=20)
    fecha=models.DateField()
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.no_oficio} - {self.docente} - {self.fecha}"
    
    class Meta:
        verbose_name_plural = 'Oficios de comisión'

class Calificacion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, null=True)
    calificacion = models.ForeignKey(ValorCalificacion, on_delete=models.SET_NULL, null=True)  # Calificación seleccionada
    fecha_calificacion = models.DateField(auto_now_add=True)  # Fecha en que se registra la calificación

    def __str__(self):
        return f"{self.inscripcion.usuario.first_name} {self.inscripcion.usuario.last_name_paterno} - {self.inscripcion.evento.curso.nombre} - {self.calificacion}"

    class Meta:
        verbose_name_plural = 'Calificaciones'
        unique_together = ('inscripcion', 'fecha_calificacion')

def evidencia_upload_path(instance, filename):
    """Guarda los archivos en: media/evidencias/curso/instructor siempre como 'evidencia.png'."""

    curso_slug = slugify(instance.evento.curso.nombre)
    instructor_slug = slugify(instance.evento.curso.instructor.user.get_user_full_name())

    folder_path = os.path.join("evidencias", curso_slug, instructor_slug)
    return os.path.join(folder_path, "evidencia.jpg")  # Siempre guardado como "evidencia.jpg"

class Evidencia(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    evidencia = models.BooleanField(default=False)
    archivo_evidencia = models.ImageField(upload_to=evidencia_upload_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Evidencias'


    def save(self, *args, **kwargs):
        """ Marcar `evidencia = True` si se sube un archivo """
        if self.archivo_evidencia:
            self.evidencia = True
        else:
            self.evidencia = False
        super().save(*args, **kwargs)
