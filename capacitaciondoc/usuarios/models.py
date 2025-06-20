from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models

#Agregado para crear un administrador de usuarios, esto permite que cuando creemos un superusuario no se solicite el nombre de usuario
#pero solicita CURP y será asignado el CURP como el nombre de usuario automaticamente
class CustomUserManager(BaseUserManager):
    def create_user(self, curp, password=None, **extra_fields):
        if not curp:
            raise ValueError('El campo CURP debe ser proporcionado.')
        extra_fields.setdefault('is_active', True)
        user = self.model(curp=curp, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, curp, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(curp, password, **extra_fields)
    

class CustomUser(AbstractUser):
    last_name_paterno = models.CharField(max_length=50, verbose_name="Apellido paterno")
    last_name_materno = models.CharField(max_length=50, verbose_name="Apellido materno")
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    rol = models.CharField(
        max_length=50,
        choices=[
            ('Docente', 'Docente'), 
            ('Instructor', 'Instructor'), 
            ('Jefe de Capacitación', 'Jefe de Capacitación'),
            ('Jefe Académico', 'Jefe Académico'),
            ('Subdirección', 'Subdirección')
        ],
        verbose_name="Rol"
    )
    email = models.EmailField(unique=True, blank=True, null=True,verbose_name="Correo electrónico")

    USERNAME_FIELD = 'curp'  #Agregado: Define al CURP como el identificador inicial para permitir el Login con CURP
    objects = CustomUserManager()  # Asigna el nuevo UserManager
    
    def save(self, *args, **kwargs):
        # Asignar el valor de CURP al campo username
        self.username = self.curp
        is_new = self.pk is None  # ¿Es un usuario nuevo?
        super().save(*args, **kwargs)  # Llamar al método save del modelo base

        # Si es nuevo usuario, asignar al grupo según su rol
        if is_new and self.rol:
            try:
                group, created = Group.objects.get_or_create(name=self.rol)
                # Primero limpiar grupos existentes (opcional, evita duplicados si cambió rol)
                self.groups.clear()
                self.groups.add(group)
            except Exception as e:
                print(f"Error asignando grupo al usuario {self}: {e}")

    def __str__(self):
        return f"{self.first_name} {self.last_name_paterno} {self.last_name_materno} - {self.rol}"
    
    def get_user_full_name(self):
        return f"{self.first_name} {self.last_name_paterno} {self.last_name_materno}"