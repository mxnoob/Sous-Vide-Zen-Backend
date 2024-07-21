from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from src.base.code_text import (
    PASSWORDS_ARE_NOT_SIMILAR,
)
from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Serializer for CustomUser model for create endpoint with email and two
    passwords
    """

    password2 = serializers.CharField(
        style={"input_type": "password"}, required=True, write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password", "password2"]
        extra_kwargs = {"email": {"required": True}}

    def validate(self, attrs):
        validate_password(attrs["password"])
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                PASSWORDS_ARE_NOT_SIMILAR, code="passwords_are_not_similar"
            )
        del attrs["password2"]

        return attrs


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model
    """

    username = serializers.CharField(required=False, read_only=True)
    email = serializers.EmailField(required=False, read_only=True)
    is_active = serializers.BooleanField(required=False, read_only=True)
    is_staff = serializers.BooleanField(required=False, read_only=True)
    is_admin = serializers.BooleanField(required=False, read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "display_name",
            "email",
            "avatar",
            "phone",
            "date_joined",
            "country",
            "city",
            "first_name",
            "last_name",
            "bio",
            "is_active",
            "is_staff",
            "is_admin",
        ]


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model for list endpoint
    """

    is_follow = serializers.BooleanField()
    is_follower = serializers.BooleanField()
    recipes_count = serializers.IntegerField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "display_name",
            "avatar",
            "recipes_count",
            "is_follow",
            "is_follower",
        )


class CustomUserMeSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model for me endpoint
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "display_name",
            "avatar",
            "is_active",
            "is_staff",
            "is_admin",
        )


class AuthorInRecipeSerializer(serializers.ModelSerializer):
    """
    Author in recipe serializer
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "display_name", "avatar")
