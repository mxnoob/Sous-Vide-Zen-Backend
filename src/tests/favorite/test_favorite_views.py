from collections import OrderedDict
import pytest

from src.apps.favorite.models import Favorite
from src.apps.recipes.serializers import FavoriteRecipesSerializer


@pytest.mark.favorite
@pytest.mark.models
class TestFavoriteRecipesListPage:
    def test_favorite_recipes_list_page(self, api_client, new_user, new_recipe):
        """
        Favorite recipes list pagination and serializer test
        [GET] http://127.0.0.1:8000/api/v1/recipe/favorites/
        """
        example_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                OrderedDict(
                    [
                        ("id", new_recipe.id),
                        ("title", new_recipe.title),
                        ("slug", new_recipe.slug),
                        (
                            "author",
                            OrderedDict(
                                [
                                    ("id", new_recipe.author.id),
                                    ("username", new_recipe.author.username),
                                    ("display_name", None),
                                    ("avatar", None),
                                ]
                            ),
                        ),
                        ("preview_image", new_recipe.preview_image),
                        ("short_text", new_recipe.short_text),
                        ("tag", []),
                        ("comments_count", 0),
                        ("reactions_count", 0),
                        ("views_count", 0),
                        ("cooking_time", new_recipe.cooking_time),
                        ("pub_date", None),
                    ]
                )
            ],
        }
        Favorite.objects.create(author=new_user, recipe=new_recipe)

        url = f"/api/v1/recipe/favorites/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        response_data = response.data.get("results")
        response_data[-1]["pub_date"] = None

        assert response.data == example_data
        assert response.status_code == 200

        serializer = FavoriteRecipesSerializer(new_recipe)
        serializer_data = serializer.data.copy()
        serializer_data.pop("pub_date", None)
        example_data = example_data["results"][-1]
        example_data.pop("comments_count")
        example_data.pop("reactions_count")
        example_data.pop("views_count")
        example_data.pop("pub_date")

        assert OrderedDict(serializer_data) == example_data

    def test_favorite_recipes_list_unauthorized(self, api_client, new_user, new_recipe):
        """
        Favorite recipes list for unauthorized user test
        [GET] http://127.0.0.1:8000/api/v1/recipe/favorites/
        """
        url = f"/api/v1/recipe/favorites/"
        response = api_client.get(url)

        assert response.data == {"detail": "Учетные данные не были предоставлены."}
        assert response.status_code == 401

    def test_favorite_recipes_empty_page(self, api_client, new_user, new_recipe):
        """
        Favorite recipes empty page test
        [GET] http://127.0.0.1:8000/api/v1/recipe/favorites/
        """
        url = f"/api/v1/recipe/favorites/"
        api_client.force_authenticate(user=new_user)
        response = api_client.get(url)
        assert response.data == {"detail": "Список избранных рецептов пуст."}
        assert response.status_code == 200


class TestFavoriteRecipeCreationDeletionView:
    def test_recipe_add_to_favorites(self, api_client, new_user, new_recipe):
        """
        Adding recipe to favorites test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """
        slug = new_recipe.slug
        url = f"http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/"

        response = api_client.post(url)
        assert response.data == {"detail": "Учетные данные не были предоставлены."}
        assert response.status_code == 401

        api_client.force_authenticate(user=new_user)
        response = api_client.post(url)

        assert Favorite.objects.filter(recipe=new_recipe, author=new_user).exists()
        assert response.data == {"detail": "Рецепт добавлен в избранное."}
        assert response.status_code == 201

    def test_already_favorited_add_to_favorites(self, api_client, new_user, new_recipe):
        """
        Adding already favorited recipe to favorites test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """
        slug = new_recipe.slug
        url = f"http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/"

        Favorite.objects.create(recipe=new_recipe, author=new_user)
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url)

        assert response.data == {"detail": "Рецепт уже находится в избранном."}
        assert response.status_code == 400

    def test_non_existing_recipe_add_to_favorites(
        self, api_client, new_user, new_recipe
    ):
        """
        Adding non-existing recipe to favorites test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """
        url = f"http://127.0.0.1:8000/api/v1/recipe/non-existing-recipe/favorite/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url)

        assert response.data == {"detail": "Страница не найдена."}
        assert response.status_code == 404

    def test_recipe_remove_from_favorites(self, api_client, new_user, new_recipe):
        """
        Deleting recipe from favorites test
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """
        slug = new_recipe.slug
        url = f"http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/"

        Favorite.objects.create(recipe=new_recipe, author=new_user)

        response = api_client.delete(url)
        assert response.data == {"detail": "Учетные данные не были предоставлены."}
        assert response.status_code == 401

        api_client.force_authenticate(user=new_user)
        response = api_client.delete(url)
        assert not (
            Favorite.objects.filter(recipe=new_recipe, author=new_user).exists()
        )
        assert response.data == {"detail": "Рецепт удален из избранного."}
        assert response.status_code == 204

    def test_non_existing_recipe_remove_from_favorites(
        self, api_client, new_user, new_recipe
    ):
        """
        Deleting non-existing recipe from favorites test
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """
        url = f"http://127.0.0.1:8000/api/v1/recipe/non-existing-recipe/favorite/"
        api_client.force_authenticate(user=new_user)
        response = api_client.delete(url)

        assert response.data == {"detail": "Страница не найдена."}
        assert response.status_code == 404

    def test_not_favorited_recipe_remove_from_favorites(
        self, api_client, new_user, new_recipe
    ):
        """
        Deleting not favorited recipe from favorites test
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/
        """

        slug = new_recipe.slug
        url = f"http://127.0.0.1:8000/api/v1/recipe/{slug}/favorite/"

        api_client.force_authenticate(user=new_user)
        response = api_client.delete(url)
        assert response.data == {"detail": "Рецепт не находится в избранном."}
        assert response.status_code == 400
