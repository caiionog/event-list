# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm, EventImageFormSet
from django.contrib.auth.decorators import login_required
from .models import Event, SolicitacaoAcesso, EventImage
from django.contrib import messages
import requests

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        formset = EventImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()  # Salva o evento primeiro

            # Associa o evento ao formset e salva as imagens
            for form in formset:
                if form.cleaned_data.get('image'):  # Verifica se há uma imagem no formulário
                    image = form.cleaned_data['image']
                    EventImage.objects.create(event=event, image=image)  # Salva manualmente

            return redirect('feed:index')
    else:
        form = EventForm()
        formset = EventImageFormSet()

    return render(request, 'events/create_event.html', {'form': form, 'formset': formset})

def solicitar_acesso(request):
    if request.method == 'POST':
        # Cria uma nova solicitação de acesso
        mensagem = request.POST.get('message', '')
        SolicitacaoAcesso.objects.create(
            user=request.user,  # Atualize para user
            mensagem=mensagem
        )
        messages.success(request, 'Sua solicitação de acesso foi enviada aos administradores.')
        return redirect('feed:index')
    return render(request, 'events/solicitar_acesso.html')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Recupera o evento pelo ID ou retorna 404
    return render(request, 'events/event_detail.html', {'event': event})