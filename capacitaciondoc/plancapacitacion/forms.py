from django import forms
from .models import registroCurso

class EditarCursoForm(forms.ModelForm):
    class Meta:
        model = registroCurso
        fields = ['clave', 'nombre', 'objetivo', 'periodo', 'sede', 'horas', 'instructor', 'dirigido', 'perfilCurso']

class AñadirCursoForm(forms.ModelForm):
    class Meta:
        model= registroCurso
        fields = ['clave', 'nombre', 'objetivo', 'periodo', 'sede', 'horas', 'instructor', 'dirigido', 'perfilCurso']