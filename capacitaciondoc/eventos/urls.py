from django.urls import path
from . import views

urlpatterns = [
    #Evento
    path('eventolista/', views.eventolista, name='eventolista'),
    path('crearevento/<int:evento_id>/', views.crearevento, name='crearevento'),
    path('eventover/<int:evento_id>/', views.eventover, name='eventover'),
    path('eventodeshacer/<int:evento_id>/', views.eventodeshacer, name='eventodeshacer'),

    path('lugarcrearnuevo/', views.lugarcrearnuevo, name='lugarcrearnuevo'), 
    path('evento/<int:evento_id>/cambiarinstructor/', views.cambiarinstructor, name='cambiarinstructor'), 
    # path('evento/<int:evento_id>/añadirinstructor/', views.añadirinstructor, name='añadirinstructor'),
    
    #Inscripcion
    path('inscripcionlista/', views.inscripcionlista, name='inscripcionlista'),
    path('vercurso/<int:evento_id>/', views.vercurso, name='vercurso'),
    path('aceptarinscripcion/<int:evento_id>/', views.aceptarinscripcion, name='aceptarinscripcion'),
    path('invalidar/<int:evento_id>/', views.invalidarinscripcion, name='invalidarinscripcion'),

    #Cursos y asistencias
    path('asistencia/', views.listacursosasistencia, name='asistencia'),
    path('asistencia/<int:evento_id>/', views.detalle_curso_asistencia, name='detalle_curso_asistencia'),
    path('tomar-asistencia/<int:evento_id>/', views.tomar_asistencia, name='tomar-asistencia'),

    # #Cursos y calificaciones
    path('evidencia/<int:evento_id>/', views.evidencia, name='evidencia'),

    path('calificacion/', views.listacursoscalificacion, name='calificacion'),
    path('calificacion/<int:evento_id>/', views.detalle_curso_calificacion, name='detalle_curso_calificacion'),
    path('asignar-calificacion/<int:evento_id>/', views.asignar_calificacion, name='asignar_calificacion'),

    # Oficio de comisión
    path('oficio_comision', views.oficioslista, name='oficioslista'),
    path('oficiocrear/<int:docente_id>/', views.oficiocrear, name='oficiocrear'),
    path('oficioactualziar/<int:oficio_id>/', views.oficioactualizar, name='oficioactualizar'),
    path('descargar_oficio/<int:oficio_id>/', views.descargar_oficio, name='descargar_oficio'),

    #Criterios de seleccion del Instructor
    path('criteriosseleccionlista/', views.criteriosseleccionlista, name='criteriosseleccionlista'),
    path('criteriosseleccionver/<int:curso_id>/', views.criteriosseleccionver, name='criteriosseleccionver'),
    path('criteriosseleccioncrear/<int:curso_id>/', views.criteriosseleccioncrear, name='criteriosseleccioncrear'),
    path('criteriosseleccionactualizar/<int:curso_id>/', views.criteriosseleccionactualizar, name='criteriosseleccionactualizar'),
    path('criteriosseleccionpdf/<int:curso_id>/', views.criteriosseleccionpdf, name='criteriosseleccionpdf'),
]
