from django.urls import path
from . import views

urlpatterns = [
    #Evento
    path('eventolista/', views.eventolista, name='eventolista'),
    path('crearevento/<int:evento_id>/', views.crearevento, name='crearevento'),
    path('eventover/<int:evento_id>/', views.eventover, name='eventover'),
    path('añadirlugar/', views.añadirlugar, name='añadirlugar'), 
    path('evento/<int:evento_id>/cambiarinstructor/', views.cambiarinstructor, name='cambiarinstructor'), 
    path('evento/<int:evento_id>/añadirinstructor/', views.añadirinstructor, name='añadirinstructor'),
    
    #Inscripcion
    path('inscripcionlista/', views.inscripcionlista, name='inscripcionlista'),
    path('vercurso/<int:evento_id>/', views.vercurso, name='vercurso'),
    path('aceptar/<int:inscripcion_id>/', views.aceptarinscripcion, name='aceptarinscripcion'),
    path('invalidar/<int:inscripcion_id>/', views.invalidarinscripcion, name='invalidarinscripcion'),
]