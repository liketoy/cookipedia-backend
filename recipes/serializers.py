from rest_framework import serializers
from recipes import models
from users.serializers import TinyRelatedUserSerializer
from foods.serializers import FoodSerializer
from ingredients.serializers import TinyIngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    writer = TinyRelatedUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y %m %d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y %m %d %H:%M")
    
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
            "created_at",
            "updated_at"
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(
            {
                "food": FoodSerializer(instance.food, read_only=True).data,
                "ingredients": TinyIngredientSerializer(
                    instance.ingredients, many=True, read_only=True
                ).data,
            }
        )
        return response


class IngredientsNeededSerializer(RecipeSerializer):
    ingredients_needed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Recipe
        fields = RecipeSerializer.Meta.fields + ("ingredients_needed",)

    def get_ingredients_needed(self, obj):
        user_ingredients = self.context.get("user_ingredients")
        recipe = models.Recipe.objects.get(pk=obj.pk)

        ingredients_needed = recipe.ingredients.exclude(pk__in=user_ingredients)
        serializer = TinyIngredientSerializer(ingredients_needed, many=True)

        return serializer.data