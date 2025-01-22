from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CatalogosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogos'

    def ready(self):
        
        from django.contrib.auth.models import Group, Permission
        from django.db.models.signals import post_migrate
        from django.core.exceptions import ObjectDoesNotExist

        # Permisos
        def configurar_grupos_y_permisos(sender, **kwargs):
            # Crea o obtiene los grupos en la BD
            docente_group, created = Group.objects.get_or_create(name='Docente')
            instructor_group, created = Group.objects.get_or_create(name='Instructor')
            academico_group, created = Group.objects.get_or_create(name='Jefe Académico')
            capacitacion_group, created = Group.objects.get_or_create(name='Jefe de Capacitación')
            subdireccion_group, created = Group.objects.get_or_create(name='Subdirección')

            try:
                # Obtener permisos definidos en los modelos
                permission_view_instructor = Permission.objects.get(codename='view_instructor')
                permission_edit_instructor = Permission.objects.get(codename='change_instructor')
                permission_delete_instructor = Permission.objects.get(codename='delete_instructor')
                permission_add_instructor = Permission.objects.get(codename='add_instructor')

                permission_view_docente = Permission.objects.get(codename='view_docente')
                permission_edit_docente = Permission.objects.get(codename='change_docente')
                permission_delete_docente = Permission.objects.get(codename='delete_docente')
                permission_add_docente = Permission.objects.get(codename='add_docente')

                # Asignar permisos a los grupos
                # Grupo Instructor: solo puede ver y editar instructores
                instructor_group.permissions.add(permission_view_instructor, permission_edit_instructor)

                # Grupo Docente: solo puede ver y editar docentes
                docente_group.permissions.add(permission_view_docente, permission_edit_docente)

                # Grupo Jefe Académico: puede ver instructores y docentes, pero no editarlos
                academico_group.permissions.add(permission_view_instructor, permission_view_docente)

                # Grupo Jefe Capacitación: puede ver, agregar, modificar y eliminar instructores y docentes
                capacitacion_group.permissions.add(
                    permission_view_instructor,
                    permission_edit_instructor,
                    permission_add_instructor,
                    permission_delete_instructor,
                    permission_delete_docente,
                    permission_add_docente,
                    permission_view_docente,
                    permission_edit_docente,
                )
            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)