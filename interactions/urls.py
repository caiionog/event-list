# interactions/urls.py
from django.urls import path
from .views import like_event, save_event

app_name = 'interactions'

urlpatterns = [
    path('like/<int:event_id>/', like_event, name='like_event'),
    path('save/<int:event_id>/', save_event, name='save_event'),
]