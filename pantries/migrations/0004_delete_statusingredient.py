# Generated by Django 4.1.1 on 2022-10-14 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pantries", "0003_statusingredient"),
    ]

    operations = [
        migrations.DeleteModel(
            name="StatusIngredient",
        ),
    ]
