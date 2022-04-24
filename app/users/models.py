from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from neomodel import StructuredNode, IntegerProperty, Relationship, db

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

    @staticmethod
    def friend_reqs(mongo_id):
        cypher_query = """
        CALL {
            MATCH (u:UserNode)-[a:ATTENDED]-(e:EventNode)
            WHERE a.rating >= 4
            UNWIND e.categories as x
            return [u.mongo_id, [counts in apoc.coll.sortMaps(apoc.coll.frequencies(collect(x)), 'count')[0..5] | counts.item]] as top_cats
        }
        // Convert the previously created list of pairs into a mapping from mongo_id -> list of top categories
        CALL {
            with top_cats
            return apoc.map.fromPairs(collect(top_cats)) as user_mapped_top_cats
        }
        WITH apoc.map.mergeList(collect(user_mapped_top_cats)) as user_top_cats
        // only match top categories of users who aren't friends but have a mutual friends
        MATCH (u1:UserNode {mongo_id: %d})-[f:FRIEND]-(mutual:UserNode)-[f2:FRIEND]-(u2:UserNode)
        WHERE apoc.coll.isEqualCollection(user_top_cats[apoc.convert.toString(u1.mongo_id)], user_top_cats[apoc.convert.toString(u2.mongo_id)]) and u1.mongo_id <> u2.mongo_id and user_top_cats[apoc.convert.toString(u1.mongo_id)] IS NOT NULL and user_top_cats[apoc.convert.toString(u2.mongo_id)] IS NOT NULL
        AND NOT (u1)-[]-(u2)
        return u2
        """ % (mongo_id)
        results, columns = db.cypher_query(cypher_query)
        nodes = [UserNode.inflate(row[0]) for row in results]
        ids = set([node.mongo_id for node in nodes])
        return Profile.objects.filter(id__in=ids).all()
