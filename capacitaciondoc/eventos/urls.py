from django.urls import path
from . import views

urlpatterns = [
    path('eventolista/', views.eventolista, name='eventolista'),
    path('crearevento/<int:evento_id>/', views.crearevento, name='crearevento'),
    path('eventover/<int:evento_id>/', views.eventover, name='eventover'),
    path('añadirlugar/', views.añadirlugar, name='añadirlugar'), 
]