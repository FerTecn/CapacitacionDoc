from django.contrib import admin
from .models import registroCurso
from .models import fichaTecnica
from .models import validarCurso

# Register your models here.
class registroCursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'periodo', 'horas', 'instructor', 'aceptado')
    list_filter=('instructor', 'aceptado')
admin.site.register(registroCurso, registroCursoAdmin)

class validarCursoAdmin(admin.ModelAdmin):
    list_display = ('curso__nombre', 'curso__periodo', 'curso__horas', 'curso__instructor', 'curso__aceptado')
    list_filter=('curso__instructor', 'curso__periodo', 'curso__aceptado')
    
    def get_queryset(self, request):
        # Generar automáticamente los cursos que ya se registraron 
        cursos = registroCurso.objects.all()
        for curso in cursos:
            validarCurso.objects.get_or_create(curso=curso)

        return super().get_queryset(request)

admin.site.register(validarCurso, validarCursoAdmin)

class fichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'instructor', 'horas', 'departamento')
admin.site.register(fichaTecnica, fichaTecnicaAdmin)