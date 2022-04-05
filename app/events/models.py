from email.policy import default
from djongo import models
from users.models import Profile

EVENT_CATEGORIES = (
    ('Sports','Sports'),
    ('Concert', 'Concert'),
    ('Movie','Movie'),
    ('Conference','Conference'),
    ('Festival','Festival'),
    ('Community','Community'),
)

RATINGS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class Address(models.Model):
    addressLine1 = models.CharField(max_length=30)
    addressLine2 = models.CharField(max_length=10)
    city = models.CharField(max_length=64, default='Boston')
    state = models.CharField(max_length=2, default='MA')
    zip_code = models.CharField(max_length=5)

    class Meta:
        abstract = True

class Rating(models.Model):
    stars = models.CharField(max_length=1, choices=RATINGS)
    # user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Event(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=10, choices=EVENT_CATEGORIES)
    description = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_of_occurence = models.DateTimeField()
    location = models.EmbeddedField(Address)
    # add creator
    # ratings = models.ArrayField(Rating, default=[])

    def __str__(self):
        return self.name