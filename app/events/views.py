from django.shortcuts import render
from django.http import Http404
from .models import Event

def show(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    return render(request, 'events/show.html', {'event': event})
