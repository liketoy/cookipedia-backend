from django.db import models
from common.models import TimeStampedModel
import datetime


now = datetime.datetime.now().date()


class Pantry(TimeStampedModel):
    """팬트리 Model에 관한 정의"""

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient",
        through="StoreIngredient",
        related_name="pantries",
    )

    def __str__(self) -> str:
        return f"{self.user}의 Pantry"

    def count_ingredients(self):
        return self.ingredients.count()


class StoreIngredient(TimeStampedModel):
    """팬트리 M2M중간관계 Model에 관한 정의"""

    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    date_bought = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.pantry.user}가 산 {self.ingredient}"

    def status_ingredient(self):
        print("zz", self.date_bought)
        print("zz", self.ingredient.expiry_date)
        if self.date_bought and self.ingredient.expiry_date:
            if (
                self.date_bought + datetime.timedelta(days=self.ingredient.expiry_date)
                > now
            ):
                return "😄"
            else:
                return "🤮"
        else:
            return ""
