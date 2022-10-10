from django.db import models
from core.models import TimeStampedModel

# Create your models here.

FOOD_CATEGORY_CHOICES = [
    ("한식", "한식"),
    ("양식", "양식"),
    ("일식", "일식"),
    ("중식", "중식"),
    ("분식", "분식"),
    ("베이킹", "베이킹"),
    ("기타", "기타"),
]


class FoodCategory(models.Model):
    food_category = models.CharField(
        blank=False, choices=FOOD_CATEGORY_CHOICES, max_length=40, default=""
    )


class MachineCategory(models.Model):
    machine_category = models.CharField(blank=False, max_length=40, default="")


class Recipe(models.Model):
    LEVEL_CHOICES = [
        ("*", "*"),
        ("**", "**"),
        ("***", "***"),
        ("****", "****"),
        ("*****", "*****"),
    ]
    COOK_HOUR = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
    ]
    COOK_MINUTE = [
        ("10", "10"),
        ("20", "20"),
        ("30", "30"),
        ("40", "40"),
        ("50", "50"),
    ]
    recipe = models.TextField()
    food = models.ForeignKey(
        "Food", related_name="food_recipe", on_delete=models.CASCADE
    )
    level = models.CharField(
        blank=False, choices=LEVEL_CHOICES, max_length=40, default=""
    )
    cooktime_hour = models.CharField(
        blank=False, choices=COOK_HOUR, max_length=40, default=""
    )
    cooktime_minute = models.CharField(
        blank=False, choices=COOK_MINUTE, max_length=40, default=""
    )
    ingredient = models.ManyToManyField(
        "ingredient.Ingredient", related_name="food_ingredient"
    )
    machine = models.ForeignKey(
        MachineCategory,
        on_delete=models.SET_DEFAULT,
        default="",
    )


class Food(models.Model):
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=50, default="", null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.food_name}"


class Comment(TimeStampedModel):
    comment_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, default="", blank=False
    )
    comment_food = models.ForeignKey(
        "Food", on_delete=models.CASCADE, default="", blank=False
    )
    comment = models.TextField()
