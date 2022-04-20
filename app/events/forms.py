from events.models import Event, EVENT_CATEGORIES
from django import forms
from django.contrib.admin import widgets

class EventForm(forms.Form):
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', widget=forms.Textarea, max_length=100)
    date_of_occurrence = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(format=['%Y-%m-%dT%H:%M'], attrs={'type': 'datetime-local'}))
    categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=EVENT_CATEGORIES)
    address_line = forms.CharField()
    city = forms.CharField()
    state = forms.CharField(max_length=2)
    zip_code = forms.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_of_occurrence"].input_formats = ["%Y-%m-%dT%H:%M"]

