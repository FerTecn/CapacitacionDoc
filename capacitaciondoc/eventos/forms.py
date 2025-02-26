from django import forms

from catalogos.models import Departamento
from .models import Evento, Evidencia, OficioComision

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
        curso = self.instance.curso
        periodo = curso.periodo

        # Validar fechas
        if fechaInicio and fechaFin and fechaInicio > fechaFin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        # Validar horas
        if horaInicio and horaFin and horaInicio >= horaFin:
            raise forms.ValidationError("La hora de inicio debe ser menor que la hora de fin.")
        
        
        if periodo:
            periodo_inicio = periodo.inicioPeriodo
            periodo_fin = periodo.finPeriodo

            # Validaciones de fechas
            if fechaInicio and (fechaInicio < periodo_inicio or fechaInicio > periodo_fin):
                raise forms.ValidationError({'fechaInicio': f"La fecha de inicio debe estar dentro del periodo {periodo_inicio} - {periodo_fin}"})
            
            if fechaFin and (fechaFin < periodo_inicio or fechaFin > periodo_fin):
                raise forms.ValidationError({'fechaFin': f"La fecha de fin debe estar dentro del periodo {periodo_inicio} - {periodo_fin}"})

            if fechaInicio and fechaFin and fechaInicio > fechaFin:
                raise forms.ValidationError({'fechaFin': "La fecha de fin no puede ser anterior a la fecha de inicio."})

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

# Formulario de la lista seleccionable para SELECCIONAR DEPARTAMENTO
class DepartamentoForm(forms.Form):
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        empty_label="-- Selecciona un departamento --",
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True,
    )

    def clean_departamento(self):
        departamento = self.cleaned_data.get('departamento')
        if not departamento:  # Si el valor es None o vacío
            raise forms.ValidationError("Por favor selecciona un departamento válido.")
        return departamento

    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        # Si se pasa un valor inicial, establecerlo en el campo departamento
        self.fields['departamento'].initial = kwargs['initial']['departamento']

class OficioComisionForm(forms.ModelForm):
    class Meta:
        model = OficioComision
        fields = ['no_oficio', 'fecha']
        labels ={
            'no_oficio': 'No. de oficio',
            'fecha': 'Fecha de emisión',
        }
        widgets = {
            'no_oficio': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        }