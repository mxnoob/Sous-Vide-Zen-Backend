from django.conf import settings
from django.db import models


class Favorite(models.Model):
    """
    Favorite model

    Attrs:
    • author (ForeignKey): author of favorite recipe.
    • recipe (ForeignKey): recipe that has been added to favorites.
    • pub_date (DateTimeField): date that recipe has been added to favorite.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe", on_delete=models.CASCADE, related_name="favorite"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}'s favorite recipe: {self.recipe.title}"
