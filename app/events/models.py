from djongo import models
from users.models import Profile, UserNode
from neomodel import StructuredNode, ArrayProperty, StringProperty, DateTimeProperty, Relationship, StructuredRel, \
    IntegerProperty

RATINGS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
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
    categories = ArrayProperty(StringProperty(), required=True)
    datetime = DateTimeProperty(required=True)
    attended = Relationship(UserNode, 'ATTENDED', model=AttendanceRel)
