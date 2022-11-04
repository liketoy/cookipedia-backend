from django.db import models
from common.models import TimeStampedModel
from django.core.validators import MaxValueValidator, MinValueValidator


class Recipe(TimeStampedModel):
    """레시피 Model에 관한 정의"""

    cover = models.ImageField(upload_to="recipes/%Y/%m/%d/", blank=True)
    title = models.CharField(max_length=120)
    food = models.ForeignKey(
        "foods.Food", related_name="recipes", on_delete=models.CASCADE
    )
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", related_name="recipes", through="TypeIngredient"
    )
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="recipes"
    )
    content = models.TextField()
    likes_user = models.ManyToManyField(
        "users.User", related_name="likes_user", blank=True
    )
    evaluations_user = models.ManyToManyField(
        "users.User",
        related_name="evaluations_user",
        blank=True,
        through="RecipeEvaluation",
    )


class TypeIngredient(models.Model):
    class IngredientTypeChoices(models.TextChoices):
        MAIN = ("main", "주재료")
        SUB = ("sub", "부재료")
        SAUCE = ("sauce", "양념")

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=IngredientTypeChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"], name="recipe_ingredient_type"
            )
        ]


# TypeIngredient._meta.auto_created = True
# models.CharField(max_length=10, choices=TypeIngredient.IngredientTypeChoices.choices).contribute_to_class(Recipe.ingredients.through, "type")


class RecipeEvaluation(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        default=1, validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="recipe_evaluation")
        ]
