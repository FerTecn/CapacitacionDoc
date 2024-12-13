from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from catalogos.models import Lugar 
from catalogos.models import Horas


# Create your views here.
def eventolista(request):
    eventos = Evento.objects.all()
    return render(request, 'eventolista.html', {'eventos': eventos})

def eventover(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  
    return render(request, 'eventover.html', {'evento': evento})

def crearevento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  # Obtener el evento
    lugares = Lugar.objects.all()  # Obtener todos los lugares disponibles

    # Guardar el ID del evento en la sesión para redirección
    request.session['evento_id'] = evento_id
    
    # Verificar si hay un lugar recién creado
    nuevo_lugar_id = request.session.pop('nuevo_lugar_id', None)
    lugar_seleccionado = None
    if nuevo_lugar_id:
        lugar_seleccionado = get_object_or_404(Lugar, id=nuevo_lugar_id)
        evento.lugar = lugar_seleccionado
        evento.save()

    if request.method == 'POST':
        lugar_id = request.POST.get('lugar')
        lugar = get_object_or_404(Lugar, id=lugar_id)
        evento.lugar = lugar
        evento.save()
        return redirect('eventolista')

    return render(request, 'crearevento.html', {
        'evento': evento,
        'lugares': lugares,
        'lugar_seleccionado': lugar_seleccionado,
    })

def añadirlugar(request):
    if request.method == 'POST':
        nombre_edificio = request.POST.get('nombreEdificio')
        ubicacion = request.POST.get('ubicacion')
        
        if nombre_edificio and ubicacion:
            # Crear el nuevo lugar
            nuevo_lugar = Lugar.objects.create(
                nombreEdificio=nombre_edificio,
                ubicacion=ubicacion
            )

            # Guardar el ID del nuevo lugar en la sesión
            request.session['nuevo_lugar_id'] = nuevo_lugar.id
            
            # Redirigir a la página de crear evento con el lugar seleccionado
            return redirect('crearevento', evento_id=request.session.get('evento_id'))

    return render(request, 'añadirlugar.html')


def añadirhoras(request):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        descripcion = request.POST.get('descripcion')

        if cantidad:  # Verifica que al menos la cantidad esté presente
            # Crear el nuevo horario
            nuevo_horario = Horas.objects.create(
                cantidad=cantidad,
                descripcion=descripcion or ""  # Si descripción está vacía, usa un string vacío
            )

            # Guardar el ID del nuevo horario en la sesión (opcional, si lo necesitas)
            request.session['nuevo_horario_id'] = nuevo_horario.id

            # Redirigir a la página de crear evento
            return redirect('crearevento', evento_id=request.session.get('evento_id'))

    return render(request, 'añadirhoras.html')