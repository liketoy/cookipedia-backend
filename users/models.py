from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.

phoneNumberReg = RegexValidator(
    regex=r"^01([0|1|6|7|8|9]{1,1})-?([0-9]{3,4})-?([0-9]{4})$"
)


class User(AbstractUser):
    AGE_CHOICES = [
        ("10대", "10대"),
        ("20대", "20대"),
        ("30대", "30대"),
        ("40대", "40대"),
        ("50대 이상", "50대 이상"),
    ]
    nickname = models.CharField(max_length=40, unique=True, default="")
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/%Y/%m/%d/")
    age = models.CharField(blank=True, choices=AGE_CHOICES, max_length=10, default="")
    phone_number = models.CharField(
        validators=[phoneNumberReg], max_length=11, unique=True
    )
    useringredients = models.ManyToManyField(
        "ingredient.Ingredient", through="UserIngredientDate"
    )


class UserIngredientDate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    useringredient = models.ForeignKey(
        "ingredient.Ingredient", on_delete=models.CASCADE
    )
    bought_ingredient_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )
