from rest_framework import serializers
from pantries import models
from users.serializers import TinyRelatedUserSerializer, PrivateUserSerializer


class StoreIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
        )


class ReadOnlyStoreIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()

    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
        )


class PantrySerializer(serializers.ModelSerializer):
    user = TinyRelatedUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Pantry
        fields = ("user", "ingredients")

    def get_ingredients(self, obj):
        queryset = models.StoreIngredient.objects.filter(pantry=obj)
        return [
            ReadOnlyStoreIngredientSerializer(ingredient).data
            for ingredient in queryset
        ]


class PantryListSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Pantry
        fields = ("__str__", "count_ingredients", "ingredients")

    def get_ingredients(self, obj):
        queryset = models.StoreIngredient.objects.filter(pantry=obj)
        return [
            ReadOnlyStoreIngredientSerializer(ingredient).data
            for ingredient in queryset
        ]
