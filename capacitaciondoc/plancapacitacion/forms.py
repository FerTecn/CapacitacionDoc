from django import forms
from .models import RegistroCurso

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

