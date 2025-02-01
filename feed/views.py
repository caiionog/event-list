from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from chat.models import Message
from interactions.models import Like
from chat.forms import MessageForm

@login_required
def index(request):
    # Lógica da view
    events = Event.get_ranked_events()
    messages = Message.objects.all().order_by('created_at')[:50]
    liked_event_ids = Like.objects.filter(user=request.user).values_list('event_id', flat=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('feed:index')  # Redireciona para evitar reenvio do formulário
    else:
        form = MessageForm()

    return render(request, 'feed/index.html', {
        'events': events,
        'chat_messages': messages,
        'form': form,
        'liked_event_ids': liked_event_ids,
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Verifica se o usuário é o dono da mensagem ou um admin
    if request.user == message.sender or request.user.is_staff:
        message.delete()
        messages.success(request, "Mensagem apagada com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para apagar esta mensagem.")
    
    return redirect('feed:index')  # Redireciona de volta ao chat

@login_required
def report_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Verifica se o usuário não é o dono da mensagem
    if request.user != message.sender:
        message.reported = True
        message.save()
        messages.success(request, "Mensagem denunciada com sucesso.")
    else:
        messages.error(request, "Você não pode denunciar sua própria mensagem.")
    
    return redirect('feed:index')  # Redireciona de volta ao chat