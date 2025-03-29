from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from encuesta.models import Encuesta
from catalogos.models import Autoridad, Docente, Instructor
from eventos.models import Calificacion, Evento

# Create your models here.
class ConstanciaInstructor(models.Model):
    curso = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True)
    director = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Validación de que el curso debe haber terminado antes de generar la constancia
        if self.curso.fechaFin > now().date():
            raise ValidationError("No se puede generar la constancia hasta que el curso haya terminado.")

    def save(self, *args, **kwargs):
        """ Llama a la validación antes de guardar el objeto. """
        self.clean()  # Llama a la validación
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.curso.curso} - {self.instructor.user.get_user_full_name()} - {self.fecha}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['curso', 'instructor'], name='unique_constancia_instructor')
        ]
        verbose_name_plural = "Constancias de instructores"
        verbose_name = "Constancia de instructor"

class ConstanciaDocente(models.Model):
    curso = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE, null=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True)
    director = models.ForeignKey(Autoridad, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # Validación de que el curso debe haber terminado antes de generar la constancia
        if self.curso.fechaFin > now().date():
            raise ValidationError("No se puede generar la constancia hasta que el curso haya terminado.")

    def save(self, *args, **kwargs):
        """ Llama a la validación antes de guardar el objeto. """
        self.clean()  # Llama a la validación
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.curso.curso.nombre} - {self.docente.user.get_user_full_name()} - {self.fecha}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['curso', 'docente'], name='unique_constancia_docente')
        ]
        verbose_name_plural = "Constancias de docentes"
        verbose_name = "Constancia de docente"