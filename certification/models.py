from django.db import models
from common.models import TimeStampedModel


# Create your models here.
class Certification(TimeStampedModel):
    food = models.ForeignKey(
        "foods.Food",
        on_delete=models.CASCADE,
        related_name="certification_food",
        null=False,
        blank=False,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="certification_recipe",
        null=False,
        blank=False,
    )

    photo = models.ImageField(
        blank=False, null=False, upload_to="certification_photo/%Y/%m/%d/"
    )
    target = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="target"
    )
    status = models.BooleanField(default=False)
