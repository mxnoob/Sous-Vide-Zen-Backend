import factory
from factory.django import DjangoModelFactory
from src.apps.users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    """
    CustomUser factory.

    Generates a CustomUser with a unique username, corresponding email,
    and a predefined password.
    """

    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"test_user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@x.com")
    password = "test_password"
