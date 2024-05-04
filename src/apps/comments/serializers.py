from rest_framework.serializers import ModelSerializer

from src.apps.comments.models import Comment
from src.apps.users.serializers import AuthorInRecipeSerializer


class CommentListSerializer(ModelSerializer):
    """
    Serializer for viewing comments
    """

    author = AuthorInRecipeSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "text", "pub_date", "updated_date")


class CommentCreateSerializer(ModelSerializer):
    """
    Serializer for creating and updating comments
    """

    class Meta:
        model = Comment
        fields = ("text", "parent")
