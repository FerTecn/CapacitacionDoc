from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'

    def ready(self):
        import eventos.signals # Agregado para el signals de borrar archivos
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
                permisos_eventos = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='evento')
                permisos_inscripciones = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='inscripcion')
                permisos_asistencias = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='asistencia')
                permisos_calificaciones = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='calificacion')
                permisos_evidencias = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='evidencia')
                permisos_oficios_comision = Permission.objects.filter(content_type__app_label='eventos', codename__icontains='oficiocomision')

                def limpiar_permisos(grupo):
                    permisos_actuales = grupo.permissions.filter(content_type__app_label='eventos')
                    grupo.permissions.remove(*permisos_actuales)

                limpiar_permisos(docente_group)
                limpiar_permisos(instructor_group)
                limpiar_permisos(academico_group)
                limpiar_permisos(capacitacion_group)
                limpiar_permisos(subdireccion_group)

                # Asignar permisos a los grupos
                # Grupo Instructor: no puede crear eventos, ve inscripciones de su curso
                instructor_group.permissions.add(
                    *permisos_eventos.filter(codename__startswith='view'),
                    *permisos_asistencias, *permisos_calificaciones, *permisos_evidencias
                )
                
                # Grupo Docente: puede ver los eventos de los cursos para poder inscribirse y pude hacer su inscripcion
                docente_group.permissions.add(
                    *permisos_inscripciones, 
                    *permisos_eventos.filter(codename__startswith='view'),
                )

                # Grupo Jefe Académico: solo puede ver los eventos, no puede inscribirse
                
                academico_group.permissions.add(
                    *permisos_eventos.filter(codename__startswith='view'),
                    *permisos_inscripciones.filter(codename__startswith='view'),
                    *permisos_inscripciones.filter(codename__startswith='change'),
                    *permisos_oficios_comision,
                )

                # Grupo Jefe Capacitación: puede ver, agregar, modificar y eliminar eventos
                capacitacion_group.permissions.add(
                    *permisos_eventos, 
                    *permisos_inscripciones.filter(codename__startswith='view'),
                    *permisos_asistencias,
                )

                # Grupo Subdirección Académica: Solo ve eventos
                subdireccion_group.permissions.add(
                    *permisos_eventos.filter(codename__startswith='view'),
                )

            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)

