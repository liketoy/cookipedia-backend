from rest_framework import serializers
from recipes import models
from users.serializers import TinyRelatedUserSerializer
from foods.serializers import TinyFoodSerializer
from ingredients.serializers import TinyIngredientSerializer
from pantries.serializers import StoreIngredientSerializer
from pantries.models import StoreIngredient, Pantry


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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = TinyIngredientSerializer()

    class Meta:
        model = models.TypeIngredient
        fields = (
            "ingredient",
            "type",
        )


class RecommendSerializer(serializers.ModelSerializer):
    food = serializers.StringRelatedField()
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Recipe

        fields = (
            "title",
            "food",
            "ingredients",
        )

    def get_ingredients(self, obj):
        queryset = models.TypeIngredient.objects.filter(recipe=obj)
        serializer = RecipeIngredientSerializer(queryset, many=True)
        return {"results": serializer.data}


# class RecommendPantrySerializer(serializers.ModelSerializer):
#     ingredients = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Pantry
#         fields = ("ingredients",)

#     def get_ingredients(self, obj):
#         queryset = StoreIngredient.objects.filter(pantry=obj)
#         serializer = StoreIngredientSerializer(queryset, many=True)
#         return {"results": serializer.data}
