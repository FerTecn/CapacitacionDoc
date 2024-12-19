from django.db import models
from catalogos.models import Lugar, Instructor
from plancapacitacion.models import registroCurso


# Create your models here.
class Evento(models.Model):
    curso= models.ForeignKey(registroCurso, on_delete=models.CASCADE, null=True)
    instructor=models.ForeignKey(Instructor,on_delete=models.SET_NULL, null=True, blank=True )
    lugar=models.ForeignKey(Lugar,on_delete=models.SET_NULL, null=True )
    fecha = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.curso} - {self.fecha}"
    class Meta:
        verbose_name_plural = 'Eventos'

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.evento}"

    
class asistencia(models.Model):
    clave = models.CharField(max_length=10)
    nombre=models.CharField(max_length=40)
    periodo=models.CharField(max_length=40)
    lugar=models.CharField(max_length=40)
    horas=models.CharField(max_length=40)
    instructor=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.nombre} {self.periodo} {self.lugar} {self.horas} {self.instructor} "
    #FALTA UNA PESTAÑA DONDE SE MUESTRAN LOS DOCENTES INSCRITOS PARA PONER ASISTENCIA

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
    #FALTA UNA PESTAÑA DONDE SE MUESTRAN LOS DOCENTES INSCRITOS PARA ASINGAR CALIFICACION

class Hora(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.hora_inicio} - {self.hora_fin}"
