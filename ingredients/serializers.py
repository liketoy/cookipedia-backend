from rest_framework import serializers
from . import models


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ingredient
        fields = (
            "category",
            "name",
            "expiry_date",
            "preservation"
        )