from django.urls import path
from . import views

urlpatterns = [
    #REGISTRO DE CURSOS
    path('registrolista/', views.registrolista, name='registrolista'),
    path('registrover/<int:curso_id>/', views.registrover, name='registrover'),
    path('registroactualizar/<int:curso_id>/', views.registroactualizar, name='registroactualizar'),
    path('registroeliminar/<int:curso_id>/', views.registroeliminar, name='registroeliminar'),
    path('registroañadir/', views.registroañadir, name='registroañadir'),
    
    #VALIDACION DE CURSOS
    path('validarcursolista/', views.validarcursolista, name='validarcursolista'),
    path('validarver/<int:validar_id>/', views.validarver, name='validarver'),
    path('curso/aceptar/<int:curso_id>/', views.aceptar_curso, name='aceptar_curso'),
    path('curso/invalidar/<int:curso_id>/', views.invalidar_curso, name='invalidar_curso'),

]