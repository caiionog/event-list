from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Você se registrou com sucesso!')
            return redirect('feed:index')  # Mude para a sua página inicial
    else:
        form = RegistrationForm()
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
                login(request, user)
                messages.success(request, 'Você logou com sucesso!')
                return redirect('feed:index')  # Redirecione para a página inicial
            else:
                messages.error(request, 'Credenciais inválidas. Verifique seu nickname e senha.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)  # Remove todas as informações da sessão do usuário
    return redirect('login')  # Redireciona para a página de login
