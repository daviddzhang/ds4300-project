from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserNode
from events.models import Event, EventNode, EVENT_CATEGORIES_MAP
from faker import Faker
import random

NUM_USERS = 40
NUM_FRIENDS = 4
NUM_EVENTS = 10
RATINGS = ['1', '2', '3', '4', '5']


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        print("Creating users...")
        all_users = self.__create_users(fake)
        random.shuffle(all_users)

        print("Creating friendships...")
        for i in range(int(NUM_USERS / 4)):
            current_user = all_users[i]
            added_friends = self.__add_friends(current_user, all_users)
            for j in range(int(NUM_FRIENDS / 2)):
                self.__add_friends(added_friends[j], all_users)

        print("Creating events...")
        all_events = self.__create_events(fake, all_users)

        print("Creating ratings...")
        self.__create_ratings(all_users, all_events)
        print("Done!!!")

    def __create_users(self, fake):
        mongo_ids = []
        users = []
        for _ in range(NUM_USERS):
            try:
                profile = fake.simple_profile()
                name = profile['name'].split()
                user = User.objects.create_user(profile['username'], password='ds4300rox')
                user.first_name = name[0]
                user.last_name = name[1]
                user.save()
                user.refresh_from_db()
                mongo_ids.append(user.profile.id)
                users.append(user)
            except Exception as e:
                print(f"Error creating user: #{e}")

        UserNode.create_or_update(*[{'mongo_id': id} for id in mongo_ids])
        return users

    def __create_events(self, fake, all_users):
        events = []
        categories = list(EVENT_CATEGORIES_MAP.values())
        for i in range(NUM_EVENTS):
            user = all_users[i]
            location = {
                "address_line": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip_code": fake.zipcode()
            }
            event = Event(creator=user.profile, name=fake.sentence(nb_words=3), description=fake.sentence(nb_words=7),
                          date_of_occurrence=fake.date_time_this_year(),
                          categories=random.sample(categories, random.randint(1, len(categories) - 1)),
                          location=location)
            event.save()
            event.refresh_from_db()
            events.append(event)

        EventNode.create_or_update(
            *[{"mongo_id": event.id, "categories": event.categories, "datetime": event.date_of_occurrence} for event in
              events])
        return events

    def __create_ratings(self, all_users, all_events):
        for user in all_users:
            num_events_to_rate = random.randint(0, 5)
            events = random.sample(all_events, num_events_to_rate)
            for event in events:
                rating = random.choice(RATINGS)
                event.ratings.append({"stars": rating, "user_id": user.profile.id})
                event.save()
                user_node = UserNode.nodes.get(mongo_id=user.profile.id)
                event_node = EventNode.nodes.get(mongo_id=event.id)
                event_node.attended.connect(user_node, {'rating': int(rating)})

    def __add_friends(self, current_user, users_to_choose_from):
        friends = [user for user in random.sample(users_to_choose_from, NUM_FRIENDS) if user.id != current_user.id]
        for friend in friends:
            current_user.profile.friends.add(friend.profile)
            current_user.save()
            user_node = UserNode.nodes.get(mongo_id=current_user.profile.id)
            friend_node = UserNode.nodes.get(mongo_id=friend.profile.id)
            user_node.friends.connect(friend_node)

        return friends
