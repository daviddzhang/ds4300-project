from django.shortcuts import render


def index(request):
    upcoming_events = {'Picnic': "10 January, 2022 at 3PM",
                       "Super cool concert!": "12 January, 2022 at 5:15PM",
                       "Workout session": "16 January, 2022 at 6:30AM"}
    friend_reqs = {'Alice': "Williams", "Bob": "Jones", "John": "Miller"}

    event_reqs = {'Cooking Class': "10 January, 2022 at 3PM",
                  "Festival": "12 January, 2022 at 5:15PM",
                  "Fashion Show": "16 January, 2022 at 6:30AM"}

    return render(request, 'index.html',
                  {'friend_reqs': friend_reqs, 'upcoming_events': upcoming_events,
                   'event_reqs': event_reqs})
