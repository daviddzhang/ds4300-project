from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def browseUsers(request):
    return render(request, 'browseUsers.html')
