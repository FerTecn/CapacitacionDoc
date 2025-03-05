from django.db import models
from eventos.models import Inscripcion

from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Encuesta(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='encuestas', null=True)
    fecha_realizacion = models.DateTimeField(auto_now_add=True, null=True)
    
    #Catagoría del instructor
    instructor1= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor2= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor3= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor4= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor5= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor6= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    instructor7= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    
    #Categoria del curso
    curso1= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    curso2= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    curso3= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    curso4= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    
    #Categoria del material
    material1= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    material2= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    material3= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    
    #Categoria de la infraestructura
    insfraestructura1= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    insfraestructura2= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    insfraestructura3= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    insfraestructura4= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)])
    insfraestructura5= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)], null=True, blank=True)
    insfraestructura6= models.IntegerField(choices=[(i, str(i)) for i in range (1, 6)], null=True, blank=True)
    
    comentarios= models.TextField(blank=True, null=True) 

    def clean(self):
        # Verificar si el curso ha comenzado y no ha finalizado
        if self.inscripcion:
            curso = self.inscripcion.evento.curso
            curso_comenzado = curso.fechaInicio <= timezone.now()
            curso_finalizado = curso.fechaFin < timezone.now()

            if not curso_comenzado:
                raise ValidationError('No puedes realizar la encuesta hasta que el curso haya comenzado.')

            if curso_finalizado:
                raise ValidationError('El curso ya ha finalizado. No puedes realizar la encuesta.')
    
    def __str__(self):
        return f"Encuesta #{self.id} de {self.inscripcion.usuario} para {self.inscripcion.evento.curso.nombre} - {self.fecha_realizacion}"

    class Meta:
        verbose_name_plural = 'Encuestas'
        