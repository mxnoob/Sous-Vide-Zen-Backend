from rest_framework.serializers import IntegerField, SerializerMethodField

from src.apps.recipes.serializers import BaseRecipeListSerializer, CategorySerializer


class FeedSerializer(BaseRecipeListSerializer):
    """
    Reflection of Feed page with count of emojies by type in reactions field
    """

    activity_count = IntegerField()
    category = CategorySerializer(many=True, required=False)
    is_favorite = SerializerMethodField()

    class Meta(BaseRecipeListSerializer.Meta):
        fields = BaseRecipeListSerializer.Meta.fields + (
            "category",
            "activity_count",
            "is_favorite",
        )

    def get_is_favorite(self, instance):

        return instance.favorite.filter(
            author__id=self.context.get("request").user.id
        ).exists()
