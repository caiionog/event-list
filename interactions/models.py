# interactions/models.py
from django.db import models
from django.contrib.auth.models import User
from events.models import Event  # Supondo que o app de eventos se chame "events"
from django.conf import settings

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Impede que o mesmo usuário curta o mesmo evento mais de uma vez

    def __str__(self):
        return f'{self.user.nickname} curtiu {self.event.name}'
    
class Save(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saves')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='saves')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # Impede que o mesmo usuário salve o mesmo evento mais de uma vez

    def __str__(self):
        return f'{self.user.nickname} salvou {self.event.name}'
    
class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shares')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='shares')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.nickname} compartilhou {self.event.name}'