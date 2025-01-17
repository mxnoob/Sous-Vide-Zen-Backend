from django.db import models


class Unit(models.Model):
    """
    Unit model

    Attrs:
    • name (CharField(30)): name of unit.
    """

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient model

    Attrs:
    • name (CharField(100)): name of ingredient.

    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    IngredientInRecipe model

    Attrs:
    • ingredient (ForeignKey): ingredient in recipe.
    • recipe (ForeignKey):  recipe, in which an ingredient is added.
    • unit (ForeignKey): unit of ingredient in recipe.
    • amount (PositiveIntegerField): amount of an ingredient.
    """

    ingredient = models.ForeignKey(
        "Ingredient",
        null=True,
        on_delete=models.SET_NULL,
        related_name="ingredientsinrecipe",
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="ingredientsinrecipe"
    )
    unit = models.ForeignKey(
        Unit, null=True, on_delete=models.SET_NULL, related_name="ingredientsinrecipe"
    )
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.recipe.title}_{self.ingredient.name}"
