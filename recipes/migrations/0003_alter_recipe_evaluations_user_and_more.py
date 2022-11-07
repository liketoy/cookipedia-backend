# Generated by Django 4.1.1 on 2022-11-04 09:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="evaluations_user",
            field=models.ManyToManyField(
                blank=True,
                through="recipes.RecipeEvaluation",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="recipeevaluation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="evaluations_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
