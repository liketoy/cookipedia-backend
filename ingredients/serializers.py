from rest_framework import serializers
from ingredients import models


class TinyIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            "pk",
            "name",
            "category"
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            "pk",
            "category",
            "name",
            "expiry_date",
            "preservation",
        )
