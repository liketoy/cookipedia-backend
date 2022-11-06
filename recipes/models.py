from django.db import models
from common.models import TimeStampedModel


class Recipe(TimeStampedModel):
    """레시피 Model에 관한 정의"""

    cover = models.ImageField(upload_to="recipes/%Y/%m/%d/", blank=True)
    title = models.CharField(max_length=120, default="")
    food = models.ForeignKey(
        "foods.Food", related_name="recipes", on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", related_name="recipes", through="TypeIngredient"
    )
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="recipes"
    )
    content = models.TextField(default="")


class TypeIngredient(TimeStampedModel):
    class IngredientTypeChoices(models.TextChoices):
        MAIN = ("main", "주재료")
        SUB = ("sub", "부재료")
        SOURCE = ("source", "양념")

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=IngredientTypeChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="recipe_ingredient"
            ),
        ]

    def __str__(self) -> str:
        return self.ingredient.name
