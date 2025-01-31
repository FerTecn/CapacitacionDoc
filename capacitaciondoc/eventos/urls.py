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
    path('evento/<int:evento_id>/añadirinstructor/', views.añadirinstructor, name='añadirinstructor'),
    
    #Inscripcion
    path('inscripcionlista/', views.inscripcionlista, name='inscripcionlista'),
    path('vercurso/<int:evento_id>/', views.vercurso, name='vercurso'),
    path('aceptarinscripcion/<int:evento_id>/', views.aceptarinscripcion, name='aceptarinscripcion'),
    path('invalidar/<int:evento_id>/', views.invalidarinscripcion, name='invalidarinscripcion'),

    #Cursos y asistencias
    path('miscursos/', views.miscursosinstructor, name='miscursos'),
    path('mis-cursos/<int:curso_id>/', views.detalle_curso, name='detalle_curso'),
    path('tomar-asistencia/<int:evento_id>/', views.tomar_asistencia, name='tomar-asistencia'),
]