from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from .models import CustomUser
from catalogos.models import Docente, Instructor
from .forms import CreateUserForm, SignupForm, SigninForm
from django.contrib import messages

# Create your views here.
def signup(request):
    if request.method == 'POST':
        print("Datos recibidos del formulario:", request.POST)  # Para depuración, imprime los datos recibidos
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                # Crear usuario
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])  # Usar la contraseña ingresada

                # Añadir depuración antes de guardar
                print("Datos del usuario a guardar:", user)
                user.save()
                print("Usuario guardado correctamente:", user)

                # Asignar grupo basado en el rol
                group, created = Group.objects.get_or_create(name=user.rol)
                user.groups.add(group)
                
                
                # Crea una instancia de docente o instructor si se registran con ese rol para posteriormente modificar su información
                if user.rol == 'Docente':
                    Docente.objects.create(user=user)
                if user.rol == 'Instructor':
                    Instructor.objects.create(user=user)


                # Iniciar sesión automáticamente después de registro
                login(request, user)

                # Mensaje de éxito y redirección al index
                messages.success(request, 'Registro exitoso. ¡Bienvenido al sistema!')
                return redirect('/')  
            except IntegrityError as e:
                messages.error(request, f'Ya existe un usuario con esa CURP.{e}')
            except Exception as e:
                messages.error(request, f'Ocurrió un error: {e}')
        else:
            # Mostrar errores específicos del formulario
            messages.error(request, 'Por favor, corrige los errores del formulario.')
            # return render(request, 'signup.html', {'form': form})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# Vista para iniciar sesión
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': SigninForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': SigninForm, 'error': 'Usuario y/o contraseña incorrectos'})
        else:
            login(request, user) #Inicia la sesión y
            messages.success(request, f"¡Bienvenido de nuevo, {user.get_user_full_name()}!")
            return redirect('/') # redirecciona a la página principal
        
            # # Redirecciones basadas en grupo
            # if user.groups.filter(name='Instructor').exists():
            #     return redirect('instructor_dashboard')
            # elif user.groups.filter(name='Docente').exists():
            #     return redirect('docente_dashboard')
            # else:
            #     return redirect('home')

@login_required(login_url='signin')
@permission_required('usuarios.view_customuser', raise_exception=True)
def usuariolista(request):
    usuario = request.user
    usuarios = []

    if usuario.rol == 'Jefe de Capacitación':
        usuarios = CustomUser.objects.exclude(rol__in=['Docente', 'Instructor']).exclude(id=usuario.id)

    return render(request, 'usuariolista.html', {'usuarios': usuarios, 'usuario': usuario})

@login_required(login_url='signin')
@permission_required('usuarios.view_customuser', raise_exception=True)
def usuariover(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    form = CreateUserForm(instance=usuario)
    return render(request, 'usuariover.html', {'usuario': usuario, 'form': form})

@login_required(login_url='signin')
@permission_required('usuarios.add_customuser', raise_exception=True)
def usuariocrear(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect('usuariolista')
        else:
            print(form.errors)
    else:
        form = CreateUserForm()
    return render(request, 'usuariocrear.html', {'form': form})

@login_required(login_url='signin')
@permission_required('usuarios.change_customuser', raise_exception=True)
def usuarioactualizar(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=usuario)
        if request.user.pk == usuario.pk:
            # Eliminar el campo is_active si se está editando a sí mismo
            form.fields.pop('is_active', None)

        if form.is_valid():
            user = form.save(commit=False)

            # Proteger is_active si se edita a sí mismo
            if request.user.pk == usuario.pk:
                user.is_active = CustomUser.objects.get(pk=user.pk).is_active

            user.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('usuariolista')
    else:
        form = CreateUserForm(instance=usuario)

        # Eliminar el campo is_active si está editando su propio perfil
        if request.user.pk == usuario.pk:
            form.fields.pop('is_active', None)
    return render(request, 'usuarioactualizar.html', {'form': form})

@login_required(login_url='signin')
@permission_required('usuarios.delete_customuser', raise_exception=True)
def usuarioeliminar(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('usuariolista')
    return render(request, 'usuarioeliminar.html', {'usuario': usuario})
 
# Vista para cerrar sesión
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('signin')
 
 
# Vistas protegidas por roles
def instructor_dashboard(request):
    if not request.user.groups.filter(name='Instructor').exists():
        return redirect('no_autorizado')
    return render(request, 'instructor_dashboard.html')
 
def docente_dashboard(request):
    if not request.user.groups.filter(name='Docente').exists():
        return redirect('no_autorizado')
    return render(request, 'docente_dashboard.html')
 
 
# Vista para "No autorizado"
def no_autorizado(request):
    return render(request, 'no_autorizado.html')
 
 
# Vista para el Home (solo accesible para roles específicos)
@login_required(login_url='signin')
def home(request):
    if request.user.rol in ['Docente', 'Instructor', 'Jefe Académico', 'Jefe de Capacitación', 'Subdirección']:
        return render(request, 'index.html')  
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
# Vista para el error 403
def custom_403_view(request, exception=None):
    # Obtener la URL previa usando HTTP_REFERER
    previous_url = request.META.get('HTTP_REFERER', None)
    return render(request, '403.html', {'previous_url': previous_url}, status=403)

# Vista para el error 404
def custom_404_view(request, exception=None):
    # Obtener la URL previa usando HTTP_REFERER
    previous_url = request.META.get('HTTP_REFERER', None)
    return render(request, '404.html', {'previous_url': previous_url}, status=404)

# Vista para recuperar la contraseña usando la CURP
def password_reset(request):
    if request.method == 'POST':
        curp = request.POST.get('curp')
        User = get_user_model()
        try:
            user = User.objects.get(curp=curp)  # Buscar usuario por CURP
        except User.DoesNotExist:
            messages.error(request, "La CURP no es válida.")
            return redirect('password_reset')

        # Si la CURP es válida, redirigir a la vista para cambiar la contraseña
        return redirect('password_reset_confirm', curp=curp)
    
    return render(request, 'password_reset.html')

# Vista para confirmar el restablecimiento de la contraseña
def password_reset_confirm(request, curp):
    User = get_user_model()
    try:
        user = User.objects.get(curp=curp)
    except User.DoesNotExist:
        raise Http404("Usuario no encontrado")

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva contraseña
            return redirect('password_reset_complete')  # Redirige a la página de confirmación
    else:
        form = SetPasswordForm(user)

    return render(request, 'password_reset_confirm.html', {'form': form})

# Vista para completar el restablecimiento de contraseña
def password_reset_complete(request):
    messages.success(request, "Tu contraseña ha sido restablecida con éxito.")
    
    # Renderizar la plantilla de confirmación
    return render(request, 'password_reset_complete.html')