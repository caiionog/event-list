from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

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

class LoginForm(forms.Form):  # Modificando para não herdar diretamente de AuthenticationForm
    nickname = forms.CharField(label="Nickname", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
