from factory import SubFactory
from factory.django import DjangoModelFactory

from src.apps.follow.models import Follow
from src.tests.factories.feed import UserFactory


class FollowFactory(DjangoModelFactory):
    """
    Follow factory.

    Generates a Follow instance, associating a user with an author.
    """

    class Meta:
        model = Follow

    user = SubFactory(UserFactory)
    author = SubFactory(UserFactory)
