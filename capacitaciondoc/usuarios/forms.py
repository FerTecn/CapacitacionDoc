from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name_paterno', 'last_name_materno', 'curp', 'rol', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Nombre(s)'

        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control','maxlength': '18'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

            

class SigninForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     curp = cleaned_data.get('curp')
    #     password = cleaned_data.get('password')
        
    #     # Validamos que el CURP exista y sea correcto
    #     usuario = CustomUser.objects.filter(curp=curp).first()
    #     if not usuario:
    #         raise forms.ValidationError('CURP no encontrado.')
    #     if not usuario.check_password(password):  # Usamos check_password para verificar la contraseña encriptada
    #         raise forms.ValidationError('Contraseña incorrecta.')
        
    #     cleaned_data['user'] = usuario
    #     return cleaned_data