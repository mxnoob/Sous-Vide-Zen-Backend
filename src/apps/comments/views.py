# from django.db.models import Count
from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.apps.comments.models import Comment
# from src.apps.favorite.models import Favorite
# from src.apps.view.models import ViewRecipes
from src.base.paginators import CommentPagination
# from src.base.permissions import IsOwnerOrStaffOrReadOnly
# from src.base.services import increment_view_count
from src.apps.recipes.models import Recipe
from .serializers import CommentSerializer


class CommentViewSet(
    GenericViewSet,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # filter_backends = (SearchFilter,)
    # search_fields = ("title",)
    # lookup_field = "slug"
    # http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        recipe = get_object_or_404(Recipe, slug=slug)
        queryset = Comment.objects.filter(recipe__slug=recipe.slug).select_related("author")
        return queryset

    # def get_permissions(self):
    #     if self.request.method == "POST" or "favorites" in self.request.path:
    #         self.permission_classes = (IsAuthenticated,)
    #     else:
    #         self.permission_classes = (IsOwnerOrStaffOrReadOnly,)
    #     return super(RecipeViewSet, self).get_permissions()

    # def get_serializer_class(self):
    #     serializer_classes = {
    #         "GET": RecipeRetriveSerializer,
    #         "POST": RecipeCreateSerializer,
    #         "PATCH": RecipeUpdateSerializer,
    #     }
    #     self.serializer_class = serializer_classes.get(self.request.method)

    #     return super(RecipeViewSet, self).get_serializer_class()

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     increment_view_count(ViewRecipes, instance, request)

    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     """Delete recipe"""
    #     self.get_object().delete()
    #     return Response(
    #         {"message": "Рецепт успешно удален"}, status=status.HTTP_204_NO_CONTENT
    #     )

