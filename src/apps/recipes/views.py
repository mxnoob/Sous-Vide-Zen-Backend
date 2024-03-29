from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.favorite.models import Favorite
from src.apps.view.models import ViewRecipes
from src.base.paginators import FeedPagination
from src.base.permissions import IsOwnerOrStaffOrReadOnly
from src.base.services import increment_view_count
from .models import Recipe
from .serializers import (
    RecipeRetriveSerializer,
    RecipeCreateSerializer,
    RecipeUpdateSerializer,
    FavoriteRecipesSerializer,
)


class RecipeViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    filter_backends = (SearchFilter,)
    search_fields = ("title",)
    lookup_field = "slug"
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if "favorites" in self.request.path:
            queryset = (
                Recipe.objects.filter(favorite__author=self.request.user)
                .order_by("-pub_date")
                .prefetch_related("tag", "reactions", "comments")
                .annotate(
                    reactions_count=Count("reactions", distinct=True),
                    views_count=Count("views", distinct=True),
                    comments_count=Count("comments", distinct=True),
                )
            )
            return queryset
        slug = self.kwargs.get("slug")
        queryset = (
            Recipe.objects.filter(slug=slug)
            .select_related("author")
            .prefetch_related(
                "ingredients",
                "category",
                "tag",
                "reactions",
            )
            .annotate(
                reactions_count=Count("reactions", distinct=True),
                views_count=Count("views", distinct=True),
            )
        )
        return queryset

    def get_permissions(self):
        if self.request.method == "POST" or "favorites" in self.request.path:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwnerOrStaffOrReadOnly,)
        return super(RecipeViewSet, self).get_permissions()

    def get_serializer_class(self):
        if "favorites" in self.request.path:
            self.serializer_class = FavoriteRecipesSerializer
        elif self.request.method == "GET":
            self.serializer_class = RecipeRetriveSerializer
        elif self.request.method == "POST":
            self.serializer_class = RecipeCreateSerializer
        elif self.request.method == "PATCH":
            self.serializer_class = RecipeUpdateSerializer
        return super(RecipeViewSet, self).get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        increment_view_count(ViewRecipes, instance, request)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete recipe"""
        self.get_object().delete()
        return Response(
            {"message": "Рецепт успешно удален"}, status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, slug):
        """Добавление рецепта в избранное/удаление из избранного."""

        recipe = self.get_object()
        favorite_recipe = Favorite.objects.filter(author=request.user, recipe=recipe)
        if request.method == "DELETE":
            if not favorite_recipe.exists():
                return Response(
                    {"detail": "Рецепт не находится в избранном."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite_recipe.delete()
            return Response(
                {"detail": "Рецепт удален из избранного."},
                status=status.HTTP_204_NO_CONTENT,
            )

        if favorite_recipe.exists():
            return Response(
                {"detail": "Рецепт уже находится в избранном."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.create(author=request.user, recipe=recipe)

        return Response(
            {"detail": "Рецепт добавлен в избранное."}, status=status.HTTP_201_CREATED
        )

    @action(
        methods=[
            "get",
        ],
        detail=False,
        pagination_class=FeedPagination,
    )
    def favorites(self, request):
        """Получение списка избранных рецептов пользователя с пагинацией."""

        queryset = self.get_queryset()
        if not queryset:
            return Response({"detail": "Список избранных рецептов пуст."})

        serializer = self.get_serializer_class()
        page = self.paginate_queryset(queryset)
        serializer = serializer(page, many=True)

        return self.get_paginated_response(serializer.data)
