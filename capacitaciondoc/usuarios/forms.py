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

    # Para solo permitir el rol "Jefe de Capacitación"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['rol'].choices = [
            ('Jefe de Capacitación', 'Jefe de Capacitación'),
        ]

class CreateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name_paterno', 'last_name_materno', 'curp', 'rol', 'email', 'is_active']
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
    
    def clean_curp(self):
        curp = self.cleaned_data['curp']
        
        # Verifica si estamos editando un usuario existente
        if self.instance.pk:
            # Si el CURP cambió y ya existe en otro usuario, lanza error
            if CustomUser.objects.filter(curp=curp).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este CURP ya está registrado.")
        else:
            # Si es creación, simplemente verifica si existe
            if CustomUser.objects.filter(curp=curp).exists():
                raise forms.ValidationError("Este CURP ya está registrado.")
        
        return curp

    
    def save(self, commit=True):
        user = super().save(commit=False)
        if self.instance._state.adding:  # Solo si es nuevo
            user.set_password(user.curp)
        if commit:
            user.save()
        return user

    # Para solo permitir agregar roles de de Capacitación, Subdirección y Jefe Académico
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].choices = [
            ('Jefe de Capacitación', 'Jefe de Capacitación'),
        ]

class SigninForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})