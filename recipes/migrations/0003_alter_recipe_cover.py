# Generated by Django 4.1.1 on 2022-10-20 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cover",
            field=models.ImageField(blank=True, upload_to="recipes/%Y/%m/%d/"),
        ),
    ]
