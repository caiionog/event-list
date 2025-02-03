# interactions/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from events.models import Event
from .models import Like, Save, Share
from django.contrib import messages

@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    messages.info(request, 'Você curtiu esse evento')
    # Verifica se o usuário já curtiu o evento
    like, created = Like.objects.get_or_create(user=request.user, event=event)
    if not created:
        messages.info(request, 'Você descurtiu esse evento')
        like.delete()  # Remove a curtida se já existir (funcionalidade de "descurtir")
    return redirect('feed:index')  # Redireciona para a página inicial ou outra URL

@login_required
def save_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    messages.info(request, 'Você salvou esse evento')
    # Verifica se o usuário já salvou o evento
    save, created = Save.objects.get_or_create(user=request.user, event=event)
    if not created:
        messages.info(request, 'Você removeu esse evento')
        save.delete()  # Remove o salvamento se já existir (funcionalidade de "desfazer salvamento")
    return redirect('feed:index')  # Redireciona para a página inicial ou outra URL

@login_required
def share_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    messages.info(request, 'Você compartilhou esse evento')
    # Verifica se o usuário já salvou o evento
    share, created = Share.objects.get_or_create(user=request.user, event=event)
    return redirect('feed:index')  # Redireciona para a página inicial ou outra URL
