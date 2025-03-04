from django.urls import path
from . import views

urlpatterns = [
    path('constancias/lista-cursos/', views.listacursos, name='lista_cursos'),
    path('constancias/generar/instructor/<int:evento_id>/<int:user_id>/', views.generarconstanciainstructor, name='generar_constancia_instructor'),
    path('constancias/estatus/docente/<int:evento_id>/<int:user_id>/', views.estatusconstancia, name='estatus_constancia_docente'),
    path('constancias/generar/docente/<int:evento_id>/<int:user_id>/', views.generarconstanciadocente, name='generar_constancia_docente'),
    path('constancias/lista/<int:evento_id>/', views.listaconstancias, name='lista_constancias'),
    path('descargar-constancia/<int:evento_id>/<int:user_id>/', views.generar_constancia_pdf, name='descargar_constancia'),
]