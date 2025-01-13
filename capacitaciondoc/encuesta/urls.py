from django.urls import path
from . import views

urlpatterns = [
    path('encuesta/', views.encuesta, name='encuesta'),
    path('gracias/', views.gracias, name='gracias'),
]