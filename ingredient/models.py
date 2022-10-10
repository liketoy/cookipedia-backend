from django.db import models

# Create your models here.
INGREDIENT_CATEGORY_CHOICES = [
    ("과일", "과일"),
    ("채소", "채소"),
    ("정육, 계란", "정육, 계란"),
    ("수산", "수산"),
    ("우유, 유제품", "우유, 유제품"),
    ("빵, 잼", "빵, 잼"),
    ("양념", "양념"),
    ("햄, 어묵, 통조림", "햄, 어묵, 통조림"),
    ("기타", "기타"),
]


class IngredientCategory(models.Model):
    ingredient_category = models.CharField(
        blank=False, choices=INGREDIENT_CATEGORY_CHOICES, max_length=40, default=""
    )


class Ingredient(models.Model):
    category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=40, default="", blank=False)
    expiry_date = models.CharField(max_length=30, default="", blank=True)
    calorie_per_100g = models.PositiveIntegerField(default=0)
    price = models.IntegerField(verbose_name="가격")
