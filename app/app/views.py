from django.shortcuts import render
from users.views import parse_events


def index(request):
    if request.user.is_authenticated:
        _, upcoming_events = parse_events(request.user.profile.attending_events.all())
        friend_reqs = {'Alice': "Williams", "Bob": "Jones", "John": "Miller"}

        event_reqs = {'Cooking Class': "10 January, 2022 at 3PM",
                      "Festival": "12 January, 2022 at 5:15PM",
                      "Fashion Show": "16 January, 2022 at 6:30AM"}
    else:
        upcoming_events = None
        friend_reqs = None
        event_reqs = None

    return render(request, 'index.html',
                  {'friend_reqs': friend_reqs, 'upcoming_events': upcoming_events,
                   'event_reqs': event_reqs})
