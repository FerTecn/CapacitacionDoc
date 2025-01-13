from django.contrib.auth.models import AbstractUser
from django.db import models
 
class CustomUser(AbstractUser):
    last_name_paterno = models.CharField(max_length=50, verbose_name="Apellido paterno")
    last_name_materno = models.CharField(max_length=50, verbose_name="Apellido materno")
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    rol = models.CharField(
        max_length=50,
        choices=[('Docente', 'Docente'), ('Instructor', 'Instructor')],
        verbose_name="Rol"
    )
   
    USERNAME_FIELD = 'curp'  #Agregado: Define al CURP como el identificador inicial para permitir el Login con CURP
    def save(self, *args, **kwargs):
        # Asignar el valor de CURP al campo username
        self.username = self.curp
        super().save(*args, **kwargs)  # Llamar al método save del modelo base
 
    def __str__(self):
        return f"{self.first_name} {self.last_name_paterno} {self.last_name_materno} - {self.rol}"