from django.contrib import admin
from .models import ExperienciaDocente, ExperienciaLaboral, FormacionAcademica, Instructor, ParticipacionInstructor
from .models import Docente
from .models import Genero
from .models import Departamento
from .models import GradoAcademico
from .models import Lugar
from .models import Periodo
from .models import Sede
from .models import Dirigido
from .models import PerfilCurso
from .models import Director

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
