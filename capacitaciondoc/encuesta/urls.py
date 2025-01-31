from django.urls import path
from . import views

urlpatterns = [
    path('encuesta/', views.listarcursos4encueta, name='encuesta'),
    path('encuesta/<int:curso_id>', views.encuesta, name='realizarencuesta'),
    path('gracias/', views.gracias, name='gracias'),
]