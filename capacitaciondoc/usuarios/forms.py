from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name_paterno', 'last_name_materno', 'curp', 'rol', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control','maxlength': '18'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
class SigninForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', #Username toma el dato de CURP
            'password',
            ]
 
 
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})