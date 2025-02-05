# models.py
from django.conf import settings
from django.db import models
from django.db.models import Count

class Event(models.Model):
    # Opções para a categoria
    CATEGORY_CHOICES = [
        ('BAR', 'Bar'),
        ('RESTAURANT', 'Restaurante'),
        ('PARTY', 'Festa'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)  # Localização do evento
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)  # Campo para a imagem
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do evento

    # Novo campo para categoria
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='PARTY')

    # Novo campo para cidade
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def saves_count(self):
        return self.saves.count()
    
    @property
    def shares_count(self):
        return self.shares.count()
    
    @classmethod
    def get_ranked_events(cls):
        # Retorna todos os eventos ordenados pelo número de curtidas (do maior para o menor)
        return cls.objects.annotate(total_likes=Count('likes')).order_by('-total_likes')
    
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='eventsimages/')
    
class SolicitacaoAcesso(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuario_solicitacao')
    mensagem = models.TextField(blank=True, null=True, verbose_name="Mensagem")
    data_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Solicitação")
    aprovado = models.BooleanField(default=False, verbose_name="Aprovado?")

    def __str__(self):
        return f"Solicitação de {self.user.nickname}"

    class Meta:
        verbose_name = "Solicitação de Acesso"
        verbose_name_plural = "Solicitações de Acesso"