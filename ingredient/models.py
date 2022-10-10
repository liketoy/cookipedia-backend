from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class CategoryOfIngredient(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="CategoryOfIngredient/%Y/%m/%d")


class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=50)
    calorie_per_100g = models.IntegerField(default=0)
    category = models.ForeignKey(CategoryOfIngredient, on_delete=models.CASCADE)
