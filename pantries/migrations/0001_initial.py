# Generated by Django 4.1.2 on 2023-01-04 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pantry",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "pantries",
            },
        ),
        migrations.CreateModel(
            name="StoreIngredient",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date_bought", models.DateField(blank=True, null=True)),
                ("expiry_date", models.DateField(blank=True, null=True)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ingredients.ingredient",
                    ),
                ),
                (
                    "pantry",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pantries.pantry",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="pantry",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="pantries",
                through="pantries.StoreIngredient",
                to="ingredients.ingredient",
            ),
        ),
    ]
