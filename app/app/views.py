from django.shortcuts import render
from users.views import parse_events
from users.models import UserNode
from events.models import EventNode


def index(request):
    if request.user.is_authenticated:
        _, upcoming_events = parse_events(request.user.profile.attending_events.all())
        friend_reqs = list(UserNode.friend_reqs(request.user.profile.id))
        event_reqs = list(EventNode.event_reqs(request.user.profile.id))
    else:
        upcoming_events = None
        friend_reqs = None
        event_reqs = None

    return render(request, 'index.html',
                  {'friend_reqs': friend_reqs, 'upcoming_events': upcoming_events,
                   'event_reqs': event_reqs})

