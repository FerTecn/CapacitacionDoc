from django.contrib import admin
from .models import CriteriosSeleccionInstructor, Evento
from .models import Asistencia
from .models import OficioComision
from .models import Inscripcion
from .models import Evidencia
from .models import Calificacion

# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__periodo', 'curso__horas', 'curso__instructor',)
    
admin.site.register(Evento, EventoAdmin)

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento__curso__nombre', 'evento__curso__instructor', 'usuario', 'evento__curso__horas')
admin.site.register(Inscripcion, InscripcionAdmin)

admin.site.register(Asistencia)

class OficioComisionAdmin(admin.ModelAdmin):
    def get_full_no_oficio(self, obj):
        return f"{obj.docente.departamento.nomenclatura}-{obj.no_oficio}/{obj.fecha.year}" if obj else "no_oficio"
    get_full_no_oficio.short_description = 'No. de oficio'

    list_display = ('get_full_no_oficio', 'docente', 'fecha')

admin.site.register(OficioComision, OficioComisionAdmin)

class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('evento__curso__nombre','evento__curso__instructor', 'evidencia', 'archivo_evidencia')

admin.site.register(Evidencia, EvidenciaAdmin)

admin.site.register(Calificacion)
admin.site.register(CriteriosSeleccionInstructor)

