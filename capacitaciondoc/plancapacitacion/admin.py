from django.contrib import admin
from .models import ActividadAsignatura, ActividadModulosEspecialidad, AsignaturaDeteccionNecesidades, ConcentradoDiagnostico, ContenidoTematico, CriterioEvaluacion, DeteccionNecesidades, RegistroCurso
from .models import FichaTecnica
from .models import ValidarCurso

# Register your models here.
class RegistroCursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'periodo', 'horas', 'instructor', 'aceptado')
    list_filter=('instructor', 'aceptado')
admin.site.register(RegistroCurso, RegistroCursoAdmin)

class ValidarCursoAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__periodo', 'curso__horas', 'curso__instructor', 'curso__aceptado')
    list_filter=('curso__instructor', 'curso__periodo', 'curso__aceptado')
    
    def get_queryset(self, request):
        # Generar automáticamente los cursos que ya se registraron 
        cursos = RegistroCurso.objects.all()
        for curso in cursos:
            ValidarCurso.objects.get_or_create(curso=curso)

        return super().get_queryset(request)

admin.site.register(ValidarCurso, ValidarCursoAdmin)

class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__instructor', 'curso__horas')
admin.site.register(FichaTecnica, FichaTecnicaAdmin)

class ContenidoTematicoAdmin(admin.ModelAdmin):
    list_display = ('fichaTecnica__curso__nombre', 'tema')
admin.site.register(ContenidoTematico, ContenidoTematicoAdmin)

class CriterioEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('fichaTecnica__curso__nombre', 'criterio', 'valor', 'instrumento')
admin.site.register(CriterioEvaluacion, CriterioEvaluacionAdmin)

admin.site.register(DeteccionNecesidades)
admin.site.register(AsignaturaDeteccionNecesidades)

admin.site.register(ConcentradoDiagnostico)
admin.site.register(ActividadAsignatura)
admin.site.register(ActividadModulosEspecialidad)