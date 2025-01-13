from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.db import IntegrityError
from .forms import SignupForm, SigninForm
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
                user.save()
               
                # Añadir depuración antes de guardar
                print("Datos del usuario a guardar:", user)
                print("Usuario guardado correctamente:", user)
               
                # Asignar grupo basado en el rol
                group, created = Group.objects.get_or_create(name=user.rol)
                user.groups.add(group)
 
                # Iniciar sesión automáticamente después de registro
                login(request, user)
               
                # Mensaje de éxito y redirección al Home
                messages.success(request, 'Registro exitoso. ¡Bienvenido al sistema!')
                return redirect('home')  # Cambia 'home' por tu URL específica si es necesario
            except IntegrityError:
                messages.error(request, 'Ya existe un usuario con esa CURP.')
        else:
            # Mostrar errores específicos del formulario
            messages.error(request, 'Por favor, corrige los errores del formulario.')
            render(request, 'signup.html', {'form': form})
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
            return redirect('home') # redirecciona a la página principal
 
            # # Redirecciones basadas en grupo
            # if user.groups.filter(name='Instructor').exists():
            #     return redirect('instructor_dashboard')
            # elif user.groups.filter(name='Docente').exists():
            #     return redirect('docente_dashboard')
            # else:
            #     return redirect('home')
 
 
# Vista para cerrar sesión
@login_required(login_url='signin')
def signout(request):
    logout(request)
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
    if request.user.rol in ['Docente', 'Instructor']:
        return render(request, 'base.html')  
    else:
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
 