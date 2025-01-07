from django import forms
from .models import Curso
from .forms import SeleccionarCursoForm


class SeleccionarCursoForm(forms.Form):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        empty_label="Seleccione un curso",
        widget=forms.Select(attrs={"class": "form-control"})
    )