from django.urls import path
from . import views

urlpatterns = [
    #REGISTRO DE CURSOS
    path('registrocursolista/', views.registrocursolista, name='registrocursolista'),
    path('registrocursover/<int:curso_id>/', views.registrocursover, name='registrocursover'),
    path('registrocursoactualizar/<int:curso_id>/', views.registrocursoactualizar, name='registrocursoactualizar'),
    path('registrocursoeliminar/<int:curso_id>/', views.registrocursoeliminar, name='registrocursoeliminar'),
    path('registrocursocrear/', views.registrocursocrear, name='registrocursocrear'),
    
    #VALIDACION DE CURSOS
    path('validarcursolista/', views.validarcursolista, name='validarcursolista'),
    path('validarver/<int:validar_id>/', views.validarver, name='validarver'),
    path('curso/aceptar/<int:curso_id>/', views.aceptar_curso, name='aceptar_curso'),
    path('curso/invalidar/<int:curso_id>/', views.invalidar_curso, name='invalidar_curso'),

    path('fichatecnica/', views.cursosfichas, name='fichatecnica'),
    path('fichatecnica/<int:curso_id>/', views.fichatecnicaver, name='fichatecnicaver'),
    path('fichatecnica/datos/<int:curso_id>/', views.fichatecnicacrear, name='fichatecnicacrear'),
    path('descargar-ficha/<int:curso_id>/', views.fichatecnicapdf, name='generarficha'),
    path('oficio_comision', views.oficioslista, name='oficioslista'),
    path('descargar_oficio/<int:docente_id>/<int:departamento_id>/', views.descargar_oficio, name='descargar_oficio'),

]