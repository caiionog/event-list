# urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/', views.create_event, name='create_event'),  # URL para criar evento
    path('<int:event_id>/', views.event_detail, name='event_detail'),  # Detalhes do evento
    path('solicitar_acesso/', views.solicitar_acesso, name='solicitar_acesso'),
]