from django.db import models
from common.models import TimeStampedModel


class Food(TimeStampedModel):
    """음식 Model에 관한 정의"""

    FOOD_CATEGORY_CHOICES = [
        ("한식", "한식"),
        ("양식", "양식"),
        ("일식", "일식"),
        ("중식", "중식"),
        ("분식", "분식"),
        ("베이킹", "베이킹"),
        ("기타", "기타"),
    ]

    category = models.CharField(choices=FOOD_CATEGORY_CHOICES, max_length=40)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
