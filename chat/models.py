from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    def __str__(self):
        return f'{self.sender.nickname}: {self.content}'
