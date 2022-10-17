from django.db import models
from common.models import TimeStampedModel
from django.utils.timezone import now
import datetime


class Pantry(TimeStampedModel):
    """팬트리 Model에 관한 정의"""

    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        "ingredients.Ingredient", through="StoreIngredient", related_name="pantries"
    )

    def __str__(self):
        return f"{self.user.nickname}님의 Pantry"

    def count_ingredients(self):
        return self.ingredients.count()

    class Meta:
        verbose_name_plural = "pantries"


class StoreIngredient(TimeStampedModel):
    """팬트리 M2M중간관계 Model에 관한 정의"""

    pantry = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("ingredients.Ingredient", on_delete=models.CASCADE)
    date_bought = models.DateField(null=True, blank=True)
    
    def status_ingredient(self):
        if self.ingredient.expiry_date and self.date_bought:
            if self.date_bought + datetime.timedelta(days=self.ingredient.expiry_date) > now().date():
                return "😄"
            elif self.date_bought + datetime.timedelta(days=self.ingredient.expiry_date) < now().date():
                return "🤮"
        else:
            return ""
        
    def __str__(self):
        return f'{self.pantry.user.nickname}님이 산 {self.ingredient}'
    
    class Meta:  # ingredient의 중복 방지
        constraints = [models.UniqueConstraint(fields=['ingredient'], name="unique_ingredient")]
        
