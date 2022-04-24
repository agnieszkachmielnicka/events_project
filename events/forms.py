from django import forms
from events.models import Event
from events.widgets import DateTimePickerInput

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date',]

        widgets = {
            'event_date' : DateTimePickerInput(),
        }