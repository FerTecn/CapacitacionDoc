from django import forms
from django.forms import inlineformset_factory
from .models import ContenidoTematico, CriterioEvaluacion, FichaTecnica, RegistroCurso

class CursoForm(forms.ModelForm):
    class Meta:
        model = RegistroCurso
        #En lugar de poner todos los campos con fields = '__all__', pongo exlude y se pone el campo que no quiero que se muestre
        exclude = ['aceptado'] 
        labels={'nombre': 'Nombre del cuso', 
                'periodo': 'Periodo del curso',  
                'dirigido': 'Dirigido a', 
                'perfilCurso': 'Perfil del curso'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 


class FichaTecnicaForm(forms.ModelForm):
    class Meta:
        model = FichaTecnica
        fields = ['introduccion', 'justificacion', 'servicio', 'elementosDidacticos', 'competencias', 'fuentes']
        labels = {
            'introduccion': 'Introducción',
            'justificacion': 'Justificación',
            'servicio': 'Tipo de servicio',
            'elementosDidacticos': 'Elementos didácticos',
            'competencias': 'Competencias a desarrollar',
            'fuentes': 'Fuentes de información',
        }
        widgets = {
            'introduccion': forms.Textarea(attrs={'class': 'form-control'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control ', }),
            'competencias': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;'}),
            'elementosDidacticos': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px;'}),
            'fuentes': forms.Textarea(attrs={'class': 'form-control'}),
        }
    

class ContenidoTematicoForm(forms.ModelForm):
    class Meta:
        model = ContenidoTematico
        fields = ['tema', 'tiempo', 'actividades']
        labels = {
            'tema': 'Tema/Subtema',
            'tiempo': 'Tiempo programado en horas',
            'actividades': 'Actividades',
        }
        widgets = {
            'tema': forms.DateInput(attrs={'class': 'form-control'}),
            'tiempo': forms.NumberInput(attrs={'class': 'form-control'}),
            'actividades': forms.Textarea(attrs={'class': 'form-control ', 'style': 'height: 100px;'}),
           
        }

class CriterioEvaluacionForm(forms.ModelForm):
    class Meta:
        model = CriterioEvaluacion
        fields = ['criterio', 'valor', 'instrumento']
        labels = {
            'criterio': 'Criterio de evaluación',
            'valor': 'Valor',
            'instrumento': 'Instrumento de evaluación',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'}) 

# Crear formsets para manejar múltiples contenidos temáticos y criterios de evaluación dentro de la ficha
ContenidoTematicoFormSet = inlineformset_factory(FichaTecnica, ContenidoTematico, form=ContenidoTematicoForm, extra=1, can_delete=True)
CriterioEvaluacionFormSet = inlineformset_factory(FichaTecnica, CriterioEvaluacion, form=CriterioEvaluacionForm, extra=1, can_delete=True)
