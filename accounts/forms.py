from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

class RegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError("Este nickname já está em uso.")
        return nickname

    def clean(self):
        cleaned_data = super().clean()
        # Captura erros de validação de senha
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "As senhas não coincidem.")

        # Adiciona mensagens de erro ao sistema de mensagens do Django
        if self.errors and hasattr(self, 'request'):  # Verifica se o request está disponível
            for field, errors in self.errors.items():
                for error in errors:
                    messages.error(self.request, error)  # Adiciona a mensagem de erro ao request

        return cleaned_data
    
class LoginForm(forms.Form):  # Modificando para não herdar diretamente de AuthenticationForm
    nickname = forms.CharField(label="Nickname", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")