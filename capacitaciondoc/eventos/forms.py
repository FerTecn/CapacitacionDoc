from django import forms
from .models import Evento, Evidencia

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['fechaInicio', 'fechaFin', 'horaInicio', 'horaFin', 'lugar']
        labels ={
            'fechaInicio': 'Fecha de inicio',
            'fechaFin': 'Fecha de culminación',
        }
        widgets = {
            'fechaInicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'fechaFin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'horaInicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'horaFin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        fechaInicio = cleaned_data.get('fechaInicio')
        fechaFin = cleaned_data.get('fechaFin')
        horaInicio = cleaned_data.get('horaInicio')
        horaFin = cleaned_data.get('horaFin')

        # Validar fechas
        if fechaInicio and fechaFin and fechaInicio > fechaFin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        # Validar horas
        if horaInicio and horaFin and horaInicio >= horaFin:
            raise forms.ValidationError("La hora de inicio debe ser menor que la hora de fin.")

        return cleaned_data

class EvidenciaForm(forms.ModelForm):
    class Meta:
        model = Evidencia
        fields = ['archivo_evidencia']
        widgets = {
            'archivo_evidencia': forms.FileInput(attrs={
                'class': 'btn btn-primary',  # Clase CSS para estilos
                'accept': 'image/*',  # Aceptar solo imágenes
                'id': 'imagen-input',  # ID para JavaScript
            }),
        }