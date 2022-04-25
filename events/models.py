from djongo import models
from users.models import Profile, UserNode
from neomodel import StructuredNode, ArrayProperty, StringProperty, DateTimeProperty, Relationship, StructuredRel, \
    IntegerProperty, db

RATINGS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

EVENT_CATEGORIES_MAP = {
    '1': 'Food',
    '2': 'Outdoors',
    '3': 'Music',
    '4': 'Fitness & Wellness',
    '5': 'Sports',
    '6': 'Movies',
    '7': 'Studying'
}

EVENT_CATEGORIES = (
    ('1', 'Food'),
    ('2', 'Outdoors'),
    ('3', 'Music'),
    ('4', 'Fitness & Wellness'),
    ('5', 'Sports'),
    ('6', 'Movies'),
    ('7', 'Studying')
)


class Address(models.Model):
    address_line = models.CharField(max_length=30)
    city = models.CharField(max_length=64, default='Boston')
    state = models.CharField(max_length=2, default='MA')
    zip_code = models.CharField(max_length=5)

    @staticmethod
    def address_map_to_string(address):
        return address["address_line"] + " " + address["city"] + ", " \
               + address["state"] + " " + address["zip_code"]

    class Meta:
        abstract = True


class Rating(models.Model):
    stars = models.CharField(max_length=1, choices=RATINGS)
    # cannot use foreign key inside embedded field, per djongo's restriction :/
    user_id = models.BigIntegerField()

    class Meta:
        abstract = True


class Event(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    attendees = models.ArrayReferenceField(to=Profile, on_delete=models.CASCADE, related_name="attending", default=[])
    categories = models.JSONField()
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_occurrence = models.DateTimeField()
    location = models.EmbeddedField(Address)
    # add creator
    ratings = models.ArrayField(model_container=Rating, default=[])

    def __str__(self):
        return self.name


class AttendanceRel(StructuredRel):
    rating = IntegerProperty(required=True)


class EventNode(StructuredNode):
    mongo_id = IntegerProperty(unique_index=True, required=True)
    categories = ArrayProperty(StringProperty(), required=True)
    datetime = DateTimeProperty(required=True)
    attended = Relationship(UserNode, 'ATTENDED', model=AttendanceRel)

    @staticmethod
    def event_reqs(mongo_id):
        cypher_query = """
        MATCH (u1:UserNode {mongo_id: %d})-[f]-(u2:UserNode),
        (u2)-[a]-(e:EventNode)
        WHERE e.datetime > datetime().epochSeconds
        AND NOT (u1)-[]-(e)
        return e
        """ % (mongo_id)
        results, columns = db.cypher_query(cypher_query)
        nodes = [EventNode.inflate(row[0]) for row in results]
        ids = set([node.mongo_id for node in nodes])
        return Event.objects.filter(id__in=ids).all()
