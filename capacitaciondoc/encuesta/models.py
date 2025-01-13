from django.db import models

# Create your models here.
class Encuesta(models.Model):
    #Catagoría del instructor
    instructor1= models.IntegerField()
    instructor2= models.IntegerField()
    instructor3= models.IntegerField()
    instructor4= models.IntegerField()
    instructor5= models.IntegerField()
    instructor6= models.IntegerField()
    instructor7= models.IntegerField()
    
    #Categoria del curso
    curso1= models.IntegerField()
    curso2= models.IntegerField()
    curso3= models.IntegerField()
    curso4= models.IntegerField()
    
    #Categoria del material
    material1= models.IntegerField()
    material2= models.IntegerField()
    material3= models.IntegerField()
    
    #Categoria de la infraestructura
    insfraestructura1= models.IntegerField()
    insfraestructura2= models.IntegerField()
    insfraestructura3= models.IntegerField()
    insfraestructura4= models.IntegerField()
    insfraestructura5= models.IntegerField(null=True, blank=True)
    insfraestructura6= models.IntegerField(null=True, blank=True)
    
    comentarios= models.TextField(blank=True, null=True) 
    
    def __str__(self):
        return f"Encuesta #{self.id} - {self.fecha_respuesta}"