# interactions/urls.py
from django.urls import path
from .views import like_event, save_event, share_event

app_name = 'interactions'

urlpatterns = [
    path('like/<int:event_id>/', like_event, name='like_event'),
    path('save/<int:event_id>/', save_event, name='save_event'),
    path('share/<int:event_id>/', share_event, name='share_event'),
]