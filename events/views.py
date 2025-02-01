# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .models import Event
from django.db.models import Q
from chat.models import Message
import requests

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)  # Inclua request.FILES para lidar com uploads
        if form.is_valid():
            event = form.save(commit=False)  # Cria o objeto Event, mas não salva no banco ainda

            google_api_key = "AIzaSyCr0GbQwgjDZmGDxyl_SR1r9hLPeq9-moM"
            endereco = event.location
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={google_api_key}"
            response = requests.get(url).json()
            if response["status"] == "OK":
                location = response["results"][0]["geometry"]["location"]
                event.latitude = location["lat"]
                event.longitude = location["lng"]

            event.creator = request.user  # Atribui o usuário atual como criador do evento
            event.save()  # Agora salva o evento no banco de dados
            return redirect('feed:index')  # Redireciona para a página inicial após salvar
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})
def search_events(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        events = Event.objects.all()
    
    # Recupere as mensagens do chat
    messages = Message.objects.all()  # Ou filtre conforme necessário
    
    return render(request, 'feed/index.html', {
        'events': events,
        'messages': messages,  # Passa as mensagens para o template
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Recupera o evento pelo ID ou retorna 404
    return render(request, 'events/event_detail.html', {'event': event})