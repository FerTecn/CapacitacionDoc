from django.urls import path
from . import views

urlpatterns = [
    #GRADO ACADEMICO
    path('gradolista/', views.gradolista, name='gradolista'),
    path('gradocrear/', views.gradocrear, name='gradocrear'),
    path('gradover/<int:grado_id>/', views.gradover, name='gradover'),
    path('gradoactualizar/<int:grado_id>/', views.gradoactualizar, name='gradoactualizar'),
    path('gradoeliminar/<int:grado_id>/', views.gradoeliminar, name='gradoeliminar'),
    
    #LUGARES
    path('lugarlista/', views.lugarlista, name='lugarlista'),
    path('lugarcrear/', views.lugarcrear, name='lugarcrear'),
    path('lugarver/<int:lugar_id>/', views.lugarver, name='lugarver'),
    path('lugaractualizar/<int:lugar_id>/', views.lugaractualizar, name='lugaractualizar'),
    path('lugareliminar/<int:lugar_id>/', views.lugareliminar, name='lugareliminar'),
    
    #SEDES
    path('sedelista/', views.sedelista, name='sedelista'),
    path('sedecrear/', views.sedecrear, name='sedecrear'),
    path('sedever/<int:sede_id>/', views.sedever, name='sedever'),
    path('sederactualizar/<int:sede_id>/', views.sedeactualizar, name='sedeactualizar'),
    path('sedeeliminar/<int:sede_id>/', views.sedeeliminar, name='sedeeliminar'),
    
    #INTRUCTORES
    path('instructorlista/', views.instructorlista, name='instructorlista'),
    path('instructorcrear/', views.instructorcrear, name='instructorcrear'),
    path('instructorver/<int:instructor_id>/', views.instructorver, name='instructorver'),
    path('instructoractualizar/<int:instructor_id>/', views.instructoractualizar, name='instructoractualizar'),
    path('instructoreliminar/<int:instructor_id>/', views.instructoreliminar, name='instructoreliminar'),

    path('instructor/<int:instructor_id>/generar_cv_pdf/', views.generar_cv_pdf, name='generar_cv_pdf'),
    
    #DOCENTES
    path('docentelista/', views.docentelista, name='docentelista'),
    path('docentercrear/', views.docentecrear, name='docentecrear'),
    path('docentever/<int:docente_id>/', views.docentever, name='docentever'),
    path('docenteactualizar/<int:docente_id>/', views.docenteactualizar, name='docenteactualizar'),
    path('docenteeliminar/<int:docente_id>/', views.docenteeliminar, name='docenteeliminar'),

    #DEPARTAMENTOS
    path('departamentolista/', views.departamentolista, name='departamentolista'),
    path('departamentocrear/', views.departamentocrear, name='departamentocrear'),
    path('departamentover/<int:departamento_id>/', views.departamentover, name='departamentover'),
    path('departamentoactualizar/<int:departamento_id>/', views.departamentoactualizar, name='departamentoactualizar'),
    path('departamentoeliminar/<int:departamento_id>/', views.departamentoeliminar, name='departamentoeliminar'),

    #DIRIGIDO
    path('dirigidolista/', views.dirigidolista, name='dirigidolista'),
    path('dirigidocrear/', views.dirigidocrear, name='dirigidocrear'),
    path('dirigidover/<int:dirigido_id>/', views.dirigidover, name='dirigidover'),
    path('dirigidoactualizar/<int:dirigido_id>/', views.dirigidoactualizar, name='dirigidoactualizar'),
    path('dirigidoeliminar/<int:dirigido_id>/', views.dirigidoeliminar, name='dirigidoeliminar'),

    #GÉNERO
    path('generolista/', views.generolista, name='generolista'),
    path('generocrear/', views.generocrear, name='generocrear'),
    path('generover/<int:genero_id>/', views.generover, name='generover'),
    path('generoactualizar/<int:genero_id>/', views.generoactualizar, name='generoactualizar'),
    path('generoeliminar/<int:genero_id>/', views.generoeliminar, name='generoeliminar'),

    #PERFIL DE CURSO
    path('perfilcursolista/', views.perfilcursolista, name='perfilcursolista'),
    path('perfilcursocrear/', views.perfilcursocrear, name='perfilcursocrear'),
    path('perfilcursover/<int:perfilCurso_id>/', views.perfilcursover, name='perfilcursover'),
    path('perfilcursoactualizar/<int:perfilCurso_id>/', views.perfilcursoactualizar, name='perfilcursoactualizar'),
    path('perfilcursoeliminar/<int:perfilCurso_id>/', views.perfilcursoeliminar, name='perfilcursoeliminar'),

    #PERIODO
    path('periodolista/', views.periodolista, name='periodolista'),
    path('periodocrear/', views.periodocrear, name='periodocrear'),
    path('periodover/<int:periodo_id>/', views.periodover, name='periodover'),
    path('periodoactualizar/<int:periodo_id>/', views.periodoactualizar, name='periodoactualizar'),
    path('periodoeliminar/<int:periodo_id>/', views.periodoeliminar, name='periodoeliminar'),
    
    #DIRECTOR
    path('directorlista/', views.directorlista, name='directorlista'),
    path('directorcrear/', views.directorcrear, name='directorcrear'),
    path('directorver/<int:director_id>/', views.directorver, name='directorver'),
    path('directoractualizar/<int:director_id>/', views.directoractualizar, name='directoractualizar'),
    # path('directoreliminar/<int:director_id>/', views.directoreliminar, name='directoreliminar'),

    # VALORES CALIFICACION
    path('valorcalificacionlista/', views.valorcalificacionlista, name='valorcalificacionlista'),
    path('valorcalificacioncrear/', views.valorcalificacioncrear, name='valorcalificacioncrear'),
    path('valorcalificacionactualizar/<int:valor_id>/', views.valorcalificacionactualizar, name='valorcalificacionactualizar'),
    path('valorcalificacioneliminar/<int:valor_id>/', views.valorcalificacioneliminar, name='valorcalificacioneliminar'),

    path('formatoslista/', views.formatoslista, name='formatoslista'),
    path('formatodepartamentocrear/', views.formatodepartamentocrear, name='formatodepartamentocrear'),
    path('formatodepartamentover/<int:formato_id>/', views.formatodepartamentover, name='formatodepartamentover'),
    path('formatodepartamentoactualizar/<int:formato_id>/', views.formatodepartamentoactualizar, name='formatodepartamentoactualizar'),
    path('formatoconstanciacrear/', views.formatoconstanciacrear, name='formatoconstanciacrear'),
    path('formatoconstanciaver/<int:formato_id>/', views.formatoconstanciaver, name='formatoconstanciaver'),
    path('formatoconstanciaactualizar/<int:formato_id>/', views.formatoconstanciaactualizar, name='formatoconstanciaactualizar'),
]