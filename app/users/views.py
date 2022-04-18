from django.contrib.auth import login, authenticate
from users.forms import SignupForm
from django.shortcuts import render, redirect
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile(request, user_id):
    profile = Profile.objects.get(pk=user_id)
    return render(request, 'users/user_profile.html', {'profile': profile})

def browse_users(request):
    return render(request, 'users/browse_users.html')

def browse_events(request):
    return render(request, 'events/browse_events.html')