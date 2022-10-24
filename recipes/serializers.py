from rest_framework import serializers
from recipes import models
from users.serializers import TinyRelatedUserSerializer
from foods.serializers import TinyFoodSerializer
from ingredients.serializers import TinyIngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    writer = TinyRelatedUserSerializer(read_only=True)

    class Meta:
        model = models.Recipe
        fields = (
            "pk",
            "cover",
            "title",
            "food",
            "ingredients",
            "writer",
            "content",
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(
            {
                "food": TinyFoodSerializer(instance.food, read_only=True).data,
                "ingredients": TinyIngredientSerializer(
                    instance.ingredients, many=True, read_only=True
                ).data,
            }
        )
        return response
