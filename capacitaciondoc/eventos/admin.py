from django.contrib import admin
from .models import Evento
from .models import asistencia
from .models import oficioComision
from .models import inscripcion
from .models import calificacion

# Register your models here.
class EventoAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__periodo', 'curso__horas', 'curso__instructor',)
    
admin.site.register(Evento, EventoAdmin)

class asistenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'periodo', 'lugar', 'horas', 'instructor')
admin.site.register(asistencia, asistenciaAdmin)

class oficioComisionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'nombre', 'lugar', 'horas')
admin.site.register(oficioComision, oficioComisionAdmin)

class inscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'instructor', 'horas')
admin.site.register(inscripcion, inscripcionAdmin)

class calificacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'periodo', 'lugar', 'horas')
admin.site.register(calificacion, calificacionAdmin)