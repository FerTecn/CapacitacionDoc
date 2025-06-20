from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.db.models.signals import post_migrate
        from django.core.exceptions import ObjectDoesNotExist

        # Permisos
        def configurar_grupos_y_permisos(sender, **kwargs):
            # Crea o obtiene los grupos en la BD
            academico_group, created = Group.objects.get_or_create(name='Jefe Académico')
            capacitacion_group, created = Group.objects.get_or_create(name='Jefe de Capacitación')
            subdireccion_group, created = Group.objects.get_or_create(name='Subdirección')

            try:
                # Obtener permisos definidos en los modelos
                permisos_usuarios = Permission.objects.filter(content_type__app_label='usuarios', codename__icontains='customuser')

                def limpiar_permisos(grupo):
                    permisos_actuales = grupo.permissions.filter(content_type__app_label='usuarios')
                    grupo.permissions.remove(*permisos_actuales)

                limpiar_permisos(academico_group)
                limpiar_permisos(capacitacion_group)
                limpiar_permisos(subdireccion_group)

                # Asignar permisos a los grupos

                # Grupo Jefe Académico: puede ver usuarios, pero no editarlos
                academico_group.permissions.add(
                    *permisos_usuarios.filter(codename__startswith='view'),
                    *permisos_usuarios.filter(codename__startswith='change')
                )

                # Grupo Jefe Capacitación: puede ver, agregar, modificar y eliminar usuarios
                capacitacion_group.permissions.add(*permisos_usuarios)

                # Grupo Subdirección: puede ver usuarios
                subdireccion_group.permissions.add(
                    *permisos_usuarios.filter(codename__startswith='view'),
                    *permisos_usuarios.filter(codename__startswith='change')
                )

            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)