from django.urls import path
from . import views

urlpatterns = [
    path('constancias/lista-cursos/', views.listacursos, name='lista_cursos'),
    path('constancias/generar/<int:evento_id>/<int:user_id>/', views.generar_constancia, name='generar_constancia'),
    path('constancias/lista/<int:evento_id>/', views.listaconstancias, name='lista_constancias'),
    path('descargar-constancia/<int:evento_id>/<int:user_id>/', views.generar_constancia_pdf, name='descargar_constancia'),
]