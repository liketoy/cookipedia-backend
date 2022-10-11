from django.db import models
from common.models import TimeStampedModel


class Pantry(TimeStampedModel):
    """팬트리 Model에 관한 정의"""

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", through="StoreIngredient", related_name="pantries"
    )


class StoreIngredient(TimeStampedModel):
    """팬트리 M2M중간관계 Model에 관한 정의"""

    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    date_bought = models.DateField(null=True, blank=True)
