from django.db import models
from django.utils import timezone
from common.models import TimeStampedModel


class Pantry(TimeStampedModel):
    """팬트리 Model에 관한 정의"""

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", through="StoreIngredient", related_name="pantries"
    )

    class Meta:
        verbose_name_plural = "pantries"

    def __str__(self) -> str:
        return f"{self.user.nickname}님의 Pantry"

    def count_ingredients(self):
        return self.ingredients.count()


class StoreIngredient(TimeStampedModel):
    """팬트리 M2M중간관계 Model에 관한 정의"""

    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    date_bought = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["pantry", "ingredient"], name="pantry_ingredient"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.pantry.user.nickname}님이 산 {self.ingredient}"

    def status_ingredient(self):
        if self.ingredient is not None and self.date_bought is not None:
            today = timezone.now().date()
            if (today - self.date_bought).days < self.ingredient.expiry_date:
                return "😋"
            if (today - self.date_bought).days == self.ingredient.expiry_date:
                return "🙂"
            if (today - self.date_bought).days > self.ingredient.expiry_date:
                return "🤮"
        else:
            return ""
