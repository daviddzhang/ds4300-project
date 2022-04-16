from django.shortcuts import render


def index(request):
    friend_reqs = []
    return render(request, 'index.html', {'friend_reqs': friend_reqs})

