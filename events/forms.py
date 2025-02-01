# forms.py
from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'image']  # Não precisa do 'creator' pois será preenchido automaticamente