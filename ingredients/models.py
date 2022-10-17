from django.db import models
from common.models import TimeStampedModel


class Ingredient(TimeStampedModel):
    """재료 Model에 관한 정의"""

    INGREDIENT_CATEGORY_CHOICES = [
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
    ]

    category = models.CharField(choices=INGREDIENT_CATEGORY_CHOICES, max_length=40)
    name = models.CharField(max_length=40, unique=True)
    expiry_date = models.PositiveIntegerField(blank=True)
    preservation = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name
