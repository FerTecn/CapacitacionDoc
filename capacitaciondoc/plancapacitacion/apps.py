from django.apps import AppConfig


class PlancapacitacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'plancapacitacion'

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
                permisos_registro_curso = Permission.objects.filter(content_type__app_label='plancapacitacion', codename__icontains='registrocurso')
                permisos_validados = Permission.objects.filter(content_type__app_label='plancapacitacion', codename__icontains='validarcurso')

                def limpiar_permisos(grupo):
                    permisos_actuales = grupo.permissions.filter(content_type__app_label='plancapacitacion')
                    grupo.permissions.remove(*permisos_actuales)

                limpiar_permisos(docente_group)
                limpiar_permisos(instructor_group)
                limpiar_permisos(academico_group)
                limpiar_permisos(capacitacion_group)
                limpiar_permisos(subdireccion_group)

                # Asignar permisos a los grupos
                # Grupo Instructor: no puede registrar ni validar cursos

                # Grupo Docente: no puede registrar ni validar cursos

                # Grupo Jefe Académico: registra, modifica, crea y elimina los cursos
                academico_group.permissions.add(
                    *permisos_registro_curso
                )

                # Grupo Jefe Capacitación: solo puede ver los cursos y ver los cursos validados
                capacitacion_group.permissions.add(
                    *permisos_registro_curso.filter(codename__startswith='view'), *permisos_validados.filter(codename__startswith='view')
                )

                # Grupo Subdirección Académica: Valida cursos
                subdireccion_group.permissions.add(
                    *permisos_registro_curso, *permisos_validados #Es necesario el permiso de registrocurso ya que para validar se lista los cursos sin validar y se modifica el campo aceptado de RegistroCurso
                )

            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)
