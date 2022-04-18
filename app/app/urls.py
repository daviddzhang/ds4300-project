"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
import users.views as user_views
import events.views as event_views
import app.views as views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', user_views.signup, name='signup'),
    path('users/', user_views.browse_users, name='browse_users'),
    path('users/<int:user_id>/', user_views.profile, name='user_profile'),
    path('users/update_bio', user_views.update_bio, name='update_bio'),
    path('users/<int:user_id>/add', user_views.add, name='add'),
    path('users/<int:user_id>/remove', user_views.remove, name='remove'),
    path('events/', user_views.browse_events, name='browse_events'),
    path('events/<int:event_id>/', event_views.show, name='show'),
    path('events/<int:event_id>/rate', event_views.vote, name='vote'),
    path('events/<int:event_id>/attend', event_views.attend, name='attend'),
]
