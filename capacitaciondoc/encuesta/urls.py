from django.urls import path
from . import views

urlpatterns = [
    path('encuesta/', views.listarcursos4encuesta, name='encuesta'),
    path('encuesta/<int:curso_id>', views.encuesta, name='realizarencuesta'),
    path('resultados/<int:curso_id>', views.resultados, name='resultados'),
    path('gracias/', views.gracias, name='gracias'),
]