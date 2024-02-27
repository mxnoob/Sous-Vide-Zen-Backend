import pytest

from src.apps.recipes.models import Recipe
from src.apps.view.models import ViewRecipes


@pytest.mark.django_db
@pytest.mark.api
class TestViewRecipesModel:
    """
    Tests for ViewRecipes model
    """

    def test_view_recipes_model(self, new_user, new_author):
        """
        Test for ViewRecipes model
        """

        recipe = Recipe.objects.create(
            author=new_author,
            title="Test Recipe",
            slug="test-recipe",
            full_text="This is a test recipe full text.",
            short_text="Test short text",
            cooking_time=30,
        )

        assert ViewRecipes.objects.count() == 0

        ViewRecipes.objects.create(user=new_user, recipe=recipe)
        assert ViewRecipes.objects.count() == 1
