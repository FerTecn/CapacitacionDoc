from django import forms
from .models import Encuesta


class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        exclude = {'inscripcion'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'comentarios':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control w-75 m-4',
                    'rows': 4,
                    'cols': 50,
                })
            else:
                choices = list(self.fields[field].choices) #convertimos a lista
                self.fields[field].choices = choices[1:] # Elimina opcion  vacia
                self.fields[field].widget = forms.RadioSelect(choices=self.fields[field].choices, attrs={'class': 'horizontal-radio'})