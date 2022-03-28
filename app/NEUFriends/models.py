import uuid
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50) # or models.EmailField()
    bio = models.CharField(max_length=100)
    friends = []

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    date_of_occurence = models.DateTimeField()
    location = models.CharField(max_length=30) # could improve using some location library or location object
    creator = models.ForeignKey(User)
    ratings_per_user = []
    category = models.TextChoices('Sports', 'Concert', 'Movie', 'Conference', 'Festival', 'Community')

