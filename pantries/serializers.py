from rest_framework import serializers, exceptions
from django.core.paginator import Paginator
from django.utils import timezone
from pantries import models
from users.serializers import TinyRelatedUserSerializer
from ingredients.serializers import IngredientSerializer


class StoreIngredientSerializer(serializers.ModelSerializer):
    is_status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
            "is_status",
        )

    def get_is_status(self, obj):
        return self.Meta.model.is_status(obj)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(
            {"ingredient": IngredientSerializer(instance.ingredient).data}
        )
        return response

    def validate_date_bought(self, data):
        now = timezone.localtime(timezone.now()).date()
        if data is not None and data > now:
            raise serializers.ValidationError("미래에서 사오신 겁니까...?")
        return data


class PantrySerializer(serializers.ModelSerializer):
    user = TinyRelatedUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Pantry
        fields = ("user", "ingredients")

    def get_ingredients(self, obj):
        request = self.context.get("request")
        queryset = models.StoreIngredient.objects.filter(pantry=obj).order_by(
            "created_at"
        )
        page_size = request.query_params.get("page_size", 10)
        page = request.query_params.get("page", 1)
        try:
            paginator = Paginator(queryset, page_size)
            result = paginator.page(page)
            serializer = StoreIngredientSerializer(result, many=True)

            return {"count": queryset.count(), "results": serializer.data}
        except Exception as e:
            raise exceptions.ParseError(e)
