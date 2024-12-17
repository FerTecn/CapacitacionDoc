from django.contrib import admin
from .models import Instructor
from .models import Docente
from .models import Genero
from .models import Departamento
from .models import GradoAcademico
from .models import Lugar
from .models import Periodo
from .models import Sede
from .models import Dirigido
from .models import PerfilCurso

# Register your models here.
admin.site.register(Genero)
admin.site.register(Departamento)
admin.site.register(GradoAcademico)
admin.site.register(Sede)
admin.site.register(Dirigido)
admin.site.register(PerfilCurso)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apPaterno', 'apMaterno', 'grado')
    list_filter = ('grado',)

#Para dividir los campos con un texto
    fieldsets = (
        ('Datos personales', { 
            'fields': ('clave', 'nombre', 'apPaterno', 'apMaterno', 'fechaNac', 'CURP', 'RFC', 'telefono', 'email'),
        }),
        ('Formación Académica', { 
            'fields': ('institucion', 'grado', 'cedulaProf'),
        }),
        ('Experiencia laboral', {
            'fields': ('puesto', 'empresa'),
        }),
        ('Participación como instructor', {
            'fields': ('curso', 'nombreEmpresa', 'duracionHoras', 'fechaParticipacion'),
        }),
    )

admin.site.register(Instructor, InstructorAdmin)

class DocenteAdmin(admin.ModelAdmin):
    # Lo que quiero se muestre en el admin, como tipo tabla
    list_display = ('nombre', 'apPaterno', 'apMaterno', 'departamento')

    # Filtro de buscar 
    list_filter = ('departamento',)

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
