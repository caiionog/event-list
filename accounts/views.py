from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form.request = request
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # O usuário não estará ativo até confirmar o e-mail
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Gerar token de verificação
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construir o link de verificação
            verification_link = f"{settings.BASE_URL}/accounts/verify-email/{uid}/{token}/"

            # Enviar e-mail de verificação
            send_mail(
                'Verifique seu e-mail',
                f'Clique no link para verificar seu e-mail: {verification_link}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Por favor, verifique seu e-mail para ativar sua conta.')
            return redirect('login')  # Redirecione para a página de login
    else:
        form = RegistrationForm()
        form.request = request
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']

            # Autenticar usuário com nickname
            user = authenticate(request, username=nickname, password=password)
            if user:
                if user.is_admin:
                    login(request, user)
                    return redirect('feed:index')
                if user.is_verified:  # Verifique se o usuário está verificado
                    login(request, user)
                    messages.success(request, 'Você logou com sucesso!')
                    return redirect('feed:index')  # Redirecione para a página inicial
                else:
                    messages.error(request, "Por favor, verifique seu e-mail antes de fazer login.")
            else:
                messages.error(request, 'Credenciais inválidas. Verifique seu nickname e senha.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)  # Remove todas as informações da sessão do usuário
    return redirect('login')  # Redireciona para a página de login

User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Ativa a conta do usuário
        user.is_verified = True  # Define o campo is_verified como True
        user.save()
        messages.success(request, 'Seu e-mail foi verificado com sucesso! Agora você pode fazer login.')
        return redirect('login')
    else:
        messages.error(request, 'Link de verificação inválido ou expirado.')
        return redirect('register')
