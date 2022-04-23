from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from neomodel import StructuredNode, IntegerProperty, Relationship, StructuredRel

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    friends = models.ArrayReferenceField(to="Profile", on_delete=models.CASCADE)
    attending_events = models.ArrayReferenceField(to='events.Event', on_delete=models.CASCADE, default=[])

    def __str__(self):
        return self.user.username

    def upcomingEvent(self):
        return ''
    
    def pastEvent(self):
        return ''
    

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = Profile.objects.create(user=instance)
            UserNode(mongo_id=profile.id).save()
        instance.profile.save()

class UserNode(StructuredNode):
    mongo_id = IntegerProperty(unique_index=True, required=True)
    friends = Relationship('UserNode', 'FRIEND')
