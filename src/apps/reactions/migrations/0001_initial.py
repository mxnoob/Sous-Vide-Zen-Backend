# Generated by Django 4.2.6 on 2023-12-03 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                (
                    "emoji",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Like", "Like"),
                            ("Dislike", "Dislike"),
                            ("Angry_Face", "Angry Face"),
                            ("Heart", "Heart"),
                            ("Fire", "Fire"),
                        ],
                        default="Like",
                        max_length=10,
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            models.Q(("app_label", "recipes"), ("model", "recipe")),
                            models.Q(("app_label", "comments"), ("model", "comment")),
                            _connector="OR",
                        ),
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["content_type", "object_id"],
                        name="reactions_r_content_912cf2_idx",
                    )
                ],
            },
        ),
        migrations.AddConstraint(
            model_name="reaction",
            constraint=models.UniqueConstraint(
                fields=("author", "emoji", "content_type", "object_id"),
                name="unique_reaction",
            ),
        ),
    ]
