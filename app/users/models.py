from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from neomodel import StructuredNode, IntegerProperty, Relationship, StructuredRel
from events.models import EventNode

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True)
    friends = models.ArrayReferenceField(to="Profile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            UserNode(mongo_id=instance.id).save()
        instance.profile.save()

class AttendanceRel(StructuredRel):
    rating = IntegerProperty(required=True)

class UserNode(StructuredNode):
    mongo_id = IntegerProperty(unique_index=True, required=True)
    friends = Relationship('UserNode', 'FRIEND')
    attended = Relationship('EventNode', 'ATTENDED', model=AttendanceRel)
