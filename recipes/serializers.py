from rest_framework import serializers
from ingredients.models import Ingredient
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


class RecipeRecommendationSerializer(serializers.ModelSerializer):
    ingredient_needed = serializers.SerializerMethodField(read_only=True)

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
            "ingredient_needed",
        )

    def get_ingredient_needed(self, obj):
        user_ingredients = self.context.get('user_ingredients')
        recipe = models.Recipe.objects.get(pk=obj.pk)

        ingredient_needed = recipe.ingredients.exclude(pk__in=user_ingredients)
        serializer = TinyIngredientSerializer(ingredient_needed, many=True) # 어차피 하나만 serialize 하는데 many=True가 없으면 에러가 뜬다...
        if ingredient_needed:
            return serializer.data
        else:
            return "필요한 재료가 없어요!"
    
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