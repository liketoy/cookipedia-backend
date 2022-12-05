from rest_framework import serializers
from recipes import models
from users.serializers import TinyRelatedUserSerializer
from foods.serializers import TinyFoodSerializer
from ingredients.serializers import TinyIngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    writer = TinyRelatedUserSerializer(read_only=True)
    likes_user = TinyRelatedUserSerializer(read_only=True, many=True)
    evaluations_score = serializers.SerializerMethodField(read_only=True)

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
            "likes_user",
            "evaluations_score",
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

    def get_evaluations_score(self, obj):
        recipe = models.Recipe.objects.get(pk=obj.pk)
        users = models.RecipeEvaluation.objects.filter(recipe=recipe)
        sum = 0
        for user in users:
            sum += user.score
        return "{:.1f}".format(sum / users.count())


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
