# Generated by Django 4.1.2 on 2023-01-04 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                    "kind",
                    models.CharField(
                        choices=[
                            ("like", "좋아요"),
                            ("follow", "팔로우"),
                            ("cooking", "요리"),
                            ("certification", "인증"),
                        ],
                        max_length=20,
                    ),
                ),
                ("preview", models.CharField(max_length=200)),
                ("is_completed", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
