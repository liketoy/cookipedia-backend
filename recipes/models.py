from django.db import models
from common.models import TimeStampedModel


class Recipe(TimeStampedModel):
    """레시피 Model에 관한 정의"""

    cover = models.ImageField(upload_to="recipes/%Y/%m/%d/", blank=True)
    title = models.CharField(max_length=120)
    food = models.ForeignKey(
        "foods.Food", related_name="recipes", on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", related_name="recipes"
    )
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="recipes"
    )
    content = models.TextField()
    likes_user = models.ManyToManyField(
        "users.User", related_name="likes_user", blank=True
    )
    
