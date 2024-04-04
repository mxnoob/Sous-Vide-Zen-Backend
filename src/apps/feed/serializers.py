from rest_framework.serializers import IntegerField

from src.apps.recipes.serializers import BaseRecipeListSerializer, CategorySerializer


class FeedSerializer(BaseRecipeListSerializer):
    """
    Reflection of Feed page with count of emojies by type in reactions field
    """

    total_comments_count = IntegerField()
    total_reactions_count = IntegerField()
    total_views_count = IntegerField()
    activity_count = IntegerField()
    category = CategorySerializer(many=True, required=False)

    class Meta(BaseRecipeListSerializer.Meta):
        fields = BaseRecipeListSerializer.Meta.fields + (
            "category",
            "total_comments_count",
            "total_reactions_count",
            "total_views_count",
            "activity_count",
        )
