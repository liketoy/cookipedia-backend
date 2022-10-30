# Generated by Django 4.1.1 on 2022-10-29 21:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0002_recipe_likes_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="likes_user",
            field=models.ManyToManyField(
                blank=True, related_name="likes_user", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
