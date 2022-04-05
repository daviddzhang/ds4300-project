from djongo import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    # friends = models.ArrayReferenceField(to=Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username