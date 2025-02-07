from django.contrib import admin
from .models import Evento
from .models import Asistencia
from .models import oficioComision
from .models import Inscripcion
from .models import Evidencia
from .models import Calificacion

# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__periodo', 'curso__horas', 'curso__instructor',)
    
admin.site.register(Evento, EventoAdmin)

class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('evento__curso__nombre', 'evento__curso__instructor', 'evento__curso__horas')
admin.site.register(Inscripcion, InscripcionAdmin)

admin.site.register(Asistencia)

class oficioComisionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'nombre', 'lugar', 'horas')
admin.site.register(oficioComision, oficioComisionAdmin)

class EvidenciaAdmin(admin.ModelAdmin):
    list_display = ('evento__curso__nombre','evento__curso__instructor', 'evidencia', 'archivo_evidencia')

admin.site.register(Evidencia, EvidenciaAdmin)

admin.site.register(Calificacion)

