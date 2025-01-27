import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe


@pytest.mark.feed
@pytest.mark.api
class TestFeedResponseFields:
    def test_reactions_field_emojies_count(
        self,
        new_user,
        api_client,
    ):
        """
        Count of emojies are reflected in reactions_count field
        """

        title = "Recipe 1"
        full_text = "recipe 1 full text"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )
        content_type = ContentType.objects.get_for_model(Recipe)
        for choice in EmojyChoice:
            Reaction.objects.create(
                author=new_user,
                object_id=new_recipe.id,
                content_type=content_type,
                emoji=choice,
            )
        url = "/api/v1/feed/?ordering=-activity_count"
        response = api_client.get(url)
        assert response.data["results"][0]["reactions_count"] == len(EmojyChoice.values)

    def test_is_favorite_field(
        self,
        new_user,
        api_client,
    ):
        """
        is_favorite is True when recipe is in user's favorite otherwise False
        """

        title = "Recipe 1"
        full_text = "recipe 1 full text"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )
        new_recipe.favorite.create(author=new_user, recipe=new_recipe)

        url = "/api/v1/feed/?ordering=-activity_count"
        response = api_client.get(url)
        assert response.data["results"][0]["is_favorite"] == False

        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.data["results"][0]["is_favorite"] == True
