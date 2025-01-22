from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from .models import (
    ExperienciaDocente, 
    ExperienciaLaboral, 
    FormacionAcademica, 
    Instructor, 
    ParticipacionInstructor)
from .models import (
    Docente, Genero, Departamento, GradoAcademico, Lugar, Periodo, 
    Sede, Dirigido, PerfilCurso, Director)

# Register your models here.
admin.site.register(Genero)
admin.site.register(Departamento)
admin.site.register(GradoAcademico)
admin.site.register(Sede)
admin.site.register(Dirigido)
admin.site.register(PerfilCurso)
admin.site.register(Director)
admin.site.register(FormacionAcademica)
admin.site.register(ExperienciaLaboral)
admin.site.register(ExperienciaDocente)
admin.site.register(ParticipacionInstructor)
    
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'clave', 'fechaNac', 'genero', 'RFC', 'telefono')
    
    search_fields = ('user__curp', 'user__first_name', 'user__last_name_paterno', 'user__last_name_materno')  # Búsqueda por CURP y nombre
    ordering = ('user__curp',)

    # Campos de solo lectura (para proteger ciertos datos)
    readonly_fields = ('user',)

    # Personalización de cómo se muestra la información de un Docente
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name_paterno} {obj.user.last_name_materno}"
    get_user_full_name.short_description = 'Nombre completo'

    # Mostrar el nombre completo del docente en lugar de los nombres individuales en la lista
    list_display = ('get_user_full_name', 'clave', 'fechaNac', 'RFC', 'telefono')

    # Campos de solo lectura (para proteger ciertos datos)
    readonly_fields = ('user',)

    # Personalización de cómo se muestra la información de un Docente
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name_paterno} {obj.user.last_name_materno}"
    get_user_full_name.short_description = 'Nombre completo'

    # Mostrar el nombre completo del docente en lugar de los nombres individuales en la lista
    list_display = ('get_user_full_name', 'clave', 'fechaNac', 'RFC', 'telefono')


admin.site.register(Instructor, InstructorAdmin)

class DocenteAdmin(admin.ModelAdmin):
    list_display = ('user', 'clave', 'fechaNac', 'genero', 'RFC', 'telefono', 'departamento')
    list_filter = ('genero','departamento')  # Filtros para la lista
    search_fields = ('user_curp', 'userfirst_name', 'userlast_name_paterno', 'user_last_name_materno')  # Búsqueda por CURP y nombre
    ordering = ('user__curp',)

    # Campos de solo lectura (para proteger ciertos datos)
    readonly_fields = ('user',)

    # Personalización de cómo se muestra la información de un Docente
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name_paterno} {obj.user.last_name_materno}"
    get_user_full_name.short_description = 'Nombre completo'

    # Mostrar el nombre completo del docente en lugar de los nombres individuales en la lista
    list_display = ('get_user_full_name', 'clave', 'fechaNac', 'genero', 'RFC', 'telefono', 'departamento')

admin.site.register(Docente, DocenteAdmin)

class LugarAdmin(admin.ModelAdmin):
    list_display=('nombreEdificio','ubicacion')
    
    list_filter = ('nombreEdificio',)
    
admin.site.register(Lugar, LugarAdmin)

class PeriodoAdmin(admin.ModelAdmin):
    list_display=('inicioPeriodo', 'finPeriodo')
admin.site.register(Periodo, PeriodoAdmin)


class HoraAdmin(admin.ModelAdmin):
    list_display = ('cantidad',)
    search_fields = ('cantidad',)


# Permisos
def configurar_grupos_y_permisos():
    # Crea o obtiene los grupos en la BD
    docente_group, created = Group.objects.get_or_create(name='Docente')
    instructor_group, created = Group.objects.get_or_create(name='Instructor')
    academico_group, created = Group.objects.get_or_create(name='Jefe Académico')
    capacitacion_group, created = Group.objects.get_or_create(name='Jefe de Capacitación')
    subdireccion_group, created = Group.objects.get_or_create(name='Subdirección')

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

    # Guardar los grupos
    instructor_group.save()
    docente_group.save()
    academico_group.save()
    capacitacion_group.save()

# Llamar a la función para configurar grupos y permisos
configurar_grupos_y_permisos()
