# models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Localização do evento
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)  # Campo para a imagem
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do evento

    def __str__(self):
        return self.name
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @classmethod
    def get_ranked_events(cls):
        # Retorna todos os eventos ordenados pelo número de curtidas (do maior para o menor)
        return cls.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')
    
class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()  # URL da imagem

    def __str__(self):
        return f"Imagem de {self.event.name}"