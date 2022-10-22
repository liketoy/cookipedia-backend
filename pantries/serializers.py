from rest_framework import serializers
from . import models
from users.serializers import TinyRelatedUserSerializer


class StoreIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreIngredient
        fields = ("pk", "ingredient", "date_bought", "expiry_date")


class ReadOnlyStoreIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()

    class Meta:
        model = models.StoreIngredient
        fields = ("pk", "ingredient", "date_bought", "expiry_date")


class PantrySerializer(serializers.ModelSerializer):
    user = TinyRelatedUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Pantry
        fields = ("user", "ingredients")

    def get_ingredients(self, obj):  # obj는 models.Pantry 그 자체
        queryset = models.StoreIngredient.objects.filter(pantry=obj)
        return [
            ReadOnlyStoreIngredientSerializer(ingredient).data
            for ingredient in queryset
        ]
