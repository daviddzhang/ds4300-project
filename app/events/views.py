from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from random import sample
from events.models import Event, Address

@login_required
def show(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event_time = event.date_of_occurrence.strftime("%m/%d/%Y, %H:%M")
        event_address = Address.address_map_to_string(event.location)
        event_organizer = event.creator.user.first_name + " " + event.creator.user.last_name
        event_categories = ", ".join(event.categories)
        all_attendees = event.attendees.all()
        is_user_attending = request.user.profile in all_attendees
        attendees = [sample(all_attendees, 6)] if len(event.attendees.all()) >= 6 else all_attendees
        event_attendees = [attendee.user.first_name[0] + attendee.user.last_name[0] for attendee in attendees]
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    return render(request, 'events/show.html', {
        'event': event,
        'event_time': event_time,
        'event_address': event_address,
        'event_organizer': event_organizer,
        'event_categories': event_categories,
        'event_attendees': event_attendees,
        'is_user_attending': is_user_attending
    })

@login_required
def vote(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.ratings.append({"stars": request.POST.get('rating', None), "user_id": request.user.profile.id})
    event.save()
    return HttpResponse(status=204)

@login_required
def attend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.add(request.user.profile)
    event.save()
    request.user.profile.attending_events.add(event)
    request.user.profile.save()
    return redirect("show", event_id=event_id)

def browse_events(request):
    events = Event.objects.order_by('date_of_occurrence')
    event_data = [(event, request.user.profile in event.attendees.all()) for event in events]
    return render(request, 'events/browse_events.html', {'event_data': event_data})
