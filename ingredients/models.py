from django.db import models
from common.models import TimeStampedModel


class Ingredient(TimeStampedModel):
    """재료 Model에 관한 정의"""

    class IngredientCategoryChoices(models.TextChoices):
        FRUIT = ("과일", "과일")
        VEGETABLE = ("채소", "채소")
        MEAT_EGG = ("정육, 계란", "정육, 계란")
        SEAFOOD = ("수산", "수산")
        DIARY = ("우유, 유제품", "우유, 유제품")
        BREAD = ("빵, 잼, 시리얼", "빵, 잼, 시리얼")
        SOURCE = ("양념, 장류, 오일", "양념, 장류, 오일")
        SIDE = ("김치, 반찬, 젓갈, 김", "김치, 반찬, 젓갈, 김")
        CANNED = ("햄, 어묵, 통조림", "햄, 어묵, 통조림")
        DELIVERY = ("배달음식", "배달음식")
        ETC = ("기타", "기타")

    category = models.CharField(
        choices=IngredientCategoryChoices.choices, max_length=40
    )
    name = models.CharField(max_length=40, unique=True)
    expiry_date = models.PositiveIntegerField(blank=True, null=True)
    # calorie_per_100g = models.PositiveIntegerField(default=0)
    # price = models.PositiveIntegerField(default=0)
    preservation = models.CharField(max_length=80)

    def __str__(self) -> str:
        return self.name
