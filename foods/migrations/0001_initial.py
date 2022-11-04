# Generated by Django 4.1.1 on 2022-11-04 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Food",
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
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("한식", "한식"),
                            ("양식", "양식"),
                            ("일식", "일식"),
                            ("중식", "중식"),
                            ("분식", "분식"),
                            ("베이킹", "베이킹"),
                            ("기타", "기타"),
                        ],
                        max_length=40,
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
