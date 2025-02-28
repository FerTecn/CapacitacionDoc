from django.db import models
from django.conf import settings
from eventos.models import Inscripcion
from plancapacitacion.models import RegistroCurso

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
    
    def __str__(self):
        return f"Encuesta #{self.id} de {self.inscripcion.usuario} para {self.inscripcion.evento.curso.nombre} - {self.fecha_realizacion}"

    class Meta:
        verbose_name_plural = 'Encuestas'
        