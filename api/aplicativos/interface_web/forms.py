from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from aplicativos.energia.models import ConfiguracaoEnergetica
from aplicativos.maquinas.models import Maquina


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={'id': 'username', 'required': True}),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'id': 'password', 'required': True}),
    )


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'required': True}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class MaquinaEditForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = [
            'hostname',
            'intervalo_coleta_segundos',
            'intervalo_envio_segundos',
            'ativo',
        ]


class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ConfiguracaoEnergeticaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoEnergetica
        fields = [
            'tdp_cpu_watts',
            'fator_idle_alpha',
            'consumo_ram_por_gb',
            'ativo',
        ]
