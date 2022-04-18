from django.contrib.auth import login, authenticate
from users.models import Profile
from users.forms import SignupForm
from django.shortcuts import render, redirect

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


def browse_users(request):
    myuser = request.user
    users = Profile.objects.all().exclude(user_id = myuser.id)
    return render(request, 'users/browse_users.html', {'users':users})

def browse_events(request):
    return render(request, 'events/browse_events.html')
