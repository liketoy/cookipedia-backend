# Generated by Django 4.1.2 on 2022-12-05 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("recipes", "0001_initial"),
        ("foods", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notifications", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="creator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="food",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to="foods.food",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="recipe",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to="recipes.recipe",
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="to",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]