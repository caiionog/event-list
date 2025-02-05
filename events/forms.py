from django import forms
from django.forms import inlineformset_factory
from .models import Event, EventImage

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'category', 'city', 'location', 'image']

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ['image']

EventImageFormSet = inlineformset_factory(
    Event, 
    EventImage, 
    form=EventImageForm, 
    extra=2, 
    can_delete=False, 
    max_num=2, 
    validate_max=True
)