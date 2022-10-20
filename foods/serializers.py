from rest_framework import serializers
from foods import models


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Food
        fields = ("pk", "category", "name")
