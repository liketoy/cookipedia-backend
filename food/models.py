from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class CategoryOfFood(models.Model):
    name = models.CharField(max_length=20)


class Food(TimeStampedModel):
    name = models.CharField(max_length=30)
    content = models.TextField()
    category = models.ForeignKey(CategoryOfFood, on_delete=models.CASCADE)


class FoodPost(TimeStampedModel):
    title = models.CharField(max_length=50)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        "ingredient.Ingredient", related_name="Ingredients"
    )


class PostImage(TimeStampedModel):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Food/%Y/%m/%d")


class Comment(TimeStampedModel):
    post = models.ForeignKey(FoodPost, on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField()

    def get_absolute_url(self):  # 추후 앵커를 통해 자동 스크롤을 위한 함수
        return f"{self.pk}"
