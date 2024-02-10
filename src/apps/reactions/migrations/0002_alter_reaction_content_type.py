# Generated by Django 4.2.6 on 2024-01-17 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("reactions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reaction",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to=models.Q(
                    models.Q(("app_label", "recipes"), ("model", "recipe")),
                    models.Q(("app_label", "comments"), ("model", "comment")),
                    _connector="OR",
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
            ),
        ),
    ]