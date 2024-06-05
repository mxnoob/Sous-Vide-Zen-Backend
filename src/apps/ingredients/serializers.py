from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField

from base.services import validate_amount
from .models import IngredientInRecipe


class IngredientInRecipeSerializer(ModelSerializer):
    """
    Ingredients in recipe serializer
    """

    name = CharField(source="ingredient.name", max_length=100)
    unit = CharField(source="unit.name", max_length=30)

    class Meta:
        model = IngredientInRecipe
        fields = (
            "name",
            "unit",
            "amount",
        )

    def validate_amount(self, value):
        return validate_amount(value)
