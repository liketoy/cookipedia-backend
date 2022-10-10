# Generated by Django 4.1.1 on 2022-10-10 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingredient", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("food", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="foodpost",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="foodpost",
            name="food",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="food.food"
            ),
        ),
        migrations.AddField(
            model_name="foodpost",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="Foods", to="ingredient.ingredient"
            ),
        ),
        migrations.AddField(
            model_name="food",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="food.categoryoffood"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="food.foodpost"
            ),
        ),
    ]