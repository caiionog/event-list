from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'reported', 'created_at')  # Campos do modelo
    list_filter = ('reported',)  # Filtro por campo 'reported'
    search_fields = ('content', 'sender__nickname')  # Pesquisa por conteúdo e nome do remetente
