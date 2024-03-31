from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
)

router = DefaultRouter()
router.register(r"recipe", RecipeViewSet, basename="recipe")

urlpatterns = [
    path(
        "recipe/<slug:slug>/favorite/",
        RecipeViewSet.as_view(
            {"post": "add_to_favorites", "delete": "remove_from_favorites"}
        ),
        name="favorite-recipe",
    ),
    path("", include(router.urls)),
]
