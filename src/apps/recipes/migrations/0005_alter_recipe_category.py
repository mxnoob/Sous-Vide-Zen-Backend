# Generated by Django 4.2.6 on 2023-12-03 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_category_alter_recipe_slug_recipe_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="category",
            field=models.ManyToManyField(
                blank=True, related_name="recipes", to="recipes.category"
            ),
        ),
    ]