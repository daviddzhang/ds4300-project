from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from random import sample
from events.models import Event, Address, EVENT_CATEGORIES_MAP, EventNode
from users.models import UserNode
from events.forms import EventForm


@login_required
def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            date_of_occurrence = form.cleaned_data['date_of_occurrence']
            categories = [EVENT_CATEGORIES_MAP[category] for category in form.cleaned_data['categories']]
            address_line = form.cleaned_data['address_line']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']

            location = {
                'address_line': address_line,
                'city': city,
                'state': state,
                'zip_code': zip_code
            }
            event = Event(creator=request.user.profile, name=name, description=description,
                          date_of_occurrence=date_of_occurrence, categories=categories, location=location)
            event.save()
            event.refresh_from_db()
            EventNode(mongo_id=event.id, categories=event.categories, datetime=event.date_of_occurrence).save()
            return redirect("show", event.id)
    else:
        form = EventForm()
    return render(request, 'events/new_event.html', {'form': form})


@login_required
def show(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
        event_time = event.date_of_occurrence.strftime("%m/%d/%Y, %H:%M")
        event_address = Address.address_map_to_string(event.location)
        event_organizer = event.creator.user.first_name + " " + event.creator.user.last_name
        event_categories = ", ".join(event.categories)
        all_attendees = list(event.attendees.all())
        is_user_attending = request.user.profile in all_attendees
        attendees = sample(all_attendees, 12) if len(all_attendees) >= 12 else all_attendees
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
def rate(request, event_id):
    rating = request.POST.get('rating', None)
    if rating is None:
        return HttpResponseBadRequest("Missing rating")

    event = get_object_or_404(Event, pk=event_id)
    event.ratings.append({"stars": rating, "user_id": request.user.profile.id})
    event.save()
    user_node = UserNode.nodes.get(mongo_id=request.user.profile.id)
    event_node = EventNode.nodes.get(mongo_id=event.id)
    event_node.attended.connect(user_node, {'rating': int(rating)})
    return HttpResponse(status=204)


@login_required
def attend(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.attendees.add(request.user.profile)
    event.save()
    request.user.profile.attending_events.add(event)
    request.user.profile.save()
    return redirect("show", event_id=event_id)


@login_required
def leave(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        user = request.user.profile
        user.attending_events.remove(event)
        user.save()
        event.attendees.remove(user)
        event.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def browse_events(request):
    search_query = request.GET.get('q', '')
    events = Event.objects.filter(name__contains=search_query).order_by('date_of_occurrence')
    event_data = [(event, request.user.profile in event.attendees.all()) for event in events]
    return render(request, 'events/browse_events.html', {'event_data': event_data})