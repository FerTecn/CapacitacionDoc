from django.urls import path
from . import views

urlpatterns = [
    path('lista-cursos/', views.lista_cursos, name='lista_cursos'),
    path('generar-constancia/<int:evento_id>/', views.generar_constancia, name='generar_constancia'),
]