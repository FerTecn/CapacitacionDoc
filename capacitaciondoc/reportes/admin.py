from django.contrib import admin

from .models import ConstanciaDocente, ConstanciaInstructor

# Register your models here.

class ConstanciaInstructorAdmin(admin.ModelAdmin):
    list_display = ('curso__curso__nombre', 'instructor', 'fecha')

class ConstanciaDocenteAdmin(admin.ModelAdmin):
    list_display = ('curso__curso__nombre', 'docente', 'fecha', 'encuesta', 'calificacion')

admin.site.register(ConstanciaInstructor, ConstanciaInstructorAdmin)
admin.site.register(ConstanciaDocente, ConstanciaDocenteAdmin)