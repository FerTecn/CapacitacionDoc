from django.apps import AppConfig


class EncuestaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'encuesta'

    def ready(self):
        
        from django.contrib.auth.models import Group, Permission
        from django.db.models.signals import post_migrate

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
                permisos_encuesta = Permission.objects.filter(content_type__app_label='encuesta', codename__icontains='encuesta')

                def limpiar_permisos(grupo):
                    permisos_actuales = grupo.permissions.filter(content_type__app_label='encuesta')
                    grupo.permissions.remove(*permisos_actuales)

                limpiar_permisos(docente_group)
                limpiar_permisos(instructor_group)
                limpiar_permisos(academico_group)
                limpiar_permisos(capacitacion_group)
                limpiar_permisos(subdireccion_group)

                # Asignar permisos a los grupos
                # Grupo Instructor: no puede ver, ni crear encuestas

                # Grupo Docente: realiza las encuestas
                docente_group.permissions.add(*permisos_encuesta)

                # Grupo Jefe Académico: no puede ver ni crear encuestas

                # Grupo Jefe Capacitación: solo puede ver los resultados de las encuestas
                capacitacion_group.permissions.add(
                    *permisos_encuesta.filter(codename__startswith='view'),
                )

                # Grupo Subdirección Académica: No puede ver ni crear encuestas

            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)
