from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from pantries import models
from users.serializers import TinyUserSerializer


class StoreIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
        )

    def validate_date_bought(self, data):
        now = timezone.localtime(timezone.now()).date()
        if data is not None and data > now:
            raise serializers.ValidationError("미래에서 사오신 겁니까...?")
        return data


class ReadOnlyStoreIngredientSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()
    status_ingredient = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
            "status_ingredient",
        )

    def get_status_ingredient(self, obj):
        if (
            obj.ingredient is not None
            and obj.date_bought is not None
            and (
                obj.expiry_date is not None or obj.ingredient.expiry_date is not None
            )  # 재료가 있을 때, 재료를 산 날짜가 있을 때, 유저가 기입한 재료의 폐기날짜가 있거나, 재료의 폐기날짜 데이터가 있을 때
        ):
            today = timezone.localtime(timezone.now()).date()
            expiry_date = (
                obj.expiry_date
                if obj.expiry_date is not None
                else obj.date_bought + timedelta(obj.ingredient.expiry_date)
            )  # python 삼항 연산자(ex. print("짝수" if num % 2 == 0 else "홀수"))
            if today < expiry_date:
                return "😋"
            if today == expiry_date:
                return "🙂"
            if today > expiry_date:
                return "🤮"
        else:
            return "❓"


class PantrySerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True)
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
