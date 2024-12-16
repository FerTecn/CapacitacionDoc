from django.urls import path
from . import views

urlpatterns = [
    path('eventolista/', views.eventolista, name='eventolista'),
    path('crearevento/<int:evento_id>/', views.crearevento, name='crearevento'),
    path('eventover/<int:evento_id>/', views.eventover, name='eventover'),
    path('añadirlugar/', views.añadirlugar, name='añadirlugar'), 
    path('añadirhoras/', views.añadirhoras, name='añadirhoras'),
    path('horaslista/', views.horaslista, name='horaslista'),
    path('horaver/<int:hora_id>/', views.horaver, name='horaver'),  # Ver detalles de una hora específica
    path('crearhora/', views.crearhora, name='crearhora'),  # Crear nueva hora
    path('crearhora/<int:hora_id>/', views.crearhora, name='editarhora'),
    path('inscripcionlista/', views.inscripcionlista, name='inscripcionlista'),
    path('inscripcionver/<int:inscripcionver_id>/', views.inscripcionver, name='inscripcionver'),
]