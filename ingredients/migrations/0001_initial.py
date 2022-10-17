# Generated by Django 4.1.1 on 2022-10-17 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
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
                            ("과일", "과일"),
                            ("채소", "채소"),
                            ("정육, 계란", "정육, 계란"),
                            ("수산", "수산"),
                            ("우유, 유제품", "우유, 유제품"),
                            ("빵, 잼, 시리얼", "빵, 잼, 시리얼"),
                            ("양념, 장류, 오일", "양념, 장류, 오일"),
                            ("김치, 반찬, 젓갈, 김", "김치, 반찬, 젓갈, 김"),
                            ("햄, 어묵, 통조림", "햄, 어묵, 통조림"),
                            ("기타", "기타"),
                        ],
                        max_length=40,
                    ),
                ),
                ("name", models.CharField(max_length=40, unique=True)),
                ("expiry_date", models.PositiveIntegerField(blank=True, null=True)),
                ("preservation", models.CharField(max_length=80)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
