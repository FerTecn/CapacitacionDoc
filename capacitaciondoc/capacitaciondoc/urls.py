"""
URL configuration for capacitaciondoc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from usuarios.views import custom_403_view, custom_404_view, home
from capacitaciondoc.views import avisoprivacidad

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('',home, name="home"),
    path('usuarios/', include('usuarios.urls')),
    path('catalogos/', include('catalogos.urls')),
    path('plancapacitacion/', include('plancapacitacion.urls')),
    path('eventos/', include('eventos.urls')),
    path('encuesta/', include('encuesta.urls')),
    path('reportes/', include('reportes.urls')),
    path('avisoprivacidad/', avisoprivacidad, name='avisoprivacidad'),
]
# Asignar la vista personalizada
handler403 = custom_403_view
handler404 = custom_404_view

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)