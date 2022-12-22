from django.db import models
from common.models import TimeStampedModel


class Food(TimeStampedModel):
    """음식 Model에 관한 정의"""

    class FoodCategoryChoices(models.TextChoices):
        KOREAN = ("한식", "한식")
        WESTERN = ("양식", "양식")
        JAPANESE = ("일식", "일식")
        CHINESE = ("중식", "중식")
        SNACK = ("분식", "분식")
        BAKING = ("베이킹", "베이킹")
        ETC = ("기타", "기타")

    category = models.CharField(choices=FoodCategoryChoices.choices, max_length=40)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
