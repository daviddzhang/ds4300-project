import uuid
from django import forms
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    bio = models.CharField(max_length=100)
    friends = []

    def __str__(self):
        return self.username

EVENT_CATEGORIES = (
    ('Sports','Sports'),
    ('Concert', 'Concert'),
    ('Movie','Movie'),
    ('Conference','Conference'),
    ('Festival','Festival'),
    ('Community','Community'),
)
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=10, choices=EVENT_CATEGORIES)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_occurence = models.DateTimeField()
    location = models.CharField(max_length=30) # could improve using some location library or location object
    # add creator
    ratings_per_user = []

    def __str__(self):
        return self.name