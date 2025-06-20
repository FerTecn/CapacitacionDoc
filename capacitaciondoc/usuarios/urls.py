from django.urls import path, reverse_lazy
from .views import PasswordChangeView, signout, signup,signin, password_reset, password_reset_confirm, password_reset_complete, usuarioactualizar, usuariocrear, usuarioeliminar, usuariolista, usuariover
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),

    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_confirm/<str:curp>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),

    path('cambiar_password/', PasswordChangeView.as_view(), name='cambiar_password'),
    path('cambiar_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='cambiar_password_done.html'), name='cambiar_password_done'),

    path('usuariolista/', usuariolista, name='usuariolista'),
    path('usuariocrear/', usuariocrear, name='usuariocrear'),
    path('usuariover/<int:usuario_id>/', usuariover, name='usuariover'),
    path('usuarioactualizar/<int:usuario_id>/', usuarioactualizar, name='usuarioactualizar'),
    path('usuarioeliminar/<int:usuario_id>/', usuarioeliminar, name='usuarioeliminar'),
]