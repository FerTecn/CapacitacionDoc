import os
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from catalogos.models import Autoridad, Docente, Lugar, Instructor, ValorCalificacion
from plancapacitacion.models import RegistroCurso
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Q

# Create your models here.
class Evento(models.Model):
    curso= models.ForeignKey(RegistroCurso, on_delete=models.CASCADE, null=True)
    lugar=models.ForeignKey(Lugar,on_delete=models.SET_NULL, null=True )
    fechaInicio = models.DateField(null=True, blank=True)
    fechaFin = models.DateField(null=True, blank=True)
    horaInicio = models.TimeField(null=True, blank=True)  # Hora de inicio
    horaFin = models.TimeField(null=True, blank=True)  # Hora de fin
    cupo_inscritos = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100000000)],
        verbose_name="Cantidad de docentes a inscribir"
    )
    
    def __str__(self):
        return f"{self.curso} - {self.fechaInicio} a {self.fechaFin}"
    class Meta:
        verbose_name_plural = 'Eventos'

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True)
    aceptado = models.BooleanField(default=False)  # Campo para rastrear estado de aceptación
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Docente que se inscribe

    def clean(self):
        """ Verifica que el curso no haya empezado"""
        if self.evento.fechaInicio < now().date():
            raise ValidationError("El curso ya ha empezado. No puedes inscribirte.")
        
        """ Verifica que la inscripción no tenga empalmes de horario con otras inscripciones del usuario. """
        if Inscripcion.objects.filter(
            Q(usuario=self.usuario) &
            ~Q(pk=self.pk) &
            Q(evento__fechaInicio__lte=self.evento.fechaFin) &
            Q(evento__fechaFin__gte=self.evento.fechaInicio) &
            Q(evento__horaInicio__lt=self.evento.horaFin) &
            Q(evento__horaFin__gt=self.evento.horaInicio)
        ).exists():
            raise ValidationError("No puedes inscribirte en eventos con horarios empalmados.")
        
        """ Verifica que no se haya superado el cupo máximo del evento """
        inscritos_actuales = Inscripcion.objects.filter(evento=self.evento, aceptado=True).exclude(pk=self.pk).count()
        if inscritos_actuales >= self.evento.cupo_inscritos:
            raise ValidationError("Este curso ya ha alcanzado el cupo máximo de inscripciones.")

    def save(self, *args, **kwargs):
        if self.aceptado:  # Solo validamos si se va a aceptar
            self.clean()
        super().save(*args, **kwargs)
        
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

class CriteriosSeleccionInstructor(models.Model):
    noSolicitud = models.CharField(max_length=40)
    curso = models.ForeignKey(RegistroCurso, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(auto_now_add=True)

    criterio1 = models.BooleanField(default=False)
    criterio2 = models.BooleanField(default=False)
    criterio3 = models.BooleanField(default=False)
    criterio4 = models.BooleanField(default=False)
    criterio5 = models.BooleanField(default=False)
    criterio6 = models.BooleanField(default=False)
    criterio7 = models.BooleanField(default=False)
    criterio8 = models.BooleanField(default=False)
    criterio9 = models.BooleanField(default=False)
    criterio10 = models.BooleanField(default=False)
    
    # Nuevos campos
    total = models.PositiveSmallIntegerField(default=0, editable=False)
    aceptado = models.BooleanField(default=False, verbose_name="Aceptado")
    
    evaluador = models.ForeignKey(
        Autoridad,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Evaluador",
        related_name='evaluador_instructor'
    )
    
    titular = models.ForeignKey(
        Autoridad,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Titular",
        related_name='titular'
    )

    class Meta:
        verbose_name = "Criterio de selección de instructor"
        verbose_name_plural = "Criterios de selección de instructores"

    def __str__(self):
        return f"{self.noSolicitud} - {self.curso} - {self.evaluador}"

    def calcular_total(self):
        """Calcula el número de criterios cumplidos"""
        criterios = [
            self.criterio1, self.criterio2, self.criterio3,
            self.criterio4, self.criterio5, self.criterio6,
            self.criterio7, self.criterio8, self.criterio9,
            self.criterio10
        ]
        return sum(1 for criterio in criterios if criterio)

    def save(self, *args, **kwargs):
        """Actualiza total y aceptado automáticamente al guardar"""
        self.total = self.calcular_total()
        self.aceptado = self.total >= 8  # True si cumple 8 o más criterios
        super().save(*args, **kwargs)

    @property
    def porcentaje_cumplimiento(self):
        """Devuelve el porcentaje de criterios cumplidos"""
        return (self.total / 10) * 100 if self.total > 0 else 0