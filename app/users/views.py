from datetime import datetime
from turtle import up
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from users.models import Profile
from users.forms import SignupForm
from django.shortcuts import get_object_or_404, render, redirect

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

@login_required
def profile(request, user_id):
    profile = Profile.objects.get(pk=user_id)
    attending_events = profile.attending_events.all()
    past_events, upcoming_events = parse_events(attending_events)
    friends = profile.friends.all()
    is_friend = profile in request.user.profile.friends.all()
    print(is_friend)
    return render(request, 'users/user_profile.html', {
        'profile': profile,
        'past_events': past_events,
        'upcoming_events': upcoming_events,
        'friends': friends,
        'is_friend': is_friend,
    })

@login_required
def update_bio(request):
    if request.method == 'POST':
        print(request.POST)
        bio = request.POST['biography']
        user = request.user.profile
        user.bio = bio
        user.save()
        
    return redirect('user_profile', user_id=user.id)

@login_required
def add(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(Profile, pk=user_id)
        user = request.user.profile
        user.friends.add(friend)
        user.save()
    
    return redirect('user_profile', user_id=user_id)

@login_required
def remove(request, user_id):
    if request.method == 'POST':
        friend = get_object_or_404(Profile, pk=user_id)
        user = request.user.profile
        user.friends.remove(friend)
        user.save()
    
    return redirect('user_profile', user_id=request.POST['redirect'])

def browse_users(request):
    myuser = request.user
    users = Profile.objects.all().exclude(user_id = myuser.id)
    return render(request, 'users/browse_users.html', {'users':users})

# Helper methods

def parse_events(events):
    past_events = []
    upcoming_events = []
    
    for e in events:
        now = datetime.now()
        if e.date_of_occurrence.timestamp() >= now.timestamp():
            upcoming_events.append(e)
        else:
            past_events.append(e)
    
    return past_events, upcoming_events