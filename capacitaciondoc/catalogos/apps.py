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
                permisos_instructor = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='instructor')
                permisos_docente = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='docente')
                permisos_departamento = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='departamento')
                permisos_dirigido = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='dirigido')
                permisos_genero = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='genero')
                permisos_grado_academico = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='gradoacademico')
                permisos_sede = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='sede')
                permisos_lugar = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='lugar')
                permisos_perfil_curso = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='perfilcurso')
                permisos_director = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='director')
                permisos_periodo = Permission.objects.filter(content_type__app_label='catalogos', codename__icontains='periodo')
                
                def limpiar_permisos(grupo):
                    permisos_actuales = grupo.permissions.filter(content_type__app_label='catalogos')
                    grupo.permissions.remove(*permisos_actuales)

                limpiar_permisos(docente_group)
                limpiar_permisos(instructor_group)
                limpiar_permisos(academico_group)
                limpiar_permisos(capacitacion_group)
                limpiar_permisos(subdireccion_group)

                # Asignar permisos a los grupos
                # Grupo Instructor: solo puede ver y editar instructores
                instructor_group.permissions.add(
                    *permisos_instructor.filter(codename__startswith='view'),
                    *permisos_instructor.filter(codename__startswith='change')
                    )

                # Grupo Docente: solo puede ver y editar docentes
                docente_group.permissions.add(
                    *permisos_docente.filter(codename__startswith='view'),
                    *permisos_docente.filter(codename__startswith='change')
                )

                # Grupo Jefe Académico: puede ver instructores y docentes, pero no editarlos
                academico_group.permissions.add(
                    *permisos_instructor.filter(codename__startswith='view'),
                    *permisos_docente.filter(codename__startswith='view')
                )

                # Grupo Jefe Capacitación: puede ver, agregar, modificar y eliminar instructores y docentes
                capacitacion_group.permissions.add(
                    *permisos_docente, *permisos_instructor,
                    *permisos_dirigido, *permisos_departamento, *permisos_director, *permisos_genero, *permisos_grado_academico,
                    *permisos_lugar, *permisos_sede, *permisos_perfil_curso, *permisos_periodo
                )

                subdireccion_group.permissions.add(
                    *permisos_instructor.filter(codename__startswith='view'),
                    *permisos_docente.filter(codename__startswith='view'),
                    *permisos_dirigido.filter(codename__startswith='view'),
                    *permisos_departamento.filter(codename__startswith='view'),
                    *permisos_director.filter(codename__startswith='view'),
                    *permisos_genero.filter(codename__startswith='view'),
                    *permisos_grado_academico.filter(codename__startswith='view'),
                    *permisos_lugar.filter(codename__startswith='view'),
                    *permisos_sede.filter(codename__startswith='view'),
                    *permisos_perfil_curso.filter(codename__startswith='view'),
                    *permisos_periodo.filter(codename__startswith='view'),
                )

            except Permission.DoesNotExist as e:
                # Mostrar un error detallado en la consola si algún permiso no existe
                print(f"Error al configurar permisos: {e}")
        
        # Conectar la señal post_migrate
        post_migrate.connect(configurar_grupos_y_permisos, sender=self)