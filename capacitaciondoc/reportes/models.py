from django.db import models

from encuesta.models import Encuesta
from catalogos.models import Docente, Instructor
from eventos.models import Calificacion, Evento

# Create your models here.
class ConstanciaInstructor(models.Model):
    curso = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True)

    def __str__(self):
        return f'{self.curso.curso} - {self.instructor.user.get_user_full_name()} - {self.fecha}'

class ConstanciaDocente(models.Model):
    curso = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True)
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE, null=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True)

    def __str__(self):
        return f'{self.curso.curso.nombre} - {self.docente.user.get_user_full_name()} - {self.fecha}'